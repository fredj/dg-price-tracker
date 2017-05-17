import requests
import microdata


HTTP_HEADERS = {
    'cache-control': 'no-cache',
    'user-agent': 'foobar/2000',
}

PRODUCT_TYPE = microdata.URI('http://schema.org/Product')

BASE_URLS = {
    'g': 'https://www.galaxus.ch/en/s2/product/',
    'd': 'https://www.digitec.ch/en/s2/product/',
}

def get_price(site, product_id):
    url = BASE_URLS.get(site) + str(product_id)
    r = requests.get(url, headers=HTTP_HEADERS)
    if r.ok:
        items = microdata.get_items(r.content)
        products = [item for item in items if PRODUCT_TYPE in item.itemtype]
        offers = [product.offers for product in products if product.offers is not None]
        if len(offers) == 1:
            offer = offers[0]
            return float(offer.price)
