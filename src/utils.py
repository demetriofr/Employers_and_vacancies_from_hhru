import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config, DATABASE_NAME


def add_database(database_name=DATABASE_NAME):
    """Добавление базы данных для таблиц с работодателями и вакансиями, а перед этим удаление существующей."""

    params = config()

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn.cursor() as cur:
    
        cur.execute(f"""DROP DATABASE IF EXISTS {database_name}""")
        cur.execute(f"""CREATE DATABASE {database_name}""")

    conn.close()
