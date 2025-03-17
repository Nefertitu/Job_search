import json

from src.base_file_processor import BaseFileProcessor
from src.vacancy import Vacancy


class JsonProcessor(BaseFileProcessor):
    """Класс для работы с JSON-файлами"""

    def __init__(self, data: dict, mode: str = 'r'):
        """Конструктор для экземпляра класса `JsonProcessor`"""
        self.data = data
        self.mode = mode
        self.__file: str = "./data/vacancy.json"

    def __enter__(self):
        """Метод для входа в контекстный менеджер"""
        self.fp = open(self.__file, self.mode)
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для выхода из контекстного менеджера"""
        self.fp.close()

    def read(self):
        if self.__file:
            return self.fp

    def write(self):
        """Метод для записи данных в JSON-файл"""
        if self.data:
            vacancies = []
            for vacancy in self.data:
                if isinstance(vacancy, Vacancy):
                    vacancies.append(vacancy)


            json.dump(self.data, ensure_ascii=False, indent=4)


