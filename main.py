import re
import json
import bs4
import requests
from fake_headers import Headers

from pprint import pprint


def get_headers():
    return Headers(os='windows', browser='chrome').generate()
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=get_headers())

main_html_data = response.text
main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')
span_tags = main_soup.find_all('div', class_='vacancy-serp-item__layout')  # все вакансии

pars_data = []
for span_tag in span_tags:
    key_words = ["Django", "Flask"]


    try: # избегаем ошибки об отсутствии зарплаты
        salary_tag = span_tag.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
    except:
        salary_tag = 'зарплата не указана'

    try:
        a_tag = span_tag.find('a', class_='bloko-link') # получаем ссылку на вакансию
        relative_link = a_tag.get('href')
    except:
        relative_link = "ссылка не найдена"

    try:
        company_name = span_tag.find('div', class_='bloko-v-spacing-container bloko-v-spacing-container_base-2').text.strip() # получение названия комапании
    except:
        company_name = 'компания не указана'


    try:
        address = span_tag.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0] # получение адреса
    except:
        address = 'адрес не указан'


    soup_link = bs4.BeautifulSoup(requests.get(relative_link, headers=get_headers()).text, features='lxml') # вытаскиваем описание
    try:
        description = soup_link.find('div', class_='g-user-content').text
    except:
        description = 'описание не указано'


    if any(x in description for x in key_words): # выборка по ключевым словам

        pars_data.append({
            'salary_tag': salary_tag,
            'company_name': company_name.replace('\xa0', ' '),
            'address': address.replace('\xa0', ' '),
            'link': relative_link,

        })
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(pars_data, f, indent=4, ensure_ascii=False)



print('Данные добавлены в файл')