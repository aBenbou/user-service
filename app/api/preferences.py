from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.preference_service import (
    get_preferences,
    set_preference,
    delete_preference
)
from app.utils.auth_client import is_owner_or_admin
from uuid import UUID

preferences_bp = Blueprint('preferences', __name__)

@preferences_bp.route('/profiles/<profile_id>/preferences', methods=['GET'])
@jwt_required()
def get_all_preferences_route(profile_id):
    """Get all preferences for a user"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        result = get_preferences(profile_uuid)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>', methods=['GET'])
@jwt_required()
def get_category_preferences_route(profile_id, category):
    """Get preferences by category for a user"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        result = get_preferences(profile_uuid, category.upper())
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>/<key>', methods=['PUT'])
@jwt_required()
def set_preference_route(profile_id, category, key):
    """Set a preference value"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get value from request
        data = request.get_json()
        if not data or 'value' not in data:
            return jsonify({'success': False, 'message': 'Value is required'}), 400
        
        result = set_preference(profile_uuid, category.upper(), key, data['value'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>/<key>', methods=['DELETE'])
@jwt_required()
def delete_preference_route(profile_id, category, key):
    """Delete a preference"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        result = delete_preference(profile_uuid, category.upper(), key)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500