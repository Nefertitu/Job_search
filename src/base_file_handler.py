from abc import ABC, abstractmethod


class BaseFileHandler(ABC):
    """Базовый класс для работы с файлами"""
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def add_vacancy(self, **kwargs):
        """Метод для записи данных в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, **kwargs):
        """Метод для удаления данных из файла"""
        pass