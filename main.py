import telebot
import os
from gpt import gpt
from spellchecker import SpellChecker
from farasa.pos import FarasaPOSTagger
from farasa.ner import FarasaNamedEntityRecognizer
from farasa.stemmer import FarasaStemmer
from farasa.diacratizer import FarasaDiacritizer

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
    # الرسائل السابقة هنا
}

# إنشاء كائن SpellChecker
spell_checker = SpellChecker(language='en')

# إعداد Farasa
farasa_diacritizer = FarasaDiacritizer(interactive=True)

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
        corrected_text = ' '.join(spell_checker.candidates(word)[0] if word not in spell_checker else word for word in text.split())
    elif language == 'ar':
        # تصحيح الأخطاء الإملائية للنصوص العربية
        try:
            diacritized_text = farasa_diacritizer.diacratize(text)
        except Exception as e:
            diacritized_text = text  # التعامل مع الاستثناءات إن وجدت
        corrected_text = diacritized_text
    else:
        corrected_text = text

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
    return all('\u0600' <= c <= '\u06FF' or c.isspace() for c in text)

def is_english(text):
    # التحقق من النص الإنجليزي
    return all('a' <= c.lower() <= 'z' or c.isspace() for c in text)

# بدء الاستماع للرسائل
bot.infinity_polling()
