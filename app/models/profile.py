from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    # Use Integer for SQLite, UUID for PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(80), unique=True, nullable=False)
    biography = db.Column(db.Text)
    profession = db.Column(db.String(100))
    company = db.Column(db.String(100))
    current_job = db.Column(db.String(100))
    visibility = db.Column(db.String(20), default='PUBLIC')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    expertise_areas = db.relationship('ExpertiseArea', backref='profile', lazy=True)
    preferences = db.relationship('UserPreference', backref='profile', lazy=True)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'biography': self.biography,
            'profession': self.profession,
            'company': self.company,
            'current_job': self.current_job,
            'visibility': self.visibility,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }