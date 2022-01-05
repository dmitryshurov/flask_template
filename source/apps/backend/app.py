import logging
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)
app.config.from_object(Config())
app.logger.setLevel(logging.getLevelName(os.environ['LOGGING_LEVEL']))

app.db = SQLAlchemy(app)
app.ma = Marshmallow(app)
app.jwt = JWTManager(app)
