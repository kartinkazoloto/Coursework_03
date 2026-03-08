import psycopg2
from psycopg2.extras import execute_batch
from pathlib import Path
import json
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


def create_database(database_name: str, params) -> None:
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


def create_table_in_db(database_name: str, params) -> None:
    """Создает таблицы в базе данных"""
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
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                open_vacancies INTEGER NOT NULL
                )
        """)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies 
            (
                vacancy_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                salary INTEGER,
                currency VARCHAR(5),
                area VARCHAR(255),              
                employer_id INTEGER,
                employer VARCHAR(255),
                work_format VARCHAR(25),
                vacancy_url TEXT
            );
            ALTER TABLE vacancies ADD CONSTRAINT fk_employers_vacancies
                 FOREIGN KEY(employer_id) REFERENCES employers(employer_id);
        """)

    conn.commit()
    conn.close()


def get_vacancies_data(json_data: dict, database_name: str, params) -> list[dict]:
    """Извлекает данные о вакансиях из JSON-файла и возвращает список словарей с соответствующей информацией."""
    try:
        conn = psycopg2.connect(dbname=database_name, **params)

        with open("user_settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        employers_ids = data["employers_from_user"]
        # Подготавливаем данные для вставки
        # data: list = json_data.get("items", [])
        records_to_insert: list = []
        for item in json_data:
            employer = item.get("employer", {})
            if not isinstance(employer, dict):
                continue
            employer_id = employer.get('id')
            if employer_id not in employers_ids:
                continue

            salary = item.get('salary', {})
            if isinstance(salary, dict):
                salary_from = salary.get('from')
                currency = salary.get('currency')
            else:
                salary_from = None
                currency = None

            area = item.get('area', {})
            if isinstance(area, dict):
                area_name = area.get('name')
            else:
                area_name = None

            # Извлекаем поля, обрабатываем пропущенные значения
            record = (
                item.get('id', None),
                item.get('name', None),
                salary_from,
                currency,
                area_name,
                employer_id,
                # employer.get('id', None),
                employer.get('name', None),
                # employer_name,
                item.get('employment', {}).get('name'),
                item.get('alternate_url', None),

            )
            records_to_insert.append(record)

        # Вставляем данные в таблицу
        with conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO vacancies (
                vacancy_id, name, salary, currency, 
                area, employer_id, employer, work_format, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vacancy_id) DO NOTHING                   
                """,
                records_to_insert
            )

        conn.commit()
        print(f"Успешно вставлено {len(records_to_insert)} записей в таблицу vacancies")
        return True

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL при вставке данных: {e}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    finally:
        conn.close()


def get_employers_data(json_data: dict, database_name: str, params) -> list[dict]:
    """Извлекает данные о работодателях из JSON-файла и возвращает список словарей с соответствующей информацией."""

    try:
        conn = psycopg2.connect(dbname=database_name, **params)

        # Подготавливаем данные для вставки
        records_to_insert: list = []

        for item in json_data:
            # Извлекаем поля, обрабатываем пропущенные значения
            record = (
                item.get('id', None),
                item.get('name', None),
                item.get('open_vacancies', None)

            )
            records_to_insert.append(record)

        # Вставляем данные в таблицу
        with conn.cursor() as cur:
            execute_batch(
                cur,
                """
                INSERT INTO employers (employer_id, name, open_vacancies)
                VALUES (%s, %s, %s)
                ON CONFLICT (employer_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    open_vacancies = EXCLUDED.open_vacancies
                """,
                records_to_insert
            )

        conn.commit()
        print(f"Успешно вставлено {len(records_to_insert)} записей в таблицу employers")
        return True

    except psycopg2.Error as e:
        print(f"Ошибка PostgreSQL при вставке данных: {e}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    finally:
        conn.close()
