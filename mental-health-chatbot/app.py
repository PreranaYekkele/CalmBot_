from flask import Flask, render_template, request, jsonify, session
import random
from datetime import datetime
import json
import os
from response_model import ResponseModel

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize response model
response_model = ResponseModel()

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

class ActivityLogger:
    def __init__(self):
        self.activities = {}
    
    def log_activity(self, session_id, activity_type, data=None):
        if session_id not in self.activities:
            self.activities[session_id] = []
        
        self.activities[session_id].append({
            'type': activity_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
        
        self._save_to_file(session_id, activity_type, data)
    
    def _save_to_file(self, session_id, activity_type, data):
        log_entry = {
            'session_id': session_id,
            'type': activity_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"logs/activity_log_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

# Initialize activity logger
activity_logger = ActivityLogger()

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data['message']
        session_id = data['session_id']
        
        # Get response from model
        response = response_model.get_response(user_message, session_id)
        
        # Log the interaction
        activity_logger.log_activity(
            session_id, 
            'chat',
            {
                'user_message': user_message,
                'bot_response': response
            }
        )
        
        return jsonify({
            'response': response,
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred processing your message',
            'message': 'I apologize, but I had trouble understanding that. Could you rephrase?'
        }), 500

@app.route('/api/activities/breathing', methods=['POST'])
def handle_breathing():
    """Handle breathing exercise interactions"""
    try:
        data = request.json
        session_id = data['session_id']
        action = data.get('action', 'complete')
        
        activity_logger.log_activity(session_id, 'breathing_exercise', {'action': action})
        
        responses = {
            'start': "Let's begin. Focus on the circle - breathe in as it expands, out as it contracts.",
            'complete': "How are you feeling now? Remember, you can return to this breathing exercise anytime.",
            'end': "Well done. Taking time to breathe mindfully can really help. Would you like to share how you're feeling?"
        }
        
        return jsonify({
            'status': 'success',
            'message': responses.get(action, responses['complete'])
        })
        
    except Exception as e:
        print(f"Error in breathing endpoint: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error processing breathing exercise'}), 500

@app.route('/api/activities/mood', methods=['POST'])
def handle_mood():
    """Handle mood tracking"""
    try:
        data = request.json
        session_id = data['session_id']
        mood = data.get('mood', '')
        
        activity_logger.log_activity(session_id, 'mood_tracker', {'mood': mood})
        
        # Get personalized response based on emotion
        emotion = mood.split()[1].lower() if len(mood.split()) > 1 else 'neutral'
        response = response_model._get_personalized_suggestion(emotion, session_id)
        
        return jsonify({
            'status': 'success',
            'message': response or "Thank you for sharing how you're feeling. Would you like to talk about it?"
        })
        
    except Exception as e:
        print(f"Error in mood endpoint: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error tracking mood'}), 500

@app.route('/api/activities/gratitude', methods=['POST'])
def handle_gratitude():
    """Handle gratitude journal entries"""
    try:
        data = request.json
        session_id = data['session_id']
        entry = data.get('entry', '')
        
        activity_logger.log_activity(session_id, 'gratitude_journal', {'entry': entry})
        
        # Save context with positive emotion
        response_model.save_context(session_id, entry, 'gratitude', 'gratitude_journal_entry')
        
        return jsonify({
            'status': 'success',
            'message': "Thank you for sharing what you're grateful for. Acknowledging these positive aspects can really help our mental well-being. Would you like to explore these feelings further?"
        })
        
    except Exception as e:
        print(f"Error in gratitude endpoint: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error saving gratitude entry'}), 500

@app.route('/api/professional-resources', methods=['GET'])
def get_professional_resources():
    """Get professional mental health resources"""
    try:
        emotion = request.args.get('emotion', None)
        resources = response_model.get_professional_resources(emotion)
        return jsonify({
            'status': 'success',
            'resources': resources
        })
    except Exception as e:
        print(f"Error in professional resources endpoint: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error retrieving resources'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'status': 'error',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'An internal server error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True)