from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import openai, os, fitz, tempfile
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-12-01-preview"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...)):
    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(contents)
        temp_path = temp.name

    doc = fitz.open(temp_path)
    text = ""
    for page in doc:
        text += page.get_text()

    response = openai.ChatCompletion.create(
        deployment_id=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=[
            {"role": "system", "content": "You are an expert ATS resume analyzer."},
            {"role": "user", "content": f"Analyze this resume for ATS friendliness and give score + feedback:\n\n{text}"}
        ],
        temperature=0.3
    )
    feedback = response['choices'][0]['message']['content']
    return {"feedback": feedback}
