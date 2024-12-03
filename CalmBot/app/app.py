from flask import Flask, render_template, request, jsonify, session
import os
from app.models.response_model import ResponseModel
from flask import send_file
from PIL import Image
import io
from datetime import datetime
from .models.database import MoodEntry, db, UserActivity
from sqlalchemy import extract

app = Flask(__name__)
app.secret_key = os.urandom(24)

response_model = ResponseModel()

if not os.path.exists('logs'):
    os.makedirs('logs')


basedir = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, 'database')
if not os.path.exists(database_dir):
    os.makedirs(database_dir)

# Set the database URI to use the full path
database_path = os.path.join(database_dir, 'calmbot.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    print("Database created successfully at:", database_path)

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
        
        # if activity_type == 'breathing':
        #     return jsonify({'status': 'success', 'message': 'Breathing exercise completed'})
        # elif activity_type == 'mood':
        #     return jsonify({'status': 'success', 'message': 'Mood tracked'})
        # elif activity_type == 'gratitude':
        #     return jsonify({'status': 'success', 'message': 'Gratitude entry saved'})

        new_activity = UserActivity(
            session_id=session_id,
            activity_type=activity_type
        )
        db.session.add(new_activity)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': f'{activity_type} activity recorded'})  

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/api/activities/mood', methods=['POST'])
def track_mood():
    try:
        data = request.json
        print("Received mood data:", data)  # Debug print
        new_mood = MoodEntry(
            session_id=data['session_id'],
            mood=data['mood'],
            date=datetime.now().date(),
            notes=data.get('notes', '')
        )
        db.session.add(new_mood)
        db.session.commit()
        print("Mood saved successfully")  # Debug print
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error saving mood:", str(e))  # Debug print
        return jsonify({'error': str(e)}), 500

@app.route('/api/moods/<int:month>/<int:year>')
def get_moods(month, year):
    try:
        month_moods = MoodEntry.query.filter(
            extract('month', MoodEntry.date) == month,
            extract('year', MoodEntry.date) == year
        ).all()
        
        return jsonify({
            'moods': [{
                'date': entry.date.strftime('%Y-%m-%d'),
                'mood': entry.mood,
                'notes': entry.notes
            } for entry in month_moods]
        })
    except Exception as e:
        print("Error fetching moods:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    try:
        # Count activities for each type
        breathing_count = UserActivity.query.filter_by(activity_type='breathing').count()
        journal_count = UserActivity.query.filter_by(activity_type='gratitude').count()
        mood_count = UserActivity.query.filter_by(activity_type='mood').count()
        
        return jsonify({
            'breathing_exercises': breathing_count,
            'journal_entries': journal_count,
            'mood_checks': mood_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
