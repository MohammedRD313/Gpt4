import openai
import os

# الحصول على مفتاح API من المتغير البيئي
openai.api_key = os.getenv('API_KEY')

def gpt(message: str) -> str:
    """
    إرسال رسالة إلى نموذج GPT واستلام الرد.

    :param message: الرسالة التي سيتم إرسالها إلى النموذج.
    :return: الرد من النموذج.
    """
    try:
        # التحقق من أن الرسالة ليست فارغة
        if not message.strip():
            raise ValueError("الرسالة لا يمكن أن تكون فارغة.")

        # إرسال الرسالة إلى نموذج GPT واستلام الرد
        response = openai.ChatCompletion.create(
            model="claude-3-opus-20240229",  # استخدم النموذج الذي تفضله
            messages=[
                {"role": "user", "content": message}
            ]
        )

        # استخراج الرد من الاستجابة
        reply = response.choices[0].message['content'].strip()

        # التحقق من أن الرد ليس فارغًا
        if not reply:
            raise ValueError("الرد من النموذج كان فارغًا.")

        return reply
    except Exception as e:
        # معالجة الأخطاء وإرجاع رسالة توضيحية
        return f"حدث خطأ: {e}"

# مثال لاستخدام الدالة
if __name__ == "__main__":
    user_message = "مرحباً، كيف حالك؟"
    print(gpt(user_message))
