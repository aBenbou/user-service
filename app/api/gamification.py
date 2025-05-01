from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.gamification_service import GamificationService
from app.utils.decorators import rate_limit

gamification_bp = Blueprint('gamification', __name__)
gamification_service = GamificationService()

@gamification_bp.route('/progress', methods=['GET'])
@jwt_required()
@rate_limit
def get_progress():
    """Get user's gamification progress"""
    user_id = get_jwt_identity()
    progress = gamification_service.get_user_progress(user_id)
    
    if progress is None:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(progress), 200

@gamification_bp.route('/points', methods=['POST'])
@jwt_required()
@rate_limit
def add_points():
    """Add points to user's total"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'points' not in data or 'reason' not in data:
        return jsonify({'error': 'Points and reason are required'}), 400
    
    success, message = gamification_service.add_points(
        user_id,
        data['points'],
        data['reason']
    )
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400

@gamification_bp.route('/badges', methods=['GET'])
@jwt_required()
@rate_limit
def get_badges():
    """Get all badges for the user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'badges': [badge.to_dict() for badge in user.badges]
    }), 200

@gamification_bp.route('/badges/award', methods=['POST'])
@jwt_required()
@rate_limit
def award_badge():
    """Award a badge to user"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'type' not in data or 'requirement' not in data:
        return jsonify({'error': 'Badge type and requirement are required'}), 400
    
    success, message = gamification_service.award_badge(
        user_id,
        data['type'],
        data['requirement']
    )
    
    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 400 