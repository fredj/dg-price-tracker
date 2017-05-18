import requests
from bs4 import BeautifulSoup


HTTP_HEADERS = {
    'cache-control': 'no-cache',
    'user-agent': 'foobar/2000',
}

BASE_URLS = {
    'g': 'https://www.galaxus.ch/en/s2/product/',
    'd': 'https://www.digitec.ch/en/s2/product/',
}

def get_info(product_id):
    site, product = product_id.split('.')
    url = BASE_URLS.get(site) + str(product)
    r = requests.get(url, headers=HTTP_HEADERS)
    if r.ok:
        doc = BeautifulSoup(r.content, 'html.parser')
        title = doc.html.find('meta', property='og:title').attrs.get('content')
        image = doc.html.find('meta', property='og:image').attrs.get('content')
        price = doc.html.find('meta', itemprop='price').attrs.get('content')

        return title, image, float(price)
