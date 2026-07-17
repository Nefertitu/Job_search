import logging
from pathlib import Path

from src.utils import get_filename_path, save_file_json, user_interaction, write_copy_file

log_dir = Path(__file__).parent / "data"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = str((log_dir / "logging_reports.log").absolute().resolve()).replace("\\", "/")
# save_file = (log_dir / 'vacancies_save.json').absolute().resolve()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
shared_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
shared_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(message)s")
shared_handler.setFormatter(formatter)
logger.addHandler(shared_handler)

logger.propagate = False


if __name__ == "__main__":
    with open("./data/logging_reports.log", "w") as file:
        file.write(" ")
    result = user_interaction()
    logger.info("Вывод данных в консоль:\n")
    for item in result:
        logger.info(f"Получена вакансия: {item}")
        print(item)

    write_copy_file(save_file_json)
    new_file_name = str(get_filename_path()).split("\\")[-1]

    print(
        f"Создан файл с копией полученных данных по вакансиям\n(с учетом фильтрации по ключевому слову (словам)): '{new_file_name}'."
    )
