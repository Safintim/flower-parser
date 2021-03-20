import os
import argparse
import json
import logging
import re


import requests
from bs4 import BeautifulSoup


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

BOUQUETS_URL = 'https://floristan.ru/catalog/all'
BOUQUET_MAP_SIZE = {
    'size_small': 'SMALL',
    'size_middle': 'MIDDLE',
    'size_big': 'BIG',
}


def get_boquet_size_price(info, data_size):
    price = info.select_one(f'.price[data-size="{data_size}"]').text
    return int(re.sub('[\s₽]', '', price))


def get_bouquet_size_flowers(info, data_size):
    return [
        {
            'title':  ' '.join(flower.text.split()[1:]),
            'count': int(flower.text.split()[0])
        }
        for flower in info.select_one(f'.composition[data-size="{data_size}"]').select('div')
    ]


def get_bouquet_sizes(info):
    return [
        {
            'size': BOUQUET_MAP_SIZE[size_input.attrs['value']],
            'price': get_boquet_size_price(info, size_input.attrs['value']),
            'flowers': get_bouquet_size_flowers(info, size_input.attrs['value'])
        }
        for size_input in info.select('input[name="size"]')
    ]


def get_bouquet_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.select_one('div.info')
    return {
        'title': info.select_one('h1').text,
        'sizes': get_bouquet_sizes(info)
    }


def get_bouquets_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    return [a.attrs['href'] for a in soup.select('.products-list .img a')]


def fetch_page(url, params=None):
    logging.info(f'Fetch {url} with params={params}')
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def fetch_bouquets_links(url=BOUQUETS_URL):
    page = 1
    params = {'page': page}
    response = fetch_page(url, params=params)

    while response.status_code != 404:
        response = fetch_page(url, params=params)
        yield get_bouquets_links(response.text)
        params['page'] += 1
        return []


def fetch_bouquets_info():
    for bouquets_links in fetch_bouquets_links():
        for link in bouquets_links:
            bouquet_page = fetch_page(link).text
            yield get_bouquet_info(bouquet_page)


def save_to_json(file_path, bouquets):
    with open(file_path, 'w') as f:
        json.dump(bouquets, f, ensure_ascii=False, indent=4)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir_path', type=is_exist_dir)
    parser.add_argument('-n', '--file_name', default='bouquets')
    return parser


def is_exist_dir(dir_path):
    if os.path.exists(dir_path):
        return dir_path
    return argparse.ArgumentTypeError(f'directory {dir_path} not found')


def flow_parse():
    parser = create_parser()
    namespace = parser.parse_args()
    print(namespace.dir_path, namespace.file_name)
    try:
        bouquets = list(fetch_bouquets_info())
    except requests.RequestException as e:
        logging.error(e)
        exit(e)

    dir_path = namespace.dir_path or os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, f'{namespace.file_name}.json')
    save_to_json(file_path, bouquets)


if __name__ == '__main__':
    flow_parse()
