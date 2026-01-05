from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success():
    # Test signing up a new participant
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]


def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    # Try again
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # First signup
    client.post("/activities/Gym%20Class/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Gym%20Class/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Gym Class" in data["message"]

    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Gym Class"]["participants"]


def test_unregister_not_signed_up():
    response = client.delete("/activities/Basketball%20Team/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up for this activity" in data["detail"]


def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent%20Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]