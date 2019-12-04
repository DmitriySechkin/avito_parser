from bs4 import BeautifulSoup as bs
from exeptions import FailedGettingNumberPages


class ParserAvito:

    def __init__(self, html):

        self.html = html
        self.__soup = bs(self.html, 'lxml')

    @property
    def count_page(self):
        """
        Get count of pages
        :return: Count of pages: int
        """
        last_page_tag = self.__soup.find('a', class_='pagination-page', text='Последняя')

        if last_page_tag:
            href_last_page = last_page_tag.get('href')
            count_page = href_last_page.split('=')[1].split('&')[0]

        else:
            raise FailedGettingNumberPages()

        return int(count_page)


class PageData:

    def __init__(self):

        self.page_data = {
            'Название объявления': [],
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