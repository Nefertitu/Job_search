from src.base_file_processor import BaseFileProcessor


class JsonProcessor(BaseFileProcessor):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "./data/vacancy.json", mode='a'):
        """Конструктор для экземпляра класса `JsonProcessor`"""
        self.__filename = filename
        self.mode = mode


    def __enter__(self):
        """"""
        self.fp = HeadHunter.load_vacancies(keyword)
        self.fp.save(self.__filename)
        return self.fp




    def __exit__(self, exc_type, exc_val, exc_tb):
        """"""
        self.fp.close()


