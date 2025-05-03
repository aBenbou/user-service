from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.gamification import Points, Badge, UserBadge
from app import db

gamification_bp = Blueprint('gamification', __name__, url_prefix='/api/gamification')

@gamification_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Get user's gamification progress"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    # Calculate progress percentage (example: 1000 points per level)
    points_for_next_level = user.level * 1000
    progress_percentage = min(100, (user.total_points / points_for_next_level) * 100)
    
    # Get user's badges
    badges = [user_badge.badge.to_dict() for user_badge in user.user_badges]
    
    return jsonify({
        'level': user.level,
        'total_points': user.total_points,
        'progress_percentage': progress_percentage,
        'badges': badges
    })

@gamification_bp.route('/points', methods=['POST'])
@jwt_required()
def add_points():
    """Add points to user"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    points = data.get('points')
    reason = data.get('reason')
    
    if not points or points <= 0:
        return jsonify({'error': 'Invalid points value'}), 400
    
    # Add points record
    points_record = Points(
        user_id=user.id,
        amount=points,
        reason=reason
    )
    db.session.add(points_record)
    
    # Update user's total points
    user.total_points += points
    
    # Check for level up (1000 points per level)
    new_level = (user.total_points // 1000) + 1
    if new_level > user.level:
        user.level = new_level
    
    db.session.commit()
    
    return jsonify({
        'message': 'Points added successfully',
        'total_points': user.total_points,
        'level': user.level
    })

@gamification_bp.route('/badges', methods=['GET'])
@jwt_required()
def get_badges():
    """Get user's badges"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    badges = [user_badge.badge.to_dict() for user_badge in user.user_badges]
    
    return jsonify({
        'badges': badges
    })

@gamification_bp.route('/badges/award', methods=['POST'])
@jwt_required()
def award_badge():
    """Award a badge to user"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    data = request.get_json()
    badge_type = data.get('type')
    requirement = data.get('requirement')
    
    if not badge_type or not requirement:
        return jsonify({'error': 'Missing badge type or requirement'}), 400
    
    # Find the badge
    badge = Badge.query.filter_by(
        type=badge_type,
        requirement=requirement
    ).first_or_404()
    
    # Check if user already has this badge
    existing_badge = UserBadge.query.filter_by(
        user_id=user.id,
        badge_id=badge.id
    ).first()
    
    if existing_badge:
        return jsonify({'error': 'User already has this badge'}), 400
    
    # Award the badge
    user_badge = UserBadge(
        user_id=user.id,
        badge_id=badge.id
    )
    db.session.add(user_badge)
    db.session.commit()
    
    return jsonify({
        'message': 'Badge awarded successfully',
        'badge': badge.to_dict()
    }) 