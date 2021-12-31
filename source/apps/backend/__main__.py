import os
import uuid

from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
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

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer)
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


db.create_all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'uuid', 'first_name', 'last_name', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def index():
    return {'message': 'Hello'}


@app.route('/users')
def users():
    return {'users': users_schema.dump(User.query.all())}
