from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF
import os
import tempfile
import openai
from openai import AzureOpenAI
from typing import List

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure OpenAI configuration
client = AzureOpenAI(
    api_key="4OyA2iUgG0fkNy0iDLmaFrVC4Bka9UX1vIzMxHUkkocofV3hMEJmJQQJ99BFACHYHv6XJ3w3AAAAACOGKE2f",  # Replace this
    api_version="2024-12-01-preview",  # Or your version
    azure_endpoint="https://mayur-mbxk520z-eastus2.cognitiveservices.azure.com/"  # Replace this
)

DEPLOYMENT_NAME = "gpt-4o"  # Replace with your model deployment name


# Response model
class AnalysisResponse(BaseModel):
    ats_score: int
    suggestions: List[str]


def extract_text_from_pdf(pdf_file_path: str) -> str:
    text = ""
    with fitz.open(pdf_file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def analyze_resume_text(text: str) -> AnalysisResponse:
    prompt = f"""
You are an expert ATS (Applicant Tracking System) resume analyzer. Given the resume text below, provide:

1. An ATS-friendliness score out of 100.
2. A few key suggestions to improve the resume for better ATS performance.

Resume:
{text}
"""
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are an ATS resume analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        # Parse score and suggestions
        score_line = next((line for line in reply.splitlines() if "score" in line.lower()), "ATS Score: 70")
        ats_score = int(''.join(filter(str.isdigit, score_line)))

        suggestions = [line.strip("-• ").strip() for line in reply.splitlines()
                       if line.strip().startswith(("-", "•"))]

        return AnalysisResponse(ats_score=ats_score, suggestions=suggestions)

    except Exception as e:
        return AnalysisResponse(ats_score=50, suggestions=[f"Error: {str(e)}"])


@app.post("/analyze_resume/", response_model=AnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        resume_text = extract_text_from_pdf(tmp_path)
        result = analyze_resume_text(resume_text)

        os.remove(tmp_path)
        return result

    except Exception as e:
        return AnalysisResponse(ats_score=0, suggestions=[f"Internal server error: {str(e)}"])
