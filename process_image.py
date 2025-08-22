import os
import cv2
import json
import requests
import base64
import re
from PIL import Image, ImageDraw
from config import api_key


#批量读取图片并缩放大小
def resize_images(input_dir, output_dir, size=(640, 480)):
    #批量缩放图片并保存
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            with Image.open(img_path) as img:
                img_resized = img.resize(size)
                #保存为JPG格式
                if not filename.lower().endswith('.jpg'):
                    filename = os.path.splitext(filename)[0] + '.jpg'
                img_resized.save(os.path.join(output_dir, filename), 'JPEG')
                print(f"已缩放: {filename}")


#在指定位置画矩形框
def draw_box(image_path, output_path, box, color='red', width=3):
    #在图片上绘制矩形框
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline=color, width=width)
    img.save(output_path)
    print(f"已绘制框: {output_path}")


#调用阿里云百炼调用千问VL模型
def call_qwen_vl(api_key, image_path, prompt):
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    #读取图片转换为Base64
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    #请求体
    payload = {
        "model": "qwen-vl-plus",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"image": f"data:image/jpeg;base64,{image_data}"},
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "result_format": "text"
        }
    }

    #发送请求
    response = requests.post(url, headers=headers, json=payload)
    print(f"API响应状态码: {response.status_code}")
    return response.json()


#解析模型响应并提取坐标
def parse_response(response):
    try:
        print(f"完整响应: {json.dumps(response, indent=2, ensure_ascii=False)}")
        #检查响应是否包含错误
        if 'code' in response and response['code'] != 200:
            print(f"API返回错误: {response.get('message', '未知错误')}")
            return None

        #尝试从响应中提取内容
        if 'output' in response and 'choices' in response['output']:
            #获取content列表
            content_list = response['output']['choices'][0]['message']['content']

            #提取文本内容
            text_content = ""
            for item in content_list:
                if 'text' in item:
                    text_content += item['text']

            print(f"模型返回内容: {text_content}")

            #提取JSON部分
            json_match = re.search(r'\{.*\}', text_content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                print(f"提取的JSON字符串: {json_str}")

                #解析JSON
                result = json.loads(json_str)

                if result['result'] == 'yes':
                    return result['bounding_boxes']
                else:
                    return None
            else:
                print("响应中未找到JSON格式的结果")
                return None
        else:
            print("响应格式不符合预期")
            return None
    except Exception as e:
        print(f"解析响应时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


#主函数
def main():

    input_directory = "input_images"
    resized_dir = "resized_images"
    output_dir = "output_images"

    for dir_path in [resized_dir, output_dir]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    #提示词
    prompt = """Role: You are an intelligent assistant capable of accurately identifying debris on the road surface;
Definition: Road debris refers to foreign objects that do not belong but appear on the road surface, such as rocks, construction materials, large patches of sand, soil, household waste, plastic bags, cardboard boxes, branches, and leaves;
Task: Analyze this image and determine if there is any debris within the road area. Focus on identifying debris rather than vehicles, pedestrians, guardrails, utility poles, road cones, etc.
Output: If debris is identified, only return the result in JSON without Markdown: {"result": "yes", "bounding_boxes": [[xmin, ymin, xmax, ymax], ...]}; otherwise, return: {"result": "no"}."""

    #批量缩放图片
    print("步骤1: 批量缩放图片")
    resize_images(input_directory, resized_dir)

    #在指定位置画矩形框 (示例)
    print("\n步骤2: 在图片上绘制矩形框")
    #获取第一张图片
    image_files = [f for f in os.listdir(resized_dir) if f.lower().endswith('.jpg')]

    if image_files:
        sample_image = image_files[0]
        img_path = os.path.join(resized_dir, sample_image)
        output_path = os.path.join(output_dir, f"manual_box_{sample_image}")
        # 示例框坐标 [xmin, ymin, xmax, ymax]
        example_box = [100, 100, 300, 300]
        draw_box(img_path, output_path, example_box)

    #使用AI模型处理图片
    print("\n步骤3: 使用AI模型处理图片")
    if image_files:
        sample_image = image_files[0]
        img_path = os.path.join(resized_dir, sample_image)

        #调用API
        print("调用千问VL模型")
        try:
            response = call_qwen_vl(api_key, img_path, prompt)

            #解析响应
            boxes = parse_response(response)

            if boxes:
                print(f"检测到 {len(boxes)} 个目标")
                #使用OpenCV读取图片
                img_cv = cv2.imread(img_path)

                #绘制每个检测框
                for box in boxes:
                    xmin, ymin, xmax, ymax = box
                    cv2.rectangle(img_cv, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                #保存结果
                output_path = os.path.join(output_dir, f"ai_detected_{sample_image}")
                cv2.imwrite(output_path, img_cv)
                print(f"结果已保存: {output_path}")
            else:
                print("未检测到目标")
        except Exception as e:
            print(f"调用API时出错: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()