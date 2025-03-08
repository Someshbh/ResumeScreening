Here is a `README.md` file for your Resume Screening Application. You can use this to guide users on setting up, installing, and starting the application.

---

# Resume Screening Application

## Overview
The Resume Screening Application allows HR professionals to upload job descriptions and resumes, analyze candidates based on required skills, and receive matching scores along with candidate details such as name, email, mobile number, experience summary, missing skills, and skills found.

## Features:
- Upload job descriptions and resumes (PDF format).
- Get a matching score based on job description and required skills.
- Extract candidate details: Name, Email, Mobile, Experience, Skills, and Missing Skills.
- View a list of shortlisted candidates with their details.

---

## Technologies Used:

### Frontend:
- **Angular**: Used for building the frontend of the application.

### Backend:
- **FastAPI**: Python-based backend framework.
- **Python**: The primary programming language.
- **Gemini AI API**: Used for analyzing resumes and job descriptions.
- **PyMuPDF**: For extracting text from PDF resumes.

---

## Setup & Installation

Follow these steps to set up and run the application locally.

### Prerequisites
Ensure you have the following installed on your system:
- **Python** (>=3.7)
- **Node.js** and **npm** (for Angular frontend)
- **Git** (for version control)

### Step 1: Clone the Repository

Clone the project repository using the following command:

```bash
git clone https://github.com/your-repository/resume-screening.git
cd resume-screening
```

### Step 2: Backend Setup

#### Install Python Dependencies

1. **Create a virtual environment**:

```bash
python -m venv venv
```

2. **Activate the virtual environment**:

- On Windows:

```bash
venv\Scripts\activate
```

- On macOS/Linux:

```bash
source venv/bin/activate
```

3. **Install required Python packages**:

```bash
pip install -r requirements.txt
```

#### Environment Variables

1. Create a `.env` file in the root directory of the project.
2. Add the following lines to the `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Run the Backend

1. Start the FastAPI backend:

```bash
uvicorn main:app --reload
```

The backend will now be running at `http://127.0.0.1:8000`.

---

### Step 3: Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. **Install Angular Dependencies**:

```bash
npm install
```

3. **Start the Angular Development Server**:

```bash
ng serve
```

The frontend will now be running at `http://localhost:4200`.

---

### Step 4: Access the Application

Once both the frontend and backend are up and running, open your browser and navigate to:

```url
http://localhost:4200
```

---

## How It Works

### Flow:
1. **Upload PDF**: Upload the job description and candidate resumes (in PDF format).
2. **Extract Text**: The text from resumes is extracted using **PyMuPDF**.
3. **Gemini Analysis**: The extracted text and job description are sent to the **Gemini AI API** to get a matching score and analysis.
4. **Process Response**: The response is processed to extract useful details like the candidate's name, email, experience, skills, missing skills, and match percentage.
5. **Return Results**: The results are displayed in the UI for HR personnel to review and make informed decisions.

---

## Limitations

### 1. Initial AI Setup
Initially, **spaCy** and **BERT** were used for resume analysis, but these models had limitations in accuracy and could not effectively handle the matching process with job descriptions. This prompted a shift towards using **Gemini AI** for better accuracy and performance.

### 2. Gemini AI Limitations
- **Free Version Limitations**: There are token and usage limitations in the free version of Gemini AI.
- **Pricing**: Paid versions may have limitations on API requests and response sizes.

### 3. Security Considerations
- **API Key Security**: The Gemini API key should be stored securely and never exposed in public repositories.
- **Sensitive Data**: All resumes and job descriptions are processed securely, but it's recommended to use HTTPS for production environments.

---

## Future Scope

- **Integration with ATS**: Integrate the application with popular Applicant Tracking Systems (ATS) for direct resume import and processing.
- **Advanced Filtering**: Implement more advanced filtering based on candidate scores, skills, and experience.
- **Support for More File Formats**: Expand resume support to file formats like DOCX and TXT.
- **Improved AI Models**: Explore other AI models and further improve the accuracy of candidate matching.

---

## Conclusion

This application provides an automated solution for HR professionals to efficiently screen resumes, ensuring they find the best-fit candidates based on the job description and required skills.

---

Feel free to ask if you need any more help setting up or working with this project!