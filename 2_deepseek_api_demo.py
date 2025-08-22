#报错没有余额！
#没有找到获取免费额度的地方

import requests
import json
from config import api_key_2_deepseek


url = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key_2_deepseek}"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "请用一句话介绍一下Python。"}
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        result = response_data['choices'][0]['message']['content']
        print("deepseek的回复：")
        print(result)

    else:
        print(f"请求失败！状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

except Exception as e:
    print ("发生未知错误:", e)