import requests
import json
from config import api_key_4_Google

model = "gemini-2.0-flash"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key_4_Google}"
headers = {"Content-Type": "application/json"}
prompt = "用一句话介绍一下python？"

payload = {
    "contents": [
        {"role": "user", "parts": [{"text": prompt}]}
    ]
}

response = requests.post(url, headers = headers, json = payload)

if response.status_code == 200:
    data = response.json()
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        print("GEMINI的回复：", text)
    except (KeyError, IndexError):
        print("没有找到模型生成的文本。")
else:
    print("请求失败，状态码：", response.status_code)
    print(response.text)
