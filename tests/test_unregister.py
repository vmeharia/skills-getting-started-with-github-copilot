"""Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister)."""

import pytest


def test_unregister_removes_participant_successfully(client):
    """Test that a participant can successfully unregister from an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_verifies_participant_was_removed(client):
    """Test that participant actually disappears from the activity after unregister."""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already registered
    
    # Act
    client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test that unregister fails with 404 for non-existent activity."""
    # Arrange
    activity_name = "Non-Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_participant_not_registered(client):
    """Test that unregister fails with 400 if student is not registered."""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"  # Not registered
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"]


def test_unregister_decreases_participant_count(client):
    """Test that participant count decreases after unregister."""
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"  # Already registered
    
    # Get initial count
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity_name]["participants"])
    
    # Act
    client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Get count after
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity_name]["participants"])
    
    # Assert
    assert count_after == count_before - 1


def test_unregister_then_signup_same_participant(client):
    """Test that a participant can unregister and then sign up again."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act - Unregister
    response_unregister = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Act - Sign up again
    response_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response_unregister.status_code == 200
    assert response_signup.status_code == 200
    
    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]
