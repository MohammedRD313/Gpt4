import pytgpt.phind
import re

bot = pytgpt.phind.PHIND()

def is_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def gpt(message):
    if is_english(message) or is_arabic(message):
        return bot.chat(f'{message}')
    else:
        return "الرسالة يجب أن تكون باللغة الإنجليزية أو العربية فقط."
