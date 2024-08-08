import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from gpt import gpt

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# إنشاء بوت Telegram
bot = telebot.TeleBot(TOKEN)

# تخزين تفضيلات المستخدمين
user_preferences = {}

# رسائل الترحيب واستجابة خاصة لكل لغة
messages = {
    'ar': {
        'start': (
            '<a href="https://t.me/ScorGPTbot">𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗚𝗣𝗧 𝟰</a>\n\n'
            '<b>✎┊‌ أهلاً بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب.</b>\n'
            '<b>يمكنك طرح أي سؤال أو طلب خدمة، وسنكون سعداء بالإجابة عليه إن شاء الله 😁</b>\n\n'
            '<b>للتحويل الى اللغه الانجليزيه استخدم الأمر</b> \n<code>/language en</code>\n\n'
            '<b>تم الصنيع بواسطة:</b>\n'
            'المطور <a href="https://t.me/Zo_r0">𝗠𝗼𝗵𝗮𝗺𝗲𝗱</a> \n'
            'المطور <a href="https://t.me/I_e_e_l">𝗔𝗹𝗹𝗼𝘂𝘀𝗵</a>'
        ),
        'commands': (
            '**الأوامر المتاحة:**\n'
            '`/start` - بدء التفاعل مع البوت\n'
            '`/language [ar/en]` - تغيير اللغة\n'
            '`/format [html/markdown]` - تغيير تنسيق الرسائل\n'
        ),
        'set_language': 'تم التغيير الى اللغة العربية.',
        'set_format': 'تم تغيير التنسيق إلى {format}.',
        'error': 'حدث خطأ: {error}',
        'response_prefix': '**العقرب:** '
    },
    'en': {
        'start': (
            '<a href="https://t.me/ScorGPTbot">𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗚𝗣𝗧 𝟰</a>\n\n'
            '<b>✎┊‌ Welcome to the Scorpio AI bot.</b>\n'
            '<b>You can ask any question or request a service, and we will be happy to answer it, God willing 😁</b>\n\n'
            '<b>To switch to Arabic, use the command</b> \n<code>/language ar</code>\n\n'
            '<b>Created by:</b>\n'
            'Developer <a href="https://t.me/Zo_r0">𝗠𝗼𝗵𝗮𝗺𝗲𝗱</a> \n'
            'Developer <a href="https://t.me/I_e_e_l">𝗔𝗹𝗹𝗼𝘂𝘀𝗵</a>'
        ),
        'commands': (
            '**Available commands:**\n'
            '`/start` - Start interacting with the bot\n'
            '`/language [ar/en]` - Change language\n'
            '`/format [html/markdown]` - Change message format\n'
        ),
        'set_language': 'Language set to English.',
        'set_format': 'Format set to {format}.',
        'error': 'An error occurred: {error}',
        'response_prefix': '**Scorpio:** '
    }
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    language = user_preferences.get(user_id, {}).get('language', 'ar')  # اللغة الافتراضية هي العربية
    start_message = messages[language]['start']

    # إنشاء زر للاشتراك في القناة
    markup = InlineKeyboardMarkup()
    subscribe_button = InlineKeyboardButton("𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 ✍🏻 ", url="https://t.me/Scorpion_scorp")
    markup.add(subscribe_button)

    bot.send_message(user_id, start_message, parse_mode='HTML', disable_web_page_preview=True, reply_markup=markup)

@bot.message_handler(commands=['language'])
def set_language(message):
    user_id = message.chat.id
    if len(message.text.split()) > 1:
        lang = message.text.split()[1].lower()
        if lang in messages:
            if user_id not in user_preferences:
                user_preferences[user_id] = {}
            user_preferences[user_id]['language'] = lang
            response_message = messages[lang]['set_language']
        else:
            response_message = '✎┊‌ لغة غير مدعومة. يرجى اختيار "ar" للغة العربية أو "en" للغة الإنجليزية. \n\n Unsupported language. Please choose "ar" for Arabic or "en" for English.'
    else:
        response_message = 'Please specify a language code. Usage: /language [ar/en]'
    
    bot.send_message(user_id, response_message, parse_mode='Markdown')

@bot.message_handler(commands=['format'])
def set_format(message):
    user_id = message.chat.id
    if len(message.text.split()) > 1:
        fmt = message.text.split()[1].lower()
        if fmt in ['html', 'markdown']:
            if user_id not in user_preferences:
                user_preferences[user_id] = {}
            user_preferences[user_id]['format'] = fmt.capitalize()
            language = user_preferences[user_id].get('language', 'ar')
            response_message = messages[language]['set_format'].format(format=fmt.capitalize())
        else:
            response_message = '✎┊‌ لغة غير مدعومة. يرجى اختيار "ar" للغة العربية أو "en" للغة الإنجليزية. \n\n Unsupported language. Please choose "ar" for Arabic or "en" for English.'
    else:
        response_message = 'Please specify a format. Usage: /format [html/markdown]'
    
    bot.send_message(user_id, response_message, parse_mode='Markdown')

@bot.message_handler(commands=['commands'])
def show_commands(message):
    user_id = message.chat.id
    language = user_preferences.get(user_id, {}).get('language', 'ar')  # اللغة الافتراضية هي العربية
    commands_message = messages[language]['commands']
    bot.send_message(user_id, commands_message, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def gpt_message(message):
    user_id = message.chat.id
    language = user_preferences.get(user_id, {}).get('language', 'ar')  # اللغة الافتراضية هي العربية
    text = message.text
    if (language == 'ar' and not is_arabic(text)) or (language == 'en' and not is_english(text)):
        response_message = '✎┊‌اللغة المستخدمة غير صالحة. يرجى استخدام اللغة المحددة فقط.\n\n Invalid language used. Please use the selected language only.'
        format_type = user_preferences.get(user_id, {}).get('format', 'markdown')
        if format_type == 'html':
            bot.send_message(user_id, f'<b>{response_message}</b>', parse_mode='HTML')
        else:
            bot.send_message(user_id, response_message, parse_mode='Markdown')
        return
    
    try:
        # إرسال الرسالة إلى دالة gpt واستلام الرد
        response = gpt(text)
        response_prefix = messages[language]['response_prefix']
        formatted_response = f"**{response}**"
        format_type = user_preferences.get(user_id, {}).get('format', 'markdown')
        if format_type == 'html':
            bot.send_message(user_id, f'{response_prefix}<b>{response}</b>', parse_mode='HTML')
        else:
            bot.send_message(user_id, f'{response_prefix}{formatted_response}', parse_mode='Markdown')
    except Exception as e:
        # التعامل مع الأخطاء وإرسال رسالة تنبيهية
        error_message = messages[language]['error'].format(error=e)
        format_type = user_preferences.get(user_id, {}).get('format', 'markdown')
        if format_type == 'html':
            bot.send_message(user_id, f'<b>{error_message}</b>', parse_mode='HTML')
        else:
            bot.send_message(user_id, error_message, parse_mode='Markdown')

# دوال للتحقق من اللغة
def is_arabic(text):
    # التحقق من النص العربي ودعمه للرموز الإنجليزية
    return all('\u0600' <= c <= '\u06FF' or c.isspace() or c in {'\u0020', '\u002D', '\u002E', '\u002C', '\u003A', '\u003B', 
           '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', '[', ']', '{', '}', ';', ':', '"', '\'', ',', '.', 
           '/', '<', '>', '?', '\\', '|', '`', '~'} for c in text)

def is_english(text):
    # التحقق من النص الإنجليزي
    return all('a' <= c.lower() <= 'z' or c.isspace() or c in {'!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '+', 
           '[', ']', '{', '}', ';', ':', '"', '\'', ',', '.', '/', '<', '>', '?', '\\', '|', '`', '~'} for c in text)

# بدء الاستماع للرسائل
bot.infinity_polling()
