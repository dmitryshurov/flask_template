from flask import Blueprint, current_app as app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, set_access_cookies, unset_jwt_cookies

from . import jwt_hooks  # noqa:F401
from .decorators import auth_required
from .models import TokenBlocklist, User
from .password_utils import check_password, get_password_hash
from .schemas import user_schema, users_schema

blueprint = Blueprint('users', __name__, url_prefix='/users')


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
        return {'msg': 'User with this email already exists'}, 409

    else:
        user['hashed_password'] = get_password_hash(user['password'])
        del user['password']

        user_db = User(**user)
        app.db.session.add(user_db)
        app.db.session.commit()
        return {'msg': 'User created successfully'}, 201


@blueprint.route('/login', methods=['POST'])
def user_login():
    request_data = get_json_or_form_data(request)
    email = request_data['email']
    password = request_data['password']

    user = User.query.filter_by(email=email).one_or_none()
    if user and check_password(password, user.hashed_password):
        access_token = create_access_token(identity=user.email)
        response = jsonify(msg='Login succeeded')
        set_access_cookies(response, access_token)
        return response
    else:
        return {'msg': 'Login failed'}, 401


@blueprint.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    jti = get_jwt()['jti']
    app.db.session.add(TokenBlocklist(jti=jti))
    app.db.session.commit()
    response = jsonify(msg='Logout succeeded')
    unset_jwt_cookies(response)
    return response
