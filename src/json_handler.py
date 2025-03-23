import json
from json import JSONDecodeError

from src.base_file_handler import BaseFileHandler


class JsonHandler(BaseFileHandler):
    """Класс для работы с JSON-файлами"""

    def __init__(self, data: list = None, mode: str = 'w'):
        """Конструктор для экземпляра класса `JsonProcessor`"""
        self.data = data
        self.mode: str = mode
        self.__file: str = "./data/vacancies_save.json"
        super().__init__()

    def __enter__(self):
        """Метод для входа в контекстный менеджер"""
        self.fp = open(self.__file, self.mode, encoding="utf-8")
        return self.fp

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Метод для выхода из контекстного менеджера"""
        self.fp.close()

    def read(self):
        with open(self.__file, mode='r', encoding='utf-8') as f:
            read_json = json.load(f)
            # dict_vacancies = json.dumps(read_json, ensure_ascii=False, indent=4)
            return read_json

    def get_data(self):
        """Метод для получения данных из JSON-файла"""
        if self.__file:
            with open(self.__file) as f:
                data = json.load(f)
            return data
        return "Файл не найден."


    def add_vacancy(self, vacancy):
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
            print("")
            vacancies.append(data)
            with open(self.__file, self.mode, encoding='utf-8') as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=4)

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
                    json.dump(vacancies, f, ensure_ascii=False, indent=4)

            else:
                vacancies.append(data)
                with open(self.__file, self.mode, encoding='utf-8') as f:
                    json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy):
        """Метод для удаления данных из JSON-файла"""

        try:
            with open(self.__file, mode='r', encoding='utf-8') as f:
                file_vacancies = json.load(f)
        except JSONDecodeError as e:
            print(f"Ошибка при попытке чтения файла: {e}")

        else:
            new_data = [dict for dict in file_vacancies if list(dict.keys())[0] != vacancy.id_vacancy]

            with open(self.__file, self.mode, encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)


