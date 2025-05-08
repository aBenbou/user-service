from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.expertise_service import (
    get_expertise_areas,
    add_expertise_area,
    update_expertise_area,
    delete_expertise_area
)
from app.utils.auth_client import is_owner_or_admin
from uuid import UUID

expertise_bp = Blueprint('expertise', __name__)

@expertise_bp.route('/profiles/<profile_id>/expertise', methods=['GET'])
@jwt_required()
def get_expertise_areas_route(profile_id):
    """Get expertise areas for a user"""
    current_app.logger.info("Get expertise areas endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        result = get_expertise_areas(profile_uuid)
        
        if result['success']:
            current_app.logger.info("Expertise areas retrieved successfully")
            return jsonify(result), 200
        else:
            current_app.logger.error(f"Failed to get expertise areas: {result['message']}")
            return jsonify(result), 404
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        current_app.logger.error("Unexpected error getting expertise areas")
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

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
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get data from request
        data = request.get_json()
        if not data:
            current_app.logger.error("No data provided")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Add expertise area
        result = add_expertise_area(profile_uuid, data)
        
        if result['success']:
            current_app.logger.info("Expertise area added successfully")
            return jsonify(result), 201
        else:
            current_app.logger.error(f"Failed to add expertise area: {result['message']}")
            return jsonify(result), 400
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        current_app.logger.error("Unexpected error adding expertise area")
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

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
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get data from request
        data = request.get_json()
        if not data:
            current_app.logger.error("No data provided")
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Update expertise area
        result = update_expertise_area(profile_uuid, expertise_uuid, data)
        
        if result['success']:
            current_app.logger.info("Expertise area updated successfully")
            return jsonify(result), 200
        else:
            current_app.logger.error(f"Failed to update expertise area: {result['message']}")
            return jsonify(result), 400
    except ValueError:
        current_app.logger.error("Invalid ID")
        return jsonify({'success': False, 'message': 'Invalid ID'}), 400
    except Exception as e:
        current_app.logger.error("Unexpected error updating expertise area")
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

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
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Delete expertise area
        result = delete_expertise_area(profile_uuid, expertise_uuid)
        
        if result['success']:
            current_app.logger.info("Expertise area deleted successfully",)
            return jsonify(result), 200
        else:
            current_app.logger.error(f"Failed to delete expertise area: {result['message']}")
            return jsonify(result), 400
    except ValueError:
        current_app.logger.error("Invalid ID")
        return jsonify({'success': False, 'message': 'Invalid ID'}), 400
    except Exception as e:
        current_app.logger.error("Unexpected error deleting expertise area")
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500