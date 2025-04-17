from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.docs import expertise_ns as ns
from app.api.docs import (
    expertise_base_model,
    expertise_response_model,
    expertise_list_model,
    expertise_detail_model,
    error_model
)
from app.services.expertise_service import (
    get_expertise_areas,
    add_expertise_area,
    update_expertise_area,
    delete_expertise_area
)
from app.utils.auth_client import is_owner_or_admin
from uuid import UUID

# Use parameter in route definition for documentation
@ns.route('/')
@ns.param('profile_id', 'The profile identifier')
class ExpertiseListResource(Resource):
    
    @jwt_required()
    @ns.doc('get_expertise_areas')
    @ns.response(200, 'Success', expertise_list_model)
    @ns.response(404, 'Profile not found', error_model)
    def get(self, profile_id):
        """Get expertise areas for a user"""
        try:
            profile_uuid = UUID(profile_id)
            result = get_expertise_areas(profile_uuid)
            
            if result['success']:
                return result, 200
            else:
                return result, 404
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('add_expertise_area')
    @ns.expect(expertise_base_model)
    @ns.response(201, 'Created', expertise_detail_model)
    @ns.response(400, 'Invalid data', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def post(self, profile_id):
        """Add an expertise area for a user"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Get data from request
            data = request.json
            if not data:
                return {'success': False, 'message': 'No data provided'}, 400
            
            # Add expertise area
            result = add_expertise_area(profile_uuid, data)
            
            if result['success']:
                return result, 201
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/<string:expertise_id>')
@ns.param('profile_id', 'The profile identifier')
@ns.param('expertise_id', 'The expertise area identifier')
class ExpertiseResource(Resource):
    
    @jwt_required()
    @ns.doc('update_expertise_area')
    @ns.expect(expertise_base_model)
    @ns.response(200, 'Success', expertise_detail_model)
    @ns.response(400, 'Invalid data', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def put(self, profile_id, expertise_id):
        """Update an expertise area"""
        try:
            profile_uuid = UUID(profile_id)
            expertise_uuid = UUID(expertise_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Get data from request
            data = request.json
            if not data:
                return {'success': False, 'message': 'No data provided'}, 400
            
            # Update expertise area
            result = update_expertise_area(profile_uuid, expertise_uuid, data)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('delete_expertise_area')
    @ns.response(200, 'Success')
    @ns.response(400, 'Invalid request', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def delete(self, profile_id, expertise_id):
        """Delete an expertise area"""
        try:
            profile_uuid = UUID(profile_id)
            expertise_uuid = UUID(expertise_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Delete expertise area
            result = delete_expertise_area(profile_uuid, expertise_uuid)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500