from typing import Dict, Any
import re

def validate_profile_data(data: Dict[str, Any], update: bool = False) -> Dict[str, Any]:
    """Validate profile data
    
    Args:
        data: The profile data to validate
        update: Whether this is an update operation
        
    Returns:
        Dictionary with validation result
    """
    # For updates, any fields are allowed
    if update:
        return {'valid': True}
    
    # For new profiles, username is required
    if not data.get('username'):
        return {
            'valid': False,
            'message': 'Username is required'
        }
    
    # Validate username format
    username = data.get('username')
    if username and not re.match(r'^[a-zA-Z0-9_-]{3,50}$', username):
        return {
            'valid': False,
            'message': 'Username must be 3-50 characters and contain only letters, numbers, underscores, and hyphens'
        }
    
    # Validate other fields if provided
    if 'linkedin_url' in data and data['linkedin_url']:
        if not data['linkedin_url'].startswith('https://www.linkedin.com/'):
            return {
                'valid': False,
                'message': 'LinkedIn URL must start with https://www.linkedin.com/'
            }
    
    # Validate visibility
    valid_visibility = ['PUBLIC', 'PRIVATE', 'CONNECTIONS_ONLY']
    if 'visibility' in data and data['visibility'] not in valid_visibility:
        return {
            'valid': False,
            'message': f'Visibility must be one of: {", ".join(valid_visibility)}'
        }
    
    return {'valid': True}

def sanitize_input(text: str) -> str:
    """Sanitize user-generated text input
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>]', '', text)
    
    # Limit length
    max_length = 5000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()