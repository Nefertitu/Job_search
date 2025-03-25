import re

from src.external_api import get_external_rate


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ("id_vacancy", "name_vacancy", "area", "company", "url_vacancy", "salary_from", "salary_to", "salary_currency", "requirements", "status", "date_published", "work_format", "experience")
    vacancies = []

    def __init__(self, data) -> None:
        """Конструктор для создания экземпляра класса `Vacancy`"""
        self.__validate_data(data)
        self.id_vacancy: str = data["id"]
        self.name_vacancy: str = data["name"]
        self.area: str = data["area"]["name"]
        self.company = (data.get("employer", {}).get("name", "не указано"))
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
        if data["salary"]["currency"] != "RUR":
            self.salary_from = round(self.salary_from * get_external_rate(self.salary_currency))
            self.salary_to = round(self.salary_to * get_external_rate(self.salary_currency))
            self.salary_currency = "RUR"
        requirement = data["snippet"]["requirement"]
        self.requirements: str = re.sub(r'<highlighttext>(.\w*)</highlighttext>', r'\1', requirement) if requirement else ""
        self.status: str = data["type"]["name"]
        self.date_published: str = data["published_at"]
        self.work_format: str = (data.get("employment_form", {}).get("name") or "")
        self.experience: str = (data.get("experience", {}).get("name") or "")
        super().__init__()

    def __repr__(self) -> str:
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
        status='{self.status}', 
        published_at='{self.date_published}', 
        employment_form='{self.work_format}', 
        experience='{self.experience}'
        )"""

    def __str__(self) -> str:
        """Строковое отображение экземпляра класса `Vacancy`"""

        if self.salary_to == 0 and self.salary_from == 0:
            return (f"""
            Наименование вакансии - {self.name_vacancy},
            месторасположение - {self.area},
            работодатель - {self.company},
            url-адрес вакансии на сайте hh.ru - {self.url_vacancy},
            заработная плата - не указана,
            требования - {self.requirements},
            статус вакансии - {self.status},
            форма трудоустройства - {self.work_format},
            опыт работы - {self.experience}
""")
        else:
            return (f"""
            Наименование вакансии - {self.name_vacancy},
            месторасположение - {self.area},
            работодатель - {self.company},
            url-адрес вакансии на сайте hh.ru - {self.url_vacancy},
            заработная плата - от {self.salary_from} до {self.salary_to} {self.salary_currency},
            требования - {self.requirements},
            статус вакансии - {self.status},
            дата публикации вакансии - {self.date_published},
            форма трудоустройства - {self.work_format},
            опыт работы - {self.experience}
""")

    @classmethod
    def __validate_data(cls, data: dict) -> bool:
        """Метод валидации загруженных данных о вакансиях"""

        if not isinstance(data, dict):
            raise TypeError("Ошибка: данные должны быть словарем.")

        basic_keys = {
            "id":
                {
                "name", "area", "employer",
                "alternate_url", "salary", "snippet",
                "type", "published_at",
                "employment_form", "experience"
                }
        }
        # nested_keys = {
        #     "area": ["name"],
        #     "employer": ["name"],
        #     "salary": ["from", "to", "currency"],
        #     "snippet": ["requirement"],
        #     "type": ["name"],
        #     "employment_form": ["name"],
        #     "experience": ["name"]
        # }
        missing_keys = [key for key in basic_keys.keys() if key not in data]

        if missing_keys or data["id"] is None:
            raise KeyError(f"Отсутствуют необходимые ключи - {missing_keys}")

        # for first_key, second_keys in nested_keys:
        #     if first_key not in data:
        #         continue
        #     if not isinstance(first_key, dict):
        #         raise ValueError(f"Ключ '{first_key}' должен быть словарём")
        #
        #     missing_nested = [k for k in second_keys if k not in data[first_key]]
        #     if missing_nested:
        #         raise KeyError(f"В '{first_key}' отсутствуют ключи: {missing_nested}")

        else:
            return True

    # @property
    # def validate_data(self):
    #     """Метод возвращает значение данных о вакансиях, прошедших валидацию"""
    #
    #     return self.__validate_data

    @classmethod
    def cast_vacancies_in_list(cls, vacancies_data: list) -> list:
        """Метод возвращает список вакансий"""

        try:
            vacancies_objects = [cls(vacancy) for vacancy in vacancies_data]
        except KeyError as e:
            raise ValueError(f"Ошибка в данных вакансии: {e}") from e

        return vacancies_objects

    def __le__(self, other) -> bool:
        """Метод сравнения зарплат - меньше или равно"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) <= int(other.salary_to)

    def __lt__(self, other) -> bool:
        """Метод сравнения зарплат - меньше"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) < int(other.salary_to)

    def __ge__(self, other) -> bool:
        """Метод сравнения зарплат - больше или равно"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) >= int(other.salary_to)

    def __gt__(self, other) -> bool:
        """Метод сравнения зарплат - больше"""
        if isinstance(other, Vacancy):
            return int(self.salary_to) > int(other.salary_to)

    # def __eq__(self, other):
    #     """Метод сравнения зарплат - больше"""
    #     if isinstance(other, Vacancy):
    #         return int(self.salary_to) == int(other.salary_to)
    #
    # def __ne__(self, other):
    #     """Метод сравнения зарплат - больше"""
    #     if isinstance(other, Vacancy):
    #         return int(self.salary_to) != int(other.salary_to)

    # def __len__(self) -> int:
    #     """Метод для подсчета количества экземпляров
    #     класса `Vacancy` в списке"""
    #
    #     if self.vacancies:
    #         return len(self.vacancies)
    #     else:
    #         return 0

    def get_vacancies_by_salary(self, salary_range: str) -> bool:
        """Метод для поиска вакансий с заданным диапазоном заработной платы"""

        list_salary = re.findall(r"([\d]{1,})", salary_range)
        if len(list_salary) != 2:
            return False
        min_salary, max_salary = (min(int(i) for i in list_salary)), (max(int(i) for i in list_salary))
        if min_salary <= self.salary_to <= max_salary:
            return True
        else:
            return False




