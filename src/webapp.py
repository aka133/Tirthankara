from flask import Flask, request, jsonify, render_template_string
import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv("Tirthankara/.env")

# Initialize the Flask app
app = Flask(__name__)

# HTML template for the main page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Tirthankara Image Generator</title>
    <!-- Google Fonts for the Buddhist/Asian style font -->
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&display=swap" rel="stylesheet">
    <style>
        /* Modern CSS reset */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* Custom properties for easy theme changes */
        :root {
            --gold: #D4AF37;
            --dark-bg: #0F1115;
            --text: #ffffff;
        }
        
        body {
            font-family: 'Cormorant Garamond', serif;
            background: radial-gradient(circle at center, #1a1f2c 0%, var(--dark-bg) 100%);
            background-attachment: fixed;
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            position: relative;
            overflow-x: hidden;
        }
        
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 20%, rgba(212, 175, 55, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(212, 175, 55, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: 1;
        }
        
        .container {
            max-width: 800px;
            width: 100%;
            text-align: center;
            position: relative;
            z-index: 2;
        }
        
        h1 {
            font-family: 'Cinzel Decorative', cursive;
            color: var(--gold);
            font-size: 3.2em;
            margin-bottom: 50px;
            text-shadow: 0 0 20px rgba(212, 175, 55, 0.3);
            letter-spacing: 3px;
        }
        
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            width: 100%;
        }
        
        input[type="text"] {
            width: 90%;
            max-width: 600px;
            padding: 20px 30px;
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 30px;
            background: rgba(15, 17, 21, 0.7);
            color: var(--text);
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.3em;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.6);
            font-style: italic;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: var(--gold);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
            background: rgba(15, 17, 21, 0.9);
        }
        
        input[type="submit"] {
            padding: 15px 40px;
            border: 2px solid var(--gold);
            border-radius: 30px;
            background: transparent;
            color: var(--gold);
            font-family: 'Cormorant Garamond', serif;
            font-size: 1.2em;
            font-weight: 600;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }
        
        input[type="submit"]:hover {
            background: var(--gold);
            color: var(--dark-bg);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
        }
        
        .result-container {
            margin-top: 50px;
            width: 100%;
        }
        
        .generated-image {
            max-width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease;
            border: 1px solid rgba(212, 175, 55, 0.2);
        }
        
        .generated-image:hover {
            transform: scale(1.02);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease forwards;
        }
        
        .error {
            color: #ff6b6b;
            margin-top: 20px;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="fade-in">Tirthankara</h1>
        <form action="/generate" method="POST" class="fade-in">
            <input type="text" name="prompt" placeholder="Describe your vision..." required>
            <input type="submit" value="Generate">
        </form>
        {% if image_data %}
        <div class="result-container fade-in">
            <img class="generated-image" src="{{ image_data }}" alt="Generated image">
        </div>
        {% endif %}
        {% if error %}
        <div class="error fade-in">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

# Get the Stability API key from the environment variable
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')
STABILITY_API_HOST = "https://api.stability.ai"
STABILITY_API_PATH = "/v2beta/stable-image/generate/core"

@app.route('/', methods=['GET'])
def hello():
    """
    Display the main page with the image generation form.
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_image():
    """
    Endpoint to handle image generation requests.
    Now accepts both JSON and form data.
    """
    # Get the prompt from either JSON or form data
    if request.is_json:
        data = request.get_json()
        prompt = data.get('prompt') if data else None
    else:
        prompt = request.form.get('prompt')

    # Check if we received a prompt
    if not prompt:
        return jsonify({
            'error': 'No prompt provided',
            'status': 'error'
        }), 400

    # Prepare the request to Stability API
    url = f"{STABILITY_API_HOST}{STABILITY_API_PATH}"

    # Send the request to Stability API
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*"
            },
            files={"none": ""},
            data={
                "prompt": f"A retrofuturistic representation of {prompt}",
                "output_format": "png"
            }
        )

        if response.status_code == 200:
            # Convert binary image data to base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            image_data = f"data:image/png;base64,{image_base64}"
            
            # If the request came from a browser (form submission)
            if not request.is_json:
                return render_template_string(HTML_TEMPLATE, image_data=image_data)
            
            # If it's an API request
            return jsonify({
                "status": "success",
                "image_data": image_data
            }), 200
        else:
            error_message = f"Stability API error: {response.text}"
            if not request.is_json:
                return render_template_string(HTML_TEMPLATE, error=error_message)
            return jsonify({
                "error": error_message,
                "status": "error"
            }), response.status_code
    except Exception as e:
        error_message = str(e)
        if not request.is_json:
            return render_template_string(HTML_TEMPLATE, error=error_message)
        return jsonify({
            "error": error_message,
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)