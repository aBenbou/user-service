from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.docs import preference_ns as ns
from app.api.docs import (
    preference_response_model,
    preference_list_model,
    preference_detail_model,
    preference_value_model,
    error_model
)
from app.services.preference_service import (
    get_preferences,
    set_preference,
    delete_preference
)
from app.utils.auth_client import is_owner_or_admin
from uuid import UUID

@ns.route('/')
@ns.param('profile_id', 'The profile identifier')
class PreferenceListResource(Resource):
    
    @jwt_required()
    @ns.doc('get_all_preferences')
    @ns.response(200, 'Success', preference_list_model)
    @ns.response(403, 'Unauthorized', error_model)
    @ns.response(404, 'Profile not found', error_model)
    def get(self, profile_id):
        """Get all preferences for a user"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            result = get_preferences(profile_uuid)
            
            if result['success']:
                return result, 200
            else:
                return result, 404
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/<string:category>')
@ns.param('profile_id', 'The profile identifier')
@ns.param('category', 'Preference category', enum=['NOTIFICATIONS', 'PRIVACY', 'APPEARANCE'])
class PreferenceCategoryResource(Resource):
    
    @jwt_required()
    @ns.doc('get_category_preferences')
    @ns.response(200, 'Success', preference_list_model)
    @ns.response(403, 'Unauthorized', error_model)
    @ns.response(404, 'Profile not found', error_model)
    def get(self, profile_id, category):
        """Get preferences by category for a user"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            result = get_preferences(profile_uuid, category.upper())
            
            if result['success']:
                return result, 200
            else:
                return result, 404
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/<string:category>/<string:key>')
@ns.param('profile_id', 'The profile identifier')
@ns.param('category', 'Preference category', enum=['NOTIFICATIONS', 'PRIVACY', 'APPEARANCE'])
@ns.param('key', 'Preference key')
class PreferenceResource(Resource):
    
    @jwt_required()
    @ns.doc('set_preference')
    @ns.expect(preference_value_model)
    @ns.response(200, 'Success', preference_detail_model)
    @ns.response(400, 'Invalid data', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def put(self, profile_id, category, key):
        """Set a preference value"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Get value from request
            data = request.json
            if not data or 'value' not in data:
                return {'success': False, 'message': 'Value is required'}, 400
            
            result = set_preference(profile_uuid, category.upper(), key, data['value'])
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('delete_preference')
    @ns.response(200, 'Success')
    @ns.response(400, 'Bad request', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def delete(self, profile_id, category, key):
        """Delete a preference"""
        try:
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            result = delete_preference(profile_uuid, category.upper(), key)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500