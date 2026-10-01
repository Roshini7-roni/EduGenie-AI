from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text


def test_health_page():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_validation_rejects_empty_question():
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422


def test_validation_rejects_too_many_quiz_questions():
    response = client.post("/quiz", json={"text": "A lesson", "count": 11})
    assert response.status_code == 422
