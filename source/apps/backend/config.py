import os


class Config:
    JSON_SORT_KEYS = False

    JWT_COOKIE_SECURE = True
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_TOKEN_LOCATION = ['cookies']

    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
    )
