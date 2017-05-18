import base64
import datetime
import json
import logging
import os
import re

import requests

from product import get_info


CONTENTS_API_URL = 'https://api.github.com/repos/fredj/dg-price-tracker/contents/%s?ref=gh-pages'

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
assert GITHUB_TOKEN is not None, 'GITHUB_TOKEN environment variables is undefined'

session = requests.Session()
session.headers.update({
    'Authorization': 'token %s' % GITHUB_TOKEN
})

def push_commit(path, content, message, sha):
    commit = {
        'message': message,
        'content': base64.b64encode(bytes(content, 'utf-8')).decode('ascii'),
        'sha': sha,
        'branch': 'gh-pages',
    }
    r = session.put(CONTENTS_API_URL % path, data=json.dumps(commit))
    assert r.ok, r.text

def update_price(product_id, price):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    path = 'prices/%s.csv' % product_id
    sha = None
    entry = session.get(CONTENTS_API_URL % path)
    if entry.status_code == 404:
        logging.info('create price file for %s' % product_id)
        prices = ['date,price']
    else:
        download_url = entry.json().get('download_url')
        prices = session.get(download_url).text.split('\n')
        # remove empty entries
        prices = list(filter(None, prices))
    last = prices[-1]
    # avoid duplicated entries
    if not last.startswith(today) and not last.endswith(str(price)):
        prices.append('%s,%s' % (today, price))
        push_commit(path, '\n'.join(prices), '[skip ci] Update product price', sha)
    else:
        logging.info('no change for %s' % product_id)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # get all tracked products
    entry = session.get(CONTENTS_API_URL % 'products.csv').json()
    content = session.get(entry.get('download_url')).text.split('\n')
    content = list(filter(None, content))
    for i, product in enumerate(content[1:], 1):
        # too lazy to use csv module
        product_id = re.match(r'^([^,]*)', product).group(1)
        assert product_id, 'product_id is undefined'
        title, image, price = get_info(product_id)
        logging.info('got product info: %s "%s": %s CHF' % (product_id, title, price))
        update_price(product_id, price)
        # update products.csv with title and image
        # 'title' may contains commas
        content[i] = ','.join([product_id, '"%s"' % title, image])

    push_commit(entry.get('path'), '\n'.join(content), '[skip ci] Update products.csv', entry.get('sha'))
