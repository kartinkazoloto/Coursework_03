from src.api_hh import get_vacancies_hh, get_employers_hh
from src.db_manager import DBManager
from src.file_handler import (create_database, create_table_in_db,
                              save_json, get_vacancies_data,
                              get_employers_data, print_result)
from config import config
from src.user_menu import UserInteraction


def main():
    print("Добро пожаловать!")
    print("Загружаем данные...")
    # while True:
    #     keyword = input("Введите ключевое слово для поиска вакансии: ").lower()
    #     if keyword:
    #         break
    # while True:
    #     currency = input("Выберете валюту (RUR, EUR, USD): ")
    #     if currency.upper() in ("RUR", "EUR", "USD"):
    #         break
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")
    vac = get_vacancies_hh()
    vac_json = save_json(vac, "vacancies.json")
    database_name = input("Введите наименование базы данных: ").lower()
    params = config()
    create_database(database_name, params)
    create_table_in_db(database_name, params)
    employers = get_employers_data(emp_json, database_name, params)
    vacancies = get_vacancies_data(vac_json, database_name, params)

    db = DBManager(database_name, **params)
    db.connect()
    ui = UserInteraction(db)
    ui.run()
    if 'db' in locals():
        db.close()



if __name__ == '__main__':
    main()
    # text = "python" Выберете ключевое слово для поиска вакансии
    # area = "Россия" Выберете область для поиска
    # currency = "руб" Выберете валюту
    # salary = 50000 Выберете уровень заработной платы от
    # work_format =    Выберете формат работы: 1. На территории работодателя , 2. Удаленно
