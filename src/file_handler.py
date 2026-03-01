import os
import psycopg2
from pathlib import Path
import json
from config import config


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
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                salary INTEGER,
                currency VARCHAR(5),
                vacancy_url TEXT,
                employer_id INTEGER,
                employer VARCHAR,
                work_format VARCHAR,
                )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                open_vacancies INTEGER NOT NULL,
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


def create_db():
    """Общий файл для создания БД и заполнения ее данными о вакансиях и работодателях."""
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_employers_table(cur)
                print("Таблица employers успешно создана")

                suppliers = get_employers_data(json_file)
                insert_employers_data(cur, suppliers)
                print("Данные в employers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
