from abc import ABC, abstractmethod


class BaseFileHandler(ABC):
    """Базовый класс для работы с файлами"""
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def add_data(self):
        """Метод для записи данных в файл"""
        pass

    # @abstractmethod
    # def del_data(self):
    #     """Метод для удаления данных из файла"""
    #     pass