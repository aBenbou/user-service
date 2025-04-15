import json
import pytest
from uuid import UUID


def test_get_profile(client, test_profile, user_token):
    """Test getting a profile."""
    response = client.get(
        f"/api/profiles/{test_profile.id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["profile"]["username"] == test_profile.username


def test_get_my_profile(client, test_profile, user_token):
    """Test getting current user's profile."""
    response = client.get(
        "/api/profiles/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["profile"]["username"] == test_profile.username


def test_update_profile(client, test_profile, user_token):
    """Test updating a profile."""
    update_data = {
        "biography": "Updated by API test",
        "profession": "Test Engineer"
    }
    
    response = client.put(
        f"/api/profiles/{test_profile.id}",
        headers={"Authorization": f"Bearer {user_token}"},
        json=update_data
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["profile"]["biography"] == "Updated by API test"
    assert data["profile"]["profession"] == "Test Engineer"


def test_deactivate_profile(client, test_profile, user_token):
    """Test deactivating a profile."""
    response = client.put(
        "/api/profiles/deactivate",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert "Profile deactivated successfully" in data["message"]


def test_search_profiles(client, test_profile, user_token):
    """Test searching profiles."""
    response = client.get(
        "/api/profiles/search?q=test",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert len(data["profiles"]) > 0
    assert test_profile.username in [p["username"] for p in data["profiles"]]