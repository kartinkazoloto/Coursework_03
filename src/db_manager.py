from psycopg2 import _psycopg


class DBManager:
    """Класс работы с данными из базы данных"""
    def __init__(self):
        pass



    def connect_db(self):
        """Подключение к БД"""
        pass


    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании"""
        pass


    def get_all_vacancies(self):
        """Получение списка всех вакансий, с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию"""
        pass


    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""
        pass


    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass


    def get_vacancies_with_keyword(self):
        """Получение списка всех вакансий, в названии которы содержатся переданные в метод слова"""
        pass