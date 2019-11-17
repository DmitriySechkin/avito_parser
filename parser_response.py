from bs4 import BeautifulSoup as bs


class Parser:

    def __init__(self, html):
        self.html = html
        self.soup = bs(self.html, 'lxml')
