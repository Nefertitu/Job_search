import re

from src.head_hunter_api import HeadHunterAPI
from src.json_handler import JsonHandler
from src.vacancy import Vacancy


def filter_vacancies(vacancies: list, filter_words: str, param: str = "positive") -> str | list:
    """Функция для выбора вакансий по ключевым словам"""

    vacancies_filter =[]

    list_words = re.findall(r"([\w]{3,})", filter_words.lower())

    for vacancy in vacancies:
        vacancy = Vacancy(vacancy)
        if param == "positive":
            if set(list_words).issubset(set(re.findall(r"(\w{3,})", f"{vacancy.name_vacancy} {vacancy.area} {vacancy.requirements}".lower()))):
                vacancies_filter.append(vacancy)
            else:
                continue
        if param == "negative":
            if set(list_words).issubset(set(re.findall(r"(\w{3,})", f"{vacancy.name_vacancy} {vacancy.area} {vacancy.requirements}".lower()))):
                continue
            else:
                vacancies_filter.append(vacancy)

    if vacancies_filter is None:
        return []

    return vacancies_filter


def sort_vacancies(vacancies: list) -> list:
    """Функция для сортировки вакансий по заработной плате в порядке убывания"""

    return sorted(vacancies, key=lambda vacancy: vacancy.salary_to, reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Функция для выбора топ N вакансий"""

    if len(vacancies) >= top_n:
        return vacancies[:top_n]
    else:
        return vacancies


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    platform = ["HeadHunter"]
    vacancies_save = []
    hh_api = HeadHunterAPI()

    search_query = input(
        f"\nВведите данные для выполнения поискового запроса о вакансиях на платформе {platform}: ")
    with open("./data/vacancies_save.json", "w") as f:
        f.write("")
    hh_vacancies = hh_api.load_vacancies(search_query)
    vacancies_list = Vacancy.cast_vacancies_in_list(hh_vacancies)
    print("\nВыполняется запрос к API сайта hh.ru...")
    json_saver = JsonHandler()
    for vacancy in vacancies_list:
        vacancy_ = Vacancy(vacancy)
        vacancies_save.append(vacancy_)
        json_saver.add_vacancy(vacancy_)

    print(f"\nПроизведена запись полученных данных в файл 'vacancies_save.json'.")

    filter_words = input("""\nВведите ключевое слово (или список слов) для фильтрации вакансий
(пример: Москва, Junior): """)
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    if filtered_vacancies is None:
        return "\nПо заданным ключевым словам совпадений не найдено."

    else:
        print("\nВыполнен перерасчет заработной платы, указанной в другой валюте, в рубли с помощью API ЦБ РФ.")
        salary_range = input("\nВведите диапазон зарплат (пример: 100000 - 150000): ")

        ranged_vacancies = []
        not_ranged_vacancies = []
        for vacancy in filtered_vacancies:
            if vacancy.get_vacancies_by_salary(salary_range):
                ranged_vacancies.append(vacancy)
            else:
                not_ranged_vacancies.append(vacancy)

        answer_dif = input("\nЗаписать отфильтрованные данные по вакансиям в файл 'vacancies_save.json'? (Введите: да/нет): ")

        answers = ["да", "lf", "нет", "ytn"]

        while answer_dif.lower() not in answers:
            input("\nВведите 'да' или 'нет': ")

        if answer_dif.lower() == "да" or answer_dif.lower() == "lf":
            filtered_vacancies_negative = filter_vacancies(vacancies_list, filter_words, param="negative")
            print("\nВыполняется запись данных в файл...")
            vacancies_to_del = []
            for vacancy in filtered_vacancies_negative:
                # vacancy_ = Vacancy(vacancy)
                vacancies_to_del.append(vacancy)
            for vacancy in not_ranged_vacancies:
                vacancies_to_del.append(vacancy)
            for vacancy in vacancies_to_del:
                json_saver.delete_vacancy(vacancy)

        if answer_dif.lower() == "нет" or answer_dif.lower() == "ytn":
            print("\nВ файле 'vacancies_save.json' остается полный перечень вакансий.")

        sorted_vacancies = sort_vacancies(ranged_vacancies)

        print(f"\nОбщее количество вакансий, полученных после фильтрации, составляет {len(sorted_vacancies)} шт.")

        top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        return top_vacancies


