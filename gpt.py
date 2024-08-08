import pytgpt.phind

class ChatBot:
    def __init__(self):
        self.bot = pytgpt.phind.PHIND()

    def gpt(self, message):
        try:
            if isinstance(message, str):
                response = self.bot.chat(message)
                return response
            elif isinstance(message, list):
                responses = [self.bot.chat(msg) for msg in message]
                return responses
            else:
                return "Unsupported input type. Please provide a string or a list of strings."
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Usage
chatbot = ChatBot()

# Single message
response = chatbot.gpt("مرحبًا، كيف حالك؟")
print(response)

# Multiple messages
responses = chatbot.gpt(["ما هي أخبار الطقس اليوم؟", "هل يمكنك مساعدتي في البرمجة؟"])
for res in responses:
    print(res)
