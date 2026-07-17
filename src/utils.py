import json
import logging
import re
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.head_hunter_api import HeadHunterAPI
from src.json_handler import JsonHandler
from src.vacancy import Vacancy

log_dir = Path(__file__).parent.parent / "data"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = str((log_dir / "logging_reports.log").absolute().resolve()).replace("\\", "/")
save_file_json = str((log_dir / "vacancies_save.json").absolute().resolve()).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
shared_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
shared_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(message)s")
shared_handler.setFormatter(formatter)
shared_handler.setFormatter(formatter)
logger.addHandler(shared_handler)

logger.propagate = False
# print(f"Лог-файл: {log_file}")


def filter_vacancies(vacancies: list, filter_words: str, param: str = "positive") -> str | list:
    """Функция для выбора вакансий по ключевым словам"""

    vacancies_filter = []

    list_words = re.findall(r"(\b[\w]{3,}\b)+", filter_words.lower())

    for vacancy in vacancies:
        if param == "positive":
            if set(list_words).issubset(
                set(
                    re.findall(
                        r"(\b[\w]{3,}\b)+", f"{vacancy.name_vacancy} {vacancy.area} {vacancy.requirements}".lower()
                    )
                )
            ):
                vacancies_filter.append(vacancy)
            else:
                continue

        if param == "negative":
            if set(list_words).issubset(
                set(
                    re.findall(
                        r"(\b[\w]{3,}\b)+", f"{vacancy.name_vacancy} {vacancy.area} {vacancy.requirements}".lower()
                    )
                )
            ):
                continue
            else:
                vacancies_filter.append(vacancy)
    return vacancies_filter


def sort_vacancies(vacancies: list) -> list:
    """Функция для сортировки вакансий по заработной плате в порядке убывания"""

    return sorted(vacancies, key=lambda vacancy: vacancy.salary_to, reverse=True)


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """Функция для выбора топ N вакансий"""

    if len(vacancies) >= top_n:
        logger.info(f"Получен список топ-{top_n} вакансий.")
        return vacancies[:top_n]
    else:
        logger.info(f"Получен список из {len(vacancies)} вакансий.")
        return vacancies


def user_interaction() -> Any:
    """Функция для взаимодействия с пользователем"""

    platform = ["HeadHunter"]
    vacancies_save = []
    hh_api = HeadHunterAPI()

    search_query = input(f"\nВведите данные для выполнения поискового запроса о вакансиях на платформе {platform}: ")
    print("\nВыполняется запрос к API сайта hh.ru...")

    with open(save_file_json, "w", encoding="utf-8") as f:
        f.write("")
    hh_vacancies = hh_api.load_vacancies(search_query)

    vacancies_list = Vacancy.cast_vacancies_in_list(hh_vacancies)
    logger.info(f"""Получены вакансии по ключевому слову: {search_query} в количестве {len(hh_vacancies)} шт.""")

    # print(vacancies_list)
    # print("\nВыполнен перерасчет заработной платы, указанной в другой валюте, в рубли с помощью API ЦБ РФ.")

    json_saver = JsonHandler()
    for vacancy in vacancies_list:
        vacancies_save.append(vacancy)
        json_saver.add_vacancy(vacancy)
    # print(vacancies_save)
    print("\nПроизведена запись полученных данных в файл 'data/vacancies_save.json'.")

    filter_words = input(
        """\nВведите ключевое слово (или список слов) для фильтрации вакансий
(пример: Москва, Junior): """
    )
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    logger.info(
        f"""Произведена фильтрация полученных вакансий по ключевому
слову (словам): '{filter_words}', количество полученных вакансий составило: {len(filtered_vacancies)} шт."""
    )
    # print(filtered_vacancies)

    if filtered_vacancies is None:
        logger.error(f"По ключевому слову (словам):{filter_words} совпадений не найдено")
        return "\nПо заданным ключевым словам совпадений не найдено."

    else:
        salary_range = input("\nВведите диапазон зарплат (пример: 100000 - 150000): ")

        ranged_vacancies = []
        not_ranged_vacancies = []
        for vacancy in filtered_vacancies:
            if vacancy.get_vacancies_by_salary(salary_range):
                ranged_vacancies.append(vacancy)
            else:
                not_ranged_vacancies.append(vacancy)
        logger.info(
            f"""Вакансии отфильтрованы по установленному размеру заработной
платы ({salary_range}), количество полученных вакансий: {len(ranged_vacancies)} шт."""
        )

        answer_dif = input(
            "\nЗаписать отфильтрованные данные по вакансиям в файл 'data/vacancies_save.json'? (Введите: да/нет): "
        )

        answers = ["да", "lf", "нет", "ytn"]

        while answer_dif.lower() not in answers:
            input("\nВведите 'да' или 'нет': ")

        if answer_dif.lower() == "да" or answer_dif.lower() == "lf":
            filtered_vacancies_negative = filter_vacancies(vacancies_list, filter_words, param="negative")
            print("\nВыполняется запись данных в файл...")
            vacancies_to_del = []
            for vacancy in filtered_vacancies_negative:
                vacancies_to_del.append(vacancy)
            for vacancy in not_ranged_vacancies:
                vacancies_to_del.append(vacancy)
            for vacancy in vacancies_to_del:
                json_saver.delete_vacancy(vacancy)

        if answer_dif.lower() == "нет" or answer_dif.lower() == "ytn":
            print("\nВ файле 'vacancies_save.json' остается полный перечень вакансий.")

        sorted_vacancies = sort_vacancies(ranged_vacancies)
        print(f"\nОбщее количество вакансий, полученных после фильтрации, составляет {len(sorted_vacancies)} шт.")

        top_n = int(input("\nВведите количество вакансий для вывода в топ N: "))
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        return top_vacancies


def get_filename_path() -> Path:
    """Функция для получения абсолютного пути с именем файла,
    включающим текущую дату"""

    date_today = datetime.today()
    date_today_str = date_today.strftime("%Y_%m_%d")
    file_name = f"vacancies_save_{date_today_str}.json"
    save_dir = Path(__file__).parent.parent / "data"
    save_dir.mkdir(parents=True, exist_ok=True)
    absolute_file_name = (log_dir / file_name).absolute().resolve()

    return absolute_file_name


# print(get_filename_path())


def write_copy_file(filename: Path | str) -> bool:
    """Функция для записи копии JSON-файла"""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as e:
        logger.error(f"Ошибка: {e}. Файл {filename} не найден.")
        return False

    new_copy_name = get_filename_path()

    try:
        with open(new_copy_name, "w", encoding="utf-8") as file:
            file.write("[\n")
            for i, item in enumerate(data):
                json.dump(item, file, ensure_ascii=False, indent=4)  # type: ignore
                if i < len(data) - 1:
                    file.write(",")
                file.write("\n")
            file.write("]")

    except JSONDecodeError as e:
        logger.error(f"Ошибка: {e}.\nЗапись копии полученных данных по вакансиям не выполнена.")
        return False
    except Exception as e:
        logger.error(f"Ошибка: {e}.\nЗапись копии полученных данных по вакансиям не выполнена.")
        return False
    else:
        logger.info(
            f"Выполнена запись копии данных по вакансиям в файл: '{str((log_dir / 'logging_reports.log').absolute().resolve()).split("\\")[-1]}'"
        )
        return True
