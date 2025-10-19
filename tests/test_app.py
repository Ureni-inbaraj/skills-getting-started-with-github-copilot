from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity_name = "Art Club"
    email = "test.user@example.com"

    # Ensure email is not already present
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    # Signup
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert signup_resp.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]

    # Signup again should fail
    signup_resp2 = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp2.status_code == 400

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert unregister_resp.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]

    # Unregister again should fail
    unregister_resp2 = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp2.status_code == 400
