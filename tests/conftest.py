import pytest

from src.vacancy import Vacancy, log_file


@pytest.fixture
def vacancy_1() -> Vacancy:
    """Возвращает экземпляр класса `Vacancy`"""
    data = {
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
    return Vacancy(data)


@pytest.fixture
def vacancy_2() -> Vacancy:
    """Возвращает экземпляр класса `Vacancy`"""
    data = {
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
    return Vacancy(data)

@pytest.fixture
def vacancy_3() -> Vacancy:
    """Возвращает экземпляр класса `Vacancy`"""
    data = {
        "id": '2222222',
        "name": 'Junior, backend разработчик',
        "area": {"name": 'Санкт-Петербург'},
        "employer": {"name": 'Test_3'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 80000, "to": 120000, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-02-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    return Vacancy(data)


@pytest.fixture
def data_1() -> dict:
    """Возвращает словарь с ключами для создания экземпляра класса `Vacancy`"""
    data = {
        "id": "2222222",
        "name": "backend разработчик",
        "area": {"name": "Москва"},
        "employer": {"name": "Test_2"},
        "alternate_url": "https://example_url.com",
        "salary": {"from": None, "to": 250000, "currency": "RUR"},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": "Открытая"},
        "published_at": "2025-03-20T17:52:03+0300",
        "employment_form": {"name": "Полная"},
        "experience": {"name": "От 1 года до 3 лет"},
    }
    return data

@pytest.fixture
def data_2() -> dict:
    """Возвращает словарь с ключами для создания экземпляра класса `Vacancy`"""
    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 100000, "to": None, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    return data

@pytest.fixture
def data_3() -> dict:
    """Возвращает словарь с неполным набором ключей"""
    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": None, "to": 250000, "currency": 'RUR'},
    }
    return data

@pytest.fixture
def data_4() -> dict:
    """Возвращает словарь с ключами для создания экземпляра класса `Vacancy`"""
    data = {
        "id": '2222222',
        "name": 'backend разработчик',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test_2'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": None, "to": None, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    return data


@pytest.fixture
def data_5() -> dict:
    """Возвращает словарь с ключами для создания экземпляра класса `Vacancy`"""
    data = {
        "id": '2222222',
        "name": 'Junior, backend разработчик',
        "area": {"name": 'Санкт-Петербург'},
        "employer": {"name": 'Test_3'},
        "alternate_url": 'https://example_url.com',
        "salary": {"from": 80000, "to": 120000, "currency": 'RUR'},
        "snippet": {"requirement": 'Знание <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2025-02-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    return data


@pytest.fixture(autouse=True)
def clear_log():
    """Фикстура для очистки лог-файла перед каждым тестом"""

    open(log_file, "w", encoding="utf-8").close()


