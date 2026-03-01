from src.api_hh import get_vacancies_hh, get_employers_hh
from src.file_handler import save_json







if __name__ == '__main__':
    # text = "python"
    # area = "Россия"
    # currency = "руб"
    # salary = 50000
    vacancies = get_vacancies_hh()
    json = save_json(vacancies, "vacancies.json")
    emp = get_employers_hh()
    emp_json = save_json(emp, "employers.json")
