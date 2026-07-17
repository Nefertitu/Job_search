from abc import ABC, abstractmethod
from typing import Any

from src.vacancy import Vacancy


class BaseFileHandler(ABC):
    """Базовый класс для работы с файлами"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для записи данных в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для удаления данных из файла"""
        pass
