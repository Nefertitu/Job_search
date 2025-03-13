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
    
        except requests.exceptions.Timeout as exc_info:
            print(f"{exc_info}: Response timed out. Please check your internet connection.")
    
        except requests.exceptions.ConnectionError as exc_info:
            print(f"{exc_info}: ConnectionError. Please check your internet connection.")
        
        except requests.exceptions.HTTPError as exc_info:
            print(f"{exc_info}: HTTP Error. Please check the URL.")
        else:
            if status_code == 200:
                return f"{response.json()}"
        finally:
            print("?")

    @property
    def get_connect(self):
        return HeadHunterAPI.__get_connect(self)

    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий"""

        self.__params['text'] = keyword
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()['items']
            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1
        return self.__vacancies


hh_api = HeadHunterAPI()
print(hh_api.get_connect)
hh_vacancies = hh_api.load_vacancies("Python")
print(hh_vacancies)
