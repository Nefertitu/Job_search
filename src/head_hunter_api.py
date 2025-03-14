import requests

from src.parser import Parser


class HeadHunterAPI(Parser):
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
        """Метод подключения к API"""
        try:
            response = requests.get(self.__url)
            status_code = response.status_code
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return False
        else:
            if status_code == 200:
                return True

    @property
    def get_connect(self):
        return HeadHunterAPI.__get_connect(self)

    @property
    def vacancies(self):
        return self.__vacancies

    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий"""
        if not self.__get_connect():
            return []
        self.__params['text'] = keyword
        self.__params['page'] = 0
        while True:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                data = response.json()
                vacancies = response.json()['items']
                current_page = data['page']
                total_pages = data['pages']
                if  current_page >= total_pages - 1:
                    break

                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке вакансий: {e}")
                break

        return self.__vacancies


hh_api = HeadHunterAPI()
print(hh_api.get_connect)
hh_vacancies = hh_api.load_vacancies("Python")
print(hh_vacancies)
