class User(db.Model):
    # ... existing code ...
    
    # Gamification fields
    level = db.Column(db.Integer, default=1)
    total_points = db.Column(db.Integer, default=0)
    
    # Relationships
    points = db.relationship('Points', backref='user', lazy=True)
    badges = db.relationship('Badge', secondary='user_badges', lazy=True)
    
    def to_dict(self):
        return {
            # ... existing fields ...
            'level': self.level,
            'total_points': self.total_points,
            'badges': [badge.to_dict() for badge in self.badges]
        } 