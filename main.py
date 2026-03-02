

from src.api_hh import get_vacancies_hh, get_employers_hh
from src.file_handler import create_database, create_table_in_db
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
    # vacancies = get_vacancies_hh()
    # json = save_json(vacancies, "vacancies.json")
    # emp = get_employers_hh()
    # emp_json = save_json(emp, "employers.json")

    database_name = 'HH'  #ВВедите наименование базы данных
    params = config()
    db = create_database(database_name, params)
    t_db = create_table_in_db(database_name, params)
