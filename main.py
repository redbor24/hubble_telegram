import requests
from pathlib import Path

IMAGES_FOLDER = 'images'


def download_image(url, filename):
    headers = {
        'User-Agent': 'curl',
        'Accept-Language': 'ru-RU'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    images_directory = Path.cwd() / IMAGES_FOLDER
    if not Path.is_dir(images_directory):
        Path.mkdir(images_directory)

    with open(Path(images_directory) / filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    download_image(
        'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg',
        'hubble.jpeg')
