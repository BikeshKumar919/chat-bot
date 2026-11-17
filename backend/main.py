from backend.services.batch_evaluator import evaluate_all_candidates
from typing import List
from fastapi import UploadFile, File
from pathlib import Path
from typing import List
import uuid
from fastapi.openapi.utils import get_openapi
from backend.services.resume_parser import extract_resume_text
from pydantic import BaseModel
from fastapi import HTTPException

from backend.services.job_analyzer import analyze_job_description

from fastapi import FastAPI, UploadFile, File, HTTPException

# --------------------------------
# 1. Initialize FastAPI
# --------------------------------

app = FastAPI(
    title="AI Resume Screening System",
    description="Upload and manage candidate resumes",
    version="1.0.0"
)

# --------------------------------
# Custom OpenAPI schema compatibility
# --------------------------------

from fastapi.openapi.utils import get_openapi

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    request_schema = (
        openapi_schema["paths"]["/resumes/upload"]
        ["post"]["requestBody"]["content"]["multipart/form-data"]["schema"]
    )

    # Resolve the schema reference
    if "$ref" in request_schema:

        schema_name = request_schema["$ref"].split("/")[-1]

        request_schema = openapi_schema["components"]["schemas"][schema_name]

    # Configure multiple file upload
    request_schema["properties"]["files"] = {
        "type": "array",
        "items": {
            "type": "string",
            "format": "binary"
        },
        "title": "Files"
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi



# --------------------------------
# 2. Configure upload directory
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB per file


# --------------------------------
# 3. Health API
# --------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "UP",
        "message": "Resume Screening API is running"
    }


# --------------------------------
# 4. Resume Upload API
# --------------------------------

@app.post("/resumes/upload")
async def upload_resumes(
    files: List[UploadFile] = File(...)
):

    if len(files) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 resumes can be uploaded at once"
        )

    uploaded_resumes = []

    for file in files:

        extension = Path(file.filename or "").suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file.filename}"
            )

        # Read file content
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail=f"Empty file: {file.filename}"
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File exceeds 5 MB limit: {file.filename}"
            )

        # Generate unique filename
        candidate_id = str(uuid.uuid4())

        saved_filename = f"{candidate_id}{extension}"

        file_path = UPLOAD_DIR / saved_filename

        # Save file
        file_path.write_bytes(content)

        uploaded_resumes.append({
            "candidate_id": candidate_id,
            "original_filename": file.filename,
            "saved_filename": saved_filename,
            "size_bytes": len(content),
            "status": "uploaded"
        })

    return {
        "message": "Resumes uploaded successfully",
        "total_uploaded": len(uploaded_resumes),
        "candidates": uploaded_resumes
    }


@app.post("/resumes/extract")
async def extract_resumes():

    results = []

    for file_path in UPLOAD_DIR.iterdir():

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            # Extract resume text
            extracted_text = extract_resume_text(file_path)

            if not extracted_text:
                results.append({
                    "candidate_id": file_path.stem,
                    "filename": file_path.name,
                    "status": "failed",
                    "message": "No text found in resume"
                })
                continue

            results.append({
                "candidate_id": file_path.stem,
                "filename": file_path.name,
                "status": "success",
                "character_count": len(extracted_text),
                "extracted_text": extracted_text
            })

        except Exception as error:

            results.append({
                "candidate_id": file_path.stem,
                "filename": file_path.name,
                "status": "failed",
                "message": str(error)
            })

    return {
        "total_processed": len(results),
        "successful": sum(
            1 for result in results
            if result["status"] == "success"
        ),
        "failed": sum(
            1 for result in results
            if result["status"] == "failed"
        ),
        "candidates": results
    }

class JobDescriptionRequest(BaseModel):
    job_description: str


@app.post("/jobs/analyze")
async def analyze_job(request: JobDescriptionRequest):

    try:
        result = analyze_job_description(
            request.job_description
        )

        return {
            "message": "Job description analyzed successfully",
            "job": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.post("/candidates/evaluate")
async def evaluate_candidates(request: JobDescriptionRequest):

    try:
        job = analyze_job_description(
            request.job_description
        )

        result = evaluate_all_candidates(
            upload_dir=UPLOAD_DIR,
            job=job
        )

        return {
            "message": "Candidate evaluation completed",
            "job": job,
            "evaluation": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )    