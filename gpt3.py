import requests, os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class gpt3:
    PROMPT = 'You are GPTFree, a friendly assistant. You are communicating through the Telegram app and your username is @GPTFree_pBot. Be helpful and concise. You do not need to include the current date and time in every message, only when the User asks for it. GPTFree is conversational, You do not need to mention (e.g. hello, @GPTFree_pBot) a user when responding unless there are multiple users in the conversation; if you must use the users name, refer to them by their first name (hello, GPTFree). If in a one-on-one conversation, there is no need to mention their name in every reply. GPTFree can assist with programming, but will only output code when asked to.'
    
    def gpt3(prompt: str) -> str:
        response = requests.post(
            "https://dashboard.scale.com/spellbook/api/app/kw1n3er6", 
            json={
                "input": prompt
            },
            headers={"Authorization":f"Basic {os.getenv('SCALE')}"} 
        )
        try:
            return response.json()['text']
        except Exception as e:
            print("gpt3 err:", e)
            return '<system> error getting openai response. try again, or try using /start if your chat may be too long'
    
    async def alt_gpt3(prompt: str) -> str:
        res = await requests.post('https://plutoniumserver.onrender.com/', json={
            'prompt': prompt
        }, headers={
            'Content-Type': 'application/json'
        }).json()
        return res['bot']

    def openai(prompt, messages: list, base_inst: str = PROMPT) -> str:
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages = [{'role': 'system', 'content': base_inst}, *messages[-49:], {'role': 'user', 'content': prompt}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            print("openai err:", e)
            try:
                return gpt3.sharegpt(prompt, messages, base_inst=base_inst)
            except:
                pass
            #return "<dev> Hi, @warcusj here, my OpenAI account has reached it's billing limit. Since I have failed to generate revenue from this project, I don't think I will be refilling it. I've spent over $11 USD so far, and with 4k+ users, I don't see any way I can maintain this."
            return "<system> error getting openai response. try /start to clear your current chat, or join the group for support: https://t.me/+UGYh8W0AcWRhZDA0"

    def sharegpt(prompt, messages: list, base_inst: str = PROMPT) -> str:
        response = requests.post(
            os.getenv('SHAREGPT_URL'),
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'system', 'content': base_inst}, *messages[-29:], {'role': 'user', 'content': prompt}]
            }
        )
        return response.json()['choices'][0]['message']['content']