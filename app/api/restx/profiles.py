from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.docs import profile_ns as ns
from app.api.docs import (
    profile_base_model, 
    profile_response_model, 
    profile_detail_model, 
    profile_list_model,
    error_model
)
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

@ns.route('/<string:profile_id>')
@ns.param('profile_id', 'The profile identifier')
class ProfileResource(Resource):
    
    @jwt_required()
    @ns.doc('get_profile')
    @ns.response(200, 'Success', profile_detail_model)
    @ns.response(400, 'Invalid ID', error_model)
    @ns.response(404, 'Profile not found', error_model)
    def get(self, profile_id):
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
                return {'success': False, 'message': 'Profile not found'}, 404
            
            return {'success': True, 'profile': profile}, 200
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500
    
    @jwt_required()
    @ns.doc('update_profile')
    @ns.expect(profile_base_model)
    @ns.response(200, 'Success', profile_detail_model)
    @ns.response(400, 'Invalid data', error_model)
    @ns.response(403, 'Unauthorized', error_model)
    def put(self, profile_id):
        """Update a user profile"""
        try:
            # Convert string ID to UUID
            profile_uuid = UUID(profile_id)
            
            # Check authorization
            user_id = UUID(get_jwt_identity())
            if not is_owner_or_admin(user_id, profile_uuid):
                return {'success': False, 'message': 'Unauthorized'}, 403
            
            # Get data from request
            data = request.json
            if not data:
                return {'success': False, 'message': 'No data provided'}, 400
            
            # Update profile
            result = update_profile(profile_uuid, data)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except ValueError:
            return {'success': False, 'message': 'Invalid profile ID'}, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/me')
class MyProfileResource(Resource):
    
    @jwt_required()
    @ns.doc('get_my_profile')
    @ns.response(200, 'Success', profile_detail_model)
    def get(self):
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
                    return {'success': True, 'profile': result['profile']}, 200
                else:
                    return result, 400
            
            return {'success': True, 'profile': profile}, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/deactivate')
class DeactivateProfileResource(Resource):
    
    @jwt_required()
    @ns.doc('deactivate_profile')
    @ns.response(200, 'Success', profile_detail_model)
    def put(self):
        """Soft delete the current user's profile"""
        try:
            user_id = UUID(get_jwt_identity())
            result = deactivate_profile(user_id)
            
            if result['success']:
                return result, 200
            else:
                return result, 400
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

@ns.route('/search')
class SearchProfilesResource(Resource):
    
    @jwt_required()
    @ns.doc('search_profiles')
    @ns.param('q', 'Search query')
    @ns.param('expertise', 'Filter by expertise domain')
    @ns.param('visibility', 'Filter by visibility', enum=['PUBLIC', 'PRIVATE', 'CONNECTIONS_ONLY'], default='PUBLIC')
    @ns.param('limit', 'Maximum number of results', type=int, default=20)
    @ns.param('offset', 'Pagination offset', type=int, default=0)
    @ns.response(200, 'Success', profile_list_model)
    def get(self):
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
            
            return result, 200
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500