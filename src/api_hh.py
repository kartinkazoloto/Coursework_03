import requests


def get_vacancies_hh(text=None, area=None, currency=None,
                     salary=None, work_format=None,
                     employer_id=None, max_result=2000):
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
            "work_format": work_format,
            "page": page,
            "per_page": per_page,
            "employer_id": employer_id
        }
        try:
            response = requests.get(url, params=params_vacancies, timeout=5)
            status_code = response.status_code
            if status_code == 200:
                result = response.json()
                all_results.extend(result['items'])
                if len(all_results) >= max_result:
                    all_results = all_results[:max_result]
                    # print(status_code)
                    # print(result)
                    break
                page += 1
            elif status_code == 400:
                print(f"Ошибка 400: Неверный запрос. Параметры: {params_vacancies}")
                break
            elif status_code == 403:
                print("Ошибка 403: Доступ запрещён. Проверьте корректность параметров.")
                break
            elif status_code == 429:
                print("Ошибка 429: Превышен лимит запросов. Сделайте паузу.")
                break
            else:
                print(f"Неожиданный статус ответа: {status_code}")
                break
        except requests.exceptions.Timeout:
            print("Ошибка: Таймаут запроса. Попробуйте повторить позже.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            break
        except ValueError as e:  # Ошибка парсинга JSON
            print(f"Ошибка парсинга JSON: {e}")
            break

        # print(status_code)
        # print(result)
        return print(f"status_code: {status_code}, result: {result}")

if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    vacancies = get_vacancies_hh()