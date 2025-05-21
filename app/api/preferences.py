from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.preference_service import (
    get_preferences,
    set_preference,
    delete_preference
)
from app.utils.auth_client import is_owner_or_admin
from uuid import UUID
from app.utils.responses import success_response, error_response

preferences_bp = Blueprint('preferences', __name__)

@preferences_bp.route('/profiles/<profile_id>/preferences', methods=['GET'])
@jwt_required()
def get_all_preferences_route(profile_id: str):
    """Get all preferences for a user"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return error_response("Unauthorized", 403)
        
        result = get_preferences(profile_uuid)
        
        if result["success"]:
            return success_response(result, 200)
        return error_response(result.get("message", "Not found"), 404)
    except ValueError:
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unhandled error in get_all_preferences_route")
        return error_response(str(e), 500)

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>', methods=['GET'])
@jwt_required()
def get_category_preferences_route(profile_id: str, category: str):
    """Get preferences by category for a user"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return error_response("Unauthorized", 403)
        
        result = get_preferences(profile_uuid, category.upper())
        
        if result["success"]:
            return success_response(result, 200)
        return error_response(result.get("message", "Not found"), 404)
    except ValueError:
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unhandled error in get_category_preferences_route")
        return error_response(str(e), 500)

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>/<key>', methods=['PUT'])
@jwt_required()
def set_preference_route(profile_id: str, category: str, key: str):
    """Set a preference value"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return error_response("Unauthorized", 403)
        
        # Get value from request
        data = request.get_json()
        if not data or 'value' not in data:
            return error_response("Value is required", 400)
        
        result = set_preference(profile_uuid, category.upper(), key, data['value'])
        
        if result["success"]:
            return success_response(result, 200)
        return error_response(result.get("message", "Bad request"), 400)
    except ValueError:
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unhandled error in set_preference_route")
        return error_response(str(e), 500)

@preferences_bp.route('/profiles/<profile_id>/preferences/<category>/<key>', methods=['DELETE'])
@jwt_required()
def delete_preference_route(profile_id: str, category: str, key: str):
    """Delete a preference"""
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            return error_response("Unauthorized", 403)
        
        result = delete_preference(profile_uuid, category.upper(), key)
        
        if result["success"]:
            return success_response(result, 200)
        return error_response(result.get("message", "Bad request"), 400)
    except ValueError:
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unhandled error in delete_preference_route")
        return error_response(str(e), 500)