import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import db

class ExpertiseArea(db.Model):
    __tablename__ = 'expertise_areas'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Enum('BEGINNER', 'INTERMEDIATE', 'EXPERT', name='expertise_level'), nullable=False)
    years_experience = db.Column(db.Integer)
    
    # Relationships
    user = db.relationship('UserProfile', back_populates='expertise_areas')
    
    def to_dict(self):
        """Convert the expertise area to a dictionary for API responses"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'domain': self.domain,
            'level': self.level,
            'years_experience': self.years_experience
        }
    
    def __repr__(self):
        return f'<ExpertiseArea {self.domain} ({self.level})>'