import os
import uuid

from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)

DATABASE_URL = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    database=os.environ['POSTGRES_DB'],
)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


db.create_all()


class UserSchema(ma.Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    class Meta:
        additional = ('id', 'uuid')
        ordered = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    return {'message': 'Hello'}


@app.route('/users', methods=['GET'])
def get_users():
    return {'users': users_schema.dump(User.query.all())}


@app.route('/users', methods=['POST'])
def create_user():
    user = user_schema.load(request.form)

    existing_user_with_email = User.query.filter_by(email=user['email']).first()
    if existing_user_with_email:
        return {'message': 'User with this email already exists'}, 409

    else:
        user_db = User(**user)
        db.session.add(user_db)
        db.session.commit()
        return {'message': "User created successfully"}, 201
