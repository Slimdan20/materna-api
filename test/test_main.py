from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_groq
import json

client = TestClient(app)

def test_invalid_ai_response():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content="not valid json"
                )
            )]
        )
        return fake

    app.dependency_overrides[get_groq] = fake_get_groq

    response = client.post(
        "/v1/risk-assessment",
        json={
            "trimester": 2,
            "symptoms": ["headache"]
        }
    )

    assert response.status_code == 500

def test_risk_assessment():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "risk_level": "high",
                        "urgency": "immediate",
                        "recommendations": ["Consult your healthcare provider immediately"],
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
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


def test_weekly_guidance():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "week": 20,
                        "fetal_development": "The fetus is developing rapidly, with all major organs forming.",
                        "maternal_changes": "You may experience increased fatigue and mood swings.",
                        "nutritional_tips": "Consult your healthcare provider immediately",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    response = client.get("/v1/weekly-guidance/20")
    assert response.status_code == 200
    data = response.json()
    assert "week" in data
    assert "fetal_development" in data
    assert "maternal_changes" in data


def test_drug_safety():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "risk_level": "low",
                        "potential_effects": "effects on fetal development are minimal",
                        "alternatives": "paracetamol",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )
            ])

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq

    response = client.post(
        "/v1/drug-safety",
        json={
            "drug_name": "Ibuprofen",
            "trimester": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "risk_level" in data
    assert "potential_effects" in data
    assert "alternatives" in data


def test_antenatal_schedule():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "schedule": [
                            {
                                "visit": "booking visit",
                                "weeks": "before 12 weeks",
                                "purpose": "Initial consultation and health assessment",
                                "tests": ["Physical Examination", "Blood Tests"]
                            }
                        ],
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    response = client.get("/v1/antenatal-schedule")
    assert response.status_code == 200
    data = response.json()
    assert "weeks" in data["schedule"][0]
    assert "purpose" in data["schedule"][0]
    assert "tests" in data["schedule"][0]


def test_condition_info():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "condition": "Gestational Diabetes",
                        "description": "A type of diabetes that develops during pregnancy.",
                        "symptoms": ["Increased thirst", "Frequent urination"],
                        "management": "Dietary changes, regular exercise, and monitoring blood sugar levels.",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    response = client.post(
        "/v1/condition-info",
        json={
            "condition": "Gestational Diabetes"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "condition" in data
    assert "description" in data
    assert "symptoms" in data
    assert "management" in data
    assert "disclaimer" in data


def test_nutritional_guidance():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "nutrient_priority": "Folic acid, iron, calcium, and protein are essential nutrients during pregnancy.",
                        "recommended_meals": "Focus on folic acid-rich foods, such as leafy greens and fortified cereals.",
                        "foods_to_avoid": "This is for informational purposes only. Always consult a qualified healthcare provider.",
                        "disclaimer": "Avoid high-mercury fish, unpasteurized dairy products, and undercooked meats."
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    response = client.post(
        "/v1/nutritional-guidance",
        json={
            "trimester": 1,
            "nationality": "Indian"
        })
    assert response.status_code == 200
    data = response.json()
    assert "nutrient_priority" in data
    assert "recommended_meals" in data
    assert "foods_to_avoid" in data


def test_delivery_prep():
    def fake_groq_call():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "preparation_steps": "monitor fetal movements, attend childbirth classes, and create a birth plan.",
                        "health_discussion": "discuss pain management options, labor signs, and postpartum care with your healthcare provider.",
                        "hospital_bag_checklist": "comfortable clothing, toiletries, important documents, and items for the baby.",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )
        return fake
    app.dependency_overrides[get_groq] = fake_groq_call
    response = client.post(
        "/v1/delivery-prep",
        json={
            "week": 20
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "preparation_steps" in data
    assert "health_discussion" in data
    assert "hospital_bag_checklist" in data


def test_labour_signs():
    def fake_get_groq():
        fake = MagicMock()
        fake.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "true_labor_signs": "cervical dilation, regular contractions, and water breaking.",
                        "false_labor_signs": "braxton hicks contractions, irregular contractions, and no cervical changes.",
                        "early_signs": "light spotting, backache, and pelvic pressure.",
                        "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
                    })
                )
            )]
        )

        return fake

    app.dependency_overrides[get_groq] = fake_get_groq
    response = client.get(
        "/v1/labor-signs"
    )
    assert response.status_code == 200
    data = response.json()
    assert "true_labor_signs" in data
    assert "false_labor_signs" in data
    assert "early_signs" in data

def test_invalid_trimester():
    response = client.post(
        "/v1/risk-assessment",
        json={
            "trimester": 5,
            "symptoms": ["headache", "blurred vision"]
        }
    )

    assert response.status_code == 422

def test_missing_symptoms():
    response = client.post(
        "/v1/risk-assessment",
        json={
            "trimester": 2
        }
    )

    assert response.status_code == 422

def test_wrong_data_types():
    response = client.post(
        "/v1/risk-assessment",
        json={
            "trimester": "second",
            "symptoms": ["headache", "blurred vision"]
        }
    )

    assert response.status_code == 422
    
def test_invalid_week():
    response = client.get("/v1/weekly-guidance/50")
    assert response.status_code == 422

def test_optional_fields():
    response = client.post(
        "/v1/nutritional-guidance",
        json={
            "trimester": 3,
            "nationality": "indian"
        }
    )
    assert response.status_code == 200

