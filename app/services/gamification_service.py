from datetime import datetime
from app import db
from app.models.user import User
from app.models.gamification import Points, Badge, UserBadge
from app.utils.auth_client import get_user_basic

class GamificationService:
    def __init__(self):
        self.points_per_level = 1000  # Points needed to level up
        self.max_level = 100  # Maximum level cap
        
    def add_points(self, user_id, points, reason):
        """Add points to user's total"""
        try:
            user = self._get_or_create_user(user_id)
            if not user:
                return False, "User not found"
            
            # Create points record
            points_record = Points(
                user_id=user_id,
                amount=points,
                reason=reason,
                created_at=datetime.utcnow()
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
        user = self._get_or_create_user(user_id)
        if not user:
            return None
        
        # Points thresholds for the *start* of current and next levels
        current_level_points = (user.level - 1) * self.points_per_level
        next_level_points = user.level * self.points_per_level

        # Clamp to [0, 100]
        progress = max(0, min(100, (user.total_points - current_level_points) / self.points_per_level * 100))
        
        return {
            'level': user.level,
            'total_points': user.total_points,
            'current_level_points': current_level_points,
            'next_level_points': next_level_points,
            'progress_percentage': progress,
            'badges': [ub.badge.to_dict() for ub in user.user_badges]
        }
    
    def award_badge(self, user_id, badge_type, requirement):
        """Award a specific badge to user"""
        try:
            badge = Badge.query.filter_by(
                type=badge_type,
                requirement=requirement
            ).first()
            
            if not badge:
                return False, "Badge not found", None
            
            if UserBadge.query.filter_by(
                user_id=user_id,
                badge_id=badge.id
            ).first():
                return False, "User already has this badge", None
            
            user_badge = UserBadge(
                user_id=user_id,
                badge_id=badge.id,
                awarded_at=datetime.utcnow()
            )
            
            db.session.add(user_badge)
            db.session.commit()
            return True, "Badge awarded successfully", badge.to_dict()
        except Exception as e:
            db.session.rollback()
            return False, str(e), None

    # -------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------

    def _get_or_create_user(self, user_id):
        """Return a User row; create one from Auth Service if absent."""
        user = db.session.get(User, user_id)
        if user:
            return user

        # Try to fetch minimal info from Auth Service; fall back to placeholders
        basic = get_user_basic(user_id)

        try:
            user = User(
                id=user_id,
                email=(basic.get("email") if basic.get("success") else None) or f"{user_id}@placeholder.local",
                username=(basic.get("username") if basic.get("success") else None) or f"user{str(user_id)[:8]}",
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            return None 