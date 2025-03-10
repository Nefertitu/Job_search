import requests

from src.parser import Parser


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self, file_worker) -> None:
        """Конструктор для создания экземпляра класса `HH`"""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        super().__init__(file_worker)

    def __get_connet(self):
        """Метод подключения к API"""
        try:
            response = requests.get(self.__url)
            status_code = response.status_code
            response.raise_for_status()
    
        except requests.exceptions.Timeout:
            print("response timed out. Please check your internet connection.")
    
        except requests.exceptions.ConnectionError:
            print( "ConnectionError. Please check your internet connection.")
        
        except requests.exceptions.HTTPError:
            print("HTTP Error. Please check the URL.")
        else:
            if status_code == 200:
                return response.json()
        finally:
            print("Подключение завершено.")


def load_vacancies(self, keyword):
        """Метод для загрузки вакансий"""
        self.params['text'] = keyword
        while self.params.get('page') != 20:
            response = requests.get(self.url, headers=self.headers, params=self.params)
            vacancies = response.json()['items']
            self.vacancies.extend(vacancies)
            self.params['page'] += 1
