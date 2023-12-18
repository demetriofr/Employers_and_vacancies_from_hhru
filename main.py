from src.api_hhru_employers import HhruApiEmployers
from src.api_hhru_vacancies import HhruApiVacancies
from src.utils import add_database


def main():
    """Основной интерфейс программы."""
    add_database()
    hhru_employers = HhruApiEmployers()
    hhru_employers.add_data_to_database()
    hhru_vacancies = HhruApiVacancies()
    hhru_vacancies.add_data_to_database()


if __name__ == '__main__':
    main()
