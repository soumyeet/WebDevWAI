import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create Applicants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applicants (
            applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT,
            membership_level TEXT,
            join_date DATE,
            resume_path TEXT,
            password TEXT NOT NULL,
            linkedin_link TEXT,
            github_link TEXT,
            skills TEXT,
            industry TEXT
        )
    """)

    # Create Jobs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_older_name TEXT,
            industry TEXT,
            company_name TEXT NOT NULL,
            location TEXT,
            company_size TEXT,
            website TEXT,
            logo_path TEXT,
            contact_number TEXT,
            linkedin_link TEXT,
            github_link TEXT
        )
    """)

    # Create ApplicantProfiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantProfiles (
            applicant_profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER UNIQUE NOT NULL REFERENCES Applicants(applicant_id),
            name TEXT NOT NULL,
            location TEXT,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT,
            experience_years REAL,
            degree TEXT,
            availability TEXT,
            expected_salary_range TEXT,
            linkedin_link TEXT,
            portfolio_link TEXT,
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
            location TEXT,
            salary TEXT,
            email TEXT,
            company_rating REAL,
            requirements TEXT
        )
    """)

    # Create ApplicantExperiences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ApplicantExperiences (
            experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL REFERENCES Applicants(applicant_id),
            type TEXT NOT NULL,
            company_name TEXT,
            duration TEXT,
            skills_utilized TEXT,
            description TEXT
        )
    """)

    # Create ApplicantSkillsQuantified table
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

    # Create CommunityReviews table
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

def populate_sample_data(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Sample Applicants
    cursor.execute("INSERT INTO Applicants (name, location, email, password) VALUES (?, ?, ?, ?)",
                   ("John Doe", "New York", "john.doe@example.com", "password123"))
    cursor.execute("INSERT INTO Applicants (name, location, email, password) VALUES (?, ?, ?, ?)",
                   ("Jane Smith", "Los Angeles", "jane.smith@example.com", "securepass"))

    # Sample Jobs
    cursor.execute("INSERT INTO Jobs (company_name, industry, location) VALUES (?, ?, ?)",
                   ("TechCorp", "Technology", "San Francisco"))
    cursor.execute("INSERT INTO Jobs (company_name, industry, location) VALUES (?, ?, ?)",
                   ("MediCare", "Healthcare", "Boston"))

    # Sample ApplicantProfiles
    cursor.execute("INSERT INTO ApplicantProfiles (applicant_id, name, email, experience_years) VALUES (?, ?, ?, ?)",
                   (1, "John Doe", "john.doe@example.com", 5.0))
    cursor.execute("INSERT INTO ApplicantProfiles (applicant_id, name, email, experience_years) VALUES (?, ?, ?, ?)",
                   (2, "Jane Smith", "jane.smith@example.com", 3.0))

    # Sample JobProfiles
    cursor.execute("INSERT INTO JobProfiles (job_id, company_name, job_type) VALUES (?, ?, ?)",
                   (1, "TechCorp", "Software Engineer"))
    cursor.execute("INSERT INTO JobProfiles (job_id, company_name, job_type) VALUES (?, ?, ?)",
                   (2, "MediCare", "Data Analyst"))

    # Sample ApplicantExperiences
    cursor.execute("INSERT INTO ApplicantExperiences (applicant_id, type, description) VALUES (?, ?, ?)",
                   (1, "Project", "Developed a web application using Python and Django."))
    cursor.execute("INSERT INTO ApplicantExperiences (applicant_id, type, description) VALUES (?, ?, ?)",
                   (2, "Skill", "Proficient in Java and data analysis."))

    # Sample ApplicantSkillsQuantified
    cursor.execute("INSERT INTO ApplicantSkillsQuantified (applicant_id, leadership, technical_skills) VALUES (?, ?, ?)",
                   (1, 80, 90))
    cursor.execute("INSERT INTO ApplicantSkillsQuantified (applicant_id, leadership, technical_skills) VALUES (?, ?, ?)",
                   (2, 70, 85))

    # Sample CommunityReviews
    cursor.execute("INSERT INTO CommunityReviews (company_id, reviewer_name, rating) VALUES (?, ?, ?)",
                   (1, "Alice Brown", 4))
    cursor.execute("INSERT INTO CommunityReviews (company_id, reviewer_name, rating) VALUES (?, ?, ?)",
                   (2, "Bob White", 5))

    # Sample Schedules
    cursor.execute("INSERT INTO Schedules (company_id, applicant_id, date, time) VALUES (?, ?, ?, ?)",
                   (1, 1, "2025-03-10", "10:00"))
    cursor.execute("INSERT INTO Schedules (company_id, applicant_id, date, time) VALUES (?, ?, ?, ?)",
                   (2, 2, "2025-03-12", "14:00"))

    # Sample ApplicantWatchlists
    cursor.execute("INSERT INTO ApplicantWatchlists (applicant_id, company_id) VALUES (?, ?)", (1, 2))
    cursor.execute("INSERT INTO ApplicantWatchlists (applicant_id, company_id) VALUES (?, ?)", (2, 1))

    # Sample CompanyWatchlists
    cursor.execute("INSERT INTO CompanyWatchlists (company_id, applicant_id) VALUES (?, ?)", (1, 2))
    cursor.execute("INSERT INTO CompanyWatchlists (company_id, applicant_id) VALUES (?, ?)", (2, 1))

   # Sample CompanySkillsQuantified
    cursor.execute("INSERT INTO CompanySkillsQuantified (company_id, leadership, technical_skills) VALUES (?, ?, ?)",
                   (1, 75, 85))
    cursor.execute("INSERT INTO CompanySkillsQuantified (company_id, leadership, technical_skills) VALUES (?, ?, ?)",
                   (2, 80, 70))

    # Sample CompanyData
    cursor.execute("INSERT INTO CompanyData (company_id, people_hired, response_rate) VALUES (?, ?, ?)",
                   (1, 15, 0.85))
    cursor.execute("INSERT INTO CompanyData (company_id, people_hired, response_rate) VALUES (?, ?, ?)",
                   (2, 20, 0.90))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    db_name = "new2.db"
    create_database(db_name)
    populate_sample_data(db_name)
    print(f"Database '{db_name}' created and populated with sample data.")
