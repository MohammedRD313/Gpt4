import telebot
from gpt import gpt
import os

bot = telebot.TeleBot(os.environ['TOKEN'])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'مرحباً أنا سانكا:')

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    resp = gpt(message)
    bot.send_message(message.chat.id, f'سانكا: {resp}')

bot.infinity_polling()