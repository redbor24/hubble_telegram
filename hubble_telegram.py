import decouple
import os

from nasa import *
from telegram_bot import start_bot


if __name__ == '__main__':
    NASA_TOKEN = decouple.config('NASA_TOKEN', '')
    # get_epic_images(NASA_TOKEN, Path(os.getcwd()) / 'epic1')
    # get_launches_with_images(NASA_TOKEN)
    TELEGRAM_TOKEN = decouple.config('TELEGRAM_TOKEN', '')
    start_bot(TELEGRAM_TOKEN)
