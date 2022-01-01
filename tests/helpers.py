import os
from contextlib import contextmanager
from hashlib import md5

import psycopg2

BASE_URL = f'http://nginx:{os.environ["BACKEND_INTERNAL_PORT"]}'

DATABASE_TABLES = ['users', 'user_roles', 'token_blocklist']


def get_password_hash(password):
    return md5((password + os.environ['SECRET_KEY']).encode('utf-8')).hexdigest()


@contextmanager
def connect_to_db():
    conn = psycopg2.connect(
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT'],
        database=os.environ['POSTGRES_DB'],
    )

    cur = conn.cursor()
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def clear_all_tables_in_database():
    with connect_to_db() as db:
        for table in DATABASE_TABLES:
            db.execute(f'DELETE FROM {table}')


def add_user_roles_to_database():
    with connect_to_db() as db:
        db.execute("INSERT INTO user_roles (id, title) VALUES ('user', 'User')")
        db.execute("INSERT INTO user_roles (id, title) VALUES ('admin', 'Admin')")


def add_admin_user_to_database():
    with connect_to_db() as db:
        db.execute("INSERT INTO users (uuid, first_name, last_name, email, password, role) "
                   "VALUES ('fc23b6f2-6485-4b06-a43c-8b3409a7b34d' , 'Admin', 'Tester', "
                   f"'admin@admin.com', '{get_password_hash('123456')}', 'admin')"
                   )
