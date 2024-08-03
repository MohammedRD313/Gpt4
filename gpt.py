import openai
import os

# تأكد من أنك قد أضفت مفتاح API الخاص بك كمتغير بيئي
openai.api_key = os.getenv("API_KEY")

if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# استدعاء نموذج GPT-4o mini
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",  # استخدم النموذج المطلوب
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "مرحبًا، كيف حالك؟"}
    ]
)

# طباعة الرد
print(response['choices'][0]['message']['content'])
