from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import List
from pathlib import Path
import logging

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

def get_db_connection():
    try:
        conn = sqlite3.connect('dummy_data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Changed port to 8001