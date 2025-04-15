import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import db

class UserConnection(db.Model):
    __tablename__ = 'user_connections'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    requester_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    recipient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum('PENDING', 'ACCEPTED', 'REJECTED', name='connection_status'), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Prevent duplicate connections
    __table_args__ = (db.UniqueConstraint('requester_id', 'recipient_id', name='unique_connection'),)
    
    def to_dict(self):
        """Convert the user connection to a dictionary for API responses"""
        return {
            'id': str(self.id),
            'requester_id': str(self.requester_id),
            'recipient_id': str(self.recipient_id),
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<UserConnection {self.requester_id} -> {self.recipient_id} ({self.status})>'