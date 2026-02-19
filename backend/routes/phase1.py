from fastapi import APIRouter
from models.schemas import RoleRequest
from services.ai_service import generate_response
import json

router = APIRouter()

@router.post("/role-roadmap")
def role_roadmap(data: RoleRequest):

    prompt = f"""
    For the role: {data.role}

    Return the response STRICTLY in JSON format like this:

    {{
        "roadmap": "...",
        "required_skills": "...",
        "future_prediction": "..."
    }}

    Do not add any extra text outside JSON.
    """

    result = generate_response(prompt)

    try:
        parsed_result = json.loads(result)
        return parsed_result
    except:
        return {"error": "AI response not in valid JSON format", "raw": result}
