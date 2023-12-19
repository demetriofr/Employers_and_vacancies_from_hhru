import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import DATABASE_NAME, config


class DBManager:
    """Подключается к базе данных."""

    param = config()

    def __init__(self):
        self.conn = psycopg2.connect(dbname=DATABASE_NAME, **self.param)
        self.conn.autocommit = True
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех работодателей и количество вакансий у каждого из них."""

        self.cur.execute("""
                SELECT employer_name, open_vacancies  
                FROM employers
                """)
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия работодателя и вакансии, зарплаты и ссылки на неё."""

        self.cur.execute("""
                SELECT employer_name, vacancy_name, salary, vacancy_url
                FROM vacancies
                JOIN employers USING (employer_id)
                ORDER BY employers.employer_name DESC
                """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        self.cur.execute("""
                SELECT ROUND(AVG(salary), 2) AS salary_avg
                FROM vacancies
                """)
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        self.cur.execute("""
                SELECT * 
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """)
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданное слово."""

        self.cur.execute(f"""
            SELECT * 
            FROM vacancies 
            WHERE vacancy_name 
            LIKE '%{keyword}%'
        """)
        return self.cur.fetchall()
