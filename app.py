from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import sqlite3
from greeting_generator import GreetingGenerator

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

# Database initialization
def init_db():
    conn = sqlite3.connect('greetings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS greetings
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         recipient TEXT NOT NULL,
         greeting TEXT NOT NULL,
         couplet TEXT NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

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
        
        # Save to database
        conn = sqlite3.connect('greetings.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO greetings (recipient, greeting, couplet)
            VALUES (?, ?, ?)
        ''', (recipient, greeting, f"{horizontal}|{upper}|{lower}"))
        conn.commit()
        conn.close()
        
        return jsonify({
            'greeting': greeting,
            'couplet': {
                'horizontal': horizontal,
                'upper': upper,
                'lower': lower
            },
            'image': image_base64
        })
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        conn = sqlite3.connect('greetings.db')
        c = conn.cursor()
        c.execute('SELECT * FROM greetings ORDER BY timestamp DESC LIMIT 10')
        history = c.fetchall()
        conn.close()
        
        return jsonify([{
            'id': h[0],
            'recipient': h[1],
            'greeting': h[2],
            'couplet': h[3],
            'timestamp': h[4]
        } for h in history])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 