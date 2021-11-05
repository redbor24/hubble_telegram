from os import getcwd
from pathlib import Path

import decouple

NASA_TOKEN = decouple.config('NASA_TOKEN', '')
TELEGRAM_TOKEN = decouple.config('TELEGRAM_TOKEN', '')
DELIVERY_TIMEOUT = int(decouple.config('DELIVERY_TIMEOUT', '86400'))
TELEGRAM_CHANNEL_NAME = decouple.config('TELEGRAM_CHANNEL_NAME', '')

_ = decouple.config('IMAGES_PATH', 'images')
if not Path(_).is_absolute():
    IMAGES_PATH = Path(getcwd()) / _
else:
    IMAGES_PATH = Path(_)
