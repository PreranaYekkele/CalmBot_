from flask import Flask, render_template, request, jsonify, session
import os
from app.models.response_model import ResponseModel
from flask import send_file
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = os.urandom(24)

response_model = ResponseModel()

if not os.path.exists('logs'):
    os.makedirs('logs')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        response = response_model.get_response(data['message'], data['session_id'])
        return jsonify({'response': response, 'session_id': data['session_id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/activities/<activity_type>', methods=['POST'])
def handle_activity(activity_type):
    try:
        data = request.json
        session_id = data['session_id']
        
        if activity_type == 'breathing':
            return jsonify({'status': 'success', 'message': 'Breathing exercise completed'})
        elif activity_type == 'mood':
            return jsonify({'status': 'success', 'message': 'Mood tracked'})
        elif activity_type == 'gratitude':
            return jsonify({'status': 'success', 'message': 'Gratitude entry saved'})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    # In a real application, you would fetch this from your database
    # This is just sample data
    return jsonify({
        'breathing_exercises': 15,
        'journal_entries': 8,
        'mood_checks': 23
    })

@app.route('/api/log-specialist-selection', methods=['POST'])
def log_specialist_selection():
    data = request.json
    # In a real application, you would save this to your database
    # For now, we'll just log it
    print(f"Specialist selected: {data}")
    return jsonify({'status': 'success'})

@app.route('/api/placeholder/<int:width>/<int:height>')
def placeholder_image(width, height):
    # Create a simple placeholder image
    img = Image.new('RGB', (width, height), color = 'lightgray')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)