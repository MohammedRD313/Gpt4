import telebot
from gpt import gpt
import os

# إنشاء البوت
bot = telebot.TeleBot(os.environ['TOKEN'])

# تعيين معرّف المشرف
ADMIN_ID = 815010872  # استبدل هذا الرقم بمعرّف المشرف

# قائمة للمستخدمين المحظورين
banned_users = set()

# معالجة الأمر /start
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in banned_users:
        bot.send_message(message.chat.id, 'آسف، أنت محظور من استخدام هذا البوت.')
    else:
        bot.send_message(message.chat.id, '<b>✎┊‌ اهلا بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب يمكنك طرح اي سؤال او خدمه وسيتم الاجآبه عنها إن شاء الله :</b>', parse_mode='HTML')
        # معالجة الرسائل النصية
@bot.message_handler(content_types=['text'])
def gptMessage(message):
    if message.from_user.id in banned_users:
        bot.send_message(message.chat.id, 'آسف، أنت محظور من استخدام هذا البوت.')
    else:
        resp = gpt(message.text)
        bot.send_message(message.chat.id, f'<b>العقرب : <b> {resp}')

# معالجة أوامر المشرف
@bot.message_handler(commands=['ban', 'unban'])
def admin_commands(message):
    if message.from_user.id == ADMIN_ID:
        command = message.text.split()[0]
        if command == '/ban':
            user_id = int(message.text.split()[1])
            banned_users.add(user_id)
            bot.send_message(message.chat.id, f'تم حظر المستخدم {user_id}.')
        elif command == '/unban':
            user_id = int(message.text.split()[1])
            if user_id in banned_users:
                banned_users.remove(user_id)
                bot.send_message(message.chat.id, f'تم إلغاء حظر المستخدم {user_id}.')
            else:
                bot.send_message(message.chat.id, f'المستخدم {user_id} ليس محظوراً.')

# بدء البوت
bot.infinity_polling()
