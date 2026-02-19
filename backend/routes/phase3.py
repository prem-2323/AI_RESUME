from fastapi import APIRouter
from models.schemas import CompanyRoleRequest
from services.ai_service import generate_response
import json

router = APIRouter()

@router.post("/company-role-analysis")
def company_role_analysis(data: CompanyRoleRequest):

    prompt = f"""
    Provide detailed preparation guidance for the role 
    '{data.job_role}' at the company '{data.company_name}'.

    Return STRICTLY in JSON format:

    {{
        "preparation_roadmap": [
            "Step 1",
            "Step 2"
        ],
        "preferred_skills_by_company": [
            "Skill1",
            "Skill2"
        ],
        "hiring_trends_in_company": [
            "Trend1",
            "Trend2"
        ],
        "future_prediction_5_years": "Detailed future prediction text"
    }}

    Do not include any extra text outside JSON.
    """

    result = generate_response(prompt)

    try:
        parsed_result = json.loads(result)
        return parsed_result
    except:
        return {"error": "AI response not valid JSON", "raw": result}
