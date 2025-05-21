from app import db
import uuid

class ExpertiseArea(db.Model):
    __tablename__ = 'expertise_areas'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user_profiles.id'), nullable=False)
    domain = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), nullable=False)  # BEGINNER, INTERMEDIATE, EXPERT
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