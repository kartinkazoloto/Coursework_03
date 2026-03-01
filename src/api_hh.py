import requests



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

        return result


def get_employers_hh(text=None, area=None, max_result=2000):
    """Функция получения данных с сайта hh.ru"""
    all_results = []
    page = 0
    per_page = min(max_result, 100)
    url = "https://api.hh.ru/employers"
    while len(all_results) < max_result:
        params_vacancies = {
            "text": text,
            "area": area,
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

        return result





if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    vacancies = get_vacancies_hh()
    json = save(vacancies)
