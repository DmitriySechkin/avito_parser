import requests

from datetime import datetime
import csv
import pandas as pd
from random import uniform
from time import sleep


def get_html(url):
    """
    getting html code of web page
    :param url: url of required web page
    :return: html code of web page
    """

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'mc.yandex.ru',
        'cookie': '5.367a37203faa7618a7d90a8d0f8c6e0b47e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b984dcacfe8ebe897bfa4d7ea84258c63d59c9621b2c0fa58f897baa7410138ead3de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe23de19da9ed218fe2cd39050aceac4b90d0dc958cdeccdc4675d0caa58fe5eefe01df084c0cadacc688ba95ac8dca91fe38571b39497804ddaeb0b8428d5861b3db8108da9e496db560768b50dd5e12c31321afc52f74340e63b9239109e833b2465d5650ed2fd5c1685428d00dc691fa9e82118971f2ed6494d66450ac1e7292f63a0d5cf077a1cf3de19da9ed218fe23de19da9ed218fe2fe6ea02d92bd8a116ccf980009adbe889026067667e1df74b841da6c7dc79d0b;',
        'Origin': 'https://www.avito.ru',
        'Referer': 'https://www.avito.ru/nizhniy_novgorod/doma_dachi_kottedzhi/prodam/dom?p=&pmax=4000000&pmin=2000000&s_trg=4&user=1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
    }

    data = requests.get(url)

    return data.text


def get_count_pages(html):
    """
    getting number of pages in the search result on avito
    :param html: html code of a web pages with a search result
    :return: number pages
    """

    soup = bs(html, 'lxml')
    pages = soup.find_all('a', class_='pagination-page')[-1].get('href')
    count_page = pages.split('=')[1].split('&')[0]

    return int(count_page)


def write_csv(data):
    """
    writing result to a csv file
    :param data: obtained result
    """

    with open('avito.csv', 'a', encoding='utf16', newline='') as f:
        writer = csv.writer(f)

        writer.writerow((data['Название объявления'],
                         data['Url'],
                         data['Цена'],
                         data['Дата'],
                         data['Расположение'],
                         data['Метро'],
                         data['Этажи'],
                         data['Материал дома'],
                         data['Расстояние от города'],
                         data['Описание']))


# def check_page(html):
#     """
#     check the title of page
#     :param html: html code of web page avito
#     :return:
#     """
#     return "Купить дом в Нижнем Новгороде на Avito" in


def get_page_data(html):
    """
    getting data from html code of a web page
    :param html: html code
    :return:
    """

    if not check_page(html):
        return

    soup = bs(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    for ad in ads:
        try:
            title = ad.find('div', class_='description').find('h3').text.strip()
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')

        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        try:
            date = ad.find('div', class_='js-item-date').get('data-absolute-date').strip()
        except:
            date = ''
        try:
            place = ad.find('p', class_='address').text.strip()
        except:
            place = ''

        data_result['Название объявления'].append(title)
        data_result['Url'].append(url)
        data_result['Цена'].append(price)
        data_result['Расположение'].append(place)
        data_result['Дата'].append(date)

    metro = soup.find_all('p', class_="address")

    for i in metro:
        if i.find('i') is not None:
            metro = i.text.split(',')[0].strip()
        else:
            metro = i.text.strip()
        data_result['Метро'].append(metro)


def get_more_data(html):
    """
    getting detailed information from the search result on avito
    :param html: html code
    """

    soup = bs(html, 'lxml')
    try:
        description = soup.find('div', class_='item-description-text').text
    except:
        description = ''
    try:
        views = soup.find('div', class_='title-info-metadata-item title-info-metadata-views').text
    except:
        views = ''

    data_result['Описание'].append(description)
    data_result['Просмотры'].append(views)

    items = soup.find_all('li', class_='item-params-list-item')
    floor = ''
    material = ''
    distance = ''

    for item in items:
        if 'Этажей' in item.text:
            floor = item.text.split(': ')[1]
        if 'Материал' in item.text:
            material = item.text.split(': ')[1]
        if 'Расстояние' in item.text:
            distance = item.text.split(': ')[1]

    data_result['Этажи'].append(floor)
    data_result['Материал дома'].append(material)
    data_result['Расстояние от города'].append(distance)


def main():
    """
    main function
    """
    url = 'https://www.avito.ru/nizhniy_novgorod/doma_dachi_kottedzhi/prodam/dom?p=1&pmax=4000000&pmin=2000000&s_trg=4&user=1'
    base_url = 'https://www.avito.ru/nizhniy_novgorod/doma_dachi_kottedzhi/prodam/dom?'
    page = 'p='
    query = '&pmax=4000000&pmin=2000000&s_trg=4&user=1'

    html_code = get_html(url)
    total_pages = get_count_pages(html_code)

    for i in range(1, total_pages + 1):
        sleep(uniform(1, 8))
        gen_url = base_url + page + str(i) + query
        html = get_html(gen_url)
        get_page_data(html)
    n = 0

    for url in data_result['Url']:
        n += 1
        print(url)
        print(n)
        sleep(uniform(1, 4))
        html = get_html(url)
        get_more_data(html)

        write_csv(data_result)


if __name__ == '__main__':
    urls = []

    data_result = {'Название объявления': [],
                   'Url': [],
                   'Цена': [],
                   'Дата': [],
                   'Расположение': [],
                   'Метро': [],
                   'Этажи': [],
                   'Материал дома': [],
                   'Расстояние от города': [],
                   'Описание': [],
                   'Просмотры': []
                   }
    main()
