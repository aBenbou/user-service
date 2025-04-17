from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.docs import connection_ns as ns
from app.api.docs import (
    connection_response_model,
    connection_list_model,
    connection_detail_model,
    connection_status_model,
    error_model
)
from app.services.connection_service import (
    get_connections,
    request_connection,
    update_connection_status,
    delete_connection
)
from uuid import UUID

@ns.route('/')
@ns.param('profile_id', 'The profile identifier')
class ConnectionListResource(Resource):
    
    @jwt_required()
    @ns.doc('get_connections')
    @ns.param('status', 'Connection status filter', enum=['PENDING', 'ACCEPTED', 'REJECTED'], default='ACCEPTED')
    @ns.param('direction', 'Direction filter', enum=['all', 'incoming', 'outgoing'], default='all')
    @ns.response(200, 'Success', connection_list_model)
    @ns.response(404, 'Profile not found', error_model)
    def get(self, profile_id):
        """Get connections for a user"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Get query parameters
            status = request.args.get('status', 'ACCEPTED')
            direction = request.args.get('direction', 'all')
            
            result = get_connections(profile_uuid, status, direction)
            
            if result['success']:
                return result, 200
            else:
                return result, 404
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('request_connection')
    @ns.response(201, 'Success', connection_detail_model)
    @ns.response(400, 'Invalid request', error_model)
    def post(self, profile_id):
        """Request a connection with another user"""
        try:
            recipient_uuid = UUID(profile_id)
            requester_uuid = UUID(get_jwt_identity())
            
            result = request_connection(requester_uuid, recipient_uuid)
            
            if result['success']:
                return result, 201
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/<string:connection_id>')
@ns.param('profile_id', 'The profile identifier')
@ns.param('connection_id', 'The connection identifier')
class ConnectionResource(Resource):
    
    @jwt_required()
    @ns.doc('update_connection')
    @ns.expect(connection_status_model)
    @ns.response(200, 'Success', connection_detail_model)
    @ns.response(400, 'Invalid data', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def put(self, profile_id, connection_id):
        """Update a connection status (accept or reject)"""
        try:
            profile_uuid = UUID(profile_id)
            connection_uuid = UUID(connection_id)
            
            # Verify the user matches the profile ID
            user_id = UUID(get_jwt_identity())
            if user_id != profile_uuid:
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Get status from request
            data = request.json
            if not data or 'status' not in data:
                return {'success': False, 'message': 'Status is required'}, 400
            
            result = update_connection_status(profile_uuid, connection_uuid, data['status'])
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('delete_connection')
    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid request', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def delete(self, profile_id, connection_id):
        """Delete a connection"""
        try:
            profile_uuid = UUID(profile_id)
            connection_uuid = UUID(connection_id)
            
            # Verify the user matches the profile ID
            user_id = UUID(get_jwt_identity())
            if user_id != profile_uuid:
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            result = delete_connection(profile_uuid, connection_uuid)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500