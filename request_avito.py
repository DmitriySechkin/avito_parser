import requests
from urllib.parse import urlparse, urlencode, urlunsplit
import requests

from exeptions import ErrorSummParameter, ZeroPageNumber, FailedGetRequest

HEADERS = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
    }


class Url:

    def __init__(self, base_url):
        self.base_url = base_url

        self.min_price = 0
        self.max_price = 0
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

        if self.min_price != 0:
            query_data['pmin'] = self.min_price
        if self.max_price != 0:
            query_data['pmax'] = self.max_price

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

        if self.max_price < self.min_price:
            raise ErrorSummParameter(self.min_price, self.max_price)


class RequestHandler:

    def __init__(self):

        self.__session = requests.session()
        self.__headers = HEADERS

    def get_html(self, url):
        """
        Get html code of web page
        :param url: url of required web page
        :return: html code of web page
        """

        response = requests.get(url, headers=self.__headers)
        self.__check_result_response(response)

        return response.text


    def __check_result_response(self, response):
        if response.status_code != 200:
            raise FailedGetRequest(response.status_code)




def get_html(url):
    """
    getting html code of web self.page_number
    :param url: url of required web self.page_number
    :return: html code of web self.page_number
    """

    data = requests.get(url)

    return data.text
