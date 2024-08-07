import telebot
import os
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

# تخزين اللغة المفضلة لكل مستخدم
user_languages = {}

# رسائل الترحيب واستجابة خاصة لكل لغة
messages = {
    'ar': {
        'start': (
            '✎┊‌ أهلاً بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب.\n'
            'يمكنك طرح أي سؤال أو طلب خدمة، وسنكون سعداء بالإجابة عليه إن شاء الله 😁\n\n'
            'للتحويل الى اللغه الانجليزيه ارسل هذا الامر '
            ' \language en \n\n'
            'تم الصنيع بواسطة:\n'
            'المطور [𝗠𝗼𝗵𝗮𝗺𝗲𝗱](t.me/Zo_r0) \n'
            'المطور [𝗔𝗹𝗹𝗼𝘂𝘀𝗵](t.me/I_e_e_l)'
        ),
        'set_language': 'اللغة تم تعيينها إلى العربية.',
        'error': 'حدث خطأ: {error}',
        'response_prefix': 'العقرب: '
    },
    'en': {
        'start': (
            '✎┊‌ Welcome to the Scorpio AI bot.\n'
            'You can ask any question or request a service, and we will be happy to answer it, God willing 😁\n\n'
            'To convert to Arabic, send this command'
            ' /language ar \n\n'
            'Created by:\n'
            'Developer [𝗠𝗼𝗵𝗮𝗺𝗲𝗱](t.me/Zo_r0) \n'
            'Developer [𝗔𝗹𝗹𝗼𝘂𝘀𝗵](t.me/I_e_e_l)'
        ),
        'set_language': 'Language set to English.',
        'error': 'An error occurred: {error}',
        'response_prefix': 'Scorpio: '
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    language = user_languages.get(user_id, 'ar')  # اللغة الافتراضية هي العربية
    start_message = messages[language]['start']
    bot.send_message(user_id, start_message, parse_mode='Markdown', disable_web_page_preview=True)

@bot.message_handler(commands=['language'])
def set_language(message):
    user_id = message.chat.id
    if len(message.text.split()) > 1:
        lang = message.text.split()[1].lower()
        if lang in messages:
            user_languages[user_id] = lang
            response_message = messages[lang]['set_language']
        else:
            response_message = 'Unsupported language. Please choose "ar" for Arabic or "en" for English.'
    else:
        response_message = 'Please specify a language code. Usage: /language [ar/en]'
    
    bot.send_message(user_id, response_message)

@bot.message_handler(content_types=['text'])
def gpt_message(message):
    user_id = message.chat.id
    language = user_languages.get(user_id, 'ar')  # اللغة الافتراضية هي العربية
    try:
        # إرسال الرسالة إلى دالة gpt واستلام الرد
        response = gpt(message.text)
        response_prefix = messages[language]['response_prefix']
        bot.send_message(user_id, f'<b>{response_prefix}{response}</b>', parse_mode='HTML')
    except Exception as e:
        # التعامل مع الأخطاء وإرسال رسالة تنبيهية
        error_message = messages[language]['error'].format(error=e)
        bot.send_message(user_id, error_message, parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
