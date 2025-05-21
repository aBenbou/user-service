from datetime import datetime
import uuid
from app import db

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    # Use UUID for primary key across all environments
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(80), unique=True, nullable=False)
    biography = db.Column(db.Text)
    profession = db.Column(db.String(100))
    company = db.Column(db.String(100))
    current_job = db.Column(db.String(100))
    visibility = db.Column(db.String(20), default='PUBLIC')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    github_username = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(255))

    # Soft-delete
    deleted_at = db.Column(db.DateTime)
    
    # Relationships
    expertise_areas = db.relationship('ExpertiseArea', back_populates='user', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='profile', lazy=True, cascade='all, delete-orphan')
    
    def is_active(self) -> bool:
        """Return True if the profile has not been soft-deleted."""
        return self.deleted_at is None

    def to_dict(self, include_private: bool = False):
        """Serialize profile to dict.
        If include_private=True, send all fields; otherwise omit potentially sensitive ones like biography.
        """
        data = {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'visibility': self.visibility,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }

        if include_private:
            # Build a quick lookup of privacy preferences for this profile
            privacy_prefs = {
                p.key: p.value for p in self.preferences if p.category == 'PRIVACY'
            }

            # Helper – True means the field should be shown (default)
            def _visible(pref_key: str) -> bool:
                return privacy_prefs.get(pref_key, True) is not False

            # Always include these private fields unless explicitly hidden
            if _visible('show_biography'):
                data['biography'] = self.biography
            if _visible('show_profession'):
                data['profession'] = self.profession
            if _visible('show_company'):
                data['company'] = self.company
            if _visible('show_current_job'):
                data['current_job'] = self.current_job
            if _visible('show_github_username'):
                data['github_username'] = self.github_username
            if _visible('show_linkedin_url'):
                data['linkedin_url'] = self.linkedin_url
        return data

    def __repr__(self):
        return f'<UserProfile {self.username}>'