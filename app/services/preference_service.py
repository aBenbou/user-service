from typing import Dict, Optional, List, Any
from uuid import UUID
from app import db
from app.models.preference import UserPreference
from app.models.profile import UserProfile

def get_preferences(profile_id: UUID, category: Optional[str] = None) -> Dict[str, Any]:
    """Get user preferences, optionally filtered by category
    
    Args:
        profile_id: UUID of the user profile
        category: Optional category filter
        
    Returns:
        Dictionary with preferences
    """
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Filter query by category if provided
    query = UserPreference.query.filter_by(user_id=profile_id)
    if category:
        query = query.filter_by(category=category)
    
    preferences = query.all()
    
    return {
        'success': True,
        'preferences': [pref.to_dict() for pref in preferences]
    }

def set_preference(profile_id: UUID, category: str, key: str, value: Any) -> Dict[str, Any]:
    """Set a user preference value
    
    Args:
        profile_id: UUID of the user profile
        category: Preference category
        key: Preference key
        value: Preference value
        
    Returns:
        Dictionary with success status and preference data
    """
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Validate category
    valid_categories = ['NOTIFICATIONS', 'PRIVACY', 'APPEARANCE']
    if category not in valid_categories:
        return {
            'success': False,
            'message': f'Invalid category. Must be one of {", ".join(valid_categories)}'
        }
    
    # Check if preference already exists
    preference = UserPreference.query.filter_by(
        user_id=profile_id,
        category=category,
        key=key
    ).first()
    
    if preference:
        # Update existing preference
        preference.value = value
    else:
        # Create new preference
        preference = UserPreference(
            user_id=profile_id,
            category=category,
            key=key,
            value=value
        )
        db.session.add(preference)
    
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Preference set successfully',
        'preference': preference.to_dict()
    }

def delete_preference(profile_id: UUID, category: str, key: str) -> Dict[str, Any]:
    """Delete a user preference
    
    Args:
        profile_id: UUID of the user profile
        category: Preference category
        key: Preference key
        
    Returns:
        Dictionary with success status
    """
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Find the preference
    preference = UserPreference.query.filter_by(
        user_id=profile_id,
        category=category,
        key=key
    ).first()
    
    if not preference:
        return {
            'success': False,
            'message': 'Preference not found'
        }
    
    db.session.delete(preference)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Preference deleted successfully'
    }