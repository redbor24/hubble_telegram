import decouple

from telegram_bot import start_bot


if __name__ == '__main__':
    TELEGRAM_TOKEN = decouple.config('TELEGRAM_TOKEN', '')
    start_bot(TELEGRAM_TOKEN)
