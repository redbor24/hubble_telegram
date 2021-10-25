import os

import requests
from pathlib import Path
import json


def download_image(url, full_filename):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    img_dir = Path(full_filename).parent
    if not Path.is_dir(img_dir) and img_dir != '.':
        Path.mkdir(img_dir, parents=True)

    with open(full_filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(id_launch, save_path):
    url = f'https://api.spacexdata.com/v4/launches/{id_launch}'
    response = requests.get(url)
    response.raise_for_status()

    jsn = json.loads(response.content)
    links = jsn['links']['flickr']['original']
    links_count = len(links)
    for num, link in enumerate(links, start=1):
        download_image(link, Path(save_path) / f'spacex{num}.jpg')
        print(f'{num}/{links_count} image downloaded')


if __name__ == '__main__':
    # try:
    #     download_image(
    #         'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg',
    #         'hubble.jpeg')
    #     download_image(
    #         'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg',
    #         r'\2')
    # except Exception as e:
    #     print(f'Ошибка сохранения файла: {e}')

    # 19 images
    # fetch_spacex_last_launch('5eb87ce3ffd86e000604b336', Path(os.getcwd()) / 'images')
    # 2 images
    fetch_spacex_last_launch('60e3bf0d73359e1e20335c37', Path(os.getcwd()) / 'images')
