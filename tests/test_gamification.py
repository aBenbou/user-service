import pytest
from app.models.gamification import Badge, Points, UserBadge
from app.models.user import User

def test_gamification_flow(client, auth_headers, test_user, db_session):
    """Test the complete gamification flow"""
    # 1. Get initial progress
    progress_response = client.get('/api/gamification/progress', headers=auth_headers)
    assert progress_response.status_code == 200
    initial_progress = progress_response.get_json()
    assert initial_progress["level"] == 1
    assert initial_progress["total_points"] == 0
    
    # 2. Add points
    points_response = client.post('/api/gamification/points', 
                                headers=auth_headers,
                                json={'points': 500, 'reason': 'Test points'})
    assert points_response.status_code == 200
    
    # 3. Check progress after points
    progress_response = client.get('/api/gamification/progress', headers=auth_headers)
    assert progress_response.status_code == 200
    new_progress = progress_response.get_json()
    assert new_progress["total_points"] == 500
    
    # 4. Award badge
    badge_response = client.post('/api/gamification/badges/award',
                                headers=auth_headers,
                                json={'type': 'level', 'requirement': '1'})
    assert badge_response.status_code == 200
    
    # 5. Check badges
    badges_response = client.get('/api/gamification/badges', headers=auth_headers)
    assert badges_response.status_code == 200
    badges = badges_response.get_json()
    assert len(badges["badges"]) > 0

def test_level_progression(client, auth_headers, test_user, db_session):
    """Test level progression system"""
    # 1. Add enough points to level up
    points_response = client.post('/api/gamification/points',
                                headers=auth_headers,
                                json={'points': 1500, 'reason': 'Level up test'})
    assert points_response.status_code == 200
    
    # 2. Check level progression
    progress_response = client.get('/api/gamification/progress', headers=auth_headers)
    assert progress_response.status_code == 200
    progress = progress_response.get_json()
    assert progress["level"] > 1
    assert progress["progress_percentage"] > 0

def test_badge_system(client, auth_headers, test_user, db_session):
    """Test badge awarding system"""
    # 1. Try to award invalid badge
    invalid_badge_response = client.post('/api/gamification/badges/award',
                                       headers=auth_headers,
                                       json={'type': 'invalid', 'requirement': 'invalid'})
    assert invalid_badge_response.status_code == 400
    
    # 2. Award valid badge
    valid_badge_response = client.post('/api/gamification/badges/award',
                                     headers=auth_headers,
                                     json={'type': 'level', 'requirement': '1'})
    assert valid_badge_response.status_code == 200
    
    # 3. Try to award same badge again
    duplicate_badge_response = client.post('/api/gamification/badges/award',
                                         headers=auth_headers,
                                         json={'type': 'level', 'requirement': '1'})
    assert duplicate_badge_response.status_code == 400

def test_get_progress(client, auth_headers, test_user):
    """Test getting user's gamification progress"""
    response = client.get('/api/gamification/progress', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['level'] == 1
    assert data['total_points'] == 0
    assert 'progress_percentage' in data
    assert 'badges' in data

def test_add_points(client, auth_headers, test_user, db_session):
    """Test adding points to user"""
    response = client.post('/api/gamification/points', 
                          headers=auth_headers,
                          json={'points': 500, 'reason': 'Test points'})
    assert response.status_code == 200
    
    # Verify points were added
    user = db_session.query(User).get(test_user.id)
    assert user.total_points == 500
    
    # Verify points record was created
    points = db_session.query(Points).filter_by(user_id=test_user.id).first()
    assert points is not None
    assert points.amount == 500
    assert points.reason == 'Test points'

def test_level_up(client, auth_headers, test_user, db_session):
    """Test user leveling up when reaching points threshold"""
    # Add enough points to level up
    response = client.post('/api/gamification/points', 
                          headers=auth_headers,
                          json={'points': 1000, 'reason': 'Level up test'})
    assert response.status_code == 200
    
    # Verify level up
    user = db_session.query(User).get(test_user.id)
    assert user.level == 2
    assert user.total_points == 1000

def test_get_badges(client, auth_headers, test_user):
    """Test getting user's badges"""
    response = client.get('/api/gamification/badges', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'badges' in data
    assert isinstance(data['badges'], list)

def test_award_badge(client, auth_headers, test_user, db_session):
    """Test awarding a badge to user"""
    response = client.post('/api/gamification/badges/award',
                          headers=auth_headers,
                          json={'type': 'level', 'requirement': '1'})
    assert response.status_code == 200
    
    # Verify badge was awarded
    user_badge = db_session.query(UserBadge).filter_by(user_id=test_user.id).first()
    assert user_badge is not None
    assert user_badge.badge.type == 'level'
    assert user_badge.badge.requirement == '1'

def test_duplicate_badge_award(client, auth_headers, test_user, db_session):
    """Test attempting to award the same badge twice"""
    # Award badge first time
    response = client.post('/api/gamification/badges/award',
                          headers=auth_headers,
                          json={'type': 'level', 'requirement': '1'})
    assert response.status_code == 200
    
    # Try to award same badge again
    response = client.post('/api/gamification/badges/award',
                          headers=auth_headers,
                          json={'type': 'level', 'requirement': '1'})
    assert response.status_code == 400
    assert 'already has this badge' in response.get_json()['message']

def test_invalid_points(client, auth_headers):
    """Test adding points with invalid data"""
    response = client.post('/api/gamification/points',
                          headers=auth_headers,
                          json={'points': -100, 'reason': 'Invalid points'})
    assert response.status_code == 400

def test_invalid_badge_award(client, auth_headers):
    """Test awarding non-existent badge"""
    response = client.post('/api/gamification/badges/award',
                          headers=auth_headers,
                          json={'type': 'invalid', 'requirement': '999'})
    assert response.status_code == 400
    assert 'Badge not found' in response.get_json()['message'] 