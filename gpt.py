import pytgpt.phind

# إنشاء مثيل من بوت PHIND
bot = pytgpt.phind.PHIND()

def gpt(message: str) -> str:
    """
    إرسال رسالة إلى بوت PHIND واستلام الرد.

    :param message: الرسالة التي سيتم إرسالها إلى البوت.
    :return: الرد من البوت.
    """
    try:
        # التحقق من أن الرسالة ليست فارغة
        if not message.strip():
            raise ValueError("الرسالة لا يمكن أن تكون فارغة.")
        
        # إرسال الرسالة واستلام الرد
        response = bot.chat(message)
        
        # التحقق من أن الرد ليس فارغًا
        if not response.strip():
            raise ValueError("الرد من البوت كان فارغًا.")
        
        return response
    except Exception as e:
        # معالجة الأخطاء وإرجاع رسالة توضيحية
        return f"حدث خطأ: {e}"

# مثال لاستخدام الدالة
if __name__ == "__main__":
    user_message = "مرحباً، كيف حالك؟"
    print(gpt(user_message))
