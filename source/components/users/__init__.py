import os
import uuid
from functools import wraps

import bcrypt
from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    current_user,
    get_jwt,
    jwt_required,
    verify_jwt_in_request
)
from marshmallow import fields
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from apps.backend.app import db, jwt, ma

blueprint = Blueprint('users', __name__, url_prefix='/users')


class UserRole(db.Model):
    __tablename__ = 'user_roles'

    id = Column(String, primary_key=True)
    title = Column(String)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, ForeignKey('user_roles.id'), server_default='user')
    is_active = Column(Boolean, server_default='TRUE')


class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False, index=True)


def get_password_hash(password):
    num_rounds = int(os.environ['BCRYPT_NUM_ROUNDS'])
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=num_rounds)).decode('utf-8')


def check_password(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@jwt.user_lookup_loader
def user_lookup_callback(_, jwt_data):
    current_user_email = jwt_data["sub"]
    return User.query.filter_by(email=current_user_email).one_or_none()


class UserSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(dump_only=True)
    is_active = fields.Boolean(dump_only=True)

    class Meta:
        additional = ('id', 'uuid')
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def auth_required(roles_required=None, optional=False, fresh=False, refresh=False, locations=None):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            def access_denied():
                return {'message': "Access denied"}, 401

            verify_jwt_in_request(optional, fresh, refresh, locations)

            if not current_user:
                return access_denied()

            if not current_user.is_active:
                return access_denied()

            if roles_required is None:
                return fn(*args, **kwargs)

            if current_user.role not in roles_required:
                return access_denied()

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def get_json_or_form_data(request):
    if request.is_json:
        return request.json
    else:
        return request.form


@blueprint.route('/', methods=['GET'])
@auth_required(['admin'])
def get_users():
    return {'users': users_schema.dump(User.query.all())}


@blueprint.route('/', methods=['POST'])
def create_user():
    request_data = get_json_or_form_data(request)
    user = user_schema.load(request_data)

    existing_user_with_email = User.query.filter_by(email=user['email']).first()
    if existing_user_with_email:
        return {'message': 'User with this email already exists'}, 409

    else:
        user['hashed_password'] = get_password_hash(user['password'])
        del user['password']

        user_db = User(**user)
        db.session.add(user_db)
        db.session.commit()
        return {'message': 'User created successfully'}, 201


@blueprint.route('/login', methods=['POST'])
def user_login():
    request_data = get_json_or_form_data(request)
    email = request_data['email']
    password = request_data['password']

    user = User.query.filter_by(email=email).one_or_none()
    if user and check_password(password, user.hashed_password):
        access_token = create_access_token(identity=email)
        return {'message': 'Login succeeded', 'access_token': access_token}
    else:
        return {'message': "Login failed"}, 401


@blueprint.route("/logout", methods=["POST"])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return {'message': 'Logout succeeded'}
