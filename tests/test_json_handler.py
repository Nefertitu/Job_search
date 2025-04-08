import json

from json import JSONDecodeError
from unittest.mock import patch
from src.base_file_handler import BaseFileHandler
from src.json_handler import JsonHandler, log_file, logger
from src.vacancy import Vacancy


def test_json_handler_init():
    """Тест инициализации экземпляра класса `JsonHandler`"""

    object_json = JsonHandler()
    assert isinstance(object_json, JsonHandler)
    assert issubclass(type(object_json), BaseFileHandler)
    # print(dir(object_json))
    assert object_json.mode == "w"
    assert (object_json._JsonHandler__file).split("/")[-1] == "vacancies_save.json"


def test_json_handler_get_data_logger() -> None:
    """Проверяет, что при успешном получении данных из JSON-файла,
    производится соответствующая запись в лог-файл"""

    logger.propagate = True
    object_json = JsonHandler()
    data = object_json.get_data()

    with open(log_file, encoding='utf-8') as file_logger:
        logger_read = (file_logger.read())
        assert "Получены данные из файла: 'vacancies_save.json'.\n" in logger_read


def test_json_handler_get_data_success() -> None:
    """Проверяет, что метод читает данные из JSON-файла"""

    object_json = JsonHandler()

    with patch.object(object_json, "get_data", return_value={"item": {"vacancy": "Test vacancy"}}) as mock_get_data:
        object_json.get_data()
        assert object_json.get_data() == {"item": {"vacancy": "Test vacancy"}}


def test_json_handler_get_data_no_file(caplog) -> None:
    """Проверяет, что при отсутствии файла для чтения выбрасывается исключение
    `FileNotFoundError` и производится соответствующая запись в лог-файл"""

    logger.propagate = True

    object_json = JsonHandler()
    object_json._JsonHandler__file = "example.json"
    assert object_json._JsonHandler__file == "example.json"

    try:
        object_json.get_data()
    except FileNotFoundError as e:
        assert f"{e.__class__.__name__}" == "FileNotFoundError"

    with open(log_file, encoding='utf-8') as file_logger:
        logger_read = file_logger.read()
        assert "Файл 'example.json' не найден.\n" in logger_read
        assert "Файл 'example.json' не найден." in caplog.text


def test_json_handler_get_data_decode_error(tmp_path) -> None:
    """Проверяет, что срабатывает исключение `JsonDecoderError`
    при попытке чтения некорректных данных из JSON-файла"""

    invalid_json_data = "{'vacancy': 'Test vacancy'}"
    test_file = tmp_path / "invalid.json"
    test_file.write_text(invalid_json_data, encoding='utf-8')

    handler = JsonHandler()
    handler._JsonHandler__file = str(test_file)
    assert test_file.exists()

    try:
        handler.get_data()
    except JSONDecodeError as e:
        assert f"{e.__class__.__name__}" == "JsonDecoderError"


def test_json_handler_add_vacancy_success(vacancy_1: Vacancy, vacancy_2: Vacancy, tmp_path) -> None:
    """Проверяет, что данные корректно добавляются в JSON-файл"""

    json_data = ""
    test_file = tmp_path / "data.json"
    test_file.write_text(json_data, encoding='utf-8')

    object_json = JsonHandler()
    object_json._JsonHandler__file = test_file
    object_json.add_vacancy(vacancy_1)

    with open(test_file, encoding="utf-8") as file:
        data = json.load(file)

        data_id = list(data[0].keys())[0]
        data_values = list(data[0].values())[0]
        assert data_id == vacancy_1.id_vacancy
        assert data_values["name"] == vacancy_1.name_vacancy
        assert data_values["area"] == vacancy_1.area
        assert data_values["employer"] == vacancy_1.company
        assert data_values["url"] == vacancy_1.url_vacancy
        assert data_values["salary"] == f"от {vacancy_1.salary_from} до {vacancy_1.salary_to} {vacancy_1.salary_currency}"
        assert data_values["requirement"] == vacancy_1.requirements
        assert data_values["status"] == vacancy_1.status
        assert data_values["published_at"] == vacancy_1.date_published
        assert data_values["employment_form"] == vacancy_1.work_format
        assert data_values["experience"] == vacancy_1.experience

    object_json.add_vacancy(vacancy_2)
    with open(test_file, encoding="utf-8") as file:
        data_2 = json.load(file)
        data_id_2 = list(list(data_2)[1].keys())[0]
        data_id_1 = list(list(data_2)[0].keys())[0]
        assert data_id_2 == vacancy_2.id_vacancy
        assert data_id_1 == vacancy_1.id_vacancy

    object_json.add_vacancy(vacancy_1)
    with open(test_file, encoding="utf-8") as file:
        data_3 = json.load(file)
        list_id = []
        for item, data in enumerate(data_3):
            list_id.append(list(data.keys())[0])
        assert len(list_id) == 2
        assert list_id[0] == vacancy_1.id_vacancy
        assert list_id[1] == vacancy_2.id_vacancy


def test_json_handler_add_vacancy_2(tmp_path, vacancy_2: Vacancy) -> None:
    """Проверяет, что данные корректно добавляются в JSON-файл"""

    json_data = '''
       [
           {
        "2222222": {
            "name": "backend разработчик",
            "area": "Москва",
            "employer": "Test_2",
            "url": "https://example_url.com",
            "salary": "от 250000 до 250000 RUR",
            "requirement": "Знание <Python>",
            "status": "Открытая",
            "published_at": "2025-03-20T17:52:03+0300",
            "employment_form": "Полная",
            "experience": "От 1 года до 3 лет"
        }
    },
           {
        "2222222": {
            "name": "backend разработчик",
            "area": "Москва",
            "employer": "Test_2",
            "url": "https://example_url.com",
            "salary": "от 250000 до 250000 RUR",
            "requirement": "Знание <Python>",
            "status": "Открытая",
            "published_at": "2025-03-20T17:52:03+0300",
            "employment_form": "Полная",
            "experience": "От 1 года до 3 лет"
        }
    }
       ]
       '''

    test_file = tmp_path / "data.json"
    test_file.write_text(json_data, encoding='utf-8')

    with open(test_file, 'r', encoding='utf-8') as file:
        data_1 = json.load(file)
        list_id_1 = []
        for item, dict in enumerate(data_1):
            list_id_1.append((list(dict.keys())[0]))
        id_1 = list_id_1[0]
        id_2 = list_id_1[1]
        assert len(list_id_1) == 2
        assert id_1 == id_2

    object_json = JsonHandler()
    object_json._JsonHandler__file = test_file
    object_json.add_vacancy(vacancy_2)
    assert vacancy_2.id_vacancy == id_1 == id_2

    with open(test_file, "r", encoding="utf-8") as file:
        data_2 = json.load(file)
        list_id_2 = []
        for item, dict in enumerate(data_2):
            list_id_2.append(list(dict.keys())[0])
        assert len(list_id_2) == 1
        id_3 = list_id_2[0]
        assert id_3 == id_1 == id_2


def test_json_handler_delete_vacancy(vacancy_1, vacancy_2, tmp_path):
    """Проверяет, что требуемая вакансия удаляется из JSON-файла"""

    json_data = ""
    test_file = tmp_path / "data.json"
    test_file.write_text(json_data, encoding='utf-8')

    object_json = JsonHandler()
    object_json._JsonHandler__file = test_file
    object_json.add_vacancy(vacancy_1)
    object_json.add_vacancy(vacancy_2)

    with open(test_file, encoding="utf-8") as file:
        data_1 = json.load(file)
        list_id_1 = []
        for item, dict in enumerate(data_1):
            list_id_1.append(list(dict.keys())[0])
        len_list_id_1 = len(list_id_1)
        id_1 = vacancy_1.id_vacancy
        id_2 = vacancy_2.id_vacancy

    object_json.delete_vacancy(vacancy_1)

    with open(test_file, encoding="utf-8") as file:
        data_2 = json.load(file)
        list_id_2 = []
        for item, dict in enumerate(data_2):
            list_id_2.append(list(dict.keys())[0])
        len_list_id_2 = len(list_id_2)

        assert id_2 in list_id_2
        assert id_1 not in list_id_2
        assert len_list_id_2 < len_list_id_1


def test_json_handler_delete_vacancy_decode_error(vacancy_1, tmp_path, caplog) -> None:
    """Проверяет, что при чтении JSON-файла, содержащего ошибки,
    при попытке удаления вакансии, срабатывает исключение `JsonDecodeError`,
    также данное сообщение логируется в лог-файл и в консоль"""

    logger.propagate = True

    json_data = ""
    test_file = tmp_path / "data.json"
    test_file.write_text(json_data, encoding='utf-8')

    object_json = JsonHandler()
    object_json._JsonHandler__file = test_file
    try:
        object_json.delete_vacancy(vacancy_1)

    except JSONDecodeError as e:
        assert f"{e.__class__.__name__}" == "JsonDecoderError"

    with open(log_file, encoding='utf-8') as file_logger:
        logger_read = file_logger.read()
        assert "Ошибка при попытке чтения файла: JSONDecodeError.\n" in logger_read
        assert "Ошибка при попытке чтения файла: JSONDecodeError." in caplog.text















