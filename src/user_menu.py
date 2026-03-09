from tabulate import tabulate

from src.db_manager import DBManager


class UserInteraction:
    """Класс взаимодействия с пользователем"""

    def __init__(self, db_manger: DBManager):
        self.db = db_manger
        self.menu_items = {
            "1": (
                "Получение списка всех компаний и количество вакансий у каждой компании",
                self.get_01,
            ),
            "2": (
                "Получение списка всех вакансий, с указанием названия компании, названия вакансии, "
                "зарплаты и ссылки на вакансию",
                self.get_02,
            ),
            "3": ("Получение средней зарплаты по вакансиям", self.get_03),
            "4": (
                "Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям",
                self.get_04,
            ),
            "5": (
                "Получение списка всех вакансий, в названии которы содержатся переданные в метод слова",
                self.get_05,
            ),
            "0": ("Выход", self.exit_program),
        }

    def user_menu(self):
        """Главное меню"""
        for key, (description, _) in self.menu_items.items():
            print(f"  {key}. {description}")

    def get_user_choice(self):
        """Выбор пользователя"""
        while True:
            choice = input("Выберите пункт меню: ").strip()
            if choice in self.menu_items:
                return choice
            elif choice == "":
                print("Выбор не может быть пустым.")
            else:
                print("Попробуйте снова.")

    def display_results(self, data):
        """Отображение результата в таблице"""
        if not data:
            print("Данные не найдены.")
            return
        print(f"Найдено записей: {len(data)}")
        print(tabulate(data, headers="keys", tablefmt="grid"))

    def get_01(self):
        return self.db.get_companies_and_vacancies_count()

    def get_02(self):
        return self.db.get_all_vacancies()

    def get_03(self):
        return self.db.get_avg_salary()

    def get_04(self):
        return self.db.get_vacancies_with_higher_salary()

    def get_05(self):
        while True:
            keyword = input("Введите ключевое слово для поиска: ").strip()

            if not keyword:
                print("Ключевое слово не может быть пустым")
                continue

            break
        return self.db.get_vacancies_with_keyword(keyword)

    def run(self):
        """Запускает цикл меню"""
        while True:
            try:
                self.user_menu()
                choice = self.get_user_choice()

                _, action = self.menu_items[choice]
                result = action()

                if result is False:
                    break

                if result:
                    self.display_results(result)

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                input("Нажмите Enter, чтобы продолжить.")

    def exit_program(self):
        """Завершение работы"""
        print("Завершение работы. До свидания!")
        return False
