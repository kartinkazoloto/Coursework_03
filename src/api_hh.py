import requests
import json

from src.file_handler import save_json


def get_employers_hh():
    """Функция получения данных о работодателях из списка с сайта hh.ru"""
    with open("user_settings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    employers_ids = data["employers_from_user"]

    results = []

    for emp_id in employers_ids:
        url = f"https://api.hh.ru/employers/{emp_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                emp = response.json()

                results.append({
                    "id": emp["id"],
                    "name": emp["name"],
                    "open_vacancies": emp["open_vacancies"]
                })

            else:
                print(f"{emp_id} ошибка {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"{emp_id} ошибка запроса: {e}")

    return results


def get_vacancies_hh(text=None, area=None, salary=None, max_result=2000):
    """Функция получения данных о вакансиях по выбранным работодателям с сайта hh.ru"""
    with open("user_settings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    employers_ids = data["employers_from_user"]

    all_results: list = []
    page = 0
    per_page = min(max_result, 100)

    url = "https://api.hh.ru/vacancies"

    while len(all_results) < max_result:
        params_vacancies = {
            # "text": text,
            # "area": area,
            # "currency": 'RUR',
            "employer_id": employers_ids,
            "only_with_salary": True,
            # "salary": salary,
            "page": page,
            "per_page": per_page
        }
        try:
            response = requests.get(url, params=params_vacancies, timeout=5)
            if response.status_code != 200:
                print(f"Ошибка {response.status_code}")
                break

            result = response.json()

            if not result["items"]:
                break


            all_results.extend(result["items"])
            if len(all_results) >= max_result:
                all_results = all_results[:max_result]
                break
            page += 1


        except requests.exceptions.Timeout:
            print("Ошибка: Таймаут запроса. Попробуйте повторить позже.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            break
        except ValueError as e:
            print(f"Ошибка: {e}")
            break

    return all_results


if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    # vacancies = get_vacancies_hh()
    # json = save(vacancies)
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")
