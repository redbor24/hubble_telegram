import requests

headers = {
    'User-Agent': 'curl',
    'Accept-Language': 'ru-RU'
}

filename = 'hubble.jpeg'
url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"

response = requests.get(url, headers=headers)
response.raise_for_status()

with open(filename, 'wb') as file:
    file.write(response.content)

