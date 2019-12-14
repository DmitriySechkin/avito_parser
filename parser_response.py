from bs4 import BeautifulSoup as bs
from exeptions import FailedGettingNumberPages, FailedAdsDataGet, FailedItemsGetting


class ParserAvito:

    def __init__(self):

        self.__soup = None
        self.result_data = PageData()
        self.__number_page = 0

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

    @property
    def html(self):
        return self.html

    @html.setter
    def html(self, data_html):

        self.__soup = bs(data_html, 'lxml')

    def __get_ads(self):
        """
        Get list of the ads tags
        :return: None
        """

        ads = self.__soup.find('div', class_='js-catalog_serp')
        ads = ads.find_all('div', class_='item_table')

        if not ads:
            raise FailedAdsDataGet(self.__number_page)
        else:
            return ads

    def __get_name_ad(self, ad):
        """
        Get name of the ad
        :param ad: tag of the ad
        :return: name
        """

        title = ''
        title_tag = ad.find('div', class_='description').find('h3')

        if title_tag:
            title = title_tag.text.strip()

        return title

    def __get_url_ad(self, ad):
        """
        Get url of the ad
        :param ad: tag of the ad
        :return: url
        """

        url = ''
        url_base = 'https://www.avito.ru{}'

        url_tag = ad.find('div', class_='description').find('h3').find('a')

        if url_tag:
            url_patt = url_tag.get('href')
            url = url_base.format(url_patt)

        return url

    def __get_price_ad(self, ad):
        """
        Get price of the house in the ad
        :param ad: tag of the ad
        :return: price
        """
        price = ''

        price_tag = ad.find('div', class_='about')

        if price_tag:
            price = price_tag.text.strip()

        return price

    def __get_date_ad(self, ad):
        """
        Get date of the ad
        :param ad: tag of the ad
        :return: date
        """
        date = ''
        date_tag = ad.find('div', class_='js-item-date')

        if date_tag:
            date = date_tag.get('data-absolute-date').strip()

        return date

    def __get_place_ad(self, ad):
        """
        Get place of the house
        :param ad: tag of the ad
        :return: date
        """
        place = ''
        place_tag = ad.find('p', class_='address')

        if place_tag:
            place = place_tag.text.strip()

        return place

    def __get_metro(self):
        """
        Gets the name of the metro station in the ad
        :return: None
        """

        metro = ''

        metro_tag = self.__soup.find_all('p', class_="address")

        for ad in metro_tag:
            if ad.find('i') is not None:
                metro = ad.text.split(',')[0].strip()
            else:
                metro = ad.text.strip()

            self.result_data.append_data('Metro', metro)

    def __get_description_ad(self):
        """
        Gets a description of the house in ad
        :return: description
        """
        description = ''
        description_tag = self.__soup.find('div', class_='item-description-text')
        if description_tag:
            description = description_tag.text
        return description

    def __get_views_ad(self):
        """
        Gets an info about the number of views
        :return: number of views
        """

        views = ''
        views_tag = self.__soup.find('div', class_='title-info-metadata-item title-info-metadata-views')
        if views_tag:
            views = views_tag.text
        return views

    def __get_items_ads(self):
        """
        Gets items in the ad for retrieving the data about the material of the house,
        distance from the city and number of floors
        :return: items tag
        """

        items_tag = self.__soup.find_all('li', class_='item-params-list-item')

        if items_tag:
            return items_tag
        else:
            raise FailedItemsGetting()

    def __get_detail_data_in_ad(self):
        """
        Gets in every ad the data about the number of floors, material of the house
        and distance from the city
        :return: data of the parameter
        """

        items = self.__get_items_ads()

        data_keys = {}

        for item in items:
            data_keys = {}
            key = item.find('span', class_='item-params-label').text
            data_keys[key] = []
            data_keys[key].append(self.__get_data_in_item(item).strip())
            # data_keys = {
            #     'Floors Number': self.__get_data_in_item('Floors Number'),
            #     'Material': self.__get_data_in_item('Material'),
            #     'Distance': self.__get_data_in_item('Distance')
            # }

            data = [self.result_data.append_data(key, data_keys[key]) for key in data_keys]

    def __get_data_in_item(self, item):

        return item.text


    def parse_main_data(self):
        """
        Retrieving data from an ad
        In the first cycle we get main data from an ad(Name of ad, url, price, date, place, metro)
        :return: None
        """

        ads = self.__get_ads()

        for ad in ads:
            data_keys = {
                'Name ad': self.__get_name_ad(ad),
                'Url': self.__get_url_ad(ad),
                'Price': self.__get_price_ad(ad),
                'Date': self.__get_date_ad(ad),
                'Place': self.__get_place_ad(ad)
            }

            data = [self.result_data.append_data(key, data_keys[key]) for key in data_keys]

        self.__get_metro()

    def parse_detail_data(self):
        """
        Getting detailed information from the search result on the avito site
        :return: None
        """

        data_keys = {
            'Description': self.__get_description_ad(),
            'Views': self.__get_views_ad(),
        }

        data = [self.result_data.append_data(key, data_keys[key]) for key in data_keys]

        self.__get_detail_data_in_ad()




class PageData:

    def __init__(self):
        self.page_data = {
            'Name ad': [],
            'Url': [],
            'Price': [],
            'Date': [],
            'Place': [],
            'Metro': [],
            'Floors Number': [],
            'Material': [],
            'Distance': [],
            'Description': [],
            'Views': []
        }

    def append_data(self, key, value):
        """
        Add value of data in dictionary
        :param key: data dictionary key
        :param value: value
        :return: None
        """

        if key in self.page_data:
            self.page_data[key].append(value)
        else:
            self.page_data[key] = value

