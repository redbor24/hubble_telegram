from os import getcwd, getenv
from pathlib import Path

from decouple import config


NASA_TOKEN = config('NASA_TOKEN', '')
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN', '')
DELIVERY_TIMEOUT = int(getenv('DELIVERY_TIMEOUT', '86400'))
TELEGRAM_CHANNEL_NAME = config('TELEGRAM_CHANNEL_NAME', '')

_ = config('IMAGES_PATH', 'images')
if not Path(_).is_absolute():
    IMAGES_PATH = Path(getcwd()) / _
else:
    IMAGES_PATH = Path(_)
