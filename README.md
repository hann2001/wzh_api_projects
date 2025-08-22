# 我的API项目

包含了与四个不同平台API交互的代码。

## 如何运行

1.  确保你的电脑上安装了Python 3。
2.  克隆这个仓库到你的电脑上。
3.  安装所需的库：`pip install requests` 
4.  创建一个 `config.py` 文件，并按照以下格式填入你的API密钥：

    ```python
    api_key_1_silicon = "你的API密钥"
    api_key_2_deepseek = "你的API密钥"
    api_key_3_bailian = "你的API密钥"
    api_key_4_Google = "你的API密钥"
    ```
5.  运行对应的Python文件，例如：`1_silicon_api_demo.py`