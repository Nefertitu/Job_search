from abc import ABC, abstractmethod


class Parser(ABC):
    """Базовый класс для работы с API сайтов"""

    def __init__(self, *args, **kwargs) -> None:   # Должен ли быть инициализатор в абстрактном классе?
        """Конструктор для создания экземпляра класса `Parser`"""
        super().__init__()

    @abstractmethod
    def _get_connect(self):
        """Метод подключения к API"""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str):
        """Метод для получения вакансий"""
        pass