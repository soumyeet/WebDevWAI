from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List
from pathlib import Path
import logging
import json
import textwrap
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Configure Gemini
# genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
genai.configure(api_key='AIzaSyCIoJroIWY9szjPTWna1RYLET1KwEKPhpM')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to the database file
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "dummy_data.db"

class Job(BaseModel):
    job_id: int
    company_id: int
    job_type: str
    availability_needed: str
    location: str
    salary: int
    requirements: str

class Applicant(BaseModel):
    profile_id: int
    applicant_id: int
    experience_years: int
    availability: str
    expected_salary_min: int
    expected_salary_max: int
    linkedin_link: str
    portfolio_link: str
    current_role: str
    education_degree: str
    college_name: str
    photo_filename: str
    skills: str

class WatchlistJob(BaseModel):
    profile_id: str
    applicant_name: str
    current_role: str
    college_name: str
    salary_range: str
    skills: str
    photo_filename: str
    availability: str

class ResumeText(BaseModel):
    text: str

class HiringText(BaseModel):
    text: str

def get_db_connection():
    try:
        conn = sqlite3.connect('dummy_data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

def generate_prompt_for_resume_analysis(resume_text):
    return textwrap.dedent(f"""
    You are an expert resume evaluator. Given the following resume text, analyze it thoroughly to:

    1. Score the following skills on a scale of 1 to 100:
        - Communication
        - Technical Skills
        - Creativity
        - Leadership
        - Problem Solving
    2. Determine the person's top **strengths** based on these scores.
    3. Identify the person's **weaknesses** or areas for improvement.
    4. Google search for ways to strengthen their weaknesses, and recommend specific courses/action items they can do to improve that score.
    5. Provide a summary of the resume in 3-4 sentences, highlighting key achievements and experiences.

    Resume Text:
    \"\"\"{resume_text}\"\"\"
    """)

def analyze_resume(resume_text):
    """Analyze resume using Google's Gemini API"""
    try:
        print("Analyzing resume...")
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("Gemini model initialized.")
        
        # Generate the prompt
        prompt = generate_prompt_for_resume_analysis(resume_text)
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Parse the response text as JSON
        # Note: Assuming Gemini returns properly formatted JSON
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback in case response isn't proper JSON
            logger.error("Failed to parse Gemini response as JSON")
            return {
                "status": "error",
                "data": {
                    "skills": {
                        "Communication": 0,
                        "Technical Skills": 0,
                        "Creativity": 0,
                        "Leadership": 0,
                        "Problem Solving": 0
                    },
                    "strengths": [],
                    "weaknesses": [],
                    "action_items": [],
                    "summary": "Failed to analyze resume."
                }
            }
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
    
def analyze_hiring(hiring_text):
    """Analyze resume using Google's Gemini API"""
    try:
        print("Analyzing hiring scheme...")
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("Gemini model initialized.")
        
        # Generate the prompt
        prompt = generate_prompt_for_resume_analysis(hiring_text)
        
        # Get response from Gemini
        response = model.generate_content(prompt)
        
        # Parse the response text as JSON
        # Note: Assuming Gemini returns properly formatted JSON
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback in case response isn't proper JSON
            logger.error("Failed to parse Gemini response as JSON")
            return {
                "status": "error",
                "data": {
                    "skills": {
                        "Communication": 0,
                        "Technical Skills": 0,
                        "Creativity": 0,
                        "Leadership": 0,
                        "Problem Solving": 0
                    },
                    "strengths": [],
                    "weaknesses": [],
                    "action_items": [],
                    "summary": "Failed to analyze hiring scheme."
                }
            }
            
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")


@app.get("/api/jobs")
async def get_jobs():
    try:
        conn = sqlite3.connect('dummy_data.db')
        cursor = conn.cursor()
        
        # Join with companies table to get company info
        cursor.execute("""
            SELECT jp.*, c.name as company_name, c.logo_filename 
            FROM job_profiles jp
            JOIN companies c ON jp.company_id = c.company_id
        """)
        
        columns = [desc[0] for desc in cursor.description]
        jobs = []
        
        for row in cursor.fetchall():
            job_dict = dict(zip(columns, row))
            # Format salary range
            job_dict['salary_range'] = f"${job_dict['salary']:,} - ${job_dict['salary'] + 20000:,}"
            jobs.append(job_dict)
        jobs.append
        data = {
            "status": "success",
            "count": len(jobs),
            "data": jobs
        } 
        conn.close()
        return data
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/jobs")
async def create_job(job: Job):
    try:
        conn = sqlite3.connect('dummy_data.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO job_profiles (
                company_id, job_type, availability_needed, 
                location, salary, requirements
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job.company_id, job.job_type, job.availability_needed,
            job.location, job.salary, job.requirements
        ))
        
        conn.commit()
        conn.close()
        return {
            "status": "success",
            "data": jobs
        }
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/applicants")
async def get_applicants():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        logger.info(f"Fetching applicants from database at {DB_PATH}")
        
        cursor.execute("""
            SELECT 
                ap.profile_id,
                ap.applicant_id,
                ap.experience_years,
                ap.availability,
                ap.expected_salary_min,
                ap.expected_salary_max,
                ap.linkedin_link,
                ap.portfolio_link,
                ap.current_role,
                ap.education_degree,
                ap.college_name,
                ap.photo_filename,
                ap.skills,
                a.name as applicant_name,
                a.email
            FROM applicant_profiles ap
            LEFT JOIN applicants a ON ap.applicant_id = a.applicant_id
            ORDER BY ap.experience_years DESC
        """)
        
        rows = cursor.fetchall()
        logger.info(f"Found {len(rows)} applicant profiles")
        
        applicants = []
        for row in rows:
            applicant = dict(row)
            applicant['salary_range'] = f"${applicant['expected_salary_min']:,} - ${applicant['expected_salary_max']:,}"
            applicant['photo_filename'] = applicant['photo_filename'] or 'https://via.placeholder.com/150'
            applicant['skills_list'] = [skill.strip() for skill in applicant['skills'].split(',')]
            applicants.append(applicant)
        
        return {
            "status": "success",
            "count": len(applicants),
            "data": applicants
        }
        
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

@app.get("/api/applicants/{profile_id}")
async def get_applicant_details(profile_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                ap.*,
                a.name as applicant_name,
                a.email
            FROM applicant_profiles ap
            LEFT JOIN applicants a ON ap.applicant_id = a.applicant_id
            WHERE ap.profile_id = ?
        """, (profile_id,))
        
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Applicant profile not found")
            
        applicant = dict(row)
        applicant['salary_range'] = f"${applicant['expected_salary_min']:,} - ${applicant['expected_salary_max']:,}"
        applicant['photo_filename'] = applicant['photo_filename'] or 'https://via.placeholder.com/150'
        applicant['skills_list'] = [skill.strip() for skill in applicant['skills'].split(',')]
        
        return {
            "status": "success",
            "data": applicant
        }
        
    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

@app.post("/api/watchlist/add")
async def add_to_watchlist(job: WatchlistJob):
    try:
        # Load existing watchlist from file (if it exists)
        watchlist_file = Path("watchlist.json")
        if (watchlist_file.exists()):
            with open(watchlist_file, "r") as f:
                watchlist = json.load(f)
        else:
            watchlist = []

        # Check if job is already in watchlist
        if not any(j["profile_id"] == job.profile_id for j in watchlist):
            # Add job to watchlist
            watchlist.append(job.dict())

            # Save updated watchlist to file
            with open(watchlist_file, "w") as f:
                json.dump(watchlist, f)

            return {"status": "success", "message": "Job added to watchlist!"}
        else:
            return {"status": "info", "message": "Job already in watchlist!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/watchlist/get")
async def get_watchlist():
    try:
        # Load watchlist from file (if it exists)
        watchlist_file = Path("watchlist.json")
        if watchlist_file.exists():
            with open(watchlist_file, "r") as f:
                watchlist = json.load(f)
        else:
            watchlist = []

        return {"status": "success", "data": watchlist}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/skills-analysis")
async def skills_analysis():
    # --------------------------------------------------------------------
    # If you have genai and the gemini model set up, you’d do something like:
    #
    # import genai
    # model = genai.GenerativeModel(model_name)
    # response = model.generate_content(prompt)
    # return response.text
    #
    # --------------------------------------------------------------------

    # For now, we'll just return a dummy JSON string:
    dummy_json_response = {
        "status": "success",
        "data": {
            "skills": {
                "Communication": 88,
                "Technical Skills": 92,
                "Creativity": 76,
                "Leadership": 85,
                "Problem Solving": 80
            },
            "strengths": ["Technical Skills", "Communication", "Leadership"],
            "weaknesses": ["Creativity", "Problem Solving"],
            "action_items": [
                "Enroll in a creative thinking course",
                "Practice systematic problem-solving exercises"
            ],
            "summary": "Analysis summary here..."
        }
    }
    return json.dumps(dummy_json_response)

@app.post("/api/analyze-resume")
async def analyze_resume_endpoint(resume: ResumeText):
    try:
        # Generate the analysis
        analysis_result = analyze_resume(resume.text)
        
        # Save the analysis to a file (optional)
        analysis_file = Path("resume_analysis.json")
        with open(analysis_file, "w") as f:
            json.dump(analysis_result, f)
            
        return {
            "status": "success",
            "data": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/analyze-hiring")
async def analyze_hiring_endpoint(hiring: HiringText):
    try:
        # Generate the analysis
        analysis_result = analyze_hiring(hiring.text)
        
        # Save the analysis to a file (optional)
        analysis_file = Path("resume_analysis.json")
        with open(analysis_file, "w") as f:
            json.dump(analysis_result, f)
            
        return {
            "status": "success",
            "data": analysis_result
        }
        
    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)