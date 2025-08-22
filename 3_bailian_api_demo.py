import requests
import json
from config import api_key_3_bailian

url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"


headers = {
    "Authorization": f"Bearer {api_key_3_bailian}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen-plus",  #千问模型
    "stream": False,         #一次性返回结果
    "messages": [
        {
            "role": "user",
            "content": "请用一句话介绍一下python。"
        }
    ]
}

try:
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        result = response_data['choices'][0]['message']['content']
        print("千问的回复：")
        print(result)

    else:
        print(f"请求失败！状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

except Exception as e:
    print ("发生未知错误:", e)