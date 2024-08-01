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
def gpt_message(message):
    if message.from_user.id in banned_users:
        bot.send_message(message.chat.id, 'آسف، أنت محظور من استخدام هذا البوت.')
    else:
        resp = gpt(message.text)
        bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')

# معالجة أوامر المشرف
@bot.message_handler(commands=['ban', 'unban'])
def admin_commands(message):
    if message.from_user.id == ADMIN_ID:
        parts = message.text.split()
        if len(parts) != 2:
            bot.send_message(message.chat.id, 'الرجاء استخدام الصيغة الصحيحة: /ban <user_id> أو /unban <user_id>')
            return
        
        command = parts[0]
        try:
            user_id = int(parts[1])
        except ValueError:
            bot.send_message(message.chat.id, 'يرجى تقديم معرف مستخدم صحيح.')
            return

        if command == '/ban':
            banned_users.add(user_id)
            bot.send_message(message.chat.id, f'تم حظر المستخدم {user_id}.')
        elif command == '/unban':
            if user_id in banned_users:
                banned_users.remove(user_id)
                bot.send_message(message.chat.id, f'تم إلغاء حظر المستخدم {user_id}.')
            else:
                bot.send_message(message.chat.id, f'المستخدم {user_id} ليس محظوراً.')

# بدء البوت
bot.infinity_polling()
