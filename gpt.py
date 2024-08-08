import pytgpt.phind

bot = pytgpt.phind.PHIND()

def gpt(message, language='en'):
    # تحقق من اللغة وأرسل الرسالة وفقًا لها
    if language == 'ar':
        # إذا كانت اللغة عربية
        return bot.chat(f'{message}', language='ar')
    else:
        # إذا كانت اللغة إنجليزية أو أي لغة أخرى
        return bot.chat(f'{message}', language='en')
