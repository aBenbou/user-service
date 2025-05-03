from datetime import datetime
from app import db

class Points(db.Model):
    __tablename__ = 'points'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'reason': self.reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Badge(db.Model):
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # level, achievement, etc.
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    requirement = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)
    
    @classmethod
    def create_initial_badges(cls):
        """Create initial badges if they don't exist"""
        badges = [
            {
                'type': 'level',
                'name': 'Level 1',
                'description': 'Reached level 1',
                'requirement': '1'
            },
            {
                'type': 'level',
                'name': 'Level 2',
                'description': 'Reached level 2',
                'requirement': '2'
            },
            {
                'type': 'achievement',
                'name': 'First Points',
                'description': 'Earned your first points',
                'requirement': 'first_points'
            }
        ]
        
        for badge_data in badges:
            existing = cls.query.filter_by(
                type=badge_data['type'],
                requirement=badge_data['requirement']
            ).first()
            
            if not existing:
                badge = cls(**badge_data)
                db.session.add(badge)
        
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'description': self.description,
            'requirement': self.requirement,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate badges
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'badge_id': self.badge_id,
            'awarded_at': self.awarded_at.isoformat() if self.awarded_at else None,
            'badge': self.badge.to_dict() if self.badge else None
        } 