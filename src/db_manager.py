import psycopg2


class DBManager:
    """Класс работы с данными из базы данных"""

    def __init__(self, dbname: str, **params):
        """Инициализация менеджера базы данных"""
        self.dbname = dbname
        self.params = params
        self.conn = None

    def __enter__(self):
        """Контекстный менеджер для автоматического подключения"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Автоматическое закрытие соединения при выходе из контекста"""
        self.close()

    def connect(self) -> None:
        """Установка соединения с БД"""
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
            print(f"Подключение к БД {self.dbname} установлено")
        except psycopg2.Error as e:
            print(f"Ошибка подключения к БД: {e}")
            raise

    def close(self) -> None:
        """Закрытие соединения с БД"""
        if self.conn:
            self.conn.close()
            print("Соединение с БД закрыто")
            self.conn = None


    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employer, COUNT(vacancy_id) FROM vacancies
                INNER JOIN employers ON vacancies.employer_id = employers.employer_id
                GROUP BY employer
            """
            )
        result = cur.fetchall()
        return result

    def get_all_vacancies(self):
        """Получение списка всех вакансий, с указанием названия компании, названия вакансии,
        зарплаты и ссылки на вакансию"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employer, name, salary, vacancy_url FROM vacancies
                WHERE salary IS NOT NULL
                """
            )
        result = cur.fetchall()
        return result


    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT name, AVG(salary), currency FROM vacancies
                WHERE salary IS NOT NULL
                GROUP BY name, currency
                ORDER BY name
                """)
        result = cur.fetchall()
        return result



    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                ORDER BY name
                """)
        result = cur.fetchall()
        return result


    def get_vacancies_with_keyword(self, keyword: str):
        """Получение списка всех вакансий, в названии которы содержатся переданные
        в метод слова"""
        if not self.conn:
            self.connect()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM vacancies
                WHERE LOWER(name) LIKE LOWER(%s)
                ORDER BY salary DESC
                """,
                (f'%{keyword}%',))
        result = cur.fetchall()
        return result