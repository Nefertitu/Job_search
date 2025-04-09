from unittest.mock import patch, Mock

import pytest


from src.head_hunter_api import HeadHunterAPI, logger
from src.utils import filter_vacancies, sort_vacancies, get_top_vacancies, user_interaction
from src.vacancy import Vacancy
from tests.conftest import data_2


@pytest.mark.parametrize(
    "search_words, vacancy_data, expected_out",
    [
        ({"backend", "разработчик"},
        {'высшее', 'frontend', 'москва', 'знание',
        'языка', 'backend', 'программирования',
        'техническое', 'mobile', 'образование',
        'python'}, False),
        ({"backend", "разработчик"},
        {'знание', 'москва', 'backend', 'python',
        'разработчик'}, True),
    ])
def test_filter_vacancies_param_positive(search_words, vacancy_data, expected_out, vacancy_1: Vacancy, vacancy_2: Vacancy):
    """
    Проверяет, что список вакансий корректно фильтруется с параметром `positive` -
    в список попадают вакансии, которые соответствуют списку ключевых слов
    :param search_words:
    :param vacancy_data:
    :param expected_out:
    :param vacancy_1:
    :param vacancy_2:
    :return:
    """

    vacancies = [vacancy_1, vacancy_2]
    search_vacancies = filter_vacancies(vacancies, str(search_words), param="positive")

    assert search_words.issubset(vacancy_data) == expected_out
    assert vacancy_1 not in search_vacancies
    assert vacancy_2 == search_vacancies[0]


@pytest.mark.parametrize(
    "search_words, vacancy_data, expected_out",
    [
        ({"backend", "python", "разработчик"},
        {'высшее', 'frontend', 'москва', 'знание',
        'языка', 'backend', 'программирования',
        'техническое', 'mobile', 'образование',
        'python'}, False),
        ({"backend", "python", "разработчик"},
        {'знание', 'москва', 'backend', 'python',
        'разработчик'}, True),
    ])
def test_filter_vacancies_param_negative(search_words, vacancy_data, expected_out, vacancy_1: Vacancy, vacancy_2: Vacancy):
    """
    Проверяет, что список вакансий корректно фильтруется с параметром `negative` -
    в список попадают вакансии, которые НЕ соответствуют списку ключевых слов
    :param search_words:
    :param vacancy_data:
    :param expected_out:
    :param vacancy_1:
    :param vacancy_2:
    :return:
    """

    vacancies = [vacancy_1, vacancy_2]
    search_vacancies = filter_vacancies(vacancies, str(search_words), param="negative")

    assert search_words.issubset(vacancy_data) == expected_out
    assert vacancy_1 == search_vacancies[0]
    assert vacancy_2 not in search_vacancies


@pytest.mark.parametrize(
    "search_words, vacancy_data",
    [
        (
                {'frontend', 'python', 'разработчик'},
                {'образование', 'языка', 'техническое',
                 'mobile', 'программирования', 'python',
                 'backend', 'frontend', 'высшее',
                 'знание', 'москва'}
        ),
        (
                {'frontend', 'python', 'разработчик'},
                {'знание', 'москва', 'backend',
                 'python', 'разработчик'}
        ),
    ])
def test_filter_vacancies_param_empty(search_words, vacancy_data, vacancy_1: Vacancy, vacancy_2: Vacancy):
    """
    Проверяет, что список вакансий корректно фильтруется с параметром `negative` -
    в список попадают вакансии, которые НЕ соответствуют списку ключевых слов
    :param search_words:
    :param vacancy_data:
    :param vacancy_1:
    :param vacancy_2:
    :return:
    """

    vacancies = [vacancy_1, vacancy_2]
    search_vacancies = filter_vacancies(vacancies, str(search_words), param="positive")

    if search_words.issubset(vacancy_data) is False:
        assert search_vacancies == []


def test_sort_vacancies(vacancy_1: Vacancy, vacancy_2: Vacancy) -> None:
    """Проверяет, что список вакансий сортируется в порядке убывания"""

    vacancies = [vacancy_1, vacancy_2]
    sorted_vacancies = sort_vacancies(vacancies)
    salary_1 = vacancy_1.salary_to
    salary_2 = vacancy_2.salary_to
    assert salary_2 == 250000
    assert salary_1 == 120000
    assert 250000 > 120000
    assert sorted_vacancies[0] == vacancy_2
    assert sorted_vacancies[1] == vacancy_1
    assert salary_2 > salary_1


def test_get_top_vacancies(vacancy_1: Vacancy, vacancy_2: Vacancy, vacancy_3: Vacancy) -> None:
    """Проверяет, что из списка вакансий выбирается указанное количество вакансий"""

    vacancies = [vacancy_1, vacancy_2, vacancy_3]
    sorted_vacancies = sort_vacancies(vacancies)
    len_sorted_vacancies = len(sorted_vacancies)
    assert len_sorted_vacancies == 3
    top_vacancies = get_top_vacancies(sorted_vacancies, 2)
    assert len(top_vacancies) == 2
    top_vacancies_2 = get_top_vacancies(sorted_vacancies, 4)
    assert len(top_vacancies_2) == 3

#
@patch('requests.get')
@patch("builtins.input", side_effect=["Python", "Петербург", "100000 - 300000", "нет", "1"])
def test_user_interaction(mock_input, mock_requests_get, data_1, data_2, data_5, capsys):
    """Проверяет работу функции взаимодействия с пользователем"""

    logger.propagate = True

    test_vacancies = [
        data_1,
        data_2,
        data_5
    ]

    mock_response = Mock()
    mock_response.json.return_value = {"items": test_vacancies}
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response
    vacancies_hh = HeadHunterAPI()
    # vacancies_hh._HeadHunterAPI__url == "https://example.com"
    # print(dir(vacancies_hh))
    # connect = vacancies_hh._HeadHunterAPI__get_connect()
    # assert connect is True
    with patch("src.head_hunter_api.HeadHunterAPI.load_vacancies", return_value=test_vacancies) as mock_load:
        result = user_interaction()
        print(result)
        captured = capsys.readouterr()
        assert captured.out == """
Выполняется запрос к API сайта hh.ru...

Произведена запись полученных данных в файл 'vacancies_save.json'.

В файле 'vacancies_save.json' остается полный перечень вакансий.

Общее количество вакансий, полученных после фильтрации, составляет 1 шт.
[
        Vacancy(
        id='2222222', 
        name='Junior, backend разработчик', 
        area='Санкт-Петербург', 
        employer='Test_3', 
        url='https://example_url.com', 
        salary='от 80000 до 120000 RUR', 
        requirements='Знание <Python>', 
        status='Открытая', 
        published_at='2025-02-20T17:52:03+0300', 
        employment_form='Полная', 
        experience='От 1 года до 3 лет'
        )]\n"""

        mock_load.assert_called_once()


