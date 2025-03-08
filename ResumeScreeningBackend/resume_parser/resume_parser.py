import spacy
import re
import logging

logging.basicConfig(level=logging.DEBUG)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")  # You can fine-tune this model later

def extract_name(resume_text):
    doc = nlp(resume_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    # Fallback regex for names (capitalized first and last names)
    name_pattern = r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b"
    match = re.search(name_pattern, resume_text)
    if match:
        return match.group(0)
    return "Name not found"

def extract_email(resume_text):
    email_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(email_pattern, resume_text)
    if match:
        return match.group(0)
    return "Email not found"

def extract_skills(resume_text, required_skills):
    skills = []
    for skill in required_skills.split(","):
        skill = skill.strip()
        try:
            skill_pattern = re.compile(r"\b" + re.escape(skill) + r"\b", re.IGNORECASE)
            if re.search(skill_pattern, resume_text):
                skills.append(skill)
        except re.error as e:
            logging.error(f"Regex error for skill '{skill}': {e}")
            continue
    return skills

def extract_experience(resume_text):
    experience_pattern = r"(\d{1,2}(?:\+)?)(?:\s?(?:years|yr|experience|work))?"
    match = re.findall(experience_pattern, resume_text)
    if match:
        total_years = 0
        for year in match:
            try:
                total_years += int(year.replace('+', ''))
            except ValueError:
                continue
        return total_years
    return 0

def extract_experience_text(resume_text):
    experience_pattern = r"(Experience|Work history|Professional Experience|Employment History)(.*?)(Education|Skills|Certifications|$)"
    match = re.search(experience_pattern, resume_text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(2).strip()
    return "Experience not found"

def log_missing_skills(skills_found, required_skills):
    missing_skills = [skill for skill in required_skills.split(",") if skill.strip() not in skills_found]
    if missing_skills:
        logging.info(f"Missing Skills: {', '.join(missing_skills)}")
    return missing_skills

def parse_resume(resume_text, required_skills):
    logging.debug("Starting resume parsing...")
    name = extract_name(resume_text)
    logging.debug(f"Extracted Name: {name}")
    email = extract_email(resume_text)
    logging.debug(f"Extracted Email: {email}")
    skills_found = extract_skills(resume_text, required_skills)
    logging.debug(f"Extracted Skills: {', '.join(skills_found)}")
    experience_years = extract_experience(resume_text)
    logging.debug(f"Extracted Experience: {experience_years} years")
    experience_summary = extract_experience_text(resume_text)
    logging.debug(f"Extracted Experience Summary: {experience_summary}")
    missing_skills = log_missing_skills(skills_found, required_skills)
    return {
        "name": name,
        "email": email,
        "skills_found": skills_found,
        "experience_years": experience_years,
        "experience_summary": experience_summary,
        "missing_skills": missing_skills
    }
