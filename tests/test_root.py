"""Tests for the root endpoint (GET /)."""


def test_root_redirects_to_static_index(client):
    """Test that root endpoint redirects to static/index.html."""
    # Arrange
    expected_url = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == expected_url
