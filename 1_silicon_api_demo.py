import requests
import json
from config import api_key_1_silicon

api_url = "https://api.siliconflow.cn/v1/chat/completions"


#请求头
headers = {
    "Authorization": f"Bearer {api_key_1_silicon}",  # 使用 Bearer Token 认证授权信息，Bearer后面有一个空格
    "Content-Type": "application/json"     # 指明请求体是JSON格式
}

#字典定义信息和参数
data = {
    "model": "deepseek-ai/DeepSeek-R1",
    "messages": [
        {
            "role": "user",
            "content": "请用一句话介绍一下python。"
        }
    ]
}

try:
    #json: requests库会自动将其转换为JSON字符串
    response = requests.post(url=api_url, headers=headers, json=data)

    #状态不对会抛出异常
    response.raise_for_status()

    #解析返回的JSON响应
    #response.json()将API返回的JSON数据转换为python字典
    response_data = response.json()

    #响应结构
    result = response_data['choices'][0]['message']['content']
    print("DeepSeek-R1模型的回复：")
    print(result)

# 异常处理
except Exception as e:
    #捕捉未知异常
    print ("发生未知错误:", e)