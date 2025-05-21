from app import db
import uuid

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user_profiles.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    value = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'category': self.category,
            'key': self.key,
            'value': self.value
        }
    
    def __repr__(self):
        return f'<UserPreference {self.category}.{self.key}>'