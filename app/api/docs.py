from flask import Blueprint
from flask_restx import Api, Namespace, Resource, fields
from uuid import UUID

# Create blueprint for API documentation
docs_bp = Blueprint('api_docs', __name__)

# Create API instance for Swagger documentation
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Type "Bearer" followed by a space and then your JWT token'
    }
}

api = Api(
    docs_bp,
    version='1.0',
    title='User Profile Service API',
    description='API for managing user profiles, expertise, preferences, and connections',
    doc='/docs',
    authorizations=authorizations,
    security='Bearer Auth'
)

# Create API namespaces
profile_ns = Namespace('profiles', description='Profile management operations')
expertise_ns = Namespace('expertise', description='Expertise area operations')
preference_ns = Namespace('preferences', description='User preference operations')
connection_ns = Namespace('connections', description='User connection operations')

# Register namespaces
api.add_namespace(profile_ns, path='/api/profiles')
api.add_namespace(expertise_ns, path='/api/profiles/{profile_id}/expertise')
api.add_namespace(preference_ns, path='/api/profiles/{profile_id}/preferences')
api.add_namespace(connection_ns, path='/api/profiles/{profile_id}/connections')

# Define models for API documentation
# Note: These models reflect the structure of request/response data, not database models

# Helper models
wild_card_model = api.model('WildCardValue', {
    'value': fields.Raw(description='Any valid JSON value')
})

# Profile models
profile_base_model = api.model('ProfileBase', {
    'username': fields.String(description='Unique username', required=True, example='johnsmith'),
    'first_name': fields.String(description='First name', example='John'),
    'last_name': fields.String(description='Last name', example='Smith'),
    'biography': fields.String(description='User biography', example='Software engineer with 5 years of experience'),
    'profession': fields.String(description='User profession', example='Software Engineer'),
    'company': fields.String(description='User company', example='Tech Corp'),
    'current_job': fields.String(description='Current job title', example='Senior Developer'),
    'github_username': fields.String(description='GitHub username', example='johnsmith'),
    'linkedin_url': fields.String(description='LinkedIn profile URL', example='https://www.linkedin.com/in/johnsmith'),
    'visibility': fields.String(description='Profile visibility', enum=['PUBLIC', 'PRIVATE', 'CONNECTIONS_ONLY'], default='PUBLIC')
})

profile_response_model = api.clone('ProfileResponse', profile_base_model, {
    'id': fields.String(description='Profile UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'joined_at': fields.DateTime(description='Profile creation date', example='2025-01-01T00:00:00Z'),
    'is_active': fields.Boolean(description='Whether the profile is active', example=True)
})

profile_list_model = api.model('ProfileList', {
    'success': fields.Boolean(description='Success status', example=True),
    'profiles': fields.List(fields.Nested(profile_response_model)),
    'pagination': fields.Nested(api.model('Pagination', {
        'total': fields.Integer(description='Total number of items', example=100),
        'limit': fields.Integer(description='Items per page', example=20),
        'offset': fields.Integer(description='Pagination offset', example=0)
    }))
})

profile_detail_model = api.model('ProfileDetail', {
    'success': fields.Boolean(description='Success status', example=True),
    'profile': fields.Nested(profile_response_model)
})

# Expertise models
expertise_base_model = api.model('ExpertiseBase', {
    'domain': fields.String(required=True, description='Area of expertise', example='Machine Learning'),
    'level': fields.String(required=True, description='Expertise level', enum=['BEGINNER', 'INTERMEDIATE', 'EXPERT'], example='EXPERT'),
    'years_experience': fields.Integer(description='Years of experience', example=5)
})

expertise_response_model = api.clone('ExpertiseResponse', expertise_base_model, {
    'id': fields.String(description='Expertise UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'user_id': fields.String(description='User profile UUID', example='123e4567-e89b-12d3-a456-426614174000')
})

expertise_list_model = api.model('ExpertiseList', {
    'success': fields.Boolean(description='Success status', example=True),
    'expertise_areas': fields.List(fields.Nested(expertise_response_model))
})

expertise_detail_model = api.model('ExpertiseDetail', {
    'success': fields.Boolean(description='Success status', example=True),
    'message': fields.String(description='Response message', example='Expertise area added successfully'),
    'expertise': fields.Nested(expertise_response_model)
})

# Preference models
preference_response_model = api.model('PreferenceResponse', {
    'id': fields.String(description='Preference UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'user_id': fields.String(description='User profile UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'category': fields.String(description='Preference category', enum=['NOTIFICATIONS', 'PRIVACY', 'APPEARANCE'], example='NOTIFICATIONS'),
    'key': fields.String(description='Preference key', example='email_notifications'),
    'value': fields.Raw(description='Preference value (any JSON value)', example=True),
    'updated_at': fields.DateTime(description='Last update timestamp', example='2025-01-01T00:00:00Z')
})

preference_list_model = api.model('PreferenceList', {
    'success': fields.Boolean(description='Success status', example=True),
    'preferences': fields.List(fields.Nested(preference_response_model))
})

preference_detail_model = api.model('PreferenceDetail', {
    'success': fields.Boolean(description='Success status', example=True),
    'message': fields.String(description='Response message', example='Preference set successfully'),
    'preference': fields.Nested(preference_response_model)
})

preference_value_model = api.model('PreferenceValue', {
    'value': fields.Raw(description='Preference value (any JSON value)', example=True)
})

# Connection models
connection_response_model = api.model('ConnectionResponse', {
    'id': fields.String(description='Connection UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'requester_id': fields.String(description='Requester profile UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'recipient_id': fields.String(description='Recipient profile UUID', example='123e4567-e89b-12d3-a456-426614174000'),
    'status': fields.String(description='Connection status', enum=['PENDING', 'ACCEPTED', 'REJECTED'], example='ACCEPTED'),
    'created_at': fields.DateTime(description='Creation timestamp', example='2025-01-01T00:00:00Z'),
    'updated_at': fields.DateTime(description='Last update timestamp', example='2025-01-01T00:00:00Z')
})

connection_list_model = api.model('ConnectionList', {
    'success': fields.Boolean(description='Success status', example=True),
    'connections': fields.List(fields.Nested(connection_response_model))
})

connection_detail_model = api.model('ConnectionDetail', {
    'success': fields.Boolean(description='Success status', example=True),
    'message': fields.String(description='Response message', example='Connection request sent'),
    'connection': fields.Nested(connection_response_model)
})

connection_status_model = api.model('ConnectionStatus', {
    'status': fields.String(required=True, description='New connection status', enum=['ACCEPTED', 'REJECTED'], example='ACCEPTED')
})

# Error response model
error_model = api.model('ErrorResponse', {
    'success': fields.Boolean(description='Success status', example=False),
    'message': fields.String(description='Error message', example='An error occurred')
})

# Document API response codes with appropriate models
api_responses = {
    200: ('Success', profile_detail_model),
    201: ('Created', profile_detail_model),
    400: ('Bad Request', error_model),
    401: ('Unauthorized', error_model),
    403: ('Forbidden', error_model),
    404: ('Not Found', error_model),
    500: ('Server Error', error_model)
}