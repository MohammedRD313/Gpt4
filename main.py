import telebot
import os
from gpt import gpt
from spellchecker import SpellChecker
from camel_tools.spell import ArabSpellChecker
from camel_tools.tokenizers import word_tokenize
from camel_tools.parser import Parser

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
            '<b>✎┊‌ أهلاً بك في بوت الذكاء الاصطناعي الخاص بسورس العقرب.</b>'
            '<b>يمكنك طرح أي سؤال أو طلب ، وسنكون سعداء بالإجابة عليه إن شاء الله 😁</b>\n\n'
            '<b>للتحويل الى اللغه الانجليزيه استخدم الأمر</b> \n{ <code>/language en</code>} \n\n'
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
        'response_prefix': 'العقرب: '
    },
    'en': {
        'start': (
            '<a href="https://t.me/ScorGPTbot">𝗦𝗰𝗼𝗿𝗽𝗶𝗼𝗻 𝗚𝗣𝗧 𝟰</a>\n\n'
            '<b>✎┊‌ Welcome to the Scorpio AI bot.</b>'
            '<b>You can ask any question or request a service, and we will be happy to answer it, God willing 😁</b>\n\n'
            '<b>To switch to Arabic, use the command</b> \n{ <code>/language ar</code> }\n\n'
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
        'response_prefix': 'Scorpio:'
    }
}

# إنشاء كائن SpellChecker للغة الإنجليزية
spell_checker_en = SpellChecker(language='en')

# إنشاء كائن ArabSpellChecker للغة العربية
spell_checker_ar = ArabSpellChecker()

# إنشاء كائن Parser للغة العربية
parser = Parser()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    language = user_preferences.get(user_id, {}).get('language', 'ar')  # اللغة الافتراضية هي العربية
    start_message = messages[language]['start']
    bot.send_message(user_id, start_message, parse_mode='HTML', disable_web_page_preview=True)

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
            response_message = 'Unsupported language. Please choose "ar" for Arabic or "en" for English.'
    else:
        response_message = 'Please specify a language code. Usage: /language [ar/en]'
    
    bot.send_message(user_id, response_message)

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
            response_message = 'Unsupported format. Please choose "html" or "markdown".'
    else:
        response_message = 'Please specify a format. Usage: /format [html/markdown]'
    
    bot.send_message(user_id, response_message)

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

    # معالجة الأخطاء الإملائية
    if language == 'en':
        tokens = text.split()
        corrected_tokens = [spell_checker_en.candidates(word).pop() if word not in spell_checker_en else word for word in tokens]
        corrected_text = ' '.join(corrected_tokens)
    elif language == 'ar':
        tokens = text.split()
        corrected_tokens = [spell_checker_ar.correct(word) for word in tokens]
        corrected_text = ' '.join(corrected_tokens)
    else:
        corrected_text = text  # إذا كانت اللغة غير مدعومة، استخدم النص كما هو

    # تحليل النصوص العربية لإضافة إعراب ونحو
    if language == 'ar':
        tokens = word_tokenize(corrected_text)
        parsed = parser.parse(tokens)
        # دمج التحليل النحوي والإعرابي مع النص المصحح
        corrected_text = ' '.join(f"{word}/{analysis}" for word, analysis in zip(tokens, parsed))

    # التحقق من أن النص المدخل باللغة المحددة للمستخدم
    if (language == 'ar' and is_arabic(corrected_text)) or (language == 'en' and is_english(corrected_text)):
        try:
            # إرسال الرسالة إلى دالة gpt واستلام الرد
            response = gpt(corrected_text)
            response_prefix = messages[language]['response_prefix']
            formatted_response = f"**{response}**"
            bot.send_message(user_id, f'{response_prefix}{formatted_response}', parse_mode='Markdown')
        except Exception as e:
            # التعامل مع الأخطاء وإرسال رسالة تنبيهية
            error_message = messages[language]['error'].format(error=e)
            bot.send_message(user_id, error_message, parse_mode='Markdown')
    else:
        error_message = 'الرجاء إرسال الرسائل باللغة المحددة.'
        bot.send_message(user_id, error_message)

# دوال للتحقق من اللغة
def is_arabic(text):
    # التحقق من النص العربي
    return any('\u0600' <= c <= '\u06FF' or c.isspace() for c in text)

def is_english(text):
    # التحقق من النص الإنجليزي
    return any('a' <= c.lower() <= 'z' or c.isspace() for c in text)

# بدء الاستماع للرسائل
bot.infinity_polling()
