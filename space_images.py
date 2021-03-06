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
    _ = parse.urlparse(url).path
    return Path(parse.unquote(_)).suffix


def download_apod_images(nasa_token, images_path, image_count):
    os.makedirs(images_path, exist_ok=True)

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
            _ = parse.urlparse(apod['url']).path
            file_name = Path(parse.unquote(_)).name
        else:
            url = apod['thumbnail_url']
            file_name = f'APOD{num}.jpg'
        download_image(url, Path(images_path) / file_name)


def download_epic_images(nasa_token, images_path):
    os.makedirs(images_path, exist_ok=True)

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
            Path(images_path) / f'EPIC{num}.png',
            params=params
        )


def download_spacex_images(images_path):
    os.makedirs(images_path, exist_ok=True)
    resp = requests.get(
        'https://api.spacexdata.com/v4/launches',
    )
    resp.raise_for_status()

    for launch_num, launch in enumerate(resp.json()):
        links_item = launch['links']['flickr']['original']
        if links_item:
            for link_num, link in enumerate(links_item):
                filename = Path(images_path) / f'spacex{launch_num}' \
                    f'{link_num}.jpg'
                download_image(link, filename)


if __name__ == '__main__':
    download_apod_images(NASA_TOKEN, IMAGES_PATH, 2)
    download_epic_images(NASA_TOKEN, IMAGES_PATH)
    download_spacex_images(IMAGES_PATH)
