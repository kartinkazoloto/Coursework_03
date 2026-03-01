import pytest


@pytest.fixture
def vacancies_api_hh():
    return {'items': [
        {'id': '130147593', 'premium': False, 'name': 'Токарь - расточник', 'department': None, 'has_test': False,
         'response_letter_required': False,
         'area': {'id': '160', 'name': 'Алматы', 'url': 'https://api.hh.ru/areas/160'},
         'salary': {'from': 400000, 'to': None, 'currency': 'KZT', 'gross': False},
         'salary_range': {'from': 400000, 'to': None, 'currency': 'KZT', 'gross': False,
                          'mode': {'id': 'MONTH', 'name': 'За\xa0месяц'}, 'frequency': None},
         'type': {'id': 'open', 'name': 'Открытая'},
         'address': {'city': 'село Коксай', 'street': 'Кирпичная улица', 'building': '1', 'lat': 43.275678,
                     'lng': 76.767608, 'description': None, 'raw': 'село Коксай, Кирпичная улица, 1', 'metro': None,
                     'metro_stations': [], 'id': '22836841'}, 'response_url': None, 'sort_point_distance': None,
         'published_at': '2026-02-04T07:36:52+0300', 'created_at': '2026-02-04T07:36:52+0300', 'archived': False,
         'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=130147593',
         'show_logo_in_search': None, 'show_contacts': True, 'insider_interview': None,
         'url': 'https://api.hh.ru/vacancies/130147593?host=hh.ru', 'alternate_url': 'https://hh.ru/vacancy/130147593',
         'relations': [],
         'employer': {'id': '10119482', 'name': 'АрхиМеталл', 'url': 'https://api.hh.ru/employers/10119482',
                      'alternate_url': 'https://hh.ru/employer/10119482',
                      'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original-round/6685025.png',
                                    '90': 'https://img.hhcdn.ru/employer-logo-round/6685026.png',
                                    '240': 'https://img.hhcdn.ru/employer-logo-round/6685027.png'},
                      'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=10119482', 'country_id': 3,
                      'accredited_it_employer': False, 'trusted': True}, 'snippet': {
            'requirement': 'Опыт работы от 3 лет. Самоконтроль качества обработки. Выявление и устранение '
                           'дефектов. Соблюдение технических требований и стандартов. Желание работать и...',
            'responsibility': 'Изготовление деталей и узлов различной сложности в соответствии с чертежами,'
                              ' конструкторской документацией. Обработка деталей на токарных станках. '
                              'Контроль соответствия деталей...'},
         'contacts': None, 'schedule': {'id': 'fullDay', 'name': 'Полный день'}, 'working_days': [],
         'working_time_intervals': [], 'working_time_modes': [], 'accept_temporary': False,
         'fly_in_fly_out_duration': [], 'work_format': [{'id': 'ON_SITE', 'name': 'На\xa0месте работодателя'}],
         'working_hours': [{'id': 'HOURS_8', 'name': '8\xa0часов'}],
         'work_schedule_by_days': [{'id': 'FIVE_ON_TWO_OFF', 'name': '5/2'}], 'accept_labor_contract': False,
         'civil_law_contracts': [], 'night_shifts': False,
         'professional_roles': [{'id': '128', 'name': 'Токарь, фрезеровщик, шлифовщик'}],
         'accept_incomplete_resumes': True, 'experience': {'id': 'between3And6', 'name': 'От 3 до 6 лет'},
         'employment': {'id': 'full', 'name': 'Полная занятость'}, 'employment_form': {'id': 'FULL', 'name': 'Полная'},
         'internship': False, 'adv_response_url': None, 'is_adv_vacancy': False, 'adv_context': None}
