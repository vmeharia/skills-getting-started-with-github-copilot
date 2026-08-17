"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)."""

import pytest


def test_signup_adds_participant_successfully(client):
    """Test that a new participant can sign up for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_verifies_participant_was_added(client):
    """Test that participant actually appears in the activity after signup."""
    # Arrange
    activity_name = "Programming Class"
    email = "alice@mergington.edu"
    
    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test that signup fails with 404 for non-existent activity."""
    # Arrange
    activity_name = "Non-Existent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_participant_rejected(client):
    """Test that a student cannot sign up twice for the same activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]


def test_signup_increases_participant_count(client):
    """Test that participant count increases after signup."""
    # Arrange
    activity_name = "Gym Class"
    email = "bob@mergington.edu"
    
    # Get initial count
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity_name]["participants"])
    
    # Act
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Get count after
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity_name]["participants"])
    
    # Assert
    assert count_after == count_before + 1


def test_signup_with_special_characters_in_email(client):
    """Test that signup works with valid emails containing special characters."""
    # Arrange
    activity_name = "Chess Club"
    email = "student.name+tag@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]
