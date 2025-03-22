import re
from typing import Any

from src.utils import get_external_rate


class Vacancy:
    """Класс для работы с вакансиями"""
    __slots__ = ("id_vacancy", "name_vacancy", "area", "company", "url_vacancy", "salary_from", "salary_to", "salary_currency", "requirements", "type_vacancy", "date_published", "work_format", "experience")
    vacancies = []
    def __init__(self, data):
        """Конструктор для создания экземпляра класса `Vacancy`"""
        self.__validate_data(data)
        self.id_vacancy: str = data["id"]
        self.name_vacancy: str = data["name"]
        self.area: str = data["area"]["name"]
        self.company = data["employer"]["name"]
        self.url_vacancy: str = data["alternate_url"]
        self.salary_from: int = data["salary"]["from"]
        self.salary_to: int = data["salary"]["to"]
        if data["salary"]["to"] is None and data["salary"]["from"] is not None:
            self.salary_to = self.salary_from
        if data["salary"]["to"] is not None and data["salary"]["from"] is None:
            self.salary_from = self.salary_to
        if data["salary"]["to"] is None and data["salary"]["from"] is None:
            self.salary_to, self.salary_from = 0, 0
        self.salary_currency = data["salary"]["currency"]
        # if data["salary"]["currency"] != "RUR":
        #     self.salary_from = round(self.salary_from * get_external_rate(self.salary_currency))
        #     self.salary_to = round(self.salary_to * get_external_rate(self.salary_currency))
        #     self.salary_currency = "RUR"
        # if "highlighttext>" in data["snippet"]["requirement"] and "</" in data["snippet"]["requirement"]:
        #     self.requirements = data["snippet"]["requirement"].replace("highlighttext>", "").replace("</", ">")
        # else:
        self.requirements = data["snippet"]["requirement"]
        self.type_vacancy: str = data["type"]["name"]
        self.date_published: str = data["published_at"]
        self.work_format: str = data["employment_form"]["name"]
        self.experience: str = data["experience"]["name"]
        super().__init__()

    def __repr__(self):
        """"""
        return f"""
        Vacancy(
        id='{self.id_vacancy}', 
        name='{self.name_vacancy}', 
        area='{self.area}', 
        employer='{self.company}', 
        url='{self.url_vacancy}', 
        salary='от {self.salary_from} до {self.salary_to} {self.salary_currency}', 
        requirements='{self.requirements}', 
        type='{self.type_vacancy}', 
        published_at='{self.date_published}', 
        employment_form='{self.work_format}', 
        experience='{self.experience}'
        )"""

    def __str__(self) -> str:
        """Строковое отображение экземпляра класса `Vacancy`"""

        if self.salary_to == 0 and self.salary_from == 0:
            return (f"Наименование вакансии - {self.name_vacancy}, "
                    f"месторасположение - {self.area}, "
                    f"работодатель - {self.company}, "
                    f"url-адрес вакансии на сайте hh.ru - {self.url_vacancy}, "
                    f"заработная плата - не указана, "
                    f"требования - {self.requirements}, "
                    f"дата публикации вакансии - {self.date_published}, "
                    f"форма трудоустройства - {self.work_format}, "
                    f"опыт работы - {self.experience}")
        else:
            return (f"Наименование вакансии - {self.name_vacancy}, "
                    f"месторасположение - {self.area}, "
                    f"работодатель - {self.company}, "
                    f"url-адрес вакансии на сайте hh.ru - {self.url_vacancy}, "
                    f"заработная плата - от {self.salary_from} до {self.salary_to} {self.salary_currency}, "
                    f"требования - {self.requirements}, "
                    f"дата публикации вакансии - {self.date_published}, "
                    f"форма трудоустройства - {self.work_format}, "
                    f"опыт работы - {self.experience}")

    def __validate_data(self, data):
        """Метод валидации загруженных данных о вакансиях"""

        for vacancy in data:
            try:
                if not isinstance(vacancy, dict):
                    continue
                if not all(key in self for key in
                           ["name_vacancy", "area", "company", "url_vacancy", "salary_from", "salary_to",
                            "salary_currency", "requirements", "type_vacancy", "date_published", "work_format", "experience"]):
                    continue

            except Exception as e:
                print(f"{e}")

            else:
                self.vacancies.append(vacancy)

        return self.vacancies

    @property
    def validate_data(self):
        """Метод возвращает значение данных о вакансиях, прошедших валидацию"""
        return self.__validate_data

    def __le__(self, other):
        """Метод сравнения зарплат - меньше или равно"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) <= int(other.salary_to)

    def __ge__(self, other):
        """Метод сравнения зарплат - больше или равно"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) >= int(other.salary_to)

    def get_vacancies_by_salary(self, salary_range: str) -> Any:
        """Метод для поиска вакансий с заданным диапазоном заработной платы"""

        list_salary = re.findall(r"([\d]{1,})", salary_range)
        min_salary, max_salary = int(min(list_salary)), int(max(list_salary))

        if min_salary <= self.salary_to <= max_salary:
            return True
        return False


