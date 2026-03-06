import requests
import json
from src.file_handler import save_json


def get_vacancies_hh(text=None, area=None, currency=None, salary=None, max_result=2000):
    """Функция получения данных с сайта hh.ru"""
    all_results = []
    page = 0
    per_page = min(max_result, 100)
    url = "https://api.hh.ru/vacancies"
    while len(all_results) < max_result:
        params_vacancies = {
            "text": text,
            "area": area,
            "currency": currency,
            "salary": salary,
            "page": page,
            "per_page": per_page,
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


def get_employers_hh(text=None, area=None, open_vacancies=None, max_result=2000) -> None:
    """Функция получения данных о работодателях из списка с сайта hh.ru"""
    # with open("../user_settings.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    employers_filter: list = [
                        '15478', # VK
                        '3529', # Сбер
                        '1740', # Яндекс
                        '78638', # Тинькофф
                        '4181', # Газпромнефть
                        '3776', # МТС
                        '39305', # Ozon
                        '87021', # Wildberries
                        '2180', # Ростелеком
                        '882', # 1С
                        ]
    all_results: list = []
    page = 0
    per_page = min(max_result, 100)
    url = "https://api.hh.ru/employers"
    while len(all_results) < max_result:
        params_vacancies = {
            "text": text,
            "area": area,
            "open_vacancies": open_vacancies,
            "page": page,
            "per_page": per_page,
        }
        try:
            response = requests.get(url, params=params_vacancies, timeout=5)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                filtered_items = []
                for employer in result['items']:
                    if (employer.get('open_vacancies', 0)) > 0:
                        filtered_items.append(employer)

                all_results.extend(filtered_items)
                # all_results.extend(result['items'])
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


if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    # vacancies = get_vacancies_hh()
    # json = save(vacancies)
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")
