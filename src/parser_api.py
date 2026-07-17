from abc import ABC, abstractmethod
from typing import Any


class ParserAPI(ABC):
    """Базовый класс для работы с API сайтов"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Конструктор для создания экземпляра класса `Parser`"""
        super().__init__()

    @abstractmethod
    def load_vacancies(self, keyword: str) -> None:
        """Метод для получения вакансий"""
        pass
