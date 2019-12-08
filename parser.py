import requests

from parser_response import ParserAvito
from request_avito import Url, RequestHandler
from settings import MainSettings, ConfigHandler

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
    data = requests.get(url)

    return data.text


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


def get_object_url(settings):
    url_obj = Url(settings.base_url)

    url_obj.min_price = settings.min_summ
    url_obj.max_price = settings.max_summ

    return url_obj


def send_get_request(request_avito, url):
    return request_avito.get_html(url)


def get_main_ads_data(request_avito, total_pages, url, parser_avito):
    for i in range(1, total_pages + 1):
        url.page_number = i
        print(i)
        html_data = send_get_request(request_avito, url.url)

        parser_avito.html = html_data
        parser_avito.parse_main_data()


def main():
    """
    main function
    """
    settings = MainSettings()

    url_obj = get_object_url(settings)

    req_avito = RequestHandler()

    html_data = send_get_request(req_avito, url_obj.url)

    parser_avito = ParserAvito()

    parser_avito.html = html_data

    total_pages = parser_avito.count_page

    get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)

    # for i in range(1, total_pages + 1):
    #     sleep(uniform(1, 8))
    #     gen_url = base_url + page + str(i) + query
    #     html = get_html(gen_url)
    #     get_page_data(html)
    # n = 0
    #
    # for url in data_result['Url']:
    #     n += 1
    #     print(url)
    #     print(n)
    #     sleep(uniform(1, 4))
    #     html = get_html(url)
    #     get_more_data(html)
    #
    #     write_csv(data_result)


if __name__ == '__main__':
    # urls = []
    #
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
    # from urllib import parse
    # from urllib.parse import urlparse, ParseResult, parse_qs, urlencode, urlunsplit
    #
    # url = 'https://www.avito.ru/nizhniy_novgorod/doma_dachi_kottedzhi/prodam/dom?p=2&pmax=4000000&pmin=2000000&s_trg=4&user=1'
    #
    # data = urlparse(url)
    #
    # query_data = parse_qs(data.query)
    #
    # # меняю параметр
    # query_data['p'][0] = str(2)

    # new_url = urlunsplit((data.scheme, data.hostname, data.path, urlencode(query_data, doseq=True), ''))
    # print(new_url)

    # req_avito = RequestHandler()
    #
    # data = req_avito.get_html(url.url)
    #
    # parser_avito = ParserAvito(data)
    #
    # print(parser_avito.count_page)
    #
    # url.page_number = 3
    #
    # print(url.url)
