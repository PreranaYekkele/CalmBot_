import numpy as np
from flask import Flask, render_template, request, jsonify, session
from transformers import pipeline
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# Initialize the conversational pipeline
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Create a directory for chat logs if it doesn't exist
if not os.path.exists('chat_logs'):
    os.makedirs('chat_logs')

# Emergency resources
emergency_resources = {
    'hotlines': [
        {'name': 'National Crisis Hotline', 'number': '9999 666 555'},
        {'name': 'NAMI Helpline', 'number': '1800-599-0019'},
    ],
    'websites': [
        {'name': 'NAMI', 'url': 'https://www.nami.org'},
    ]
}

# Enhanced responses with categories
responses = {
    'POSITIVE': [
        "I'm glad you're feeling positive! What's making you feel good today?",
        "That's wonderful to hear! Would you like to talk more about it?",
        "Your positive energy is inspiring! How can we maintain this feeling?",
        "It's great that you're in a good mood! What activities have been helping you?",
    ],
    'NEGATIVE': [
        "I hear that you're going through a difficult time. Would you like to talk about it?",
        "It's okay to not feel okay. Remember that you're not alone in this.",
        "I'm here to listen. What's troubling you the most right now?",
        "Would you like to explore some coping strategies together?",
    ],
    'CRISIS': [
        "I'm very concerned about what you're sharing. Would you like information about crisis resources?",
        "Your safety is important. I can provide you with contact information for immediate support.",
        "You don't have to face this alone. There are professionals available 24/7 to help.",
    ],
    'MEDITATION': [
        "Let's try a quick breathing exercise. Take a deep breath in for 4 counts, hold for 4, and release for 4.",
        "Would you like to try a brief guided meditation together?",
        "Sometimes grounding exercises can help. Can you name 5 things you can see right now?",
    ],
    'GREETING': [
        "Hello! How are you feeling today?",
        "Welcome back! How has your day been?",
        "Hi there! I'm here to listen and support you.",
    ]
}

# Crisis keywords that trigger emergency responses
crisis_keywords = ['suicide', 'kill myself', 'want to die', 'end it all', 'harmful', 'hurt myself']

def detect_crisis(message):
    return any(keyword in message.lower() for keyword in crisis_keywords)

def get_response(user_input):
    # Check for crisis keywords first
    if detect_crisis(user_input):
        return {
            'message': np.random.choice(responses['CRISIS']),
            'type': 'crisis',
            'resources': emergency_resources
        }
    
    # Check for greetings
    greeting_words = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    if any(word in user_input.lower() for word in greeting_words):
        return {
            'message': np.random.choice(responses['GREETING']),
            'type': 'greeting'
        }
    
    # Get sentiment for other messages
    result = classifier(user_input)[0]
    label = result['label']
    
    # Check for meditation/relaxation requests
    meditation_keywords = ['anxious', 'stress', 'overwhelmed', 'breathe', 'relax', 'calm']
    if any(word in user_input.lower() for word in meditation_keywords):
        return {
            'message': np.random.choice(responses['MEDITATION']),
            'type': 'meditation'
        }
    
    return {
        'message': np.random.choice(responses[label]),
        'type': 'normal'
    }

def save_chat_log(user_message, bot_response):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_entry = {
        'timestamp': timestamp,
        'user_message': user_message,
        'bot_response': bot_response
    }
    
    filename = f'chat_logs/chat_{datetime.now().strftime("%Y%m%d")}.json'
    
    try:
        with open(filename, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')
    except Exception as e:
        print(f"Error saving chat log: {e}")

@app.route('/')
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', emergency_resources=emergency_resources)

@app.route('/get_response', methods=['POST'])
def bot_response():
    user_message = request.json['message']
    response = get_response(user_message)
    
    # Save to session history
    if 'chat_history' not in session:
        session['chat_history'] = []
    session['chat_history'].append({
        'user': user_message,
        'bot': response['message']
    })
    session.modified = True
    
    # Save to file
    save_chat_log(user_message, response)
    
    return jsonify(response)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    session['chat_history'] = []
    return jsonify({'status': 'success'})

@app.route('/feedback', methods=['POST'])
def save_feedback():
    feedback_data = request.json
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        with open('chat_logs/feedback.json', 'a') as f:
            feedback_data['timestamp'] = timestamp
            json.dump(feedback_data, f)
            f.write('\n')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)