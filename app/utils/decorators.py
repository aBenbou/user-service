from functools import wraps
from flask import request, jsonify, g, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from uuid import UUID

def jwt_required_with_permissions(permissions=None):
    """Decorator to check JWT and verify required permissions"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT is present and valid
                verify_jwt_in_request()
                
                # Get user identity from JWT
                user_id = UUID(get_jwt_identity())
                
                # Store user ID in g for access in the route
                g.current_user_id = user_id
                
                # If no permissions required, proceed
                if not permissions:
                    return fn(*args, **kwargs)
                
                # Check if user has admin permissions
                from app.utils.auth_client import is_admin
                if is_admin(user_id):
                    return fn(*args, **kwargs)
                
                # Get user permissions from Auth Service
                from app.utils.auth_client import get_user_permissions
                user_permissions = get_user_permissions(user_id)
                
                if not user_permissions.get('success', False):
                    return jsonify({'success': False, 'message': 'Error fetching permissions'}), 500
                
                # Check if user has all required permissions
                user_perms = user_permissions.get('permissions', [])
                for permission in permissions:
                    if permission not in user_perms:
                        return jsonify({
                            'success': False, 
                            'message': f'Permission denied: {permission} required'
                        }), 403
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                current_app.logger.error(f"Authentication error: {str(e)}")
                return jsonify({'success': False, 'message': f'Authentication error: {str(e)}'}), 401
                
        return wrapper
    return decorator