import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import URL_HHRU_EMPLOYERS, LIST_WITH_HHRU_ID_EMPLOYERS, PARAMS, config, DATABASE_NAME

import requests


class HhruApiEmployers:
    """Получает список работодателей по API с сайта hh.ru и сохраняет в таблицу базы данных."""

    param = config()

    def __init__(self):
        self.employers_id_list = [employer['id'] for employer in
                                  LIST_WITH_HHRU_ID_EMPLOYERS]  # Получение ID работодателей
        self.employers_list = LIST_WITH_HHRU_ID_EMPLOYERS  # Получение ID и наименований работодателей

        self.conn = psycopg2.connect(dbname=DATABASE_NAME, **self.param)
        self.conn.autocommit = True
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    @classmethod
    def get_employer(cls, employer_id):
        """Получение данных о работодателях по ID."""

        params = {"id": employer_id} | PARAMS

        url = URL_HHRU_EMPLOYERS + str(employer_id)

        response = requests.get(url, params)

        if response.status_code == 200:
            employer = response.json()

            hhru_employers = {
                'employer_id': int(employer_id),
                'employer_name': str(employer['name']),
                'employer_url': str(employer['alternate_url']),
                'open_vacancies': int(employer['open_vacancies']),
                'site_url': str(employer['site_url'])
            }
            return hhru_employers

        else:
            print(response.status_code)

    def __repr__(self):
        """Вывод полученных данных для проверки."""

        for employer in self.employers_list:
            print(f"{employer['name']}\n{self.get_employer(employer['id'])}\n\n")

    def add_database(self):
        """Добавление в базу данных таблицы с работодателями."""

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers(
                    employer_id INTEGER PRIMARY KEY,
                    employer_name VARCHAR(250) NOT NULL,
                    open_vacancies INTEGER,
                    employer_url TEXT,
                    site_url TEXT
                )
            """)

        self.conn.commit()

    def add_data_to_database(self):
        """Добавление таблиц с данными о работодателях."""

        self.add_database()

        for employer_id in self.employers_id_list:
            employer_data = self.get_employer(employer_id)
            self.cur.execute(
                """
                INSERT INTO employers(employer_id, employer_name, 
                open_vacancies, employer_url, site_url)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING employer_id
                """,
                (employer_data['employer_id'],
                 employer_data['employer_name'],
                 employer_data['open_vacancies'],
                 employer_data['employer_url'],
                 employer_data['site_url']))

        self.conn.commit()
        self.conn.close()
