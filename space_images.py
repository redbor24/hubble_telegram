from datetime import datetime
import os
from pathlib import Path
from urllib import parse

import requests

from tools import download_image, get_file_ext_from_url
from config import IMAGES_PATH, NASA_TOKEN


def get_apod_images(nasa_token, save_path, image_count):
    os.makedirs(save_path, exist_ok=True)

    params = {
        'api_key': nasa_token,
        'count': image_count,
        'thumbs': True
    }
    resp = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    resp.raise_for_status()

    for num, apod_data in enumerate(resp.json(), start=1):
        if get_file_ext_from_url(apod_data['url']):
            url = apod_data['url']
            file_name = Path(parse.unquote(parse.urlparse(
                    apod_data['url']).path)).name
        else:
            url, file_name = apod_data['thumbnail_url'], f'APOD{num}.jpg'
        download_image(url, Path(save_path) / file_name)


def get_epic_images(nasa_token, save_path):
    os.makedirs(save_path, exist_ok=True)

    params = {
        'api_key': nasa_token
    }
    resp = requests.get('https://api.nasa.gov/EPIC/api/natural/images',
                        params=params)
    resp.raise_for_status()

    for num, epic_data in enumerate(resp.json(), start=1):
        filename_time_part = datetime.strptime(
            epic_data['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        img_link = f'https://api.nasa.gov/EPIC/archive/natural/' \
                   f'{filename_time_part}/png/{epic_data["image"]}.png'
        download_image(img_link, Path(save_path) / f'EPIC{num}.png',
                       params=params)


def get_spacex_images(nasa_token, save_path):
    os.makedirs(save_path, exist_ok=True)
    params = {
        'api_key': nasa_token
    }

    resp = requests.get('https://api.spacexdata.com/v4/launches',
                        params=params)
    resp.raise_for_status()

    for launch_data in enumerate(resp.json()):
        links_item = launch_data[1]['links']['flickr']['original']
        if links_item:
            for link in enumerate(links_item):
                filename = Path(save_path) / f'spacex{launch_data[0]}' \
                                             f'{link[0]}.jpg'
                download_image(link[1], filename)


if __name__ == '__main__':
    get_apod_images(NASA_TOKEN, IMAGES_PATH, 3)
    get_epic_images(NASA_TOKEN, IMAGES_PATH)
    get_spacex_images(NASA_TOKEN, IMAGES_PATH)
