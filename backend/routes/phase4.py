from fastapi import APIRouter
from models.schemas import CareerSwitchRequest
from services.ai_service import generate_response
import json

router = APIRouter()

@router.post("/career-switch")
def career_switch(data: CareerSwitchRequest):

    prompt = f"""
    A person currently working as '{data.current_role}' 
    wants to switch to '{data.target_role}'.

    Provide response STRICTLY in JSON format:

    {{
        "transferable_skills": [
            "Skill1",
            "Skill2"
        ],
        "skill_gap": [
            "Missing Skill1",
            "Missing Skill2"
        ],
        "career_switch_roadmap": [
            "Step 1",
            "Step 2"
        ],
        "suggested_projects_for_transition": [
            "Project1",
            "Project2"
        ],
        "future_prediction_5_years": "Detailed future prediction"
    }}

    Do not include any text outside JSON.
    """

    result = generate_response(prompt)

    try:
        parsed_result = json.loads(result)
        return parsed_result
    except:
        return {"error": "AI response not valid JSON", "raw": result}
