from abc import ABC, abstractmethod


class BaseFileProcessor(ABC):
    """Базовый класс для работы с файлами"""
    super().__init__()

    @abstractmethod
    def write(self):
        """Метод для записи данных в файл"""
        pass

    @abstractmethod
    def del_data(self):
        """Метод для удаления данных из файла"""
        pass