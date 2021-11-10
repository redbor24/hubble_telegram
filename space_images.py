from datetime import datetime
import os
from pathlib import Path
from urllib import parse

import requests

from config import IMAGES_PATH, NASA_TOKEN


def download_image(url, full_filename, params=None):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    with open(full_filename, 'wb') as file:
        file.write(response.content)


def get_file_ext_from_url(url):
    return Path(parse.unquote(parse.urlparse(url).path)).suffix


def get_apod_images(nasa_token, save_path, image_count):
    os.makedirs(save_path, exist_ok=True)

    params = {
        'api_key': nasa_token,
        'count': image_count,
        'thumbs': True
    }
    resp = requests.get(
        'https://api.nasa.gov/planetary/apod',
        params=params
    )
    resp.raise_for_status()

    for num, apod in enumerate(resp.json(), start=1):
        if get_file_ext_from_url(apod['url']):
            url = apod['url']
            file_name = Path(
                parse.unquote(parse.urlparse(apod['url']).path)
            ).name
        else:
            url = apod['thumbnail_url']
            file_name = f'APOD{num}.jpg'
        download_image(url, Path(save_path) / file_name)


def get_epic_images(nasa_token, save_path):
    os.makedirs(save_path, exist_ok=True)

    params = {
        'api_key': nasa_token
    }
    resp = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images',
        params=params
    )
    resp.raise_for_status()

    for num, epic in enumerate(resp.json(), start=1):
        filename_time_part = datetime.strptime(
            epic['date'],
            '%Y-%m-%d %H:%M:%S'
        ).strftime('%Y/%m/%d')

        img_link = 'https://api.nasa.gov/EPIC/archive/natural/' \
            f'{filename_time_part}/png/{epic["image"]}.png'

        download_image(
            img_link,
            Path(save_path) / f'EPIC{num}.png',
            params=params
        )


def get_spacex_images(save_path):
    os.makedirs(save_path, exist_ok=True)
    resp = requests.get(
        'https://api.spacexdata.com/v4/launches',
    )
    resp.raise_for_status()

    for launch in enumerate(resp.json()):
        links_item = launch[1]['links']['flickr']['original']
        if links_item:
            for link in enumerate(links_item):
                filename = Path(save_path) / f'spacex{launch[0]}' \
                    f'{link[0]}.jpg'
                download_image(link[1], filename)


if __name__ == '__main__':
    get_apod_images(NASA_TOKEN, IMAGES_PATH, 3)
    get_epic_images(NASA_TOKEN, IMAGES_PATH)
    get_spacex_images(IMAGES_PATH)
