import telebot
import os
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# معرف القناة
CHANNEL_USERNAME = '@Scorpion_scorp'

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    start_message = (
        '✎┊‌ اهلا بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب '
        'يمكنك طرح أي سؤال أو خدمة وسيتم الإجابة عنها إن شاء الله 😁\n\n'
        'تم الصنيع بواسطة :\n'
        'المطور [𝗠𝗼𝗵𝗮𝗺𝗲𝗱](t.me/Zo_r0) \n'
        'المطور [𝗔𝗹𝗹𝗼𝘂𝘀𝗵](t.me/I_e_e_l)'
    )
    bot.send_message(message.chat.id, start_message, parse_mode='Markdown', disable_web_page_preview=True)

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        print(f"User ID: {user_id} Membership Status: {member.status}")  # سجل الحالة للمستخدم
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking membership for user {user_id}: {e}")  # سجل الخطأ
        return False

@bot.message_handler(content_types=['text'])
def gptMessage(message):
    user_id = message.from_user.id
    if not check_membership(user_id):
        bot.send_message(message.chat.id, f'عذراً، يجب عليك الاشتراك في القناة أولاً: {CHANNEL_USERNAME}', parse_mode='HTML')
    else:
        try:
            # إرسال الرسالة إلى دالة gpt واستلام الرد
            resp = gpt(message.text)
            bot.send_message(message.chat.id, f'<b>العقرب : {resp}</b>', parse_mode='HTML')
        except Exception as e:
            # التعامل مع الأخطاء وإرسال رسالة تنبيهية
            bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
