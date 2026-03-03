import os

import psycopg2
from pathlib import Path
import json
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, cursor


def save_json(data, file_name) -> list:
    """Сохранение инфо в файл JSON"""
    save_dir = Path(__file__).parent.parent / "data"
    save_dir.mkdir(parents=True, exist_ok=True)
    # file_name = "data.json"
    path_file = save_dir / file_name
    try:
        with open(path_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Данные успешно сохранены в {file_name}")
        return data
    except IOError as e:
        print(f"Ошибка при записи в файл {file_name}: {e}")


def create_database(database_name, params) -> None:
    """Создает новую базу данных."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur: cursor = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
    if cur.fetchone():
        cur.execute(f"DROP DATABASE {database_name}")
        print(f"База данных {database_name} удалена")
    # cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    print(f"База данных {database_name} создана")

    conn.close()


def create_table_in_db(database_name, params) -> None:
    # time.sleep(5)
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # max_attempts = 15
    # for attempt in range(1, max_attempts + 1):
    #     try:
    #         print(f"Попытка подключения к БД {database_name} (попытка {attempt}/{max_attempts})...")
    #         conn = psycopg2.connect(dbname=database_name, **params)
    #         print("Подключение к базе данных установлено")
    #         break
    #     except psycopg2.OperationalError as e:
    #         print(traceback.print_exc())
    #         error_msg = str(e).lower()
    #         if "database does not exist" in error_msg or "не существует" in error_msg:
    #             if attempt < max_attempts:
    #                 print(f"БД ещё не готова, ждём 1 сек...")
    #                 time.sleep(1)
    #             else:
    #                 print("Превышено количество попыток подключения")
    #                 return False
    #         else:
    #             print(f"Другая ошибка подключения: {e}")
    #             return False
    #     except Exception as e:
    #         print(f"Неожиданная ошибка при подключении: {e}")
    #         return False

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies 
            (
                vacancy_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                salary INTEGER,
                currency VARCHAR(5),
                vacancy_url TEXT,
                employer_id INTEGER,
                employer VARCHAR(255),
                work_format VARCHAR(25)
                )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                open_vacancies INTEGER NOT NULL
                )
        """)

    conn.commit()
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""


def create_employers_table(cur) -> None:
    """Создает таблицу employers."""
    pass


def create_vacancies_table(cur) -> None:
    """Создает таблицу vacancies."""
    pass


def get_employers_data(json_file: str) -> list[dict]:
    """Извлекает данные о работодателях из JSON-файла и возвращает список словарей с соответствующей информацией."""
    pass


def insert_employers_data(cur, employers: list[dict]) -> None:
    """Добавляет данные из employers в таблицу employers."""
    pass


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на employers_id в таблицу vacancies."""
    pass


# def create_db():
#     """Общий файл для создания БД и заполнения ее данными о вакансиях и работодателях."""
#     script_file = 'fill_db.sql'
#     json_file = 'suppliers.json'
#     db_name = 'my_new_db'
#
#     params = config()
#     conn = None
#
#     create_database(params, db_name)
#     print(f"БД {db_name} успешно создана")
#
#     params.update({'dbname': db_name})
#     try:
#         with psycopg2.connect(**params) as conn:
#             with conn.cursor() as cur:
#                 execute_sql_script(cur, script_file)
#                 print(f"БД {db_name} успешно заполнена")
#
#                 create_employers_table(cur)
#                 print("Таблица employers успешно создана")
#
#                 suppliers = get_employers_data(json_file)
#                 insert_employers_data(cur, suppliers)
#                 print("Данные в employers успешно добавлены")
#
#                 add_foreign_keys(cur, json_file)
#                 print(f"FOREIGN KEY успешно добавлены")
#
#     except(Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
