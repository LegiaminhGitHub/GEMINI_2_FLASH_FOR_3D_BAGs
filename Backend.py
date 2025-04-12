from flask import Flask, request, jsonify
from flask_cors import CORS  
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os  

app = Flask(__name__)
CORS(app) 


client = genai.Client(api_key="Chỗ này để google AI key nha")

@app.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                return jsonify({'text': part.text})
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                return jsonify({'image_data': img_str})

        return jsonify({'error': 'No image or text in the response'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)