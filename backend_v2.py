import os
import base64
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Ensure the 'uploads' directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize OpenAI client (API key retrieved from Render Environment Variables)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# --- Utility Functions ---

def decode_image(base64_string):
    """
    Process image: Remove Base64 prefix to prepare for GPT-4o-mini
    """
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    return base64_string

def generate_ai_prompt():
    """
    Generate System Instruction: Define AI persona, task, and JSON output format
    """
    return """
    You are an expert tutor. Please analyze this learning screenshot:
    1. Identify the [Question Content] and the [Student's Answer] from the image.
    2. Determine if the student's answer is correct (pay attention to technical formulas).
    3. Provide a detailed explanation of why the answer is correct or incorrect.
    4. Categorize errors as either 'careless' (simple mistake) or 'concept' (misunderstanding of the topic).
    5. Final output must be strictly in JSON format with the following fields: 
       { "status": "Correct/Incorrect", "topic": "...", "correct": true/false, "error_type": "careless/concept", "explanation": "...", "recognized_content": "..." }
    Output raw JSON only. Do not include ```json markdown tags.
    """

def call_openai_api(image_data, prompt):
    """
    Core API Call: Use GPT-4o-mini for image recognition and analysis
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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
        max_tokens=1000,
    )
    return response.choices[0].message.content

def parse_ai_response(raw_text):
    """
    Result Parsing: Clean the AI text output and convert it into a JSON dictionary
    """
    try:
        # Remove markdown formatting if GPT includes it
        json_text = raw_text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_text)
    except Exception as e:
        return {
            "status": "Error",
            "explanation": f"Failed to parse AI response: {str(e)}",
            "correct": False,
            "topic": "Unknown"
        }

# --- Route Handlers ---

@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.json
        raw_image = data.get('image')
        img_type = data.get('type', 'question') 

        if not raw_image:
            return jsonify({"status": "Error", "explanation": "No image data received"})

        # --- 1. Save Image Logic ---
        if not os.path.exists(UPLOAD_FOLDER): 
            os.makedirs(UPLOAD_FOLDER)
            
        processed_image = decode_image(raw_image)
        file_path = os.path.join(UPLOAD_FOLDER, f"{img_type}.png")
        with open(file_path, "wb") as fh:
            fh.write(base64.b64decode(processed_image))

        # --- 2. AI Diagnosis ---
        instruction = generate_ai_prompt()
        ai_raw_output = call_openai_api(processed_image, instruction)
        ai_result = parse_ai_response(ai_raw_output)

        # --- 3. Save AI Result as JSON File ---
        # This allows app.py to display the analysis by reading the file
        json_file_path = os.path.join(UPLOAD_FOLDER, f"{img_type}.json")
        with open(json_file_path, "w", encoding='utf-8') as f:
            json.dump(ai_result, f, ensure_ascii=False, indent=4)

        return jsonify(ai_result)
    
    except Exception as e:
        return jsonify({"status": "Error", "explanation": f"Internal Server Error: {str(e)}"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded images and JSON files
    """
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    # Bind to PORT provided by Render environment, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
