import requests
from pathlib import Path

headers = {
    'User-Agent': 'curl',
    'Accept-Language': 'ru-RU'
}

filename = 'hubble.jpeg'
url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

response = requests.get(url, headers=headers)
response.raise_for_status()

images_directory = Path.cwd() / 'images'
if not Path.is_dir(images_directory):
    Path.mkdir(images_directory)

with open(Path(images_directory) / filename, 'wb') as file:
    file.write(response.content)
