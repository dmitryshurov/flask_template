import os
from contextlib import contextmanager

import psycopg2

BASE_URL = f'http://nginx:{os.environ["BACKEND_INTERNAL_PORT"]}'

DATABASE_TABLES = ['users']


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
