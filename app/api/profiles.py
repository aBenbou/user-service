from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.profile_service import (
    get_profile_by_id,
    get_my_profile,
    create_profile,
    update_profile,
    deactivate_profile,
    search_profiles
)
from app.utils.auth_client import is_admin, is_owner_or_admin
from uuid import UUID

profiles_bp = Blueprint('profiles', __name__)

@profiles_bp.route('/<profile_id>', methods=['GET'])
@jwt_required()
def get_profile(profile_id):
    """Get a user profile by ID"""
    try:
        # Convert string ID to UUID
        profile_uuid = UUID(profile_id)
        
        # Check if the requesting user is the owner or an admin
        user_id = UUID(get_jwt_identity())
        include_private = is_owner_or_admin(user_id, profile_uuid)
        
        # Get the profile
        profile = get_profile_by_id(profile_uuid, include_private)
        
        if not profile:
            return jsonify({'success': False, 'message': 'Profile not found'}), 404
        
        return jsonify({'success': True, 'profile': profile}), 200
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profiles_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile_route():
    """Get the current user's profile"""
    try:
        user_id = UUID(get_jwt_identity())
        profile = get_my_profile(user_id)
        
        if not profile:
            # Create a minimal profile if it doesn't exist
            result = create_profile(user_id, {
                'username': f'user{user_id.hex[:8]}',
                'visibility': 'PRIVATE'
            })
            if result['success']:
                return jsonify({'success': True, 'profile': result['profile']}), 200
            else:
                return jsonify(result), 400
        
        return jsonify({'success': True, 'profile': profile}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profiles_bp.route('/<profile_id>', methods=['PUT'])
@jwt_required()
def update_profile_route(profile_id):
    """Update a user profile"""
    try:
        # Convert string ID to UUID
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get data from request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Update profile
        result = update_profile(profile_uuid, data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profiles_bp.route('/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_profile_route():
    """Soft delete the current user's profile"""
    try:
        user_id = UUID(get_jwt_identity())
        result = deactivate_profile(user_id)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@profiles_bp.route('/search', methods=['GET'])
@jwt_required()
def search_profiles_route():
    """Search for user profiles with filters"""
    try:
        # Get query parameters
        query = request.args.get('q')
        expertise = request.args.get('expertise')
        visibility = request.args.get('visibility', 'PUBLIC')
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        # Search profiles
        result = search_profiles(
            query=query,
            expertise=expertise,
            visibility=visibility,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500