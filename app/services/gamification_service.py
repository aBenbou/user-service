from datetime import datetime
from app import db
from app.models.user import User
from app.models.gamification import Points, Level, Badge, UserBadge

class GamificationService:
    def __init__(self):
        self.points_per_level = 1000  # Points needed to level up
        self.max_level = 100  # Maximum level cap
        
    def add_points(self, user_id, points, reason):
        """Add points to user's total"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False, "User not found"
            
            # Create points record
            points_record = Points(
                user_id=user_id,
                amount=points,
                reason=reason,
                timestamp=datetime.utcnow()
            )
            db.session.add(points_record)
            
            # Update user's total points
            user.total_points += points
            
            # Check for level up
            self._check_level_up(user)
            
            db.session.commit()
            return True, "Points added successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    def _check_level_up(self, user):
        """Check if user should level up based on points"""
        current_level = user.level
        new_level = min(user.total_points // self.points_per_level + 1, self.max_level)
        
        if new_level > current_level:
            user.level = new_level
            self._award_level_badge(user, new_level)
    
    def _award_level_badge(self, user, level):
        """Award level badge to user"""
        badge = Badge.query.filter_by(
            type='level',
            requirement=str(level)
        ).first()
        
        if badge and not UserBadge.query.filter_by(
            user_id=user.id,
            badge_id=badge.id
        ).first():
            user_badge = UserBadge(
                user_id=user.id,
                badge_id=badge.id,
                awarded_at=datetime.utcnow()
            )
            db.session.add(user_badge)
    
    def get_user_progress(self, user_id):
        """Get user's gamification progress"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        current_level_points = user.level * self.points_per_level
        next_level_points = (user.level + 1) * self.points_per_level
        progress = (user.total_points - current_level_points) / self.points_per_level * 100
        
        return {
            'level': user.level,
            'total_points': user.total_points,
            'current_level_points': current_level_points,
            'next_level_points': next_level_points,
            'progress_percentage': progress,
            'badges': [badge.to_dict() for badge in user.badges]
        }
    
    def award_badge(self, user_id, badge_type, requirement):
        """Award a specific badge to user"""
        try:
            badge = Badge.query.filter_by(
                type=badge_type,
                requirement=requirement
            ).first()
            
            if not badge:
                return False, "Badge not found"
            
            if UserBadge.query.filter_by(
                user_id=user_id,
                badge_id=badge.id
            ).first():
                return False, "User already has this badge"
            
            user_badge = UserBadge(
                user_id=user_id,
                badge_id=badge.id,
                awarded_at=datetime.utcnow()
            )
            
            db.session.add(user_badge)
            db.session.commit()
            return True, "Badge awarded successfully"
        except Exception as e:
            db.session.rollback()
            return False, str(e) 