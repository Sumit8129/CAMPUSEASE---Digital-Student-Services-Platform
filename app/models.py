from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    notices = db.relationship('Notice', backref='author', lazy=True)
    materials = db.relationship('StudyMaterial', backref='uploader', lazy=True)
    events = db.relationship('Event', backref='organizer', lazy=True)
    # NEW: Relationship linking users to opportunities they post
    opportunities = db.relationship('Opportunity', backref='poster', lazy=True)

    def __repr__(self):
        return f'<User {self.full_name} - {self.roll_number}>'

class Notice(db.Model):
    __tablename__ = 'notices'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class StudyMaterial(db.Model):
    __tablename__ = 'study_materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

# NEW: Opportunity Model
class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)       # e.g., Software Engineering Intern
    company = db.Column(db.String(100), nullable=False)     # e.g., Google / TCS
    opp_type = db.Column(db.String(50), nullable=False)     # Internship, Job, Hackathon, Competition
    stipend = db.Column(db.String(50), nullable=True)       # e.g., ₹25,000/month or Unpaid
    description = db.Column(db.Text, nullable=False)
    apply_url = db.Column(db.String(500), nullable=False)   # Application link
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Opportunity {self.title} at {self.company}>'