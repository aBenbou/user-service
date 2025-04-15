from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True)
    biography = db.Column(db.Text)
    profession = db.Column(db.String(100))
    company = db.Column(db.String(100))
    current_job = db.Column(db.String(100))
    github_username = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(255))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    visibility = db.Column(db.Enum('PUBLIC', 'PRIVATE', 'CONNECTIONS_ONLY', name='visibility_type'))
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    expertise_areas = db.relationship('ExpertiseArea', back_populates='user', cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', back_populates='user', cascade='all, delete-orphan')
    # These relationships need to account for both sides of the connection
    outgoing_connections = db.relationship('UserConnection', 
                                          foreign_keys='UserConnection.requester_id',
                                          backref=db.backref('requester', lazy='joined'),
                                          lazy='dynamic',
                                          cascade='all, delete-orphan')
    incoming_connections = db.relationship('UserConnection', 
                                          foreign_keys='UserConnection.recipient_id',
                                          backref=db.backref('recipient', lazy='joined'),
                                          lazy='dynamic',
                                          cascade='all, delete-orphan')
    
    def is_active(self):
        """Check if the user profile is active (not soft-deleted)"""
        return self.deleted_at is None
    
    def to_dict(self, include_private=False):
        """Convert the user profile to a dictionary for API responses"""
        data = {
            'id': str(self.id),
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'visibility': self.visibility,
            'is_active': self.is_active()
        }
        
        # Include more sensitive data if requested and authorized
        if include_private:
            data.update({
                'biography': self.biography,
                'profession': self.profession,
                'company': self.company,
                'current_job': self.current_job,
                'github_username': self.github_username,
                'linkedin_url': self.linkedin_url
            })
            
        return data
    
    def get_connections(self, status='ACCEPTED'):
        """Get user connections with specified status"""
        from app.models.connection import UserConnection
        
        # Get users that this user has connected with
        outgoing = self.outgoing_connections.filter_by(status=status).all()
        outgoing_ids = [connection.recipient_id for connection in outgoing]
        
        # Get users that have connected with this user
        incoming = self.incoming_connections.filter_by(status=status).all()
        incoming_ids = [connection.requester_id for connection in incoming]
        
        # Combine and return unique IDs
        return list(set(outgoing_ids + incoming_ids))
    
    def __repr__(self):
        return f'<UserProfile {self.username}>'