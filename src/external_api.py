import requests


def get_external_rate(currency_name):
    """Функция для получения текущего курса валют"""

    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url)
    if currency_name == "BYR":
        currency_name = "BYN"
    data_currency = response.json()["Valute"][currency_name]["Value"]

    return data_currency


# print(get_external_rate("BYR"))

