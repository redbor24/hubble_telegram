import os
from pathlib import Path
from time import sleep

from telegram import error, Bot

from config import (DELIVERY_TIMEOUT, IMAGES_PATH, TELEGRAM_CHANNEL_NAME,
                    TELEGRAM_TOKEN)


def send_images_to_telegram_channel(telegram_token, images_path,
                                    telegram_channel_name, delivery_timeout):
    bot = Bot(telegram_token)
    try:
        while 1 == 1:
            for filename in os.listdir(images_path):
                with open(Path(os.getcwd()) / images_path / filename,
                          'rb') as img_file:
                    bot.send_document(chat_id=telegram_channel_name,
                                      document=img_file)
                sleep(delivery_timeout)
    except error.BadRequest as e:
        print(f'Ошибка Telegram! {e}')


if __name__ == '__main__':
    send_images_to_telegram_channel(TELEGRAM_TOKEN, IMAGES_PATH,
                                    TELEGRAM_CHANNEL_NAME, DELIVERY_TIMEOUT)
