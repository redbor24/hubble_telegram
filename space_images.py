import datetime
from pathlib import Path
from urllib import parse

import requests

from tools import download_image, get_file_ext_from_url
from config import IMAGES_PATH, NASA_TOKEN


def get_apod_images(nasa_token, save_path, image_count):
    if not save_path.is_dir():
        save_path.mkdir(parents=True)

    params = {
        'api_key': nasa_token,
        'count': image_count,
        'thumbs': True
    }
    resp = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    resp.raise_for_status()

    for num, item in enumerate(resp.json(), start=1):
        if get_file_ext_from_url(item['url']):
            url, file_name = item['url'], \
                             Path(parse.unquote(parse.urlparse(item['url']).
                                                path)).name
        else:
            url, file_name = item['thumbnail_url'], f'APOD{num}.jpg'
        download_image(url, Path(save_path) / file_name)


def get_epic_images(nasa_token, save_path):
    if not save_path.is_dir():
        save_path.mkdir(parents=True)

    params = {
        'api_key': nasa_token
    }
    resp = requests.get('https://api.nasa.gov/EPIC/api/natural/images',
                        params=params)
    resp.raise_for_status()
    for num, item in enumerate(resp.json(), start=1):
        filename_time_part = datetime.datetime.strptime(
                item['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        img_link = f'https://api.nasa.gov/EPIC/archive/natural/' \
                   f'{filename_time_part}/png/{item["image"]}.png'
        download_image(img_link, Path(save_path) / f'EPIC{num}.png',
                       params=params)


def get_spacex_images(nasa_token, save_path):
    if not save_path.is_dir():
        save_path.mkdir(parents=True)

    params = {
        'api_key': nasa_token
    }

    resp = requests.get('https://api.spacexdata.com/v4/launches', params=params)
    resp.raise_for_status()

    for item in enumerate(resp.json()):
        links_item = item[1]['links']['flickr']['original']
        if links_item:
            for link in enumerate(links_item):
                filename = Path(save_path) / f'spacex{item[0]}{link[0]}.jpg'
                download_image(link[1], filename)


if __name__ == '__main__':
    get_apod_images(NASA_TOKEN, IMAGES_PATH, 3)
    get_epic_images(NASA_TOKEN, IMAGES_PATH)
    get_spacex_images(NASA_TOKEN, IMAGES_PATH)
