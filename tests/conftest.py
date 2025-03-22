import pytest

from src.vacancy import Vacancy


@pytest.fixture
def vacancy_1() -> Vacancy:
    """Возвращает экземпляр класса ⓃVacancyⓃ"""
    data = {
        "id": '1111111',
        "name": 'backend/frontend/mobile',
        "area": {"name": 'Москва'},
        "employer": {"name": 'Test'},
        "alternate_url": 'sample_url',
        "salary": {"from": 100000, "to": 120000, "currency": 'RUR'},
        "snippet": {"requirement": 'Высшее техническое образование. Знание языка программирования <Python>'},
        "type": {"name": 'Открытая'},
        "published_at": '2024-03-20T17:52:03+0300',
        "employment_form": {"name": 'Полная'},
        "experience": {"name": 'От 1 года до 3 лет'},
    }
    return Vacancy(data)
