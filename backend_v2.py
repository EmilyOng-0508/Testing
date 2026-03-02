import os
import base64
import json
from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS
from openai import OpenAI  # 导入 OpenAI 库

app = Flask(__name__)
CORS(app)

# [cite_start]确保 uploads 文件夹存在 [cite: 1]
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 这样写，代码会自动寻找你在 Render 后台填入的那个 Value
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# --- 独立函数部分 ---

def decode_image(base64_string):
    """
    处理图片：去除 Base64 前缀，准备发送给 GPT-4o
    """
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    return base64_string

def generate_ai_prompt():
    """
    生成指令：定义 AI 角色、诊断任务和 JSON 格式要求
    """
    return """
    你是一位老师。请分析这张学习截图：
    1. 识别图片中的【题目内容】和【学生的答案】。
    2. 判断学生答题是否正确（注意专业公式）。
    3. 给出详细的解释，说明为什么对或为什么错。
    4. 将错误分类为 'careless' (粗心) 或 'concept' (概念不清)。
    5. 最后严格以 JSON 格式输出，包含以下字段: 
       { "status": "Correct/Incorrect", "topic": "...", "correct": true/false, "error_type": "careless/concept", "explanation": "...", "recognized_content": "..." }
    请直接输出 JSON，不要有 ```json 这种 Markdown 标记。
    """

def call_openai_api(image_data, prompt):
    """
    核心调用：运用你的 API Credit 调用 GPT-4o-mini 进行图文识别
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini", # 性能强且节省 Credit
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        },
                    },
                ],
            }
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content

def parse_ai_response(raw_text):
    """
    结果解析：清理 AI 返回的文本并转化为 JSON 字典
    """
    try:
        # 有时 GPT 会自带 Markdown 格式，我们需要清理掉以便 json.loads 运行
        json_text = raw_text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_text)
    except Exception as e:
        return {
            "status": "Error",
            "explanation": f"AI 回复解析失败: {str(e)}",
            "correct": False,
            "topic": "Unknown"
        }

# --- 路由入口 (主流程) ---

@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.json
        raw_image = data.get('image')
        img_type = data.get('type', 'question') 

        if not raw_image:
            return jsonify({"status": "Error", "explanation": "未接收到图片数据"})

        # --- 1. 保存图片逻辑 ---
        if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
        processed_image = decode_image(raw_image)
        file_path = os.path.join(UPLOAD_FOLDER, f"{img_type}.png")
        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(processed_image))

        # --- 2. 调用 AI 诊断 ---
        instruction = generate_ai_prompt()
        ai_raw_output = call_openai_api(processed_image, instruction)
        ai_result = parse_ai_response(ai_raw_output)

        # --- 3. 【新增】保存 AI 结果为 JSON 文件 ---
        # 这样 app.py 就可以通过读取文件来显示文字了
        json_file_path = os.path.join(UPLOAD_FOLDER, f"{img_type}.json")
        with open(json_file_path, "w", encoding='utf-8') as f:
            json.dump(ai_result, f, ensure_ascii=False, indent=4)

        return jsonify(ai_result)
    
    except Exception as e:
        return jsonify({"status": "Error", "explanation": f"服务器内部错误: {str(e)}"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
