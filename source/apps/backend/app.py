import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

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

app.db = SQLAlchemy(app)
app.ma = Marshmallow(app)
app.jwt = JWTManager(app)


@app.route('/')
def index():
    return {'message': 'Hello'}
