from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from dotenv import load_dotenv
from job_seekers import analyze_skill_gap
from resume_screening import Invisible_extract_text_with_highlight, analyze_resume_with_ai, fetch_required_skills_from_role
import http.client

from routes import phase1,phase2,phase3,phase4


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not safe for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(phase1.router, prefix="/phase1")
app.include_router(phase2.router, prefix="/phase2")
app.include_router(phase3.router, prefix="/phase3")
app.include_router(phase4.router, prefix="/phase4")

def extract_text_from_pdf(file_obj) -> str:
    """Extract text from a PDF file-like object. Raises HTTPException on failure."""
    try:
        # Ensure we're at the beginning
        try:
            file_obj.seek(0)
        except Exception:
            pass

        reader = PdfReader(file_obj)
        texts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                texts.append(page_text)

        return "\n".join(texts).strip()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read PDF: {exc}")


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    job_role: Optional[str] = Form(None),
):
    # Validate at least JD or role provided
    if not job_description and not job_role:
        raise HTTPException(status_code=400, detail="Provide either job_description or job_role")

    # Basic content-type check
    if resume.content_type and "pdf" not in resume.content_type.lower():
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported")

    resume_text = extract_text_from_pdf(resume.file)

    result = analyze_skill_gap(resume_text, job_description=job_description, job_role=job_role)

    return {"analysis": result}

@app.post("/analyze-resumes")
async def resumes_screening(
    resumes: List[UploadFile] = File(...),
    job_description: Optional[str] = Form(None),
    job_role: Optional[str] = Form(None)
):

    if not job_description and not job_role:
        raise HTTPException(
            status_code=400,
            detail="Provide either job_description or job_role"
        )

    # If role given → fetch required skills using AI
    if job_role:
        required_skills = fetch_required_skills_from_role(job_role)
        job_text = f"Job Role: {job_role}\nRequired Skills: {', '.join(required_skills)}"
    else:
        job_text = job_description

    results = []

    

    for resume in resumes:
        resume.file.seek(0)
        resume_text = extract_text_from_pdf(resume.file)
        # print(resume_text)
        # print()

        resume.file.seek(0)
        invisible_text_list = Invisible_extract_text_with_highlight(resume.file)

        if invisible_text_list:
            for hidden_text in invisible_text_list:
                if hidden_text.strip():
                    resume_text = resume_text.replace(hidden_text.strip(), "")
        # print(resume_text)
        analysis = analyze_resume_with_ai(resume_text, job_text)

        results.append({
            "resume_name": resume.filename,
            "analysis": analysis
        })

    return results


@app.get('/')
def Welcome():
    return {"Greeting": "Welcome"}



# @app.post("/btn4_resume_JD")
# async def btn4(resume: UploadFile,resume2: UploadFile, JD: str = Form(...)) -> Dict[str, Any]:
#     """
#     Endpoint to analyze resume vs JD
#     Returns invisible text + final scores
#     """
#     # 1️⃣ Extract text with visibility info
#     df = extract_text_with_highlight(resume)

#     # 2️⃣ Compute final scores
#     final_score_visible, final_score_invisible = analyze_resume_vs_job(df, JD)
#     ATS_score = analyze_resume_format(resume2)

#         # Convert numpy types to native Python float
#     final_score_visible = float(final_score_visible)
#     final_score_invisible = float(final_score_invisible)

#     # 3️⃣ Get invisible text
#     invisible_text = ", ".join(df[df["Visible"] == False]["Text"].tolist())

#     # Replace multiple commas (with optional spaces between them) with single comma
#     cleaned_text = re.sub(r',\s*,+', ',', invisible_text)

#     # Also clean extra spaces around commas
#     cleaned_text = re.sub(r'\s*,\s*', ', ', cleaned_text)

#     # Remove trailing comma if exists
#     cleaned_text = cleaned_text.strip().rstrip(',')

#     return {
#         "invisible_text": cleaned_text,
#         "final_score_visible": round(final_score_visible,2),
#         "final_score_invisible": final_score_invisible,
#         "ATS Score" : ATS_score
#     }
