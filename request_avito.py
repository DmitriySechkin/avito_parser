import requests
from urllib.parse import urlparse, urlencode, urlunsplit

from exeptions import ErrorSummParameter, ZeroPageNumber

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'mc.yandex.ru',
    'Referer': 'https://www.avito.ru/nizhniy_novgorod/doma_dachi_kottedzhi/prodam/dom?p=&pmax=4000000&pmin=2000000&s_trg=4&user=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}


class Url:

    def __init__(self, base_url, min_summ=0, max_summ=0):
        self.base_url = base_url

        self.min_summ = min_summ
        self.max_summ = max_summ
        self.page_number = 1

    @property
    def url(self):
        """
        Getting new url with required parameter
        :param self.page_number: number of self.page_number
        :return: new url
        """

        self.__check_parameter()
        query_data = self.__get_query_data()

        return self.__parse_url(query_data)

    def __parse_url(self, query_data):
        """
        parse new url
        :param query_data: required settings for url
        :return: new url
        """
        data = urlparse(self.base_url)

        return urlunsplit((
            data.scheme,
            data.hostname,
            data.path, urlencode(query_data, doseq=True),
            ''
        ))

    def __get_query_data(self):
        """
        Getting url query data
        :param self.page_number: number of self.page_number
        :return: required parameter data
        """
        query_data = {}

        if self.min_summ != 0:
            query_data['pmin'] = self.min_summ
        if self.max_summ != 0:
            query_data['pmax'] = self.max_summ

        query_data['p'] = self.page_number

        return query_data

    def __check_parameter(self):
        """
        Validate passed parameter in urls query data
        :param self.page_number: number of self.page_number
        :return: None
        """

        if self.page_number == 0:
            raise ZeroPageNumber()
        if self.max_summ < self.min_summ:
            raise ErrorSummParameter(self.min_summ, self.max_summ)


def get_html(url):
    """
    getting html code of web self.page_number
    :param url: url of required web self.page_number
    :return: html code of web self.page_number
    """

    data = requests.get(url)

    return data.text
