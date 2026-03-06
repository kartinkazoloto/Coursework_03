

from src.api_hh import get_vacancies_hh, get_employers_hh
from src.file_handler import (create_database, create_table_in_db,
                              save_json, get_vacancies_data, get_employers_data)
from config import config


def main():

    pass




if __name__ == '__main__':
    # text = "python" Выберете ключевое слово для поиска вакансии
    # area = "Россия" Выберете область для поиска
    # currency = "руб" Выберете валюту
    # salary = 50000 Выберете уровень заработной платы от
    # work_format =    Выберете формат работы: 1. На территории работодателя , 2. Удаленно
# [{
# "id": "ON_SITE",
# "name": "На месте работодателя"
# },
# {
# "id": "REMOTE",
# "name": "Из дома"
# },
# {
# "id": "HYBRID",
# "name": "Гибрид"
# },
# {
# "id": "FIELD_WORK",
# "name": "Разъездная"
# }]
    vac = get_vacancies_hh()
    vac_json = save_json(vac, "vacancies.json")
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")

    database_name = 'hh'  #ВВедите наименование базы данных lower()
    params = config()

    db = create_database(database_name, params)
    t_db = create_table_in_db(database_name, params)

    vacancies = get_vacancies_data(vac_json, database_name, params)
    employers = get_employers_data(emp_json, database_name, params)

