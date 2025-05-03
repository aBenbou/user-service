from datetime import datetime
from app import db

class UserConnection(db.Model):
    __tablename__ = 'user_connections'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user_profiles.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # PENDING, ACCEPTED, REJECTED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    requester = db.relationship('UserProfile', foreign_keys=[requester_id], backref='outgoing_connections')
    recipient = db.relationship('UserProfile', foreign_keys=[recipient_id], backref='incoming_connections')
    
    def to_dict(self):
        """Convert the user connection to a dictionary for API responses"""
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'recipient_id': self.recipient_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<UserConnection {self.requester_id} -> {self.recipient_id} ({self.status})>'