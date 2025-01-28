from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from greeting_generator import GreetingGenerator
import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure OpenAI
generator = GreetingGenerator(os.getenv('OPENAI_API_KEY'))

# Configure rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per hour"],
    storage_uri="memory://"
)

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per hour")
def generate_greeting():
    data = request.get_json()
    recipient = data.get('recipient')
    extra_requirements = data.get('requirements', '')
    
    if not recipient:
        return jsonify({'error': 'Recipient name is required'}), 400
    
    try:
        # Generate greeting
        greeting = generator.generate_greeting(recipient, extra_requirements)
        
        # Generate couplet
        horizontal, upper, lower = generator.generate_couplet(recipient)
        
        # Generate couplet image
        image_base64 = generator.generate_couplet_image(horizontal, upper, lower)
        
        return jsonify({
            'greeting': greeting,
            'couplet': {
                'horizontal': horizontal,
                'upper': upper,
                'lower': lower
            },
            'image': image_base64,
            'timestamp': str(datetime.datetime.now())
        })
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000) 