from configparser import ConfigParser

URL_HHRU_VACANCIES = 'https://api.hh.ru/vacancies'
URL_HHRU_EMPLOYERS = 'https://api.hh.ru/employers/'
LIST_WITH_HHRU_ID_EMPLOYERS = [
    566,  # OCS Distribution
    1057,  # Лаборатория Касперского
    1740,  # Яндекс
    2381,  # Softline
    3776,  # МТС
    230005,  # 3LOGIC GROUP
    598471,  # evrone.ru
    906557,  # SberTech
    1122462,  # Skyeng
    1795976,  # Университет ИТМ
]


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
