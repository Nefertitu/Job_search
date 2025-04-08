import logging
import sys
from pathlib import Path

import requests

from src.parser_api import ParserAPI


log_dir = Path(__file__).parent.parent / 'data'
log_dir.mkdir(parents=True, exist_ok=True)
log_file = str((log_dir / 'logging_reports.log').absolute().resolve()).replace("\\", "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

shared_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
shared_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(message)s')
shared_handler.setFormatter(formatter)
logger.addHandler(shared_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.propagate = False

# print(f"Лог-файл: {log_file}")

class HeadHunterAPI(ParserAPI):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self) -> None:
        """Конструктор для создания экземпляра класса `HH`"""
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100, 'only_with_salary': 'true'}
        self.__vacancies = []
        super().__init__()

    def __get_connect(self) -> bool:
        """Метод проверки подключения к API"""
        try:
            response = requests.get(self.__url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error: {http_err}")
            # print(f"HTTP error: {http_err}")
            return False
        except requests.exceptions.ConnectionError as conn_err:
            logger.error(f"Ошибка: {str(conn_err)}")
            # print(f"Connection error, check your connection.")
            return False
        except requests.exceptions.Timeout as timeout_err:
            logger.error(f"Ошибка: {timeout_err}")
            # print(f"Request timeout: {timeout_err}")
            return False
        except requests.exceptions.RequestException as err:
            logger.error(f"Ошибка подключения: {err}")
            # print(f"Ошибка подключения: {err}")
            return False
        logger.info(f"Соединение с API сайта: {self.__url} установлено успешно")
        return True

    @property
    def url(self) -> str:
        """Возвращает базовый URL API класса `HeadHunter`"""
        return self.__url

    @property
    def headers(self) -> dict:
        """Возвращает стандартные HTTP-заголовки для запросов"""
        return self.__headers

    @property
    def params(self) -> dict:
        """Возвращает параметры запроса по умолчанию"""
        return self.__params

    @property
    def vacancies(self) -> list:
        """Возвращает список вакансий"""
        return self.__vacancies

    def load_vacancies(self, keyword):
        """Метод для загрузки вакансий"""
        if not self.__get_connect():
            logger.error("Не удалось загрузить вакансии, отсутствует подключение.")
            return []
        self.__params['text'] = keyword

        while self.__params.get('page') != 2:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                vacancies = response.json()['items']
                self.__vacancies.extend(vacancies)
                self.__params['page'] += 1
            except requests.exceptions.RequestException as e:
                logger.error(f"Ошибка при загрузке вакансий: {e}")
                print(f"Ошибка при загрузке вакансий: {e}")
                break
        logger.info(f"Получен список вакансий по ключевому слову: '{keyword}'.")
        return self.__vacancies


# hh_api = HeadHunterAPI()
# hh_vacancies = hh_api.load_vacancies("разработчик python")
# print(hh_vacancies)
# if hh_vacancies:
#     logging.info("Получены вакансии")
# else:
#     logging.error("Проблемы с соединением")
# json_str = json.dumps(hh_vacancies, ensure_ascii=False, indent=2)
# print(json_str)
# hh_vacancies = [{'id': '118551094', 'premium': False, 'name': 'Junior backend-разработчик', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '77', 'name': 'Рязань', 'url': 'https://api.hh.ru/areas/77'}, 'salary': {'from': 40000, 'to': None, 'currency': 'RUR', 'gross': True}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Рязань', 'street': 'Кальная улица', 'building': '5', 'lat': 54.629711, 'lng': 39.775137, 'description': None, 'raw': 'Рязань, Кальная улица, 5', 'metro': None, 'metro_stations': [], 'id': '1414103'}, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-19T12:20:57+0300', 'created_at': '2025-03-19T12:20:57+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118551094', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118551094?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118551094', 'relations': [], 'employer': {'id': '3207989', 'name': 'enKod', 'url': 'https://api.hh.ru/employers/3207989', 'alternate_url': 'https://hh.ru/employer/3207989', 'logo_urls': {'240': 'https://img.hhcdn.ru/employer-logo/3991392.png', '90': 'https://img.hhcdn.ru/employer-logo/3991391.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/887673.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3207989', 'accredited_it_employer': True, 'trusted': True}, 'snippet': {'requirement': 'Опыт работы с Go. Пройденный GoTour. Работа с git. Примеры проектов. Опыт создания HTTP-сервисов.', 'responsibility': 'Создавать веб-сервисы, автоматизирующие маркетинг. Работать с высоконагруженными приложениями. Разрабатывать на Go, работать с SQL и NoSQL базами данных.'}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'HYBRID', 'name': 'Гибрид'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118602171', 'premium': False, 'name': 'Java Developer', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 120000, 'to': 150000, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-20T13:35:46+0300', 'created_at': '2025-03-20T13:35:46+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118602171', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118602171?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118602171', 'relations': [], 'employer': {'id': '472', 'name': 'Дартс рекрутинг сервисез', 'url': 'https://api.hh.ru/employers/472', 'alternate_url': 'https://hh.ru/employer/472', 'logo_urls': {'90': 'https://img.hhcdn.ru/employer-logo/5983765.png', '240': 'https://img.hhcdn.ru/employer-logo/5983766.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/1090785.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=472', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Знакомство с Hadoop и технологиями обработки больших данных. Опыт работы с Docker. Навыки работы с bash и <highlighttext>Python</highlighttext>.', 'responsibility': 'Разработка и поддержка серверной части сервисов на Java. Участие в проектировании архитектуры и создании технической документации. Написание модульных и интеграционных...'}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'HYBRID', 'name': 'Гибрид'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118263819', 'premium': False, 'name': 'Программист (Junior - младший разработчик)', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '2', 'name': 'Санкт-Петербург', 'url': 'https://api.hh.ru/areas/2'}, 'salary': {'from': 50000, 'to': 70000, 'currency': 'RUR', 'gross': True}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Санкт-Петербург', 'street': 'Мебельная улица', 'building': '12к2', 'lat': 59.990602, 'lng': 30.241793, 'description': None, 'raw': 'Санкт-Петербург, Мебельная улица, 12к2', 'metro': {'station_name': 'Старая Деревня', 'line_name': 'Фрунзенско-Приморская', 'station_id': '18.246', 'line_id': '18', 'lat': 59.989433, 'lng': 30.255163}, 'metro_stations': [{'station_name': 'Старая Деревня', 'line_name': 'Фрунзенско-Приморская', 'station_id': '18.246', 'line_id': '18', 'lat': 59.989433, 'lng': 30.255163}], 'id': '120450'}, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-12T18:18:30+0300', 'created_at': '2025-03-12T18:18:30+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118263819', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118263819?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118263819', 'relations': [], 'employer': {'id': '803096', 'name': 'ПТМК', 'url': 'https://api.hh.ru/employers/803096', 'alternate_url': 'https://hh.ru/employer/803096', 'logo_urls': {'240': 'https://img.hhcdn.ru/employer-logo/3093877.png', '90': 'https://img.hhcdn.ru/employer-logo/3093876.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/663186.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=803096', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Знание одного из объектно-ориентированного языка программирования, к примеру: C++\\C#, Delphi, <highlighttext>Python</highlighttext>, Pascal, 1С. Знание работы с СУБД...', 'responsibility': 'Участие в интересных проектах. Доработка и разработка программного комплекса. Дополнительно: Тестирование информационных систем. Настройка информационной системы (ИС) автоматизации бизнес-процессов. '}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': True, 'fly_in_fly_out_duration': [], 'work_format': [], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118484314', 'premium': False, 'name': 'Младший программист (junior developer)', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '3', 'name': 'Екатеринбург', 'url': 'https://api.hh.ru/areas/3'}, 'salary': {'from': 90000, 'to': None, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Екатеринбург', 'street': 'улица Полежаевой', 'building': '10а', 'lat': 56.844801, 'lng': 60.559709, 'description': None, 'raw': 'Екатеринбург, улица Полежаевой, 10а', 'metro': None, 'metro_stations': [], 'id': '402391'}, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-18T09:25:27+0300', 'created_at': '2025-03-18T09:25:27+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118484314', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118484314?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118484314', 'relations': [], 'employer': {'id': '60988', 'name': 'Концерн Уралэлектроремонт', 'url': 'https://api.hh.ru/employers/60988', 'alternate_url': 'https://hh.ru/employer/60988', 'logo_urls': {'240': 'https://img.hhcdn.ru/employer-logo/2386129.png', '90': 'https://img.hhcdn.ru/employer-logo/2386128.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/486069.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=60988', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Знание <highlighttext>Python</highlighttext>, Typescript. Будет преимуществом знание: 1С, Flutter, Data science, AI, Figma.', 'responsibility': 'Разработка по направлениям: - машинное зрение. - автоматизация процессов (скрипты). - RPA роботы. - телеграмм-боты. - внешние проекты (работа в команде).'}, 'show_contacts': True, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '40', 'name': 'Другое'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118524767', 'premium': False, 'name': 'Python-разработчик (Django) Junior', 'department': None, 'has_test': False, 'response_letter_required': True, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 60000, 'to': None, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-18T20:08:21+0300', 'created_at': '2025-03-18T20:08:21+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118524767', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118524767?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118524767', 'relations': [], 'employer': {'id': '10634659', 'name': 'Саппи Аналитикс', 'url': 'https://api.hh.ru/employers/10634659', 'alternate_url': 'https://hh.ru/employer/10634659', 'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1209264.png', '90': 'https://img.hhcdn.ru/employer-logo/6457505.png', '240': 'https://img.hhcdn.ru/employer-logo/6457506.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=10634659', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Высокая самостоятельность, готовность работать без постоянного присмотра наставником. Хорошее владение <highlighttext>Python</highlighttext> и умение оформлять код. Внимательность к деталям и ответственность. ', 'responsibility': 'Находить проблемные места в коде и чинить их. Реализация индивидуальных алгоритмов ценообразования. Мониторинг метрик и логов системы. Частое взаимодействие с...'}, 'show_contacts': True, 'contacts': None, 'schedule': {'id': 'remote', 'name': 'Удаленная работа'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': True, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'REMOTE', 'name': 'Удалённо'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118279002', 'premium': False, 'name': 'Специалист по IT', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 300000, 'to': 2500000, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Москва', 'street': 'улица Бурденко', 'building': '11Ас1', 'lat': 55.738596104726845, 'lng': 37.580857945966066, 'description': None, 'raw': 'Москва, улица Бурденко, 11Ас1', 'metro': {'station_name': 'Киевская', 'line_name': 'Кольцевая', 'station_id': '5.49', 'line_id': '5', 'lat': 55.74361, 'lng': 37.56735}, 'metro_stations': [{'station_name': 'Киевская', 'line_name': 'Кольцевая', 'station_id': '5.49', 'line_id': '5', 'lat': 55.74361, 'lng': 37.56735}, {'station_name': 'Парк культуры', 'line_name': 'Сокольническая', 'station_id': '1.103', 'line_id': '1', 'lat': 55.736163, 'lng': 37.595027}, {'station_name': 'Парк культуры', 'line_name': 'Кольцевая', 'station_id': '5.104', 'line_id': '5', 'lat': 55.735221, 'lng': 37.593095}, {'station_name': 'Смоленская', 'line_name': 'Арбатско-Покровская', 'station_id': '3.131', 'line_id': '3', 'lat': 55.747713, 'lng': 37.583802}], 'id': '17786679'}, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-13T09:24:33+0300', 'created_at': '2025-03-13T09:24:33+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118279002', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118279002?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118279002', 'relations': [], 'employer': {'id': '11852949', 'name': 'Торгпром', 'url': 'https://api.hh.ru/employers/11852949', 'alternate_url': 'https://hh.ru/employer/11852949', 'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1401015.png', '240': 'https://img.hhcdn.ru/employer-logo/7223832.png', '90': 'https://img.hhcdn.ru/employer-logo/7223831.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=11852949', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Владение языками программирования: C++ / SQL / <highlighttext>Python</highlighttext> / Rust / PowerShell. Понимание сетевых протоколов (HTTP(S), Socks5 и др.). Знание принципов построения...', 'responsibility': None}, 'show_contacts': True, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}], 'working_hours': [{'id': 'HOURS_24', 'name': '24\xa0часа'}], 'work_schedule_by_days': [{'id': 'SIX_ON_ONE_OFF', 'name': '6/1'}], 'night_shifts': True, 'professional_roles': [{'id': '114', 'name': 'Системный инженер'}], 'accept_incomplete_resumes': True, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118595870', 'premium': False, 'name': 'Технический писатель', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 6000, 'to': None, 'currency': 'USD', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-20T11:58:18+0300', 'created_at': '2025-03-20T11:58:18+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118595870', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118595870?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118595870', 'relations': [], 'employer': {'id': '3242971', 'name': 'ТИН', 'url': 'https://api.hh.ru/employers/3242971', 'alternate_url': 'https://hh.ru/employer/3242971', 'logo_urls': {'240': 'https://img.hhcdn.ru/employer-logo/2626058.jpeg', '90': 'https://img.hhcdn.ru/employer-logo/2626057.jpeg', 'original': 'https://img.hhcdn.ru/employer-logo-original/546146.jpg'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3242971', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': '...ПО на любом верхнеуровневом языке (С++, <highlighttext>Python</highlighttext>, Go). Умеете проектировать и проводить интервью с <highlighttext>разработчиками</highlighttext> для создания документации. ', 'responsibility': 'Погружаться в процесс разработки через чтение кода и интервьюирование <highlighttext>разработчиков</highlighttext>. Фиксировать затраты на разработку совместно с финансистами и юристами для...'}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '126', 'name': 'Технический писатель'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'between3And6', 'name': 'От 3 до 6 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118509223', 'premium': False, 'name': 'Middle QA Manual Engineer', 'department': None, 'has_test': True, 'response_letter_required': False, 'area': {'id': '146', 'name': 'Сербия', 'url': 'https://api.hh.ru/areas/146'}, 'salary': {'from': 1500, 'to': 2200, 'currency': 'USD', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-18T14:52:27+0300', 'created_at': '2025-03-18T14:52:27+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118509223', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118509223?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118509223', 'relations': [], 'employer': {'id': '5717933', 'name': 'Your Next Agency', 'url': 'https://api.hh.ru/employers/5717933', 'alternate_url': 'https://hh.ru/employer/5717933', 'logo_urls': {'90': 'https://img.hhcdn.ru/employer-logo/4020883.jpeg', '240': 'https://img.hhcdn.ru/employer-logo/4020884.jpeg', 'original': 'https://img.hhcdn.ru/employer-logo-original/895049.jpg'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=5717933', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Подтвержденным опытом ручного тестирования, включая опыт тестирования API. Умением писать понятную, подробную и эффективную техническую документацию. С опытом использования Figma...', 'responsibility': 'Выполнять базовые SQL-запросы для проверки данных и анализа работы приложении. Взаимодействовать с <highlighttext>разработчиками</highlighttext> и дизайнерами, предлагая идеи и улучшения...'}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'remote', 'name': 'Удаленная работа'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'REMOTE', 'name': 'Удалённо'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '124', 'name': 'Тестировщик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '118466923', 'premium': False, 'name': 'QA manual (backend/frontend/mobile)', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1', 'name': 'Москва', 'url': 'https://api.hh.ru/areas/1'}, 'salary': {'from': 120000, 'to': None, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': {'city': 'Москва', 'street': 'улица Усачёва', 'building': '33с1', 'lat': 55.723181, 'lng': 37.561104, 'description': None, 'raw': 'Москва, улица Усачёва, 33с1', 'metro': None, 'metro_stations': [], 'id': '16056817'}, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-20T17:52:03+0300', 'created_at': '2025-03-20T17:52:03+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=118466923', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/118466923?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/118466923', 'relations': [], 'employer': {'id': '4938750', 'name': 'ФАЙВДЖЕН', 'url': 'https://api.hh.ru/employers/4938750', 'alternate_url': 'https://hh.ru/employer/4938750', 'logo_urls': {'90': 'https://img.hhcdn.ru/employer-logo/6787582.png', 'original': 'https://img.hhcdn.ru/employer-logo-original/1291821.png', '240': 'https://img.hhcdn.ru/employer-logo/6787583.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=4938750', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Высшее техническое образование. Понимание архитектуры и принципов работы операционной системы Linux. Знание языка программирования <highlighttext>Python</highlighttext>. Ответственность, самостоятельность, инициативность, вариативность мышления.', 'responsibility': 'Проводить тестирование backend, frontend ПО и мобильного приложения. Проводить ручные тесты протоколов взаимодействия (API) ПО. Создавать и поддерживать тестовую документацию. '}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}, {'id': 'HYBRID', 'name': 'Гибрид'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'between1And3', 'name': 'От 1 года до 3 лет'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}, {'id': '110412718', 'premium': False, 'name': 'Junior Python Developer', 'department': None, 'has_test': False, 'response_letter_required': False, 'area': {'id': '1550', 'name': 'Таганрог', 'url': 'https://api.hh.ru/areas/1550'}, 'salary': {'from': 75000, 'to': None, 'currency': 'RUR', 'gross': False}, 'type': {'id': 'open', 'name': 'Открытая'}, 'address': None, 'response_url': None, 'sort_point_distance': None, 'published_at': '2025-03-06T19:57:18+0300', 'created_at': '2025-03-06T19:57:18+0300', 'archived': False, 'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=110412718', 'show_logo_in_search': None, 'insider_interview': None, 'url': 'https://api.hh.ru/vacancies/110412718?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/110412718', 'relations': [], 'employer': {'id': '10911658', 'name': 'JavaCode', 'url': 'https://api.hh.ru/employers/10911658', 'alternate_url': 'https://hh.ru/employer/10911658', 'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1253713.png', '90': 'https://img.hhcdn.ru/employer-logo/6635281.png', '240': 'https://img.hhcdn.ru/employer-logo/6635282.png'}, 'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=10911658', 'accredited_it_employer': False, 'trusted': True}, 'snippet': {'requirement': 'Базовые знания <highlighttext>Python</highlighttext>. Опыт написания REST приложений на любом <highlighttext>Python</highlighttext> фреймворке (Flask, FastAPI, Django и др.). Понимание основ SQL и...', 'responsibility': None}, 'show_contacts': False, 'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [], 'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': True, 'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}], 'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}], 'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'night_shifts': False, 'professional_roles': [{'id': '96', 'name': 'Программист, разработчик'}], 'accept_incomplete_resumes': False, 'experience': {'id': 'noExperience', 'name': 'Нет опыта'}, 'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'}, 'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}]
# vacancies = []
# selected_vacancies = []
# for vacancy in hh_vacancies:
    # print(repr(vacancy_))
    # vacancies.append(Vacancy(vacancy))
#     # print(vacancy_)
# # print(vacancies)
#
#
# for vacancy in vacancies:
#     if vacancy.get_vacancies_by_salary("20000 - 80000"):
#         # vacancy_ = Vacancy(vacancy)
#         selected_vacancies.append(vacancy)
#     else:
#         continue
# # print(selected_vacancies)
# json_save = JsonHandler()
# read_json = json_save.read()
# print(read_json)
# # print(dir(json_save))
# # with JsonHandler(vacancies, 'w') as file:  # открываем файл в режиме записи ('w')
# #     json.dump(hh_vacancies, file, ensure_ascii=False, indent=4) # сериализуем данные в JSON и записываем в файл
# data = {
#                 "id": '1111111',
#                 "name": 'backend/frontend/mobile',
#                 "area": {"name": 'Москва'},
#                 "employer": {"name": 'Test'},
#                 "alternate_url": 'sample_url',
#                 "salary": {"from": 100000, "to": 120000, "currency": 'RUR'},
#                 "snippet": {"requirement": 'Высшее техническое образование. Знание языка программирования <Python>'},
#                 "type": {"name": 'Открытая'},
#                 "published_at": '2024-03-20T17:52:03+0300',
#                 "employment_form": {"name": 'Полная'},
#                 "experience": {"name": 'От 1 года до 3 лет'},
#             }
# vacancy_1 = Vacancy(data)
# # print(repr(vacancy_1))
# json_save.add_vacancy(vacancy_1)
# for selected_vacancy in selected_vacancies:
#     print(type(selected_vacancy))
#     json_save.add_vacancy(selected_vacancy)
#
# print(selected_vacancies)
# print(type(selected_vacancies))
# filter_vacancies = filter_vacancies(vacancies, "python, москва")
# # print(filter_vacancies)
# print(vacancies[0] <= vacancies[-1])
# # sort_vacancies = sort_vacancies(vacancies)
# # print(sort_vacancies)
# # top_n_vacancies = get_top_vacancies(sort_vacancies, 3)
# # print(top_n_vacancies)
# print()
# print(list(set(selected_vacancies) - set(selected_vacancies[:2])))

