# Employers and vacancies from hhru

Данный проект получает данные о 10 компаниях и их вакансиях с сайта hh.ru
1. ID: 566 - OCS Distribution 
2. ID: 1057 - Лаборатория Касперского 
3. ID: 1740 - Яндекс 
4. ID: 2381 - Softline  
5. ID: 3776 - МТС 
6. ID: 230005 - 3LOGIC GROUP 
7. ID: 598471 - evrone.ru 
8. ID: 906557 - SberTech 
9. ID: 1122462 - Skyeng 
10. ID: 1795976 - Университет ИТМ

Данные загружаются в таблицы БД PostgreSQL

## Ключевые шаги проекта:
1. Получение данных о работодателях и их вакансиях с сайта hh.ru и для этого используется публичный API hh.ru и библиотека requests. 
2. Применение таблиц БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях и для работы с БД используется библиотека psycopg2. 
3. Используется код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях, в том числе класс DBManager для работы с данными в БД.

## Для запуска проекта
1. Можно проект клонировать к себе
2. Потом установить зависимости из pyproject.toml 
3. А для корректной работы создать database.ini со своими данными (см. пример ниже)

```
[postgresql]
host=localhost
user=PostgreSQL
password=PostgreSQL
port=5432
```

## Для работы с проектом
1. Нужно запустить функцию main() в файле main.py
2. Следовать подсказкам для выбора интересующей информации
