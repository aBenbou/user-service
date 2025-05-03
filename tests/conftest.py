import pytest
from app import create_app, db
from app.models.user import User
from app.models.gamification import Badge

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Create initial badges
        Badge.create_initial_badges()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app, db_session):
    user = User(
        email='test@example.com',
        username='testuser'
    )
    user.set_password('testpassword')
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def auth_headers(test_user, client):
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    tokens = response.get_json()
    return {'Authorization': f"Bearer {tokens['access_token']}"}

@pytest.fixture
def db_session(app):
    """Create a fresh database session for each test."""
    with app.app_context():
        # Start a transaction
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Create a session bound to the connection
        session = db.session(bind=connection)
        
        # Begin a nested transaction
        session.begin_nested()
        
        yield session
        
        # Roll back the nested transaction
        session.rollback()
        
        # Close the session and connection
        session.close()
        connection.close()
