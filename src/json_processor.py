from src.base_file_processor import BaseFileProcessor


class JsonProcessor(BaseFileProcessor):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "./data/vacancy.json"):
        """Конструктор для экземпляра класса `JsonProcessor`"""
        self.__filename = filename