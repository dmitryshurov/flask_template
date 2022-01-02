import os
import uuid
from hashlib import md5

from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, post_load
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DB'],
)
SECRET_KEY = os.environ['SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


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
    password = Column(String)
    role = Column(String, ForeignKey('user_roles.id'), default='user')


class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String, nullable=False, index=True)


db.drop_all()
db.create_all()


def get_password_hash(password):
    return md5((password + SECRET_KEY).encode('utf-8')).hexdigest()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


class UserSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.String(dump_only=True)

    @post_load
    def hash_password(self, data, **kwargs):
        data['password'] = get_password_hash(data['password'])
        return data

    class Meta:
        additional = ('id', 'uuid')
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    return {'message': 'Hello'}


@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).one()

    if current_user.role != 'admin':
        return {'message': "Not found"}, 401
    else:
        return {'users': users_schema.dump(User.query.all())}


def get_json_or_form_data(request):
    if request.is_json:
        return request.json
    else:
        return request.form


@app.route('/users', methods=['POST'])
def create_user():
    request_data = get_json_or_form_data(request)
    user = user_schema.load(request_data)

    existing_user_with_email = User.query.filter_by(email=user['email']).first()
    if existing_user_with_email:
        return {'message': 'User with this email already exists'}, 409

    else:
        user_db = User(**user)
        db.session.add(user_db)
        db.session.commit()
        return {'message': 'User created successfully'}, 201


@app.route('/users/login', methods=['POST'])
def user_login():
    request_data = get_json_or_form_data(request)
    credentials = user_schema.load(request_data, partial=['first_name', 'last_name'])

    user_with_credentials = User.query.filter_by(**credentials).first()
    if user_with_credentials:
        access_token = create_access_token(identity=request_data['email'])
        return {'message': 'Login succeeded!', 'access_token': access_token}
    else:
        return {'message': "Bad email or password"}, 401


@app.route("/users/logout", methods=["POST"])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return {'msg': 'Logout successful'}
