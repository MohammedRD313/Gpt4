import telebot
import os
from gpt import gpt
from textblob import TextBlob
import spacy

# تحميل نموذج اللغة الإنجليزية في spacy
nlp = spacy.load("en_core_web_sm")

# الحصول على توكن البوت من المتغير البيئي
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("لم يتم تعيين متغير البيئة 'TOKEN'.")

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

def correct_spelling(text):
    """تصحيح الأخطاء الإملائية باستخدام TextBlob"""
    blob = TextBlob(text)
    return str(blob.correct())

def named_entity_recognition(text):
    """تحليل الكيان المسمى باستخدام spacy"""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

@bot.message_handler(content_types=['text'])
def gpt_message(message):
    try:
        # معالجة النص
        corrected_text = correct_spelling(message.text)
        entities = named_entity_recognition(corrected_text)
        
        # إرسال النص المعالج إلى دالة gpt واستلام الرد
        response = gpt(corrected_text)
        
        # بناء رسالة الرد
        response_message = f'<b>العقرب : {response}</b>'
        if entities:
            response_message += '\n\n<b>الكيانات المعرفة:</b>\n'
            response_message += '\n'.join([f'{text} ({label})' for text, label in entities])
        
        # إرسال الرد إلى المستخدم
        bot.send_message(message.chat.id, response_message, parse_mode='HTML')
    except Exception as e:
        # التعامل مع الأخطاء وإرسال رسالة تنبيهية
        bot.send_message(message.chat.id, f'حدث خطأ: {e}', parse_mode='HTML')

# بدء الاستماع للرسائل
bot.infinity_polling()
