import os
import pickle
from pathlib import Path

import decouple
from telegram import TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from nasa import get_apod_images

NASA_TOKEN = decouple.config('NASA_TOKEN', '')
TELEGRAM_TOKEN = decouple.config('TELEGRAM_TOKEN', '')
CHAT_LIST_FILE_NAME = 'telebot.data'
DELIVERY_TIMEOUT = int(os.getenv('DELIVERY_TIMEOUT', default=86400))
IMAGES_SUB_PATH = 'images'
chat_list = []


def on_hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello, {update.effective_user.first_name}!')


def on_start(update: Update, context: CallbackContext):
    global chat_list
    msg = f"Hi! I'm a bot {update.effective_chat.bot.first_name}!"
    chat_list.append(update.effective_chat.id)
    save_chat_list()
    try:
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        send_random_image(context)
    except Exception as e:
        chat_list.remove(update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=e)


def send_random_image(context: CallbackContext):
    file = get_apod_images(NASA_TOKEN, Path(os.getcwd()) / IMAGES_SUB_PATH, 1)
    chats_for_remove = []
    for chat_id in chat_list:
        try:
            context.bot.send_document(chat_id=chat_id,
                                      document=open(file[0], 'rb'))
        except TelegramError as e:
            chats_for_remove.append(chat_id)
    os.remove(file[0])

    for chat in chats_for_remove:
        chat_list.remove(chat)
    save_chat_list()


def load_chat_list():
    try:
        with open(CHAT_LIST_FILE_NAME, 'rb') as file_handle:
            chats = pickle.load(file_handle)
    except FileNotFoundError as e:
        chats = []
    return chats


def save_chat_list():
    global chat_list
    chat_list = list(set(chat_list))
    with open(CHAT_LIST_FILE_NAME, 'wb') as file_handle:
        pickle.dump(chat_list, file_handle)


def start_bot():
    global chat_list
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('hello', on_hello))
    dispatcher.add_handler(CommandHandler('start', on_start))
    chat_list = load_chat_list()

    updater.job_queue.run_repeating(send_random_image,
                                    interval=DELIVERY_TIMEOUT, first=10)

    updater.start_polling()
    updater.idle()
