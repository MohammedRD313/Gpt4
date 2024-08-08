import pytgpt.phind

# إنشاء مثيل من بوت PHIND
bot = pytgpt.phind.PHIND()

def gpt(message):
    try:
        # تنظيف الرسالة قبل الإرسال (يمكنك إضافة المزيد من المعالجة هنا)
        cleaned_message = message.strip()
        
        # إرسال الرسالة إلى خدمة PHIND واستلام الرد
        response = bot.chat(cleaned_message)
        
        # التحقق من صحة الاستجابة
        if response:
            return response
        else:
            return "No response received from the service."
    
    except Exception as e:
        # التعامل مع الأخطاء
        return f"An error occurred: {str(e)}"

# مثال على كيفية استخدام الدالة
if __name__ == "__main__":
    test_message = "What's the weather like today?"
    print(gpt(test_message))
