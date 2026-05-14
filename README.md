# Materna API
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Slimdan20/materna-api/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Slimdan20/materna-api/tree/main)
![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Groq](https://img.shields.io/badge/AI-Groq-orange)
![Pytest](https://img.shields.io/badge/tested%20with-pytest-blue)
![SlowAPI](https://img.shields.io/badge/rate%20limiting-SlowAPI-red)
![Render](https://img.shields.io/badge/deployed%20on-Render-purple)
![Swagger](https://img.shields.io/badge/docs-Swagger%20UI-green)
![License](https://img.shields.io/badge/license-MIT-blue)



## Overview

Materna is an AI-powered maternal health API built to close the developer tooling gap in African women's health tech. It gives developers clinical-grade pregnancy guidance, drug safety checks, and risk assessment through a clean REST interface.

## Base URL

All requests to the API are made using the following base URL:

https://materna-api-1.onrender.com

## Interactive Docs

Materna provides interactive Swagger documentation at:

https://materna-api-1.onrender.com/docs

<img width="3840" height="2160" alt="image" src="https://github.com/user-attachments/assets/7d3d44ec-c6b8-4e54-a4c1-4fe54b139506" />


## Quick start

Make your first request to the Materna API and fetch labor-signs data

**Note:** <i>Materna does not require an API key to make requests.</i>

- **Endpoint:** "v1/labor-signs"
- **Method:** "GET"
- **Request:**
```bash
curl https://materna-api-1.onrender.com/v1/labor-signs 
```
- **Response:**
Successful API call returns a `200 OK` response with JSON data:

```json
{
  "true_labor_signs": "Regular uterine contractions, cervical dilation, and effacement indicate true labor",
  "false_labor_signs": "Braxton Hicks contractions, false labor pains, and practice contractions may mimic labor but are not true labor",
  "early_signs": "Light contractions, back pain, and bloody show are common early signs of labor",
  "active_labor_signs": "Intense contractions, rapid cervical dilation, and fetal movement indicate active labor",
  "when_to_seek_care": "Seek medical attention if contractions are 5 minutes apart, water breaks, or severe pain occurs",
  "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
}
```

## Usage

You can integrate Materna API into frontend, backend, and mobile applications.

- **Javascript:**

```javascript
fetch('https://materna-api-1.onrender.com/v1/labor-signs')
  .then(response => {
    if (!response.ok) throw new Error('Network response was not ok');
    return response.json();
  })
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

- **Python:**

```python
import requests

url = "https://materna-api-1.onrender.com/v1/labor-signs"

try:
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()
    print(data)

except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")

except requests.exceptions.ConnectionError:
    print("Connection error. Unable to reach the API.")

except requests.exceptions.Timeout:
    print("Request timed out.")

except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
```

## Features

- Assess pregnancy-related risks using trimester data and client-submitted symptoms.
- Generate weekly maternal and fetal pregnancy guidance based on gestational week.
- Evaluate medication safety during pregnancy across different trimesters.
- Provide WHO-informed antenatal care schedules from booking visit to delivery.
- Evaluate user-submitted medical condition, returning structured condition information, including symptoms, pregnancy risks, and management guidance.
- Generate culturally tailored nutritional recommendations based on trimester and nationality.
- Differentiate true and false labor signs and provide guidance on when to seek medical attention.
- Validate incoming request payloads using Pydantic schemas.
- Includes automated API testing with Pytest and CI pipelines using CircleCI.

## Tech stack/architecture

Materna was built on the following stacks:

- FastAPI for API structure
- Pydantic for request validation
- Groq for AI output
- Pytest for integration and unit tests (endpoints and validation testing)
- CircleCI for automating testing and deployment
- SlowAPI for rate limiting
- Render for deployment
- Swagger UI for interactive API documentation

## Testing

Materna API uses Pytest and FastAPI TestClient for automated endpoint and validation testing.

Tests currently cover:

- Mocked AI responses to avoid real API calls during testing
- Invalid AI response handling
- Successful responses across all API endpoints
- Invalid request payloads
- Missing required fields
- Optional field handling
- Request validation and schema enforcement
- Error handling scenarios

## Continuous Integration / Deployment (CI/CD)

Materna API uses CircleCI to automate:

- Dependency installation
- Pytest test execution
- Deployment workflows to Render

This ensures endpoints are validated before deployment.

<img width="3840" height="1993" alt="Screenshot (653)" src="https://github.com/user-attachments/assets/d3a17d65-1dec-4a79-8615-7895110c3767" />

## API Endpoints

| Method |          Endpoint          | Description                                                  |
| ------ |          --------          | -----------                                                  |
| POST   | /v1/risk-assessment        | Assess pregnancy-related health risks                        |
| GET    | /v1/weekly-guidance/{week} | Generate weekly pregnancy guidance                           |
| POST   | /v1/drug-safety            | Evaluate medication safety during pregnancy                  |
| GET    | /v1/antenatal-schedule     | Return WHO-informed antenatal schedules                      |
| POST   | /v1/condition-info         | Provide pregnancy-related condition information              |
| POST   | /v1/nutritional-guidance     | Generate culturally tailored nutrition guidance              |
| POST   | /v1/delivery-prep          | Provide complication-based delivery preparation guidance     |
| GET    | /v1/labor-signs            | Return true and false labor indicators                       |

## Local Setup

To setup and utilize Materna API in your local computer, follow the outlined steps

**Step 1:** Clone the repository

```bash   
git clone https://github.com/Slimdan20/materna-api.git
```

**Step 2:** Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate       # Mac/Linux
```

**Step 3:** Install dependencies

```bash
pip install -r requirements.txt
```

**Step 4:** Create a `.env` file in your root directory

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Step 5:** Run the server

```bash
python -m uvicorn main:app --reload
```

Click on the provided docs URL to view your documented API.

## Disclaimer
Materna API is intended for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.
