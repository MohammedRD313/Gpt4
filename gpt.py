import pytgpt.phind
import gpt
# إنشاء مثيل من بوت PHIND
bot = pytgpt.phind.PHIND()

class EnhancedGPT:
    def __init__(self, bot):
        self.bot = bot
        self.context = []

    def add_to_context(self, message):
        """إضافة الرسالة إلى السياق."""
        self.context.append(message)
        if len(self.context) > 10:  # حصر عدد الرسائل المخزنة في السياق
            self.context.pop(0)

    def generate_prompt(self, message):
        """توليد المحفز باستخدام السياق."""
        context_str = "\n".join(self.context)
        return f"Context:\n{context_str}\nUser: {message}"

    def gpt(self, message):
        try:
            cleaned_message = message.strip()
            self.add_to_context(f"User: {cleaned_message}")
            
            prompt = self.generate_prompt(cleaned_message)
            response = self.bot.chat(prompt)

            if response:
                self.add_to_context(f"Bot: {response}")
                return response
            else:
                return "No response received from the service."

        except Exception as e:
            return f"An error occurred: {str(e)}"

    def clear_context(self):
        """تفريغ السياق إذا لزم الأمر."""
        self.context = []

# مثال على كيفية استخدام الكود المحسن
if __name__ == "__main__":
    gpt_instance = EnhancedGPT(bot)
    
    # اختبار السؤال الأول
    test_message1 = "What's the weather like today?"
    print(gpt_instance.gpt(test_message1))
    
    # اختبار سؤال آخر مع الحفاظ على السياق
    test_message2 = "How about tomorrow?"
    print(gpt_instance.gpt(test_message2))
    
    # تفريغ السياق إذا لزم الأمر
    gpt_instance.clear_context()
