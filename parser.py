import time

import os

from exeptions import FailedItemsGetting, FailedGetRequest
from parser_response import ParserAvito
from request_avito import Url, RequestHandler
from settings import MainSettings

import csv


# getting of data about houses in Nizhny Novgorod and write result to csv file

def write_csv(data_result, row_number):
    """
    writing result to a csv file
    :param data_result: obtained result
    :param row_number: number of element in lists of result
    """

    with open('avito.csv', 'a', encoding='utf16', newline='') as f:
        writer = csv.writer(f)

        try:
            data_row = [data_result[row][row_number] for row in data_result]
            writer.writerow(data_row)
        except IndexError:
            pass


def check_file_result():
    if os.path.exists('avito.csv'):
        os.remove('avito.csv')


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
    for i in range(1, total_pages + 1):
        url.page_number = i
        print(i, url.url, sep=' ')
        html_data = send_get_request(request_avito, url.url)

        parser_avito.html = html_data
        parser_avito.parse_main_data()


def get_detail_ads_data(request_avito, parser_avito):
    """
    Retrieving the detail data from the ad
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
        except FailedGetRequest as err:
            print(url, str(err), sep=" ")
            continue

        parser_avito.html = html_data

        try:
            parser_avito.parse_detail_data()
        except FailedItemsGetting as err:
            print(url, str(err), sep=" ")
            cnt += 1
            continue

        write_csv(parser_avito.result_data.page_data, cnt)

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

    check_file_result()

    get_detail_ads_data(req_avito, parser_avito)


if __name__ == '__main__':
    main()
