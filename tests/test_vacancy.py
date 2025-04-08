import re
from idlelib.run import capture_warnings

import pytest

from unittest.mock import patch

import src
from src.vacancy import Vacancy


def test_vacancy_init(vacancy_1: Vacancy) -> None:
    """
    Тест инициализации объекта Vacancy с конкретными атрибутами.
    Проверяет, что объект Vacancy корректно инициализирован с
    ожидаемыми параметрами
    :param vacancy_1:
    :return:
    """

    assert vacancy_1.id_vacancy == '1111111'
    assert vacancy_1.name_vacancy == 'backend/frontend/mobile'
    assert vacancy_1.area == 'Москва'
    assert vacancy_1.company == 'Test'
    assert vacancy_1.url_vacancy == 'https://example_url.com'
    assert vacancy_1.salary_from == 100000
    assert vacancy_1.salary_to == 120000
    assert vacancy_1.salary_currency == 'RUR'
    assert vacancy_1.requirements == 'Высшее техническое образование. Знание языка программирования <Python>'
    assert vacancy_1.status == 'Открытая'
    assert vacancy_1.date_published == '2024-03-20T17:52:03+0300'
    assert vacancy_1.work_format == 'Полная'
    assert vacancy_1.experience == 'От 1 года до 3 лет'
    assert isinstance(vacancy_1, Vacancy) is True


def test_vacancy_init_types(vacancy_1: Vacancy) -> None:
    """
    Проверяет, что объект Vacancy корректно инициализирован с
    ожидаемыми типами данных всех параметров
    :param vacancy_1:
    :return:
    """

    assert isinstance(vacancy_1.id_vacancy, str)
    assert isinstance(vacancy_1.name_vacancy, str)
    assert isinstance(vacancy_1.area, str)
    assert isinstance(vacancy_1.company, str)
    assert isinstance(vacancy_1.url_vacancy, str)
    assert isinstance(vacancy_1.salary_from, int)
    assert isinstance(vacancy_1.salary_to, int)
    assert isinstance(vacancy_1.salary_currency, str)
    assert isinstance(vacancy_1.requirements, str)
    assert isinstance(vacancy_1.status, str)
    assert isinstance(vacancy_1.date_published, str)
    assert isinstance(vacancy_1.work_format, str)
    assert isinstance(vacancy_1.experience, str)


def test_vacancy_validation_init_1(data_1: dict) -> None:
    """
    Проверяет, что объект корректно инициализируется при значении `None`
    атрибута `salary_from`, заменяя `None` на значение `salary_to`
    :return:
    """

    vacancy = Vacancy(data_1)
    assert vacancy.salary_from == vacancy.salary_to
    assert vacancy.salary_from == 250000


def test_vacancy_validation_init_2(data_2: dict) -> None:
    """
    Проверяет, что объект корректно инициализируется при значении `None`
    атрибута `salary_to`, заменяя `None` на значение `salary_from`
    :return:
    """

    vacancy = Vacancy(data_2)
    assert vacancy.salary_to == vacancy.salary_from
    assert vacancy.salary_to == 100000


def test_vacancy_validation_init_3(data_4: dict) -> None:
    """
    Проверяет, что объект корректно инициализируется при значении `None`
    атрибутов `salary_from` и`salary_to`, заменяя `None` на 0
    :param data_4:
    :return:
    """

    vacancy = Vacancy(data_4)
    assert vacancy.salary_to == vacancy.salary_from
    assert vacancy.salary_from == 0
    assert vacancy.salary_to == 0


@patch("src.vacancy.get_external_rate")
def test_vacancy_get_external_rate(mock_get_external_rate=None) -> None:
    """
    Проверяет, что при инициализации объекта `Vacancy`, заработная
    плата которого указана не в рублях, происходит пересчет в рубли
    с помощью стороннего сервиса (API)
    :param mock_get_external_rate:
    :return:
    """

    mock_get_external_rate.return_value = 27.0014
    result = src.vacancy.get_external_rate("BYR")
    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 5000, "to": 7500, "currency": 'BYR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }

    vacancy = Vacancy(data)
    assert vacancy.salary_from == 135007
    assert vacancy.salary_to == 202510
    assert vacancy.salary_currency == "RUR"


def test_vacancy_replace_requirement() -> None:
    """
    Проверяет, что значение атрибута `requirement` объекта `Vacancy`
    корректно инициализируется с исключением подстроки `<highlighttext>`
    :return:
    """

    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 100000, "to": 250000, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <highlighttext>Python</highlighttext>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    vacancy = Vacancy(data)
    assert vacancy.requirements == "Знание Python"
    assert "<highlighttext>" not in vacancy.requirements


def test_vacancy_value_error(capsys) -> None:
    """
    Проверяет, что при инициализации объекта с неполным набором атрибутов
    срабатывает исключение `KeyError` с соответствующим сообщением
    :param capsys:
    :return:
    """

    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        # "area": {"name": 'Москва'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 100000, "to": 250000, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <highlighttext>Python</highlighttext>'},
    }
    with pytest.raises(KeyError):
        vacancy = Vacancy(data)
        print(vacancy)

        captured = capsys.readouterr()
        assert captured.out == "KeyError: 'area'"


def test_vacancy_compars(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy, capsys) -> None:
    """
    Проверяет, что методы сравнения корректно сравнивают объекты `Vacancy`
     по атрибуту `salary_to` (максимальный размер заработной платы)
    :param vacancy_1:
    :param vacancy_2:
    :param vacancy_3:
    :param capsys:
    :return:
    """

    assert vacancy_1 < vacancy_2
    assert vacancy_1 <= vacancy_3
    assert vacancy_2 > vacancy_3
    assert vacancy_3 >= vacancy_1
    print(vacancy_1 < vacancy_2)
    captured_1 = capsys.readouterr()
    print(vacancy_2 > vacancy_1)
    captured_2 = capsys.readouterr()
    print(vacancy_1 > vacancy_2)
    captured_3 = capsys.readouterr()

    assert captured_1.out == "True\n"
    assert captured_2.out == "True\n"
    assert captured_3.out == "False\n"


def test_vacancy_get_vacancies_by_salary(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """
    Проверяет, что метод поиска вакансий с заданным диапазоном
    заработной платы корректно определяет вакансии
    :param vacancy_1:
    :param vacancy_2:
    :return:
    """

    assert 80000 <= vacancy_1.salary_to <= 120000
    assert 150000 <= vacancy_2.salary_to <= 300000
    assert vacancy_1.get_vacancies_by_salary("80000 - 120000") is True
    assert 150000 <= vacancy_2.salary_to <= 300000
    assert vacancy_2.get_vacancies_by_salary("150000 - 300000") is True
    assert vacancy_1.get_vacancies_by_salary("150000") is False

    list_vacancies = [vacancy_1, vacancy_2]
    salary_choice_less = []
    salary_choice_more = []
    for vacancy in list_vacancies:
        if vacancy.get_vacancies_by_salary("80000 - 120000"):
            salary_choice_less.append(vacancy)
        if vacancy.get_vacancies_by_salary("150000 - 300000"):
            salary_choice_more.append(vacancy)
    assert salary_choice_less == [vacancy_1]
    assert salary_choice_more == [vacancy_2]


def test_cast_vacancies_in_list() -> None:
    """
    Проверяет, что `classmethod` создает список с объектами `Vacancy`
    :return:
    """

    data_1 = {
        "id": '1111111',
        "name": 'backend/frontend/mobile',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 100000, "to": 120000, "currency": 'RUR'},
        "snippet": {"requirement": 'Высшее техническое образование. Знание языка программирования <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2024-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }

    data_2 = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": None, "to": 250000, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }

    data_in_list = [data_1, data_2]
    vacancies_list = Vacancy.cast_vacancies_in_list(data_in_list)
    assert isinstance(vacancies_list, list)

    for vacancy in vacancies_list:
        assert isinstance(vacancy, Vacancy)


def test_cast_vacancies_in_list_negative(data_1: dict, data_3: dict) -> None:
    """
    Проверяет, что `classmethod` вызывает исключение `ValueError`
    при создании списка с объектами `Vacancy`, не имеющими
    необходимых аргументов
    :param data_1:
    :param data_3:
    :return:
    """

    data_in_list = [data_1, data_3]
    with pytest.raises(ValueError):
        Vacancy.cast_vacancies_in_list(data_in_list)


def test_vacancy_str(vacancy_1: Vacancy, data_4: dict) -> None:
    """
    Проверяет, что метод возвращается строковое отображение
    объекта `Vacancy`
    :param vacancy_1:
    :param data_4:
    :return:
    """

    assert (str(vacancy_1)) == """
            Наименование вакансии - backend/frontend/mobile,
            месторасположение - Москва,
            работодатель - Test,
            url-адрес вакансии на сайте hh.ru - https://example_url.com,
            заработная плата - от 100000 до 120000 RUR,
            требования - Высшее техническое образование. Знание языка программирования <Python>,
            статус вакансии - Открытая,
            дата публикации вакансии - 2024-03-20T17:52:03+0300,
            форма трудоустройства - Полная,
            опыт работы - От 1 года до 3 лет\n"""

    vacancy_2 = Vacancy(data_4)
    assert (str(vacancy_2)) == """
            Наименование вакансии - backend разработчик,
            месторасположение - Москва,
            работодатель - Test_2,
            url-адрес вакансии на сайте hh.ru - https://example_url.com,
            заработная плата - не указана,
            требования - Знание <Python>,
            статус вакансии - Открытая,
            форма трудоустройства - Полная,
            опыт работы - От 1 года до 3 лет\n"""

def test_vacancy_repr(vacancy_1: Vacancy) -> None:
    """
    Проверяет, что метод возвращается строковое представление объекта `Vacancy`,
    предназначенное для разработчика
    :param vacancy_1:
    :return:
    """

    assert (repr(vacancy_1)) == """
        Vacancy(
        id='1111111', 
        name='backend/frontend/mobile', 
        area='Москва', 
        employer='Test', 
        url='https://example_url.com', 
        salary='от 100000 до 120000 RUR', 
        requirements='Высшее техническое образование. Знание языка программирования <Python>', 
        status='Открытая', 
        published_at='2024-03-20T17:52:03+0300', 
        employment_form='Полная', 
        experience='От 1 года до 3 лет'
        )"""


def test_vacancy_validate_data_key_error(data_1: dict, data_3: dict, capsys):
    """Проверяет корректность работы метода валидации данных"""

    with pytest.raises(KeyError):
        vacancy_1 = Vacancy(data_3)
        print(vacancy_1)
        captured_1 = capsys.readouterr()
        assert captured_1.out == "Отсутствуют необходимые ключи - ['snippet', 'type', 'published_at', 'employment_form', 'experience']"

    assert isinstance(data_1, dict) is True
    vacancy_2 = Vacancy(data_1)
    assert vacancy_2.__slots__ == ("id_vacancy", "name_vacancy", "area", "company",
                                   "url_vacancy", "salary_from", "salary_to",
                                   "salary_currency", "requirements", "status",
                                   "date_published", "work_format", "experience")

    right_len = len(data_1.keys())

    data = {
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": None, "to": 250000, "currency": 'RUR'},
    }
    assert "id" not in data.keys()

    assert len(data.keys()) != right_len

    # with pytest.raises(KeyError):
    try:
        vacancy_4 = Vacancy(data)
        # print(vacancy_4)
    except KeyError as e:
        print(f"Возникла ошибка KeyError: {e}")
    else:
        print("Не возникла ошибка KeyError")
    captured_3 = capsys.readouterr()
    assert captured_3.out == 'Возникла ошибка KeyError: "Отсутствуют необходимые ключи - [\'id\']"\n'


def test_vacancy_validate_data_type_error(data_3: dict, capsys):
    """Проверяет работу метода валидации данных при возникновении `TypeError`"""

    with pytest.raises(TypeError):
        data = [data_3]
        vacancy_2 = Vacancy(data)
        assert isinstance(data, dict) is False
        print(vacancy_2)
        captured_2 = capsys.readouterr()
        assert captured_2.out == "Ошибка: Данные должны быть словарем."





