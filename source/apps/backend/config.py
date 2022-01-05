import os
from datetime import timedelta


class Config:
    JSON_SORT_KEYS = False

    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_SESSION_COOKIE = False
    JWT_TOKEN_LOCATION = ['cookies']

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ['JWT_ACCESS_TOKEN_EXPIRES']))
    JWT_ACCESS_TOKEN_REFRESH_DEADLINE = timedelta(minutes=int(os.environ['JWT_ACCESS_TOKEN_REFRESH_DEADLINE']))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.environ['JWT_REFRESH_TOKEN_EXPIRES']))

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
    )
