from datetime import datetime
import re
import random
import json
import os

class ResponseModel:
    def __init__(self):
        self.conversation_history = {}
        self.session_counts = {}
        self.patterns = {
            'anxiety': {
                'patterns': [r'anxi(ous|ety)', r'worried?', r'stress(ed|ful)', r'nervous', r'panic'],
                'responses': [
                    "I notice you're feeling anxious. What brought these feelings up?",
                    "Anxiety can feel overwhelming. Would you like to explore what's causing these feelings?",
                    "When did you start feeling this anxiety? I'm here to listen.",
                    "It sounds like anxiety is really present for you. What would help you feel more grounded?"
                ]
            },
            'depression': {
                'patterns': [r'depress(ed|ion)', r'sad', r'down', r'hopeless', r'unmotivated'],
                'responses': [
                    "I hear how difficult things are. Would you like to talk about what's happening?",
                    "Depression can feel really heavy. How long have you been carrying this?",
                    "It takes courage to share these feelings. What support would be most helpful?",
                    "I hear the pain in your words. What would a moment of relief look like?"
                ]
            },
            'anger': {
                'patterns': [r'angry?', r'mad', r'frustrat(ed|ing)', r'irritat(ed|ing)', r'upset'],
                'responses': [
                    "I can hear your anger. What triggered these feelings?",
                    "It's okay to feel angry. Would you like to talk about what happened?",
                    "Anger often tells us something important. What do you think it's saying?",
                    "Your anger is valid. What would help you feel heard?"
                ]
            }
        }

    def get_response(self, user_input, session_id):
        if session_id not in self.session_counts:
            self.session_counts[session_id] = 1
            self.conversation_history[session_id] = []
            return "Hi! I'm here to listen and support you. How are you feeling today?"

        self.session_counts[session_id] += 1
        emotion = self._detect_emotion(user_input.lower())
        response = self._generate_response(emotion)
        
        self._log_interaction(session_id, user_input, emotion, response)
        return response

    def _detect_emotion(self, text):
        for emotion, data in self.patterns.items():
            for pattern in data['patterns']:
                if re.search(pattern, text):
                    return emotion
        return 'general'

    def _generate_response(self, emotion):
        responses = self.patterns.get(emotion, {
            'responses': ["I'm here to listen. Would you like to tell me more?"]
        })['responses']
        return random.choice(responses)

    def _log_interaction(self, session_id, user_input, emotion, response):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_input': user_input,
            'emotion': emotion,
            'response': response
        }
        
        log_file = f"app/logs/chat_log_{datetime.now().strftime('%Y%m%d')}.json"
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')