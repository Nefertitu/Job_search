import json

import requests

from src.parser import ParserAPI
from src.vacancy import Vacancy


class HeadHunterAPI(ParserAPI):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        """Конструктор для создания экземпляра класса `HH`"""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        super().__init__()

    def __get_connect(self):
        """Метод проверки подключения к API"""
        try:
            response = requests.get(self.__url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return False

    @property
    def vacancies(self):
        return self.__vacancies

    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий"""
        if not self.__get_connect():
            return []
        self.__params['text'] = keyword

        while self.__params.get('page') != 2:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                vacancies = response.json()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке вакансий: {e}")
                break

        return self.__vacancies


hh_api = HeadHunterAPI()
hh_vacancies = hh_api.load_vacancies("python разработчик")
print(hh_vacancies)
# json_str = json.dumps(hh_vacancies, ensure_ascii=False, indent=2)
# print(json_str)
# vacancies = []
# for vacancy in hh_vacancies:
#     vacancy_ = Vacancy(vacancy)
#     vacancies.append(vacancy_)
# print(vacancies)