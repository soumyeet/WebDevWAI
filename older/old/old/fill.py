import sqlite3
import pandas as pd
import random
import string

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS Applicants")
    cursor.execute("DROP TABLE IF EXISTS Jobs")
    cursor.execute("DROP TABLE IF EXISTS ApplicantProfiles")
    cursor.execute("DROP TABLE IF EXISTS JobProfiles")
    cursor.execute("DROP TABLE IF EXISTS ApplicantExperiences")
    cursor.execute("DROP TABLE IF EXISTS ApplicantSkillsQuantified")
    cursor.execute("DROP TABLE IF EXISTS CommunityReviews")
    cursor.execute("DROP TABLE IF EXISTS Schedules")
    cursor.execute("DROP TABLE IF EXISTS ApplicantWatchlists")
    cursor.execute("DROP TABLE IF EXISTS CompanyWatchlists")
    cursor.execute("DROP TABLE IF EXISTS CompanySkillsQuantified")
    cursor.execute("DROP TABLE IF EXISTS CompanyData")

    # Create Applicants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applicants (
            applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            skills TEXT,
            industry TEXT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Create Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            industry TEXT,
            location TEXT
        )
    """)

    # Create ApplicantProfiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantProfiles (
            applicant_profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER UNIQUE NOT NULL REFERENCES Applicants(applicant_id),
            name TEXT NOT NULL,
            location TEXT,
            email TEXT NOT NULL,
            experience_years REAL,
            degree TEXT,
            skills TEXT
        )
    """)

    # Create JobProfiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS JobProfiles (
            job_profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER UNIQUE NOT NULL REFERENCES Jobs(job_id),
            company_name TEXT NOT NULL,
            job_type TEXT,
            salary TEXT
        )
    """)

    # Create ApplicantExperiences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantExperiences (
            experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            type TEXT NOT NULL,
            description TEXT,
            skills_utilized TEXT
        )
    """)

    # Create ApplicantSkillsQuantified table (left unchanged for simplicity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantSkillsQuantified (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            leadership INTEGER,
            creativity INTEGER,
            problem_solving INTEGER,
            communication INTEGER,
            technical_skills INTEGER
        )
    """)

    # Create CommunityReviews table (omitted for brevity)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CommunityReviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL REFERENCES Jobs(job_id),
            reviewer_name TEXT,
            rating INTEGER,
            description TEXT
        )
    """)

    # Create Schedules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL REFERENCES Jobs(job_id),
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            job_type TEXT,
            time TEXT,
            date DATE,
            interviewer TEXT
        )
    """)

    # Create ApplicantWatchlists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantWatchlists (
            watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            company_id INTEGER NOT NULL REFERENCES Jobs(job_id),
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create CompanyWatchlists table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyWatchlists (
            watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL REFERENCES Jobs(job_id),
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            added_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create CompanySkillsQuantified table (left unchanged for simplicity)
        # Create CompanySkillsQuantified table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanySkillsQuantified (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL REFERENCES Jobs(job_id),
            leadership INTEGER,
            creativity INTEGER,
            problem_solving INTEGER,
            communication INTEGER,
            technical_skills INTEGER
        )
    """)

    # Create CompanyData table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CompanyData (
            company_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER UNIQUE NOT NULL REFERENCES Jobs(job_id),
            people_hired INTEGER,
            people_in_process INTEGER,
            people_rejected INTEGER,
            people_withdrew INTEGER,
            response_rate REAL,
            applicant_number INTEGER,
            company_rating REAL,
            hiring_timeline TEXT
        )
    """)

    conn.commit()
    conn.close()

def populate_from_csv(db_name, csv_file):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Iterate over the rows of the DataFrame and insert data into tables
    for index, row in df.iterrows():
        # Extract data from the row, providing default values for missing data
        job_title = str(row.get('Job Title', 'Default Job Title')).strip()
        job_salary = row.get('Job Salary', 'Not Disclosed by Recruiter')
        job_experience = row.get('Job Experience Required', 'Not Specified')
        key_skills = row.get('Key Skills', 'General Skills')
        location = row.get('Location', 'Anywhere')
        industry = row.get('Industry', 'Generic Industry')
        role = row.get('Role', 'General Role')
        functional_area = row.get('Functional Area', 'General Functional Area')

        # Generate a unique email address
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        email = f"default_{index}_{random_string}@example.com"

        # Insert data into Applicants table
        try:
            cursor.execute("""
                INSERT INTO Applicants (name, location, skills, industry, email, password)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (job_title, location, key_skills, industry, email, "default_password"))  # Unique email
            applicant_id = cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Skipping row {index} due to IntegrityError: {e}")
            conn.rollback()
            continue

        # Insert data into Jobs table
        cursor.execute("""
            INSERT INTO Jobs (company_name, industry, location)
            VALUES (?, ?, ?)
        """, (job_title, industry, location))  # Using job_title as company_name for simplicity
        job_id = cursor.lastrowid
        # Insert into applicant profile
        cursor.execute("""
            INSERT INTO ApplicantProfiles (applicant_id, name, location, email, experience_years, degree, skills)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (applicant_id, job_title, location, email, 2, "Bachelors", key_skills))  # defaults values as these columns don't exist in the csv

        # Insert into job profile
        cursor.execute("""
            INSERT INTO JobProfiles (job_id, company_name, job_type, salary)
            VALUES (?, ?, ?, ?)
        """, (job_id, job_title, role, job_salary))

        # Insert data into ApplicantExperiences table (example, adjust as needed)
        cursor.execute("""
            INSERT INTO ApplicantExperiences (applicant_id, type, description, skills_utilized)
            VALUES (?, ?, ?, ?)
        """, (applicant_id, "Job Description", f"Applied for {job_title} role", key_skills))  # type is "job description" as these rows are all jobs
        conn.commit()  # Commit after each row to avoid losing data if the script fails

    conn.close()
    print("Data populated from CSV successfully.")

if __name__ == "__main__":
    db_name = "new2.db"
    csv_file = "marketing_sample_for_naukri_com-jobs__20190701_20190830__30k_data.csv"  # Corrected file name
    create_database(db_name)
    populate_from_csv(db_name, csv_file)
