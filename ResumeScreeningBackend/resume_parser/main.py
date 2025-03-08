import logging
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import List
import os
import shutil
import uuid
import spacy
import json
import re
import fitz  # PyMuPDF
from gemini_api import analyze_with_gemini
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

# Allow CORS from the frontend (Angular app)
origins = [
    "http://localhost:4200",  # Allow Angular frontend to communicate with FastAPI
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load spaCy model (not used for filtering anymore, but could be reused if needed)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text

def process_gemini_response(response_json: dict) -> dict:
    """
    Process the Gemini API response to extract only the candidate data from the code block.
    Gemini returns candidate details inside a Markdown code block. This function extracts the JSON inside.
    """
    processed_candidates = []
    candidates = response_json.get("candidates", [])
    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        if parts and "text" in parts[0]:
            raw_text = parts[0]["text"]
            # Use regex to extract JSON from the Markdown code block
            match = re.search(r"```json\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
            if match:
                try:
                    candidate_data = json.loads(match.group(1))
                    processed_candidates.append(candidate_data)
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding candidate JSON: {e}")
                    continue
    # You can return a single candidate if that's what you expect,
    # or a list if multiple candidates are returned.
    return {
        "candidates": processed_candidates,
        "usageMetadata": response_json.get("usageMetadata", {}),
        "modelVersion": response_json.get("modelVersion", "")
    }

@app.post("/parse_resume/")
async def parse_resume(
    jobTitle: str = Form(...),
    minExperience: int = Form(...),
    qualification: str = Form(...),
    requiredSkills: str = Form(...),
    description: str = Form(...),
    resumes: List[UploadFile] = File(...),
):
    logging.debug(f"Received job description: {jobTitle}, {minExperience}, {qualification}, {requiredSkills}, {description}")
    resume_results = []

    if not requiredSkills:
        logging.error("Required skills are missing.")
        raise HTTPException(status_code=400, detail="Required skills are missing")

    for resume_file in resumes:
        try:
            logging.debug(f"Processing resume: {resume_file.filename}")
            unique_filename = f"{uuid.uuid4()}.pdf"
            resume_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            with open(resume_path, "wb") as buffer:
                shutil.copyfileobj(resume_file.file, buffer)
            
            # Extract the entire text from the PDF
            resume_text = extract_text_from_pdf(resume_path)
            
            # Send the entire resume text along with job details to Gemini
            gemini_response = analyze_with_gemini(
                jobTitle=jobTitle,
                minExperience=minExperience,
                qualification=qualification,
                requiredSkills=requiredSkills,
                description=description,
                resume_text=resume_text
            )
            
            logging.debug(f"Raw Gemini response: {gemini_response}")
            if gemini_response.get("error"):
                logging.error(f"Gemini API error: {gemini_response.get('error')}")
                raise HTTPException(status_code=500, detail="Gemini API error: " + gemini_response.get("error"))
            
            # Process the Gemini API response to extract only necessary candidate data
            processed_response = process_gemini_response(gemini_response)
            logging.debug(f"Processed Gemini response: {processed_response}")
            
            resume_results.append(processed_response)
        except Exception as e:
            logging.error(f"Error processing resume: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
    
    logging.debug(f"Returning results: {resume_results}")
    return {"resume_results": resume_results}
