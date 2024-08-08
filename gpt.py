import pytgpt.phind

bot = pytgpt.phind.PHIND()

def gpt(message):
    if not message:
        return "Error: Empty message"
    response = bot.chat(f'{message}')
    if not response:
        return "Error: No response received"
    return response

# Example usage
user_message = "What is the capital of France?"
response = gpt(user_message)
print(response)
