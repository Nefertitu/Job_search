import logging
import re
from pathlib import Path

from src.external_api import get_external_rate

log_dir = Path(__file__).parent.parent / "data"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = str((log_dir / "logging_reports.log").absolute().resolve()).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
shared_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
shared_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(message)s | [%(filename)s:%(lineno)d]")
shared_handler.setFormatter(formatter)
shared_handler.setFormatter(formatter)
logger.addHandler(shared_handler)
logger.propagate = False


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = (
        "id_vacancy",
        "name_vacancy",
        "area",
        "company",
        "url_vacancy",
        "salary_from",
        "salary_to",
        "salary_currency",
        "requirements",
        "status",
        "date_published",
        "work_format",
        "experience",
    )
    vacancies: list = []

    def __init__(self, data: dict) -> None:
        """Конструктор для создания экземпляра класса `Vacancy`"""
        self.__validate_data(data)
        self.id_vacancy: str = data["id"]
        self.name_vacancy: str = data["name"]
        self.area: str = data["area"]["name"]
        self.company = data.get("employer", {}).get("name", "не указано")
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
            # logger.info("Выполнен перерасчет заработной платы, указанной не в рублях.")
        requirement = data["snippet"]["requirement"]
        self.requirements: str = (
            re.sub(r"<highlighttext>(.\w*)</highlighttext>", r"\1", requirement) if requirement else ""
        )
        self.status: str = data["type"]["name"]
        self.date_published: str = data["published_at"]
        self.work_format: str = data.get("employment_form", {}).get("name") or ""
        self.experience: str = data.get("experience", {}).get("name") or ""
        super().__init__()

    def __repr__(self) -> str:
        """Возвращает однозначное строковое представление объекта класса `Vacancy`,
        пригодное для отладки объекта."""

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
            return f"""
            Наименование вакансии - {self.name_vacancy},
            месторасположение - {self.area},
            работодатель - {self.company},
            url-адрес вакансии на сайте hh.ru - {self.url_vacancy},
            заработная плата - не указана,
            требования - {self.requirements},
            статус вакансии - {self.status},
            форма трудоустройства - {self.work_format},
            опыт работы - {self.experience}
"""
        else:
            return f"""
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
"""

    @classmethod
    def __validate_data(cls, data: dict) -> bool:
        """Метод валидации загруженных данных о вакансиях"""

        if not isinstance(data, dict):
            logger.error("Ошибка: данные должны быть словарем.")
            raise TypeError("Ошибка: данные должны быть словарем.")

        basic_keys = {
            "id": {
                "name",
                "area",
                "employer",
                "alternate_url",
                "salary",
                "snippet",
                "type",
                "published_at",
                "employment_form",
                "experience",
            }
        }

        missing_keys = [key for key in basic_keys.keys() if key not in data]

        if missing_keys or data["id"] is None:
            logger.error(f"Отсутствуют необходимые ключи - {missing_keys}")
            raise KeyError(f"Отсутствуют необходимые ключи - {missing_keys}")

        else:
            return True

    @classmethod
    def cast_vacancies_in_list(cls, vacancies_data: list) -> list:
        """Метод возвращает список вакансий"""

        try:
            vacancies_objects = [cls(vacancy) for vacancy in vacancies_data]
        except KeyError as e:
            logger.error(f"Ошибка в данных вакансии: {e}")
            raise ValueError(f"Ошибка в данных вакансии: {e}") from e

        return vacancies_objects

    def __le__(self, other: "Vacancy") -> bool:
        """Метод сравнения зарплат - меньше или равно"""
        if not isinstance(other, Vacancy):
            logger.error(f"Не возможно сравнить экземпляр `Vacancy` с {type(other).__name__}")
        return int(self.salary_to) <= int(other.salary_to)

    def __lt__(self, other: "Vacancy") -> bool:
        """Метод сравнения зарплат - меньше"""
        if not isinstance(other, Vacancy):
            logger.error(f"Не возможно сравнить экземпляр `Vacancy` с {type(other).__name__}")
        return int(self.salary_to) < int(other.salary_to)

    def __ge__(self, other:"Vacancy") -> bool:
        """Метод сравнения зарплат - больше или равно"""
        if not isinstance(other, Vacancy):
            logger.error(f"Не возможно сравнить экземпляр `Vacancy` с {type(other).__name__}")
        return int(self.salary_to) >= int(other.salary_to)

    def __gt__(self, other: "Vacancy") -> bool:
        """Метод сравнения зарплат - больше"""
        if not isinstance(other, Vacancy):
            logger.error(f"Не возможно сравнить экземпляр `Vacancy` с {type(other).__name__}")
        return int(self.salary_to) > int(other.salary_to)

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
