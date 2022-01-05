from flask import current_app as app
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String


class UserRole(app.db.Model):
    __tablename__ = 'user_roles'

    id = Column(String, primary_key=True)
    title = Column(String)


class User(app.db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, ForeignKey('user_roles.id'), server_default='user')
    is_active = Column(Boolean, server_default='TRUE')


class TokenBlocklist(app.db.Model):
    __tablename__ = 'token_blocklist'

    id = app.db.Column(app.db.Integer, primary_key=True)
    jti = app.db.Column(app.db.String, nullable=False, index=True)
