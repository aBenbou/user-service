from typing import Dict, Optional, List, Any
from uuid import UUID
from app import db
from app.models.expertise import ExpertiseArea
from app.models.profile import UserProfile

def get_expertise_areas(profile_id: UUID) -> Dict[str, Any]:
    """Get all expertise areas for a user
    
    Args:
        profile_id: UUID of the user profile
        
    Returns:
        Dictionary with expertise areas
    """
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    expertise_areas = ExpertiseArea.query.filter_by(user_id=profile_id).all()
    
    return {
        'success': True,
        'expertise_areas': [area.to_dict() for area in expertise_areas]
    }

def add_expertise_area(profile_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new expertise area for a user
    
    Args:
        profile_id: UUID of the user profile
        data: Expertise area data
        
    Returns:
        Dictionary with success status and expertise area data
    """
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Validate required fields
    if not data.get('domain') or not data.get('level'):
        return {
            'success': False,
            'message': 'Domain and level are required'
        }
    
    # Check if domain already exists for this user
    existing = ExpertiseArea.query.filter_by(
        user_id=profile_id, 
        domain=data['domain']
    ).first()
    
    if existing:
        return {
            'success': False,
            'message': f'Expertise in {data["domain"]} already exists for this user'
        }
    
    # Create new expertise area
    expertise = ExpertiseArea(
        user_id=profile_id,
        domain=data['domain'],
        level=data['level'],
        years_experience=data.get('years_experience')
    )
    
    db.session.add(expertise)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Expertise area added successfully',
        'expertise': expertise.to_dict()
    }

def update_expertise_area(profile_id: UUID, expertise_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing expertise area
    
    Args:
        profile_id: UUID of the user profile
        expertise_id: UUID of the expertise area
        data: Updated expertise area data
        
    Returns:
        Dictionary with success status and updated expertise area data
    """
    # Verify the profile exists and is active
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Get the expertise area
    expertise = ExpertiseArea.query.get(expertise_id)
    if not expertise or expertise.user_id != profile_id:
        return {
            'success': False,
            'message': 'Expertise area not found for this user'
        }
    
    # Update expertise fields
    if 'domain' in data:
        expertise.domain = data['domain']
    if 'level' in data:
        expertise.level = data['level']
    if 'years_experience' in data:
        expertise.years_experience = data['years_experience']
    
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Expertise area updated successfully',
        'expertise': expertise.to_dict()
    }

def delete_expertise_area(profile_id: UUID, expertise_id: UUID) -> Dict[str, Any]:
    """Delete an expertise area
    
    Args:
        profile_id: UUID of the user profile
        expertise_id: UUID of the expertise area
        
    Returns:
        Dictionary with success status
    """
    # Verify the profile exists and is active
    profile = UserProfile.query.get(profile_id)
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Get the expertise area
    expertise = ExpertiseArea.query.get(expertise_id)
    if not expertise or expertise.user_id != profile_id:
        return {
            'success': False,
            'message': 'Expertise area not found for this user'
        }
    
    db.session.delete(expertise)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Expertise area deleted successfully'
    }