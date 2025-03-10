from abc import ABC, abstractmethod


class Parser(ABC):
    """Базовый класс для работы с API сайтов"""

    def __init__(self, *args, **kwargs) -> None:   # Должен ли быть инициализатор в абстрактном классе?
        """Конструктор для создания экземпляра класса `Parser`"""
        super().__init__()