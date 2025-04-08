import json
import logging
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.base_file_handler import BaseFileHandler
from src.vacancy import Vacancy

log_dir = Path(__file__).parent.parent / 'data'
log_dir.mkdir(parents=True, exist_ok=True)
log_file = str((log_dir / 'logging_reports.log').absolute().resolve()).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

shared_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
shared_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
shared_handler.setFormatter(formatter)
logger.addHandler(shared_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.propagate = False

# print(f"Лог файл: {log_file}")

json_saver_file = str((log_dir / 'vacancies_save.json').absolute().resolve()).replace("\\", "/")

class JsonHandler(BaseFileHandler):
    """Класс для работы с JSON-файлами"""

    def __init__(self, data: list = None, mode: str = 'w') -> None:
        """Конструктор для экземпляра класса `JsonProcessor`"""
        self.data = data
        self.mode: str = mode
        self.__file: str = json_saver_file
        super().__init__()

    def __enter__(self) -> Any:
        """Метод для входа в контекстный менеджер"""
        self.fp = open(self.__file, self.mode, encoding="utf-8")
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Метод для выхода из контекстного менеджера"""
        self.fp.close()

    def get_data(self) -> dict:
        """Метод для получения данных из JSON-файла"""
        try:
            with open(self.__file, mode='r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    logger.info(f"Получены данные из файла: '{(self.__file).split("/")[-1]}'.")
                    return data
                except JSONDecodeError as e:
                    logger.error(f"Ошибка чтения JSON-файла: {e.__class__.__name__}.")
        except FileNotFoundError:
            logger.error(f"Файл '{(self.__file).split("/")[-1]}' не найден.")


    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления данных в JSON-файл"""

        vacancies = []
        data = {vacancy.id_vacancy:
            {
                "name": vacancy.name_vacancy,
                "area": vacancy.area,
                "employer": vacancy.company,
                "url": vacancy.url_vacancy,
                "salary": f"от {vacancy.salary_from} до {vacancy.salary_to} {vacancy.salary_currency}",
                "requirement": vacancy.requirements,
                "status": vacancy.status,
                "published_at": vacancy.date_published,
                "employment_form": vacancy.work_format,
                "experience": vacancy.experience
            }
        }

        try:
            with open(self.__file, mode='r', encoding='utf-8') as f:
                file_vacancies = json.load(f)
        except JSONDecodeError as e:
            logger.error(f"Ошибка при попытке чтения файла: {e.__class__.__name__}.")
            vacancies.append(data)
            with open(self.__file, self.mode, encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)   # type: ignore

        else:
            file_vacancies_id = []

            for file_vacancy in file_vacancies:
                if list(file_vacancy.keys())[0] not in file_vacancies_id:
                    file_vacancies_id.append(list(file_vacancy.keys())[0])
                    vacancies.append(file_vacancy)
                else:
                    continue

            if vacancy.id_vacancy in file_vacancies_id:
                with open(self.__file, self.mode, encoding='utf-8') as f:
                    json.dump(vacancies, f, ensure_ascii=False, indent=4)   #type: ignore

            else:
                vacancies.append(data)
                with open(self.__file, self.mode, encoding='utf-8') as f:
                    json.dump(vacancies, f, ensure_ascii=False, indent=4)   #type: ignore

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для удаления данных из JSON-файла"""

        try:
            with open(self.__file, mode='r', encoding='utf-8') as f:
                file_vacancies = json.load(f)
        except JSONDecodeError as e:
            logger.error(f"Ошибка при попытке чтения файла: {e.__class__.__name__}.")

        else:
            new_data = [dict for dict in file_vacancies if list(dict.keys())[0] != vacancy.id_vacancy]

            with open(self.__file, self.mode, encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)   #type: ignore


# object_json = JsonHandler()
# print(object_json._JsonHandler__file)
# # data = object_json.get_data()
# # print(data)
# object_json._JsonHandler__file = "example.json"
# print(object_json._JsonHandler__file)
# json_data = object_json.get_data()
# print(json_data)

# import chardet
#
# with open('../data/logging_reports.log', 'rb') as f:
#     raw_data = f.read(1000)  # Читаем первые 1000 байт
#     print(chardet.detect(raw_data))
#
