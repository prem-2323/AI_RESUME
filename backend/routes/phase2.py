from fastapi import APIRouter
from models.schemas import JDRequest
from services.ai_service import generate_response
import json

router = APIRouter()

@router.post("/analyze-jd")
def analyze_jd(data: JDRequest):

    prompt = f"""
    Analyze the following job description:

    {data.job_description}

    Return STRICTLY in JSON format:

    {{
        "preparation_roadmap": [
            "Step 1",
            "Step 2"
        ],
        "technical_skills": [
            "Skill1",
            "Skill2"
        ],
        "soft_skills": [
            "Skill1",
            "Skill2"
        ],
        "ats_keywords": [
            "Keyword1",
            "Keyword2"
        ],
        "suggested_projects": [
            "Project idea 1",
            "Project idea 2"
        ],
        "interview_focus_areas": [
            "Topic 1",
            "Topic 2"
        ]
    }}

    Make the preparation roadmap very clear and step-by-step.
    Do not include any text outside JSON.
    """

    result = generate_response(prompt)

    try:
        parsed_result = json.loads(result)
        return parsed_result
    except:
        return {"error": "AI response not valid JSON", "raw": result}
