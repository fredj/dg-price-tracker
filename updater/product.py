from requests_html import HTMLSession


BASE_URLS = {
    'g': 'https://www.galaxus.ch/en/s2/product/',
    'd': 'https://www.digitec.ch/en/s2/product/',
}

session = HTMLSession()

def get_info(product_id):
    site, product = product_id.split('.')
    url = BASE_URLS.get(site) + str(product)
    r = session.get(url)
    if r.ok:
        title = r.html.find("meta[property='og:title']", first=True).attrs.get('content')
        image = r.html.find("meta[property='og:image']", first=True).attrs.get('content')
        # if the product is currently unavailable, the price is not set
        price_node = r.html.find("meta[property='product:price:amount']", first=True)
        price = price_node.attrs.get('content') if price_node is not None else 0

        return title, image, float(price)
