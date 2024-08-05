from transformers import AutoModelForCausalLM, AutoTokenizer

# تحميل النموذج والمحول
model_name = "EleutherAI/gpt-j-6B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def gpt(message):
    # ترميز الرسالة
    inputs = tokenizer.encode(message, return_tensors='pt')

    # توليد الاستجابة
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1)

    # فك ترميز الاستجابة
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

# اختبار الدالة
if __name__ == "__main__":
    user_message = "Hello, how are you?"
    response = gpt(user_message)
    print("Response:", response)
