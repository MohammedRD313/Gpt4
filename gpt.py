from transformers import GPT2LMHeadModel, GPT2Tokenizer

# تحميل النموذج والمحول
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

def gpt(message):
    # ترميز الرسالة
    inputs = tokenizer.encode(message, return_tensors='pt')

    # توليد الاستجابة
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)

    # فك ترميز الاستجابة
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

# اختبار الدالة
if __name__ == "__main__":
    user_message = "Hello, how are you?"
    response = gpt(user_message)
    print("Response:", response)
