import base64
import datetime
import json
import logging
import os

import requests

from product import get_info


CONTENTS_API_URL = 'https://api.github.com/repos/fredj/dg-price-tracker/contents/%s'

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
assert GITHUB_TOKEN is not None, 'GITHUB_TOKEN environment variables is undefined'

session = requests.Session()
session.headers.update({
    'Authorization': 'token %s' % GITHUB_TOKEN
})

def update_price(entry, price):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    prices = session.get(entry.get('download_url')).text.split('\n')
    # remove empty entries
    prices = list(filter(None, prices))
    last = prices[-1]
    if not last.startswith(today) and not last.endswith(str(price)):
        # avoid duplicated entries
        prices.append('%s,%s' % (today, price))
        content = '\n'.join(prices)
        commit = {
            'message': 'Update price',
            'content': base64.b64encode(bytes(content, 'utf-8')).decode('ascii'),
            'sha': entry.get('sha'),
            'branch': 'gh-pages',
        }
        r = session.put(CONTENTS_API_URL % entry.get('path'), data=json.dumps(commit))
        assert r.ok, r.text

if __name__ == "__main__":
    # update all prices
    entries = session.get(CONTENTS_API_URL % 'prices?ref=gh-pages').json()
    for entry in entries:
        name = entry.get('name')
        site, product, _ = name.split('.')
        title, price, image = get_info(site, product)
        update_price(entry, price)
