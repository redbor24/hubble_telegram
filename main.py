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

    url = 'https://api.spacexdata.com/v4/launches/5eb87d4dffd86e000604b38e'
    response = requests.get(url)
    response.raise_for_status()

    jsn = json.loads(response.content)
    links = jsn['links']['flickr']['original']

    print(links)
