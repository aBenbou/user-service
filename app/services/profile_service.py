from datetime import datetime
from typing import Dict, Optional, List, Any
from uuid import UUID
from app import db
from app.models.profile import UserProfile
from app.utils.validators import validate_profile_data

def get_profile_by_id(profile_id: UUID, include_private: bool = False) -> Optional[Dict[str, Any]]:
    """Get a user profile by ID
    
    Args:
        profile_id: UUID of the profile to retrieve
        include_private: Whether to include private fields
        
    Returns:
        Dictionary representation of the profile or None if not found
    """
    profile = db.session.get(UserProfile, str(profile_id))
    if not profile or not profile.is_active():
        return None
    
    return profile.to_dict(include_private=include_private)

def get_my_profile(user_id: UUID) -> Optional[Dict[str, Any]]:
    """Get the current user's profile
    
    Args:
        user_id: UUID of the authenticated user
        
    Returns:
        Dictionary representation of the profile or None if not found
    """
    profile = db.session.get(UserProfile, str(user_id))
    if not profile:
        return None
    
    # Always include private data for user's own profile
    return profile.to_dict(include_private=True)

def create_profile(user_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new user profile
    
    Args:
        user_id: UUID of the authenticated user
        data: Profile data
        
    Returns:
        Dictionary with success status and profile data
    """
    # Check if profile already exists
    existing_profile = db.session.get(UserProfile, str(user_id))
    if existing_profile:
        return {
            'success': False,
            'message': 'Profile already exists for this user'
        }
    
    # Validate required fields
    validate_result = validate_profile_data(data)
    if not validate_result['valid']:
        return {
            'success': False,
            'message': validate_result['message']
        }
    
    # Create new profile
    profile = UserProfile(
        id=str(user_id),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        username=data.get('username'),
        biography=data.get('biography'),
        profession=data.get('profession'),
        company=data.get('company'),
        current_job=data.get('current_job'),
        github_username=data.get('github_username'),
        linkedin_url=data.get('linkedin_url'),
        visibility=data.get('visibility', 'PUBLIC')
    )
    
    db.session.add(profile)
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Profile created successfully',
        'profile': profile.to_dict(include_private=True)
    }

def update_profile(profile_id: UUID, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing user profile
    
    Args:
        profile_id: UUID of the profile to update
        data: Updated profile data
        
    Returns:
        Dictionary with success status and updated profile data
    """
    profile = db.session.get(UserProfile, str(profile_id))
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Validate data
    validate_result = validate_profile_data(data, update=True)
    if not validate_result['valid']:
        return {
            'success': False,
            'message': validate_result['message']
        }
    
    # Update profile fields
    for field in [
        'first_name', 'last_name', 'username', 'biography', 
        'profession', 'company', 'current_job', 
        'github_username', 'linkedin_url', 'visibility'
    ]:
        if field in data:
            setattr(profile, field, data[field])
    
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Profile updated successfully',
        'profile': profile.to_dict(include_private=True)
    }

def deactivate_profile(profile_id: UUID) -> Dict[str, Any]:
    """Soft delete a user profile
    
    Args:
        profile_id: UUID of the profile to deactivate
        
    Returns:
        Dictionary with success status
    """
    profile = db.session.get(UserProfile, str(profile_id))
    if not profile or not profile.is_active():
        return {
            'success': False,
            'message': 'Profile not found'
        }
    
    # Soft delete by setting deleted_at
    profile.deleted_at = datetime.utcnow()
    db.session.commit()
    
    return {
        'success': True,
        'message': 'Profile deactivated successfully'
    }

def search_profiles(
    query: str = None, 
    expertise: str = None,
    visibility: str = 'PUBLIC',
    limit: int = 20, 
    offset: int = 0
) -> Dict[str, Any]:
    """Search for user profiles with filters
    
    Args:
        query: Search string for name, username, etc.
        expertise: Domain of expertise to filter by
        visibility: Minimum visibility level (PUBLIC by default)
        limit: Maximum number of results to return
        offset: Pagination offset
        
    Returns:
        Dictionary with profiles and pagination info
    """
    # Base query: only active profiles
    base_query = UserProfile.query.filter(UserProfile.deleted_at == None)
    
    # Filter by visibility
    base_query = base_query.filter(UserProfile.visibility == visibility)
    
    # Apply search query if provided
    if query:
        search_term = f"%{query}%"
        base_query = base_query.filter(
            db.or_(
                UserProfile.username.ilike(search_term),
                UserProfile.first_name.ilike(search_term),
                UserProfile.last_name.ilike(search_term),
                UserProfile.biography.ilike(search_term),
                UserProfile.profession.ilike(search_term),
                UserProfile.company.ilike(search_term),
                UserProfile.current_job.ilike(search_term)
            )
        )
    
    # Filter by expertise domain if provided
    if expertise:
        from app.models.expertise import ExpertiseArea
        base_query = base_query.join(ExpertiseArea).filter(
            ExpertiseArea.domain.ilike(f"%{expertise}%")
        )
    
    # Count total results for pagination
    total = base_query.count()
    
    # Apply pagination
    profiles = base_query.limit(limit).offset(offset).all()
    
    return {
        'success': True,
        'profiles': [p.to_dict() for p in profiles],
        'pagination': {
            'total': total,
            'limit': limit,
            'offset': offset
        }
    }