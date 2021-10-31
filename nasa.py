import datetime
import json
from pathlib import Path
from urllib import parse

import requests


def download_image(url, full_filename, params=None):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }

    if params:
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers)
    response.raise_for_status()

    img_dir = Path(full_filename).parent
    if not Path.is_dir(img_dir) and img_dir != '.':
        Path.mkdir(img_dir, parents=True)

    with open(full_filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_launch(launch_id, save_path):
    url = f'https://api.spacexdata.com/v4/launches/{launch_id}'
    response = requests.get(url)
    response.raise_for_status()

    file_list = []
    links = json.loads(response.content)['links']['flickr']['original']
    for num, link in enumerate(links, start=1):
        filename = Path(save_path) / f'spacex{num}.jpg'
        download_image(link, filename)
        file_list.append(filename)
    return file_list


def get_file_ext_from_url(url):
    parsed_url = parse.urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    return Path(parse.unquote(parse.urlparse(url).path)).suffix


def get_apod_images(nasa_token, save_path, image_count):
    params = {
        'api_key': nasa_token,
        'count': image_count,
        'thumbs': True
    }
    response = requests.get('https://api.nasa.gov/planetary/apod',
                            params=params)
    response.raise_for_status()
    data = json.loads(response.content)

    file_list = []
    for num, item in enumerate(data, start=1):
        if get_file_ext_from_url(item['url']):
            url, file_name = item['url'], \
                             Path(parse.unquote(parse.urlparse(item['url']).
                                                path)).name
        else:
            url, file_name = item['thumbnail_url'], f'APOD{num}.jpg'
        full_filename = Path(save_path) / file_name
        download_image(url, full_filename)
        file_list.append(full_filename)
    return file_list


def get_epic_images(nasa_token, save_path):
    params = {
        'api_key': nasa_token
    }
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/images',
                            params=params)
    response.raise_for_status()
    data = json.loads(response.content)
    file_list = []
    for num, item in enumerate(data, start=1):
        date_time_str = datetime.datetime.strptime(
                item['date'], '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d')
        link_to_img = f'https://api.nasa.gov/EPIC/archive/natural/' \
                      f'{date_time_str}/png/{data[0]["image"]}.png'
        full_filename = f'_EPIC{num}.png'
        download_image(link_to_img, Path(save_path) / full_filename,
                       params=params)
        file_list.append(full_filename)
    return file_list


def get_launches_with_images(nasa_token):
    params = {
        'api_key': nasa_token
    }
    response = requests.get('https://api.spacexdata.com/v4/launches',
                            params=params)
    response.raise_for_status()
    data = json.loads(response.content)
    launch_list = []
    for item in enumerate(data):
        links_item = item[1]['links']['flickr']['original']
        if links_item:
            launch_list_item = {'id': item[1]['id'], 'count': len(links_item)}
            launch_list.append(launch_list_item)
    return launch_list