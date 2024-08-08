import pytgpt.phind
import requests
from bs4 import BeautifulSoup

bot = pytgpt.phind.PHIND()

def gpt(message):
    return bot.chat(f'{message}')

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for item in soup.find_all('h3'):
        results.append(item.get_text())

    return results

def main(message):
    if "بحث" in message:
        query = message.replace("بحث", "").strip()
        return search_web(query)
    else:
        return gpt(message)

# Example usage
print(main("بحث عن Python programming"))
