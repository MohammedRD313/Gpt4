import openai

# إعداد المفتاح السري من OpenAI
openai.api_key = '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'

class Bot:
    def chat(self, message):
        response = openai.Completion.create(
            engine="gpt-4",  # يمكنك تعديل هذا بناءً على النموذج الذي تريده
            prompt=message,
            max_tokens=150
        )
        return response.choices[0].text.strip()

bot = Bot()

def gpt(message):
    return bot.chat(message)
