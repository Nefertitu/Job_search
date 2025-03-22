import re

import requests

from src.head_hunter_api import HeadHunterAPI
from src.json_handler import JsonHandler
from src.vacancy import Vacancy


def get_external_rate(currency_name):
    """Функция для получения текущего курса валют"""

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    data_currency = response.json()["Valute"][currency_name]["Value"]

    return data_currency


# print(get_external_rate("USD"))


def filter_vacancies(vacancies: list, filter_words: str) -> list:
    """Функция для выбора вакансий по ключевым словам"""

    vacancies_filter =[]

    list_words = re.findall(r"([\w]{3,})", filter_words.lower())

    for vacancy in vacancies:
        if set(list_words).issubset(set(re.findall(r"(\w{3,})", f"{vacancy.name_vacancy} {vacancy.area} {vacancy.requirements}".lower()))):
            vacancies_filter.append(vacancy)
        else:
            continue

    return vacancies_filter


def sort_vacancies(vacancies: list) -> list:
    """Функция для сортировки вакансий по заработной плате в порядке убывания"""

    return sorted(vacancies, key=lambda vacancy: vacancy.salary_to, reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Функция для выбора топ N вакансий"""

    if len(vacancies) <= top_n:

        return vacancies[: top_n]

    return vacancies


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    platform = ["HeadHunter"]
    vacancies_save = []
    hh_api = HeadHunterAPI()

    search_query = input(f"\nВведите данные для выполнения поискового запроса о вакансиях на платформе {platform}: ")
    hh_vacancies = hh_api.load_vacancies(search_query)

    json_saver = JsonHandler()
    for vacancy in hh_vacancies:
        vacancy_ = Vacancy(vacancy)
        vacancies_save.append(vacancy_)
        json_saver.add_vacancy(vacancy_)

    print(f"\nВыполнена запись полученных данных в файл '../data/vacancies_save.json'")

    filter_words = input("""\nВведите ключевые слова для фильтрации вакансий
    (пример: Москва, Junior): """)
    filtered_vacancies = filter_vacancies(hh_vacancies, filter_words)

    salary_range = input("\nВведите диапазон зарплат (пример: 100000 - 150000): ")  # Пример: 100000 - 150000

    ranged_vacancies = []
    for vacancy in filtered_vacancies:
        if vacancy.get_vacancies_by_salary(salary_range):
            ranged_vacancies.append(vacancy)
        else:
            continue

    answer_dif = input("\nЗаписать отфильтрованные данные по вакансиям? (Введите: да/нет): ")

    answers = ["да", "lf", "нет", "ytn"]

    while answer_dif.lower() not in answers:
        input("\nВведите 'да' или 'нет': ")

    if answer_dif.lower() == "да" or answer_dif.lower() == "lf":
        for vacancy in ranged_vacancies:
            vacancy_ = Vacancy(vacancy)
            json_saver.delete_vacancy(vacancy_)
    if  answer_dif.lower() == "нет" or answer_dif.lower() == "ytn":
        print("\nВ файле '../data/vacancies_save.json' остается полный перечень вакансий.")

    sorted_vacancies = sort_vacancies(ranged_vacancies)

    print(f"\nОбщее количество вакансий, полученных после фильтрации, составляет {len(ranged_vacancies)} шт.")

    top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    return top_vacancies