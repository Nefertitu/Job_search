class Vacancy:
    """Класс для работы с вакансиями"""
    __slots__ = ("name_vacancy", "area", "company", "url_vacancy", "salary_from", "salary_to", "salary_currency", "type_vacancy", "date_published", "work_format", "experience")

    def __init__(self, data):
        """Конструктор для создания экземпляра класса `Vacancy`"""
        self.validate_data(data)
        self.name_vacancy: str = data["name"]
        self.area: str = data["area"].get("name")
        self.company = data["employer"].get("name")
        self.url_vacancy: str = data["url"]
        self.salary_from = data["salary"].get("form")
        self.salary_to = data["salary"].get("to")
        self.salary_currency = data["salary"].get("currency")
        self.type_vacancy: str = data["type"].get("name")
        self.date_published: str = data["published_at"]
        self.work_format: str = data["work_format"].get("name")
        self.experience: str = data["experience"].get("name")


    def salary(self, data) -> str:
        """Метод возвращает заработную плату"""
        if data["salary"].get("from")  > 0 and data ["salary"].get("to") > 0:
            salary = f"От {self.salary_from} до {self.salary_to} {self.salary_currency}"
        elif data["salary"].get("from")  == "null" and data ["salary"].get("to") > 0:
            salary = f"{self.salary_to} {self.salary_currency}"
        elif data["salary"].get("from")  > 0 and data ["salary"].get("to") == "null":
            salary = f"{self.salary_from} {self.salary_currency}"
        else:
            salary = "Зарплата не указана"
        return salary


    def validate_data(self, data):
        """Метод валидации загруженных данных о вакансиях"""
        try:
            if not isinstance(data, dict):
                raise ValueError("Неверный формат данных вакансии.")
            if not all(key in Vacancy for key in ["name_vacancy", "area", "company", "url_vacancy", "salary_from", "salary_to", "salary_currency", "type_vacancy", "date_published", "work_format", "experience"]):
                raise ValueError("Отсутствуют обязательные поля.")
        except ValueError() as e:
            print(f"{e}")
        else:
            return self.validate_data


    def __lt__(self, other):
        """Метод сравнения зарплат"""
        return self.salary < other.salary