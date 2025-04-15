import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app import db

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.Enum('NOTIFICATIONS', 'PRIVACY', 'APPEARANCE', name='preference_category'), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(JSONB)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('UserProfile', back_populates='preferences')
    
    # Unique constraint to ensure one value per key/category per user
    __table_args__ = (db.UniqueConstraint('user_id', 'category', 'key', name='unique_user_preference'),)
    
    def to_dict(self):
        """Convert the user preference to a dictionary for API responses"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'category': self.category,
            'key': self.key,
            'value': self.value,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<UserPreference {self.category}.{self.key}>'