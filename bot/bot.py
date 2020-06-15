import sys

import telebot
from dotenv import load_dotenv
from os import path, getenv

env_path = path.abspath(path.join(path.dirname(path.abspath(__file__)), '../.env'))
load_dotenv(dotenv_path=env_path)

TOKEN = getenv('TOKEN')
USER_ID_OF_ADMINS = [int(x) for x in getenv('USER_ID_OF_ADMINS').split('/') if x]
USER_ID_OF_GROUP = int(getenv('USER_ID_OF_GROUP'))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello!!!")


@bot.message_handler(content_types=['video_note'])
def echo_videos(message):
    try:
        if message.from_user.id not in USER_ID_OF_ADMINS:
            bot.forward_message(USER_ID_OF_GROUP, message.chat.id, message.message_id)
        elif message.from_user.id in USER_ID_OF_ADMINS and message.reply_to_message:
            if message.reply_to_message.forward_from:
                bot.send_video_note(message.reply_to_message.forward_from.id, message.video_note.file_id)
            else:
                bot.reply_to(message, 'Private User!')
    except Exception:
        e = sys.exc_info()
        print(e)


@bot.message_handler(content_types=['voice'])
def echo_audios(message):
    try:
        if message.from_user.id not in USER_ID_OF_ADMINS:
            bot.forward_message(USER_ID_OF_GROUP, message.chat.id, message.message_id)
        elif message.from_user.id in USER_ID_OF_ADMINS and message.reply_to_message:
            if message.reply_to_message.forward_from:
                bot.send_voice(message.reply_to_message.forward_from.id, message.voice.file_id)
            else:
                bot.reply_to(message, 'Private User!')
    except Exception:
        e = sys.exc_info()
        print(e)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        if message.from_user.id not in USER_ID_OF_ADMINS:
            bot.forward_message(USER_ID_OF_GROUP, message.chat.id, message.message_id, disable_notification=True)
        elif message.from_user.id in USER_ID_OF_ADMINS and message.reply_to_message:
            if message.reply_to_message.forward_from:
                bot.send_message(message.reply_to_message.forward_from.id, message.text)
            else:
                bot.reply_to(message, 'Private User!')
    except Exception:
        e = sys.exc_info()
        print(e)


bot.polling()
