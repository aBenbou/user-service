import os
import pytest
from datetime import datetime
from uuid import uuid4
from flask_jwt_extended import create_access_token
from unittest.mock import patch, MagicMock

from app import create_app, db
from app.models.profile import UserProfile
from app.models.expertise import ExpertiseArea
from app.models.preference import UserPreference
from app.models.connection import UserConnection


@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set test configurations
    os.environ["FLASK_ENV"] = "testing"
    os.environ["TESTING"] = "True"
    os.environ["SECRET_KEY"] = "test-key"
    os.environ["JWT_SECRET_KEY"] = "test-jwt-key"
    os.environ["DATABASE_URI"] = "sqlite:///:memory:"
    
    app = create_app('testing')
    
    # Create a test context
    ctx = app.app_context()
    ctx.push()
    
    # Set up the test database
    db.create_all()
    
    yield app
    
    # Clean up
    db.session.remove()
    db.drop_all()
    
    # Pop the context
    ctx.pop()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """Create a new database session for a test."""
    yield db.session


@pytest.fixture
def test_user_id():
    """Generate a test user ID."""
    return uuid4()


@pytest.fixture
def test_profile(db_session, test_user_id):
    """Create a test user profile."""
    profile = UserProfile(
        id=test_user_id,
        first_name="Test",
        last_name="User",
        username="testuser",
        biography="Test biography",
        profession="Software Engineer",
        company="Test Company",
        current_job="Senior Developer",
        visibility="PUBLIC",
        joined_at=datetime.utcnow()
    )
    db_session.add(profile)
    db_session.commit()
    return profile


@pytest.fixture
def test_expertise(db_session, test_profile):
    """Create a test expertise area."""
    expertise = ExpertiseArea(
        user_id=test_profile.id,
        domain="Python Programming",
        level="EXPERT",
        years_experience=5
    )
    db_session.add(expertise)
    db_session.commit()
    return expertise


@pytest.fixture
def test_preference(db_session, test_profile):
    """Create a test user preference."""
    preference = UserPreference(
        user_id=test_profile.id,
        category="NOTIFICATIONS",
        key="email_notifications",
        value={"enabled": True}
    )
    db_session.add(preference)
    db_session.commit()
    return preference


@pytest.fixture
def test_connection(db_session):
    """Create a test connection between two users."""
    user1_id = uuid4()
    user2_id = uuid4()
    
    # Create profiles
    profile1 = UserProfile(id=user1_id, username="user1")
    profile2 = UserProfile(id=user2_id, username="user2")
    db_session.add_all([profile1, profile2])
    db_session.commit()
    
    # Create connection
    connection = UserConnection(
        requester_id=user1_id,
        recipient_id=user2_id,
        status="PENDING"
    )
    db_session.add(connection)
    db_session.commit()
    
    return {
        "connection": connection,
        "requester": profile1,
        "recipient": profile2
    }


@pytest.fixture
def user_token(app, test_user_id):
    """Generate a JWT token for the test user."""
    with app.app_context():
        access_token = create_access_token(identity=str(test_user_id))
        return access_token


@pytest.fixture
def mock_auth_client():
    """Mock the auth client for testing."""
    with patch('app.utils.auth_client.validate_token') as mock_validate:
        mock_validate.return_value = {"success": True, "user_id": "test-user-id"}
        
        with patch('app.utils.auth_client.get_user_permissions') as mock_permissions:
            mock_permissions.return_value = {
                "success": True,
                "permissions": ["profile:read", "profile:write"]
            }
            
            with patch('app.utils.auth_client.is_admin') as mock_is_admin:
                mock_is_admin.return_value = False
                
                with patch('app.utils.auth_client.is_owner_or_admin') as mock_is_owner:
                    mock_is_owner.return_value = True
                    yield {
                        "validate_token": mock_validate,
                        "get_permissions": mock_permissions,
                        "is_admin": mock_is_admin,
                        "is_owner": mock_is_owner
                    }