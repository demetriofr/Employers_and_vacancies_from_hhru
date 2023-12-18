import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import URL_HHRU_VACANCIES, LIST_WITH_HHRU_ID_EMPLOYERS, PARAMS, config, DATABASE_NAME

import requests


class HhruApiVacancies:
    """Получает список вакансий по API с сайта hh.ru и сохраняет в таблицу базы данных."""

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
    def get_vacancy(cls, employer_id):
        """Получение данных о вакансиях по ID."""

        vacancies_list = []
        params = {"employer_id": employer_id} | PARAMS

        response = requests.get(URL_HHRU_VACANCIES, params)

        if response.status_code == 200:
            vacancies = response.json()

            for vacancy in vacancies["items"]:
                if vacancy["salary"]["from"]:
                    hhru_vacancies = {
                        'vacancy_name': str(vacancy['name']),
                        'employer_id': int(employer_id),
                        'vacancy_url': str(vacancy['alternate_url']),
                        'salary': str(vacancy['salary']['from']),
                        'description': str(vacancy['snippet']['responsibility']),
                        'requirement': str(vacancy['snippet']['requirement']),
                        'city': str(vacancy['area']['name'])
                    }
                    vacancies_list.append(hhru_vacancies)

            return vacancies_list

        else:
            print(response.status_code)

    def __repr__(self):
        """Вывод полученных данных для проверки."""

        for employer in self.employers_list:
            print(f"{employer['name']}\n{self.get_vacancy(employer['id'])}\n\n")

    def add_database(self):
        """Добавление в базу данных таблицы с вакансиями."""

        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies(
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_name VARCHAR(250) NOT NULL,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_url TEXT,
                    salary INTEGER,
                    description TEXT,
                    requirement TEXT,
                    city VARCHAR(250)
                )
            """)

        self.conn.commit()

    def add_data_to_database(self):
        """Добавление таблиц с данными о вакансиях."""

        self.add_database()

        for employer_id in self.employers_id_list:
            vacancy_data = self.get_vacancy(employer_id)
            for vacancy in vacancy_data:
                self.cur.execute(
                    """
                    INSERT INTO vacancies(vacancy_name, employer_id, vacancy_url, 
                    salary, description, requirement, city)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['vacancy_name'],
                     vacancy['employer_id'],
                     vacancy['vacancy_url'],
                     vacancy['salary'],
                     vacancy['description'],
                     vacancy['requirement'],
                     vacancy['city']))
        self.conn.commit()
        self.conn.close()
