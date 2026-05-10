from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import Field
from fastapi import Path
from dotenv import load_dotenv
from groq import Groq
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title="Materna API",
    description="Materna is an AI-powered maternal health API that provides risk assessment, weekly pregnancy guidance, drug safety checks, antenatal scheduling, and delivery preparation — built for developers creating maternal health applications across Africa and beyond.",
    version="1.0.0"


)


def sanitize_input(text: str) -> str:
    forbidden_phrases = [
        "ignore previous instructions",
        "ignore all instructions",
        "disregard",
        "override",
        "system prompt",
        "jailbreak",
        "you are now",
        "act as"
    ]
    text_lower = text.lower()
    for phrase in forbidden_phrases:
        if phrase in text_lower:
            raise HTTPException(
                status_code=400,
                detail="Invalid input detected. Please enter a valid clinical term."
            )
    return text.strip()


def call_groq(prompt: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)


class RiskAssessmentRequest(BaseModel):
    trimester: int = Field(..., ge=1, le=3,
                           description="Trimester of pregnancy (1, 2, or 3)")
    symptoms: list[str] = Field(..., min_length=1,
                                max_length=100, description="List of symptoms")


@app.post("/v1/risk-assessment")
def risk_assessment(data: RiskAssessmentRequest):
    try:
        symptoms = [sanitize_input(s) for s in data.symptoms]
        prompt = f"""
      You are a clinical maternal health assistant. A pregnant woman in trimester {data.trimester} 
      is reporting the following symptoms: {', '.join(symptoms)}.

      Keep all field values concise — maximum 1-2 sentences per field.
    
      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "risk_level": "low | moderate | high",
          "urgency": "routine | monitor | seek care immediately",
          "recommendations": ["your recommendations here in array format"],
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}
      """

        result = call_groq(prompt)
        return result

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/v1/weekly-guidance/{week}")
def weekly_guidance(week: int = Path(..., ge=1, le=40, description="Week of pregnancy (1-40)")):
    try:
        prompt = f"""
      You are a clinical maternal health assistant. Provide weekly guidance for a pregnant woman at {week} weeks gestation.
    
       Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "week": {week},
          "fetal_development": "what is happening with the baby this week",
          "maternal_changes": "what the mother is experiencing this week",
          "nutrition_tips": "key nutrition advice for this week",
          "warning_signs": "symptoms to watch out for this week",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}
  """
        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


class DrugSafetyRequest(BaseModel):
    drug_name: str = Field(..., min_length=1, max_length=100,
                           description="Name of the drug")
    trimester: int = Field(..., ge=1, le=3,
                           description="Trimester of pregnancy (1, 2, or 3)")


@app.post("/v1/drug-safety")
def drug_safety(data: DrugSafetyRequest):
    try:
        drug_name = sanitize_input(data.drug_name)
        prompt = f"""
      You are a clinical maternal health assistant. A pregnant woman in her {data.trimester} trimester is asking about the safety of taking {drug_name}.
    
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "risk_level": "safe | caution | unsafe",
          "potential_effects": "possible effects on the mother and fetus",
          "alternatives": "safer alternatives if applicable",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}
      """
        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/v1/antenatal-schedule")
def antenatal_schedule():
    try:
        prompt = """
      You are a clinical maternal health assistant. Provide the complete recommended antenatal care schedule for a pregnant woman from booking to delivery, based on WHO and Nigerian FMOH guidelines.
    
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {
          "schedule": [
              {
                  "visit": "Booking visit",
                  "weeks": "Before 12 weeks",
                  "purpose": "what happens at this visit",
                  "tests": ["list", "of", "tests"],
                  "what_to_expect": "description"
              }
          ],
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }
      """

        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


class ConditionInformationRequest(BaseModel):
    condition: str = Field(..., min_length=1, max_length=100,
                           description="Name of the condition")


@app.post("/v1/condition-info")
def condition_info(data: ConditionInformationRequest):
    try:
        condition = sanitize_input(data.condition)
        prompt = f"""
      you are a clinical maternal health assistant. A pregnant woman is asking about {condition}. Provide information on this condition in pregnancy, including risks, management, and when to seek care.
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "condition": "{condition}",
          "description": "brief description of the condition",
          "symptoms": "common symptoms of this condition in pregnancy",
          "risks_in_pregnancy": "specific risks associated with this condition during pregnancy",
          "management": "general management strategies for pregnant women with this condition in array format",
          "when_to_seek_care": "specific symptoms or situations that should prompt immediate medical attention",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}      
  """
        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


class NutritionGuidanceRequest(BaseModel):
    trimester: int = Field(..., ge=1, le=3,
                           description="Trimester of pregnancy (1, 2, or 3)")
    dietary_restrictions: Optional[list[str]] = None
    nationality: str = Field(..., min_length=1, max_length=100,
                             description="Nationality of the pregnant woman")


@app.post("/v1/nutrition-guidance")
def nutrition_guidance(data: NutritionGuidanceRequest):
    try:
        dietary_restrictions = [sanitize_input(
            r) for r in data.dietary_restrictions] if data.dietary_restrictions else []
        nationality = sanitize_input(data.nationality)
        restrictions_text = f"with the following dietary restrictions: {', '.join(dietary_restrictions)}" if dietary_restrictions else "with no specific dietary restrictions"
        prompt = f"""
      You are a clinical maternal health assistant. Provide trimester-specific nutrition guidance for a pregnant woman in her {data.trimester} trimester {restrictions_text}. Tailor the advice to be culturally appropriate for someone from {nationality}.     
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "nutrient_priority": "key nutrients to focus on this trimester",
          "recommended_meals": "list of recommended meals or foods",
          "foods_to_avoid": "list of foods to avoid based on dietary restrictions and pregnancy",
          "cultural_tips": "any culturally specific advice or substitutions",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}
      """
        result = call_groq(prompt)
        return result

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


class DeliveryPrepRequest(BaseModel):
    week: int = Field(..., ge=1, le=40, description="Week of pregnancy")
    complications: Optional[list[str]] = Field(
        None, description="List of complications")


@app.post("/v1/delivery-prep")
def delivery_prep(data: DeliveryPrepRequest):
    try:
        complications = [sanitize_input(
            c) for c in data.complications] if data.complications else None
        complications_text = f"Consider the following complications: {', '.join(complications)}" if complications else "No specific complications reported."
        prompt = f"""
      You are a clinical maternal health assistant. Provide delivery preparation guidance for a pregnant woman at {data.week} weeks gestation. {complications_text}
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {{
          "preparation_steps": "key steps to prepare for delivery considering the complications in array format",
          "health_discussion": "important health discussions to have with the healthcare provider before delivery",
          "hospital_bag_checklist": "essential items to pack in the hospital bag in array format",
          "birth_preference": "considerations for birth preferences given the complications",
          "when_to_go_to_hospital": "specific signs or timing for when to go to the hospital",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }}
      """
        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/v1/labor-signs")
def labor_signs():
    try:
        prompt = """
      You are a clinical maternal health assistant. Provide comprehensive information on the signs of labor, including early signs, active labor signs, and when to seek medical attention.
      
      Keep all field values concise — maximum 1-2 sentences per field.

      Respond ONLY with a JSON object in this exact format, no extra text, no markdown:
      {
          "true_labor_signs": "signs that indicate true labor",
          "false_labor_signs": "signs that may mimic labor but are not true labor (Braxton Hicks contractions, etc.)",
          "early_signs": "common early signs of labor",
          "active_labor_signs": "signs that indicate active labor",
          "when_to_seek_care": "specific signs or situations that should prompt immediate medical attention",
          "disclaimer": "This is for informational purposes only. Always consult a qualified healthcare provider."
      }
      """
        result = call_groq(prompt)
        return result
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="AI returned an invalid response. Please try again.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")
