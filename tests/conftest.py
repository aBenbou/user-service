import pytest
from app import create_app, db
from app.models.user import User
from app.models.gamification import Badge
from flask_jwt_extended import create_access_token

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
def user_token(test_user, app):
    """Return a valid JWT access token for the test user."""
    with app.app_context():
        return create_access_token(identity=str(test_user.id))

@pytest.fixture
def auth_headers(user_token):
    """Authorization header helper built from user_token."""
    return {'Authorization': f"Bearer {user_token}"}

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

@pytest.fixture(autouse=True)
def _stub_auth(monkeypatch):
    """Short-circuit outbound calls to the Auth service during tests."""
    # Pretend every token is valid
    monkeypatch.setattr(
        "app.utils.auth_client.validate_token",
        lambda token: {"success": True, "user_id": "stub-user"}
    )

    # Return empty permissions list for any user
    monkeypatch.setattr(
        "app.utils.auth_client.get_user_permissions",
        lambda _user_id: {"success": True, "permissions": []}
    )

# ---------------------------------------------------------------------------
# Domain fixtures
# ---------------------------------------------------------------------------

import datetime

@pytest.fixture
def test_profile(app, db_session, test_user):
    """Create a user profile linked to *test_user* for API/service tests."""
    from app.models.profile import UserProfile

    profile = UserProfile(
        id=str(test_user.id),
        username=test_user.username,
        first_name="Test",
        last_name="User",
        joined_at=datetime.datetime.utcnow(),
    )
    db_session.add(profile)
    db_session.commit()

    yield profile

    # Teardown – remove profile explicitly to avoid leakage between tests.
    db_session.delete(profile)
    db_session.commit()

# Provide an application context automatically for all tests that need it.
# This avoids the "Working outside of application context" runtime errors when
# service-layer functions invoke Flask-SQLAlchemy models directly.

@pytest.fixture(autouse=True)
def app_context(app):
    """Push a Flask app context for the duration of each test."""
    with app.app_context():
        yield
