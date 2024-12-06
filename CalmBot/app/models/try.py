import pandas as pd
import json
import random
import os
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import joblib
from datasets import load_dataset  

class ResponseModel:
    def __init__(self):
        self.conversation_history = {}
        self.session_counts = {}

   
        if os.path.exists("chatbot_model.pkl"):
            self.model = joblib.load("chatbot_model.pkl")
        else:
            print("Model not found. Please train the model first.")
            self.model = None

    def get_response(self, user_input, session_id):
        if session_id not in self.session_counts:
            self.session_counts[session_id] = 1
            self.conversation_history[session_id] = []
            return "Hi! I'm here to listen and support you. How are you feeling today?"

        self.session_counts[session_id] += 1

        if self.model:
            emotion = self._predict_emotion(user_input)
            response = self._generate_response_from_model(user_input, emotion)
        else:
            response = "I'm unable to process your request right now. Please try again later."
        
        
        self._log_interaction(session_id, user_input, emotion, response)
        return response

    def _predict_emotion(self, user_input):
        
        emotion = self.model.predict([user_input])[0]
        return emotion

    def _generate_response_from_model(self, user_input, emotion):
       
        response = self._get_empathetic_response(emotion)
        return response

    def _get_empathetic_response(self, emotion):
        
        emotion_responses = {
            'sentimental': "Was this a friend you were in love with, or just a best friend?",
            'anxiety': "I notice you're feeling anxious. What brought these feelings up?",
            'depression': "I hear how difficult things are. Would you like to talk about what's happening?",
            'anger': "I can hear your anger. What triggered these feelings?",
            'general': "I'm here to listen. Would you like to tell me more?"
        }

        return emotion_responses.get(emotion, "I'm here to listen. Would you like to tell me more?")

    def _log_interaction(self, session_id, user_input, emotion, response):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'user_input': user_input,
            'emotion': emotion,
            'response': response
        }
        
        log_file = f"app/logs/chat_log_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Create directory if not exists
        with open(log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

    def train_model(self):
      
        dataset = load_dataset("bdotloh/empathetic-dialogues-contexts")
        
      
        print(dataset['train'].column_names)  
        print(dataset['train'][0])  
        
     
        data = pd.DataFrame(dataset['train'])  


        data = data.drop(data.columns[0], axis=1) 

      
        if len(data.columns) == 2:  
            data.columns = ['situation', 'emotion']
        else:
            raise ValueError(f"Unexpected number of columns: {len(data.columns)}")

   
        X = data['situation']  
        y = data['emotion']   

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

   
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

   
        self.model.fit(X_train, y_train)

     
        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained with accuracy: {accuracy:.2f}")

        joblib.dump(self.model, "chatbot_model.pkl")

        print("Model has been trained and saved as chatbot_model.pkl.")


response_model = ResponseModel()


response_model.train_model()


session_id = "session_1"
user_input = "I remember going to see the fireworks with my best friend."
response = response_model.get_response(user_input, session_id)
print(f"Response: {response}")
