import pytgpt.phind

# إنشاء صف للتحكم في عملية الدردشة
class ChatBot:
    def __init__(self):
        self.bot = pytgpt.phind.PHIND()

    def gpt(self, message):
        # التحقق من أن المدخل هو نص
        if not isinstance(message, str):
            return "Error: Input must be a string."

        try:
            # إرسال الرسالة إلى البوت والحصول على الرد
            response = self.bot.chat(message)
            return response
        except Exception as e:
            # إدارة أي أخطاء قد تحدث أثناء الدردشة
            return f"An error occurred: {str(e)}"

# استخدام البوت
chatbot = ChatBot()

# مثال على إرسال رسالة واحدة
response = chatbot.gpt("مرحبًا، كيف حالك؟")
print(response)
