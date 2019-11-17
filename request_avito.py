import requests


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