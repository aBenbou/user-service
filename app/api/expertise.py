# Third-party
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID

# Local services & utilities
from app.services.expertise_service import (
    get_expertise_areas,
    add_expertise_area,
    update_expertise_area,
    delete_expertise_area,
)
from app.utils.auth_client import is_owner_or_admin
from app.utils.responses import success_response, error_response

# NOTE: g is no longer used.

# Keep blueprint declaration below
expertise_bp = Blueprint('expertise', __name__)

@expertise_bp.route('/profiles/<profile_id>/expertise', methods=['GET'])
@jwt_required()
def get_expertise_areas_route(profile_id: str):
    """Get expertise areas for a user"""
    current_app.logger.info("Get expertise areas endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        result = get_expertise_areas(profile_uuid)
        
        if result["success"]:
            current_app.logger.info("Expertise areas retrieved successfully")
            return success_response(result, 200)
        current_app.logger.error("Failed to get expertise areas: %s", result.get("message"))
        return error_response(result.get("message", "Not found"), 404)
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unexpected error getting expertise areas")
        return error_response("An unexpected error occurred", 500)

@expertise_bp.route('/profiles/<profile_id>/expertise', methods=['POST'])
@jwt_required()
def add_expertise_area_route(profile_id):
    """Add an expertise area for a user"""
    current_app.logger.info("Add expertise area endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            current_app.logger.error("Unauthorized access")
            return error_response("Unauthorized", 403)
        
        # Get data from request
        data = request.get_json()
        if not data:
            current_app.logger.error("No data provided")
            return error_response("No data provided", 400)
        
        # Add expertise area
        result = add_expertise_area(profile_uuid, data)
        
        if result['success']:
            current_app.logger.info("Expertise area added successfully")
            return success_response(result, 201)
        else:
            current_app.logger.error(f"Failed to add expertise area: {result['message']}")
            return error_response(result.get("message", "Bad request"), 400)
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return error_response("Invalid profile ID", 400)
    except Exception as e:
        current_app.logger.exception("Unexpected error adding expertise area")
        return error_response("An unexpected error occurred", 500)

@expertise_bp.route('/profiles/<profile_id>/expertise/<expertise_id>', methods=['PUT'])
@jwt_required()
def update_expertise_area_route(profile_id, expertise_id):
    """Update an expertise area"""
    current_app.logger.info("Update expertise area endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        expertise_uuid = UUID(expertise_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            current_app.logger.error("Unauthorized access")
            return error_response("Unauthorized", 403)
        
        # Get data from request
        data = request.get_json()
        if not data:
            current_app.logger.error("No data provided")
            return error_response("No data provided", 400)
        
        # Update expertise area
        result = update_expertise_area(profile_uuid, expertise_uuid, data)
        
        if result['success']:
            current_app.logger.info("Expertise area updated successfully")
            return success_response(result, 200)
        else:
            current_app.logger.error(f"Failed to update expertise area: {result['message']}")
            return error_response(result.get("message", "Bad request"), 400)
    except ValueError:
        current_app.logger.error("Invalid ID")
        return error_response("Invalid ID", 400)
    except Exception as e:
        current_app.logger.exception("Unexpected error updating expertise area")
        return error_response("An unexpected error occurred", 500)

@expertise_bp.route('/profiles/<profile_id>/expertise/<expertise_id>', methods=['DELETE'])
@jwt_required()
def delete_expertise_area_route(profile_id, expertise_id):
    """Delete an expertise area"""
    current_app.logger.info("Delete expertise area endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        expertise_uuid = UUID(expertise_id)
        
        # Check authorization
        user_id = UUID(get_jwt_identity())
        if not is_owner_or_admin(user_id, profile_uuid):
            current_app.logger.error("Unauthorized access")
            return error_response("Unauthorized", 403)
        
        # Delete expertise area
        result = delete_expertise_area(profile_uuid, expertise_uuid)
        
        if result['success']:
            current_app.logger.info("Expertise area deleted successfully")
            return success_response(result, 200)
        else:
            current_app.logger.error(f"Failed to delete expertise area: {result['message']}")
            return error_response(result.get("message", "Bad request"), 400)
    except ValueError:
        current_app.logger.error("Invalid ID")
        return error_response("Invalid ID", 400)
    except Exception as e:
        current_app.logger.exception("Unexpected error deleting expertise area")
        return error_response("An unexpected error occurred", 500)