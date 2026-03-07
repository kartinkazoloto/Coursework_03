import os
import requests
import json
from pathlib import Path
from src.file_handler import save_json


def get_vacancies_hh(text=None, area=113, salary=None, max_result=2000):
    """Функция получения данных с сайта hh.ru"""
    all_results: list = []
    page = 0
    per_page = min(max_result, 100)
    url = "https://api.hh.ru/vacancies"
    while len(all_results) < max_result:
        params_vacancies = {
            # "text": text,
            "area": area,
            "currency": 'RUR',
            "only_with_salary": True,
            "salary": salary,
            "page": page,
            "per_page": per_page
        }
        try:
            response = requests.get(url, params=params_vacancies, timeout=5)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                all_results.extend(result['items'])
                if len(all_results) >= max_result:
                    all_results = all_results[:max_result]
                    break
                page += 1
            else:
                print(f"Ошибка {status_code}")
                break


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


# def get_employers_hh(text=None, area=None, max_result=2000) -> list:
#     """Функция получения данных о работодателях из списка с сайта hh.ru"""
#     with open("user_settings.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#     employers_filter = data["employers_from_user"]
#     all_results: list = []
#     page = 0
#     per_page = min(max_result, 100)
#     url = "https://api.hh.ru/employers"
#     while len(all_results) < max_result:
#         params_employers = {
#             # "text": text,
#             # "area": area,
#             "only_with_vacancies": True,
#             "sort_by": "by_vacancies_open",
#             "page": page,
#             "per_page": per_page,
#         }
#         try:
#             response = requests.get(url, params=params_employers, timeout=5)
#             status_code = response.status_code
#             if status_code == 200:
#                 result = response.json()
#                 filtered_items: list = []
#                 for employer in result['items']:
#                     for e in employers_filter:
#                         if employer.get('id') == e:
#                             filtered_items.append(employer)
#                 all_results.extend(filtered_items)
#
#                 if len(all_results) >= max_result:
#                     all_results = all_results[:max_result]
#                     break
#                 page += 1
#             else:
#                 print(f"Ошибка {status_code}")
#                 break
#
#
#         except requests.exceptions.Timeout:
#             print("Ошибка: Таймаут запроса. Попробуйте повторить позже.")
#             break
#         except requests.exceptions.RequestException as e:
#             print(f"Ошибка запроса: {e}")
#             break
#         except ValueError as e:
#             print(f"Ошибка2: {e}")
#             break
#
#     return all_results
#
#
# def get_employers_hh(text=None, area=None, max_result=2000) -> list:
#     """Получение работодателей с hh.ru"""
#
#     with open("user_settings.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#
#     employers_filter = set(map(str, data["employers_from_user"]))
#
#     all_results = []
#     page = 0
#     per_page = min(max_result, 100)
#
#     url = "https://api.hh.ru/employers"
#
#     while len(all_results) < max_result:
#
#         params = {
#             "only_with_vacancies": True,
#             "sort_by": "by_vacancies_open",
#             "page": page,
#             "per_page": per_page,
#         }
#
#         try:
#             response = requests.get(url, params=params, timeout=5)
#
#             if response.status_code != 200:
#                 print(f"Ошибка {response.status_code}")
#                 break
#
#             result = response.json()
#
#             if not result["items"]:
#                 break
#
#             for employer in result["items"]:
#                 if employer.get("id") in employers_filter:
#                     all_results.append(employer)
#
#             page += 1
#
#         except requests.exceptions.Timeout:
#             print("Таймаут запроса")
#             break
#         except requests.exceptions.RequestException as e:
#             print(f"Ошибка запроса: {e}")
#             break
#
#     return all_results[:max_result]


def get_employers_hh():
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


if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    # vacancies = get_vacancies_hh()
    # json = save(vacancies)
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")
