import os
from contextlib import redirect_stderr
from unittest.mock import Mock, patch

import requests

from src.head_hunter_api import HeadHunterAPI, log_file, logger
from src.parser_api import ParserAPI


def test_hh_api_init() -> None:
    """Тест инициализации `HeadHunterAPI class`"""

    vacancy_hh = HeadHunterAPI()
    assert isinstance(vacancy_hh, HeadHunterAPI)
    assert isinstance(vacancy_hh, ParserAPI)
    assert vacancy_hh.headers == {"User-Agent": "HH-User-Agent"}
    assert vacancy_hh.params == {"text": "", "page": 0, "per_page": 100, "only_with_salary": "true"}
    assert vacancy_hh.url == "https://api.hh.ru/vacancies"
    assert vacancy_hh.vacancies == []


@patch("requests.get")
def test_hh_api_get_connect_success(mock_requests, capsys) -> None:
    """
    Проверяет, что метод возвращает `True`, если соединение с `API`
    установлено успешно
    :param mock_requests:
    :param capsys:
    :return:
    """

    vacancy_hh = HeadHunterAPI()
    mock_requests = Mock(side_effect=200)
    requests.get("https://api.hh.ru/vacancies").status_code = mock_requests.side_effect

    try:
        vacancy_hh.load_vacancies("")
    except requests.exceptions.RequestException as e:
        print(f"{e}")
    else:
        print("Соединение c API установлено успешно.")

    captured = capsys.readouterr()
    assert captured.out == "Соединение c API установлено успешно.\n"

    assert vacancy_hh._HeadHunterAPI__get_connect() is True

    with open(log_file, "r", encoding="utf-8") as file_logger:
        logger_read = file_logger.read().split(" | ")[-1]
        assert "Соединение с API сайта: 'https://api.hh.ru/' установлено успешно.\n" in logger_read


@patch("requests.get")
def test_hh_api_get_connect_http_error(mock_requests) -> None:
    """
    Проверяет, что при возникновении исключения`HTTPError` функция
    `__get_connect()` возвращает значение `False`, а в файл для
    логирования записывается соответствующее сообщение
    :param mock_requests:
    :return:
    """

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error")
    mock_requests.return_value = mock_response

    vacancy_hh = HeadHunterAPI()

    with patch.object(logger, "error") as mock_logger:
        connect = vacancy_hh._HeadHunterAPI__get_connect()
        assert connect is False
        mock_logger.assert_called_with("HTTP error: 403 Client Error")


@patch("requests.get")
def test_hh_api_get_connect_connection_error(mock_requests) -> None:
    """
    Проверяет, что при возникновении исключения`ConnectionError` функция
    `__get_connect()` возвращает значение `False`, а в файл для
    логирования записывается соответствующее сообщение
    :param mock_requests:
    :return:
    """

    mock_requests.side_effect = requests.exceptions.ConnectionError("Connection error")

    vacancy_hh = HeadHunterAPI()

    with patch.object(logger, "error") as mock_logger:
        connect = vacancy_hh._HeadHunterAPI__get_connect()
        assert connect is False
        mock_logger.assert_called_with("Ошибка: Connection error")


@patch("requests.get")
def test_hh_api_get_connect_timeout(mock_requests) -> None:
    """
    Проверяет, что при возникновении исключения`Timeout` функция
    `__get_connect()` возвращает значение `False`, а в файл для
    логирования записывается соответствующее сообщение
    :param mock_requests:
    :return:
    """
    mock_requests.side_effect = requests.exceptions.Timeout("Request timeout")

    vacancy_hh = HeadHunterAPI()

    with patch.object(logger, "error") as mock_logger:
        connect = vacancy_hh._HeadHunterAPI__get_connect()
        assert connect is False
        mock_logger.assert_called_with("Ошибка: Request timeout")


@patch("requests.get")
def test_hh_api_get_connect_request_exception(mock_requests) -> None:
    """
    Проверяет, что при возникновении исключения`RequestException` функция
    `__get_connect()` возвращает значение `False`, а в файл для
    логирования записывается соответствующее сообщение
    :param mock_requests:
    :return:
    """
    mock_requests.side_effect = requests.exceptions.RequestException("General error")

    vacancy_hh = HeadHunterAPI()

    with patch.object(logger, "error") as file_logger:
        connect = vacancy_hh._HeadHunterAPI__get_connect()
        assert connect is False
        file_logger.assert_called_with("Ошибка подключения: General error")


# patch('requests.get')
# patch('src.head_hunter_api.', 'response.json')
# def test_hh_api_load_vacancies_success(mock_response_json, mock_requests) -> None:
#     """
#     Тест проверяет, что при ошибке подключения в файл логируется сообщение
#     о невозможности загрузить вакансии и возвращается пустой список
#     :param mock_requests:
#     :return:
#     """
#
#     mock_response = Mock()
#     mock_response.side_effect = 200
#     mock_requests.return_value = mock_response
#
#     vacancy_hh = HeadHunterAPI()
#     mock_response_json.return_value = {"item": "Test vacancy"}
#     vacancies = vacancy_hh.load_vacancies("Test")
#     print(vacancies)
#     # assert vacancies == ["Test vacancy"]
#
#
#     # with open(log_file, 'r', encoding='utf-8') as mock_logger:
#     #     logger_read = (mock_logger.read().split(" | "))
#     #     assert "Получен список вакансий по ключевому слову: 'Test'.\n" in logger_read


@patch("requests.get")
def test_hh_api_load_vacancies_error(mock_requests) -> None:
    """
    Тест проверяет, что при ошибке подключения в файл логируется сообщение
    о невозможности загрузить вакансии и возвращается пустой список
    :param mock_requests:
    :return:
    """

    with open(os.devnull, "w") as f_null:
        with redirect_stderr(f_null):
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error")
            mock_requests.return_value = mock_response

            vacancy_hh = HeadHunterAPI()
            vacancies = vacancy_hh.load_vacancies("Python")
            assert vacancies == []

    with open(log_file, "r", encoding="utf-8") as file_logger:
        logger_read = file_logger.read().split(" | ")
        assert "Не удалось загрузить вакансии, отсутствует подключение.\n" in logger_read
