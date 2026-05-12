from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_risk_assessment():
    response = client.post(
        "/v1/risk-assessment",
        json={
            "trimester": 2,
            "symptoms": ["headache", "blurred vision"],
        }
        )
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert "urgency" in data
    assert "recommendations" in data
