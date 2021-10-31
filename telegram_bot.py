import os
from pathlib import Path

import decouple
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters
from nasa import get_apod_images

NASA_TOKEN = decouple.config('NASA_TOKEN', '')


def on_hello(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hello, {update.effective_user.first_name}!')


def on_start(update: Update, context: CallbackContext):
    msg = f"Hi! I'm a bot {update.effective_chat.bot.first_name}!"
    print(msg)
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    file_list = get_apod_images(NASA_TOKEN, Path(os.getcwd()) / 'apod', 1)
    context.bot.send_document(chat_id=update.effective_chat.id,
                              document=open(file_list[0], 'rb'))
    os.remove(file_list[0])


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=update.message.text)


def start_bot(telegram_token):
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('hello', on_hello))
    dispatcher.add_handler(CommandHandler('start', on_start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command),
                                          echo))
    updater.start_polling()
    updater.idle()

