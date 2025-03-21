import re
from itertools import count

import requests


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