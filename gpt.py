import openai

# إعداد المفتاح السري من OpenAI
openai.api_key = 'sk-proj-9ws35TnrOp5sE1LzwyiMT3BlbkFJ18CUr5JPY08sUBzjkHv5'

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
