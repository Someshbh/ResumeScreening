import os
import requests
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def analyze_with_gemini(jobTitle, minExperience, qualification, requiredSkills, description, resume_text):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        logging.error("Gemini API key is missing! Please set the GEMINI_API_KEY environment variable.")
        raise ValueError("Gemini API key is missing! Please set the GEMINI_API_KEY environment variable.")
    
    # Use the correct endpoint for Gemini-2.0 Flash (update if needed)
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # Construct a combined prompt containing all necessary details
    prompt = (
        f"Job Title: {jobTitle}\n"
        f"Minimum Experience: {minExperience}\n"
        f"Qualification: {qualification}\n"
        f"Required Skills: {requiredSkills}\n"
        f"Job Description: {description}\n\n"
        f"Resume Text:\n{resume_text}\n\n"
        f"Please extract and return the following details as JSON:\n"
        f"- Candidate's Name\n"
        f"- Candidate's Email\n"
        f"- Candidate's Mobile\n"
        f"- Matching Percentage (how well the resume matches the job description and required skills)\n"
        f"- Missing Skills (if any)\n"
        f"- Candidate's Skills (skills mentioned by the candidate in their resume)\n"
        f"- Total Years of Experience\n"
        f"- A brief Experience Summary"
    )
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        logging.debug("Sending request to Gemini API...")
        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            logging.debug("Gemini API request successful.")
            return response.json()
        else:
            logging.error(f"Gemini API request failed with status code {response.status_code}. Response: {response.text}")
            return {
                "error": "Gemini API request failed",
                "status_code": response.status_code,
                "response": response.text
            }
    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while making the request: {str(e)}")
        return {"error": "Gemini API request failed", "exception": str(e)}
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return {"error": "Gemini API request failed", "exception": str(e)}
