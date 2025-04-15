import pytest
from uuid import uuid4
from app.services.profile_service import (
    get_profile_by_id,
    get_my_profile,
    create_profile,
    update_profile,
    deactivate_profile,
    search_profiles
)


def test_get_profile_by_id(test_profile):
    """Test getting a profile by ID."""
    profile = get_profile_by_id(test_profile.id)
    assert profile is not None
    assert profile["username"] == test_profile.username


def test_get_profile_by_id_not_found():
    """Test getting a non-existent profile."""
    profile = get_profile_by_id(uuid4())
    assert profile is None


def test_get_my_profile(test_profile):
    """Test getting current user's profile."""
    profile = get_my_profile(test_profile.id)
    assert profile is not None
    assert profile["username"] == test_profile.username
    assert "biography" in profile  # Private fields included


def test_create_profile():
    """Test creating a new profile."""
    user_id = uuid4()
    data = {
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "visibility": "PUBLIC"
    }
    
    result = create_profile(user_id, data)
    assert result["success"] is True
    assert result["profile"]["username"] == "newuser"


def test_update_profile(test_profile):
    """Test updating a profile."""
    data = {
        "biography": "Updated biography",
        "profession": "Updated profession"
    }
    
    result = update_profile(test_profile.id, data)
    assert result["success"] is True
    assert result["profile"]["biography"] == "Updated biography"
    assert result["profile"]["profession"] == "Updated profession"


def test_deactivate_profile(test_profile):
    """Test deactivating a profile."""
    result = deactivate_profile(test_profile.id)
    assert result["success"] is True
    
    # Verify profile is deactivated
    profile = get_profile_by_id(test_profile.id)
    assert profile is None