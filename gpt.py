from transformers import GPT2LMHeadModel, GPT2Tokenizer

# تحميل النموذج والرمز البرمجي
model_name = "gpt2"  # يمكنك تغيير النموذج إلى "gpt2-medium", "gpt2-large", أو "gpt2-xl" إذا لزم الأمر
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def gpt(message: str) -> str:
    """
    إرسال رسالة إلى نموذج GPT واستلام الرد.

    :param message: الرسالة التي سيتم إرسالها إلى النموذج.
    :return: الرد من النموذج.
    """
    try:
        # ترميز الرسالة
        inputs = tokenizer.encode(message, return_tensors="pt")
        
        # الحصول على الرد
        outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
        
        # فك ترميز الرد
        reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return reply
    except Exception as e:
        # معالجة الأخطاء وإرجاع رسالة توضيحية
        return f"حدث خطأ: {e}"

# مثال لاستخدام الدالة
if __name__ == "__main__":
    user_message = "مرحباً، كيف حالك؟"
    print(gpt(user_message))
