import telebot
from gpt import gpt
import os

bot = telebot.TeleBot(os.environ['TOKEN'])

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'✎┊‌ اهلا بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب يمكنك طرح أي سؤال أو خدمة وسيتم الإجابة عنها إن شاء الله 😁\n\nتم الصنيع بواسطة :\nالمطور [𝗠𝗼𝗵𝗮𝗺𝗲𝗱](t.me/Zo_r0 ) \nالمطور [𝗔𝗹𝗹𝗼𝘂𝘀𝗵](t.me/I_e_e_l ) ', parse_mode='Markdown', disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def gptMessage(message):
    resp = gpt(message)
    bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')

bot.infinity_polling()
