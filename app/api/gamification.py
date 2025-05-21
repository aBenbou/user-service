from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.gamification_service import GamificationService
from app.utils.responses import success_response, error_response

gamification_bp = Blueprint('gamification', __name__, url_prefix='/api/gamification')

# Instantiate the service once (it does not hold state between requests)
service = GamificationService()

@gamification_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Return current user's gamification progress."""
    user_id = get_jwt_identity()
    progress = service.get_user_progress(user_id)
    if progress is None:
        return error_response('User not found', 404)
    return success_response(progress, 200)

@gamification_bp.route('/points', methods=['POST'])
@jwt_required()
def add_points():
    """Add points to the current user."""
    data = request.get_json() or {}
    points = data.get('points')
    reason = data.get('reason', 'other')

    # Basic validation
    if not isinstance(points, int) or points <= 0:
        return error_response('Invalid points value', 400)

    success, message = service.add_points(get_jwt_identity(), points, reason)
    if not success:
        return error_response(message, 400)

    # Return updated progress for convenience
    progress = service.get_user_progress(get_jwt_identity())
    return success_response({'message': message, 'progress': progress}, 200)

@gamification_bp.route('/badges', methods=['GET'])
@jwt_required()
def get_badges():
    """Return list of badges for the current user."""
    progress = service.get_user_progress(get_jwt_identity())
    if progress is None:
        return error_response('User not found', 404)
    return success_response({'badges': progress['badges']}, 200)

@gamification_bp.route('/badges/award', methods=['POST'])
@jwt_required()
def award_badge():
    """Award a specific badge to the current user."""
    data = request.get_json() or {}
    badge_type = data.get('type')
    requirement = data.get('requirement')

    if not badge_type or not requirement:
        return error_response('Missing badge type or requirement', 400)

    success, message, badge = service.award_badge(get_jwt_identity(), badge_type, requirement)
    if success:
        response = {'message': message}
        if badge:
            response['badge'] = badge
        return success_response(response, 200)
    return error_response(message, 400) 