from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# Allow frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename

        # Dummy logic for testing
        ats_score = 78  # In a real app, GPT or parsing logic would come here
        feedback = "Add more relevant keywords. Simplify formatting."

        return {
            "filename": filename,
            "score": ats_score,
            "feedback": feedback,
            "highlights": [
                {"text": "Professional Summary", "suggestion": "Add impact metrics"},
                {"text": "Skills", "suggestion": "Include more job-specific tools"}
            ]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
