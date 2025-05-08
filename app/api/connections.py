from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.connection_service import (
    get_connections,
    request_connection,
    update_connection_status,
    delete_connection
)
from uuid import UUID

connections_bp = Blueprint('connections', __name__)

@connections_bp.route('/profiles/<profile_id>/connections', methods=['GET'])
@jwt_required()
def get_connections_route(profile_id):
    """Get connections for a user"""
    current_app.logger.info("Get connections endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        
        # Get query parameters
        status = request.args.get('status', 'ACCEPTED')
        direction = request.args.get('direction', 'all')
        
        result = get_connections(profile_uuid, status, direction)
        
        if result['success']:
            current_app.logger.info("Connections retrieved successfully")
            return jsonify(result), 200
        else:
            current_app.logger.error(f"Failed to get connections")
            return jsonify(result), 404
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@connections_bp.route('/profiles/<profile_id>/connections', methods=['POST'])
@jwt_required()
def request_connection_route(profile_id):
    """Request a connection with another user"""
    current_app.logger.info("Create connection endpoint called")
    try:
        recipient_uuid = UUID(profile_id)
        requester_uuid = UUID(get_jwt_identity())
        
        result = request_connection(requester_uuid, recipient_uuid)
        
        if result['success']:
            current_app.logger.info("Connection created successfully")
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    except ValueError:
        current_app.logger.error("Invalid profile ID")
        return jsonify({'success': False, 'message': 'Invalid profile ID'}), 400
    except Exception as e:
        current_app.logger.error("Unexpected error creating connection")
        return jsonify({'success': False, 'message': 'An unexpected error occurred'}), 500

@connections_bp.route('/profiles/<profile_id>/connections/<connection_id>', methods=['PUT'])
@jwt_required()
def update_connection_status_route(profile_id, connection_id):
    """Update a connection status (accept or reject)"""
    current_app.logger.info("Update connection endpoint called")
    try:
        profile_uuid = UUID(profile_id)
        connection_uuid = UUID(connection_id)
        
        # Verify the user matches the profile ID
        user_id = UUID(get_jwt_identity())
        if user_id != profile_uuid:
            current_app.logger.error("Unauthorized")
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        # Get status from request
        data = request.get_json()
        if not data or 'status' not in data:
            current_app.logger.error("Status is required")
            return jsonify({'success': False, 'message': 'Status is required'}), 400
        
        result = update_connection_status(profile_uuid, connection_uuid, data['status'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@connections_bp.route('/profiles/<profile_id>/connections/<connection_id>', methods=['DELETE'])
@jwt_required()
def delete_connection_route(profile_id, connection_id):
    """Delete a connection"""
    try:
        profile_uuid = UUID(profile_id)
        connection_uuid = UUID(connection_id)
        
        # Verify the user matches the profile ID
        user_id = UUID(get_jwt_identity())
        if user_id != profile_uuid:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
        result = delete_connection(profile_uuid, connection_uuid)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500