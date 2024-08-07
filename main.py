import telebot
import os
from gpt import gpt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

# تنزيل الموارد اللازمة من مكتبة nltk
nltk.download('punkt')
nltk.download('stopwords')

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

def process_text(text):
    # تقسيم النص إلى كلمات
    tokens = word_tokenize(text)

    # إزالة الكلمات الشائعة (stop words)
    stop_words = set(stopwords.words('arabic'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # حساب تكرار الكلمات
    freq_dist = FreqDist(filtered_tokens)

    # إعداد ملخص
    summary = f"عدد الكلمات: {len(tokens)}\n"
    summary += f"عدد الكلمات (بدون الكلمات الشائعة): {len(filtered_tokens)}\n"
    summary += "أكثر الكلمات تكرارًا:\n"
    for word, frequency in freq_dist.most_common(5):
        summary += f"{word}: {frequency}\n"

    return summary

@bot.message_handler(content_types=['text'])
def gpt_message(message):
    try:
        # إرسال الرسالة إلى دالة gpt واستلام الرد
        response = gpt(message.text)
        text_summary = process_text(message.text)
        final_response = f'<b>العقرب : {response}</b>\n\n<b>ملخص النص:</b>\n{text_summary}'
        bot.send_message(message.chat.id, final_response, parse_mode='HTML')
    except Exception as e:
        # التعامل مع الأخطاء وإرسال رسالة تنبيهية
        bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
