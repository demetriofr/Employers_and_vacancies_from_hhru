from configparser import ConfigParser

URL_HHRU_VACANCIES = 'https://api.hh.ru/vacancies/'
URL_HHRU_EMPLOYERS = 'https://api.hh.ru/employers/'
LIST_WITH_HHRU_ID_EMPLOYERS = [
    {'id': 566, 'name': 'OCS Distribution'},
    {'id': 1057, 'name': 'Лаборатория Касперского'},
    {'id': 1740, 'name': 'Яндекс'},
    {'id': 2381, 'name': 'Softline'},
    {'id': 3776, 'name': 'МТС'},
    {'id': 230005, 'name': '3LOGIC GROUP'},
    {'id': 598471, 'name': 'evrone.ru'},
    {'id': 906557, 'name': 'SberTech'},
    {'id': 1122462, 'name': 'Skyeng'},
    {'id': 1795976, 'name': 'Университет ИТМ'}
]
PARAMS: dict[str, bool | int] = {
    "per_page": 100,
    "only_with_salary": True
}
DATABASE_NAME = 'hhru_10_employers'

def config(filename='database.ini', section='postgresql'):
    """Получение данных для работы БД из database.ini."""

    parser = ConfigParser()  # Создание парсера
    parser.read(filename)  # Чтение данных парсером
    db = {}  # Создание словаря для данных из файла

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Некорректно заполненный файл database.ini')

    return db
