"""Tests for the activities endpoint (GET /activities)."""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    # Arrange
    expected_activity_count = 3
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    assert set(activities.keys()) == expected_activity_names


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the required fields."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"


def test_get_activities_participants_is_list(client):
    """Test that participants field is a list."""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list), \
            f"Activity '{activity_name}' participants should be a list"


def test_get_activities_max_participants_is_integer(client):
    """Test that max_participants is an integer."""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int), \
            f"Activity '{activity_name}' max_participants should be an integer"
