# In app/models/database.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # 'breathing', 'journal', 'mood'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
