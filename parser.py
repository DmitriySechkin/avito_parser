import time

import requests

from exeptions import FailedItemsGetting, FailedGetRequest
from parser_response import ParserAvito
from request_avito import Url, RequestHandler
from settings import MainSettings, ConfigHandler

import csv


# in this example we get data about houses in Nizhny Novgorod


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


def get_object_url(settings):
    url_obj = Url(settings.base_url)

    url_obj.min_price = settings.min_summ
    url_obj.max_price = settings.max_summ

    return url_obj


def send_get_request(request_avito, url, wait_flag=False):
    """
    Sends requests to the avito web server
    :param request_avito: object of the class RequestHandler
    :param url: url of the required page
    :param wait_flag: if flag = True then the programm waits for a random time
    :return: None
    """

    if wait_flag:
        request_avito.sleep_random_time()

    return request_avito.get_html(url)


def get_main_ads_data(request_avito, total_pages, url, parser_avito):
    """
    Getting the main data from an ad
    :param request_avito: object of the class RequestHandler
    :param total_pages: total numbers of the pages in the searchings result
    :param url: object of the class Url
    :param parser_avito: object of the class ParserAvito
    :return: None
    """
    for i in range(2, total_pages + 1):
        url.page_number = i
        print(i, url.url, sep=' ')
        html_data = send_get_request(request_avito, url.url)

        parser_avito.html = html_data
        parser_avito.parse_main_data()


def get_detail_ads_data(request_avito, parser_avito):
    """
    Retrieving the detail data from an ad
    :param request_avito: object of the class RequestHandler
    :param parser_avito: object of the class ParserAvito
    :return: None
    """
    cnt = 0

    start_time = time.time()

    for url in parser_avito.result_data.page_data['Url']:

        print(round(cnt / len(parser_avito.result_data.page_data['Url']) * 100, 2), "%")

        try:
            html_data = send_get_request(request_avito, url, True)
        except FailedItemsGetting as err:
            print(url, str(err), sep=" ")
            continue
        except FailedGetRequest as err:
            print(url, str(err), sep=" ")
            continue

        parser_avito.html = html_data
        parser_avito.parse_detail_data()
        cnt += 1

    print("time of discharge {} minutes".format(round((time.time() - start_time) / 60), 2))


def main():
    """
    main function
    """
    settings = MainSettings()

    url_obj = get_object_url(settings)

    req_avito = RequestHandler()

    print(url_obj.url)

    html_data = send_get_request(req_avito, url_obj.url)

    parser_avito = ParserAvito()

    parser_avito.html = html_data

    total_pages = parser_avito.count_page

    get_main_ads_data(req_avito, total_pages, url_obj, parser_avito)

    get_detail_ads_data(req_avito, parser_avito)

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
