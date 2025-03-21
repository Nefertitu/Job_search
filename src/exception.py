from typing import Any


class FileEmpty(BaseException):
    """Класс для исключений"""

    def __init__(self, message: Any = None):
        """Конструктор для определения экземпляра класса `ZeroQuantityProduct`"""
        self.message = message
        super().__init__(message)

    def __str__(self):
        """"""
        if self:
            self.message = "Файл пустой."
            return self.message