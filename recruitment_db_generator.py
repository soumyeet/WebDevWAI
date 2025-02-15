import sqlite3

def create_database(db_name="recruitment.db"):
    """
    Creates a SQLite database with the specified schema and populates it with sample data.
    """

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Applicants Table (Basic Info)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Applicants (
            applicant_key INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            university TEXT,
            degree TEXT,
            contact_number TEXT,
            email TEXT
        )
    """)

    # Experience Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Experience (
            experience_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            company_name TEXT,
            start_date TEXT,  -- e.g., YYYY-MM-DD
            end_date TEXT,    -- e.g., YYYY-MM-DD
            description TEXT,
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Projects Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            project_name TEXT,
            description TEXT,
            skills_utilized TEXT,
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Responsibilities Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Responsibilities (
            responsibility_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            organisation_name TEXT,
            position TEXT,
            description TEXT,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Achievements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Achievements (
            achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            description TEXT,
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Skills Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Skills (
            skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            skill_name TEXT,
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Qualities Table (Quantified)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Qualities (
            quality_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_key INTEGER,
            leadership INTEGER,       -- 1-100 scale
            creativity INTEGER,       -- 1-100 scale
            problem_solver INTEGER,   -- 1-100 scale
            communication INTEGER,    -- 1-100 scale
            technical_skills INTEGER, -- 1-100 scale
            FOREIGN KEY (applicant_key) REFERENCES Applicants (applicant_key)
        )
    """)

    # Sample Data
    cursor.execute("INSERT INTO Applicants (name, age, gender, university, degree, contact_number, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ("John Doe", 25, "Male", "Stanford", "CS", "123-456-7890", "john.doe@example.com"))
    applicant_key = cursor.lastrowid  # Get the auto-generated applicant_key

    cursor.execute("INSERT INTO Experience (applicant_key, company_name, start_date, end_date, description) VALUES (?, ?, ?, ?, ?)",
                   (applicant_key, "Google", "2022-01-01", "2023-12-31", "Software Engineer Intern"))

    cursor.execute("INSERT INTO Projects (applicant_key, project_name, description, skills_utilized) VALUES (?, ?, ?, ?)",
                   (applicant_key, "AI Project", "Developed an AI model", "Python, TensorFlow"))

    cursor.execute("INSERT INTO Responsibilities (applicant_key, organisation_name, position, description, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                   (applicant_key, "University Club", "President", "Led the club activities", "2021-09-01", "2022-05-31"))

    cursor.execute("INSERT INTO Achievements (applicant_key, description) VALUES (?, ?)",
                   (applicant_key, "Won a hackathon"))

    cursor.execute("INSERT INTO Skills (applicant_key, skill_name) VALUES (?, ?)",
                   (applicant_key, "Python"))
    
    cursor.execute("INSERT INTO Skills (applicant_key, skill_name) VALUES (?, ?)",
                   (applicant_key, "Data Analysis"))

    cursor.execute("INSERT INTO Qualities (applicant_key, leadership, creativity, problem_solver, communication, technical_skills) VALUES (?, ?, ?, ?, ?, ?)",
                   (applicant_key, 85, 90, 75, 92, 88))
    
    #Another Applicant 
    cursor.execute("INSERT INTO Applicants (name, age, gender, university, degree, contact_number, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ("Jane Smith", 28, "Female", "MIT", "EE", "987-654-3210", "jane.smith@example.com"))
    applicant_key2 = cursor.lastrowid  # Get the auto-generated applicant_key

    cursor.execute("INSERT INTO Experience (applicant_key, company_name, start_date, end_date, description) VALUES (?, ?, ?, ?, ?)",
                   (applicant_key2, "Amazon", "2021-06-01", "2024-01-15", "Senior Software Developer"))

    cursor.execute("INSERT INTO Projects (applicant_key, project_name, description, skills_utilized) VALUES (?, ?, ?, ?)",
                   (applicant_key2, "Cloud Infrastructure", "Designed cloud solutions", "AWS, Python"))

    cursor.execute("INSERT INTO Responsibilities (applicant_key, organisation_name, position, description, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                   (applicant_key2, "IEEE", "Vice President", "Managed technical events", "2020-09-01", "2021-05-31"))

    cursor.execute("INSERT INTO Achievements (applicant_key, description) VALUES (?, ?)",
                   (applicant_key2, "Published a research paper"))

    cursor.execute("INSERT INTO Skills (applicant_key, skill_name) VALUES (?, ?)",
                   (applicant_key2, "AWS"))
    
    cursor.execute("INSERT INTO Skills (applicant_key, skill_name) VALUES (?, ?)",
                   (applicant_key2, "C++"))

    cursor.execute("INSERT INTO Qualities (applicant_key, leadership, creativity, problem_solver, communication, technical_skills) VALUES (?, ?, ?, ?, ?, ?)",
                   (applicant_key2, 92, 80, 95, 88, 95))

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and populated successfully.")

create_database()