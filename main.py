from src.json_handler import JsonHandler
from src.utils import user_interaction
from src.vacancy import Vacancy

if "__name__" == "__main__":
    print(user_interaction())


    def save_data(vacancies=None):
        """Функция для записи данных в файл"""

        answer_save = input("""\nЗаписать данные о полученных вакансиях в файл?
        Введите: да/нет: """)

        sample_answers = ["да", "нет", "lf", "ytn"]
        while answer_save.lower() not in sample_answers:
            input("\nВведите 'да' или 'нет': ")

        if answer_save.lower() == "да":
            json_save = JsonHandler(user_interaction())
            json_save.add_data()

            search_query_2 = input("Введите дополнительный поисковый запрос: ")
            hh_vacancies_2 = hh_api.load_vacancies(search_query_2)
            json_save = JsonHandler(hh_vacancies_2)
            data = {
                "id": '1111111',
                "name": 'backend/frontend/mobile',
                "area": {"name": 'Москва'},
                "employer": {"name": 'Test'},
                "alternate_url": 'sample_url',
                "salary": {"from": 100000, "to": 120000, "currency": 'RUR'},
                "snippet": {"requirement": 'Высшее техническое образование. Знание языка программирования <Python>'},
                "type": {"name": 'Открытая'},
                "published_at": '2024-03-20T17:52:03+0300',
                "employment_form": {"name": 'Полная'},
                "experience": {"name": 'От 1 года до 3 лет'},
            }
            vacancy_1 = Vacancy(data)
            json_save.add_data(vacancy_1)




