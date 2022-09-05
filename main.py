import csv
import json
import requests
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet

HOST = 'https://www.kivano.kg'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


def get_html(url: str, category: str, headers: dict='', params: str=''):
    """ Функция для получения html кода """
    html = requests.get(
        url + category,
        headers=headers,
        params=params,
        verify=False
    )
    return html.text


def get_card_from_html(html: str) -> ResultSet:
    """ Функция для получения карточек из html кода """
    soup = BeautifulSoup(html, 'lxml')
    cards: ResultSet = soup.find_all('div', class_='item product_listbox oh')
    return cards


def parse_data_from_cards(cards: ResultSet) -> list:
    """ Фильтрация данных из карточек """
    result = []
    for card in cards:
        obj = {
            'title': card.find('strong').find('a').text,
            'price': card.find('div', class_='listbox_price text-center').find('strong').text,
            'image_link': HOST+card.find('div', class_='listbox_img pull-left').find('img').get('src'),
        }
        result.append(obj)
    return result


def write_to_csv(data: list, file_name) -> None:
    """ Запись данных в csv файл """
    fieldnames = data[0].keys()
    with open(f'{file_name}.csv', 'w') as file:
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(data)


def write_to_json(data: list, file_name):
    """ Запись данных в csv файл """
    with open(f'{file_name}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_last_page(category):
    """ Функция для получения последней страницы каталога"""
    html = get_html(HOST + '/', category)
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.find('li', class_='last').find('a').text
    return int(last_page)


def full_parse(category):
    """ Функция для парсинга всех страниц в каталоге """
    result = []
    for page in range(get_last_page(category)+1):
        html = get_html(HOST + '/', category, params=f'?page={page}', headers=HEADERS)
        cards = get_card_from_html(html)
        list_of_cards = parse_data_from_cards(cards)
        result.extend(list_of_cards)
    write_to_csv(result, category)
    write_to_json(result, category)


if __name__ == '__main__':
    # html = get_html(HOST, '/mobilnye-telefony')
    # cards = get_card_from_html(html)
    # data = parse_data_from_cards(cards)
    # write_to_csv(data, 'mobilnye-telefony')
    # write_to_json(data, 'mobilnye-telefony')
    full_parse('mobilnye-telefony')
    print(get_last_page('mobilnye-telefony'))