import unittest
from unittest.mock import patch, Mock

from src.external_api import get_external_rate


@patch('requests.get')
def test_get_external_rate(mock_requests_get):
    """
    Проверяет, что функция корректно возвращает значения курса валют
    :param mock_requests_get:
    :return:
    """

    mock_response = Mock()
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response
    mock_response.json.return_value = {
        "Valute": {
            "USD": {"Value": 75.50},
            "EUR": {"Value": 85.25},
            "BYN": {"Value": 28.30}
        }
    }

    assert get_external_rate("USD") ==  75.50
    assert get_external_rate("EUR") == 85.25
    assert get_external_rate("BYR") == 28.30  # Проверка конвертации BYR->BYN

    mock_requests_get.assert_called_with("https://www.cbr-xml-daily.ru/daily_json.js")