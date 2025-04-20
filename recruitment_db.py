import sqlite3
from datetime import datetime

def create_db_schema():
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()

    # Create Applicants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255),
            email VARCHAR(255) NOT NULL UNIQUE,
            phone VARCHAR(20),
            join_date DATE,
            resume_filename VARCHAR(255),
            password VARCHAR(255) NOT NULL,
            linkedin_link VARCHAR(255),
            github_link VARCHAR(255)
        )
    ''')

    # Create Companies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            industry VARCHAR(255),
            location VARCHAR(255),
            website VARCHAR(255),
            logo_filename VARCHAR(255),
            contact_number VARCHAR(20),
            linkedin_link VARCHAR(255),
            github_link VARCHAR(255)
        )
    ''')

    # Create ApplicantProfiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicant_profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL,
            experience_years INTEGER,
            availability VARCHAR(50),
            expected_salary_min INTEGER,
            expected_salary_max INTEGER,
            linkedin_link VARCHAR(255),
            portfolio_link VARCHAR(255),
            current_role VARCHAR(255),
            education_degree VARCHAR(255),
            college_name VARCHAR(255),
            photo_filename VARCHAR(255),
            skills TEXT,
            FOREIGN KEY (applicant_id) REFERENCES applicants (applicant_id)
        )
    ''')
    # Create JobProfiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_profiles (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            job_type VARCHAR(255),
            availability_needed VARCHAR(50),
            location VARCHAR(255),
            salary INTEGER,
            requirements TEXT,
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
    ''')

    # Create ApplicantQualities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicant_qualities (
            quality_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL,
            leadership INTEGER CHECK (leadership BETWEEN 1 AND 100),
            creativity INTEGER CHECK (creativity BETWEEN 1 AND 100),
            problem_solver INTEGER CHECK (problem_solver BETWEEN 1 AND 100),
            communication INTEGER CHECK (communication BETWEEN 1 AND 100),
            technical_skills INTEGER CHECK (technical_skills BETWEEN 1 AND 100),
            FOREIGN KEY (applicant_id) REFERENCES applicants (applicant_id)
        )
    ''')

    # Create CompanyQualities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_qualities (
            company_quality_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            leadership INTEGER CHECK (leadership BETWEEN 1 AND 100),
            creativity INTEGER CHECK (creativity BETWEEN 1 AND 100),
            problem_solver INTEGER CHECK (problem_solver BETWEEN 1 AND 100),
            communication INTEGER CHECK (communication BETWEEN 1 AND 100),
            technical_skills INTEGER CHECK (technical_skills BETWEEN 1 AND 100),
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
    ''')

    # Create Schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            applicant_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            time TIME,
            date DATE,
            interviewer VARCHAR(255),
            FOREIGN KEY (company_id) REFERENCES companies (company_id),
            FOREIGN KEY (applicant_id) REFERENCES applicants (applicant_id),
            FOREIGN KEY (job_id) REFERENCES job_profiles (job_id)
        )
    ''')

    # Create ApplicantWatchlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicant_watchlist (
            watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (applicant_id) REFERENCES applicants (applicant_id),
            FOREIGN KEY (company_id) REFERENCES companies (company_id)
        )
    ''')

    # Create CompanyWatchlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_watchlist (
            watchlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            applicant_id INTEGER NOT NULL,
            added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES companies (company_id),
            FOREIGN KEY (applicant_id) REFERENCES applicants (applicant_id)
        )
    ''')

    try:
        # Clear existing data
        tables = ['company_watchlist', 'applicant_watchlist', 'schedules', 'company_qualities',
                 'applicant_qualities', 'job_profiles', 'applicant_profiles',
                 'companies', 'applicants']
        
        for table in tables:
            cursor.execute(f'DELETE FROM {table}')
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")

        # Insert sample applicants
        cursor.execute('''
            INSERT INTO applicants (name, location, email, phone, join_date, resume_filename, password, linkedin_link, github_link)
            VALUES 
            ('John Doe', 'New York', 'john@example.com', '1234567890', '2024-01-15', 'john_resume.pdf', 'pass123', 'linkedin.com/johndoe', 'github.com/johndoe'),
            ('Jane Smith', 'San Francisco', 'jane@example.com', '2345678901', '2024-02-15', 'jane_resume.pdf', 'pass456', 'linkedin.com/janesmith', 'github.com/janesmith'),
            ('Mike Johnson', 'Chicago', 'mike@example.com', '3456789012', '2024-03-15', 'mike_resume.pdf', 'pass789', 'linkedin.com/mikej', 'github.com/mikej'),
            ('Sarah Wilson', 'Boston', 'sarah@example.com', '4567890123', '2024-04-15', 'sarah_resume.pdf', 'passabc', 'linkedin.com/sarahw', 'github.com/sarahw'),
            ('Tom Brown', 'Seattle', 'tom@example.com', '5678901234', '2024-05-15', 'tom_resume.pdf', 'passdef', 'linkedin.com/tomb', 'github.com/tomb')
        ''')

        # Insert sample companies
        cursor.execute('''
            INSERT INTO companies (name, industry, location, website, logo_filename, contact_number, linkedin_link, github_link)
            VALUES
            ('TechCorp', 'Technology', 'New York', 'techcorp.com', 'images\logo.jpg', '1234567890', 'linkedin.com/techcorp', 'github.com/techcorp'),
            ('DataSoft', 'Software', 'San Francisco', 'datasoft.com', 'images\logo.jpg', '2345678901', 'linkedin.com/datasoft', 'github.com/datasoft'),
            ('AITech', 'AI/ML', 'Seattle', 'aitech.com', 'images\logo.jpg', '3456789012', 'linkedin.com/aitech', 'github.com/aitech'),
            ('WebSolutions', 'Web Development', 'Austin', 'images\logo.jpg', 'websolutions_logo.png', '4567890123', 'linkedin.com/websolutions', 'github.com/websolutions'),
            ('CloudTech', 'Cloud Computing', 'Boston', 'images\logo.jpg', 'cloudtech_logo.png', '5678901234', 'linkedin.com/cloudtech', 'github.com/cloudtech')
        ''')

        # Insert sample applicant profiles with skills
        cursor.execute('''
            INSERT INTO applicant_profiles (
                applicant_id, experience_years, availability, expected_salary_min, expected_salary_max, 
                linkedin_link, portfolio_link, current_role, education_degree, college_name, photo_filename, skills)
            VALUES
            (1, 5, 'Full-time', 80000, 100000, 'linkedin.com/john', 'portfolio.com/john', 
             'Senior Developer', 'Masters', 'MIT', 'john_photo.jpg', 
             'Python,Java,React,AWS,Docker,Kubernetes,CI/CD,System Design'),
            
            (2, 3, 'Remote', 70000, 90000, 'linkedin.com/jane', 'portfolio.com/jane', 
             'Developer', 'Bachelors', 'Stanford', 'jane_photo.jpg', 
             'JavaScript,Node.js,Express,MongoDB,React,TypeScript,Redux,GraphQL'),
            
            (3, 7, 'Full-time', 100000, 120000, 'linkedin.com/mike', 'portfolio.com/mike', 
             'Tech Lead', 'PhD', 'Berkeley', 'mike_photo.jpg', 
             'C++,Python,TensorFlow,SQL,Machine Learning,Deep Learning,Data Science,Statistics'),
            
            (4, 2, 'Part-time', 50000, 70000, 'linkedin.com/sarah', 'portfolio.com/sarah', 
             'Junior Developer', 'Bachelors', 'Harvard', 'sarah_photo.jpg', 
             'HTML,CSS,JavaScript,React,Vue,Figma,UI/UX,Responsive Design'),
            
            (5, 4, 'Remote', 75000, 95000, 'linkedin.com/tom', 'portfolio.com/tom', 
             'Mid Developer', 'Masters', 'CMU', 'tom_photo.jpg', 
             'Java,Spring,MySQL,Redis,Angular,Microservices,REST APIs,Cloud Computing')
        ''')

        # Insert sample job profiles
        cursor.execute('''
            INSERT INTO job_profiles (company_id, job_type, availability_needed, location, salary, requirements)
            VALUES
            (1, 'Software Engineer', 'Full-time', 'New York', 100000, 'Python, Java, 5+ years experience'),
            (2, 'Data Scientist', 'Remote', 'San Francisco', 120000, 'ML, AI, Statistics'),
            (3, 'Full Stack Developer', 'Full-time', 'Seattle', 90000, 'MERN Stack, 3+ years'),
            (4, 'Frontend Developer', 'Part-time', 'Austin', 80000, 'React, Vue, UI/UX'),
            (5, 'DevOps Engineer', 'Remote', 'Boston', 110000, 'AWS, Docker, Kubernetes')
        ''')

        # Insert sample applicant qualities
        cursor.execute('''
            INSERT INTO applicant_qualities (applicant_id, leadership, creativity, problem_solver, communication, technical_skills)
            VALUES
            (1, 85, 90, 95, 80, 92),
            (2, 75, 85, 90, 95, 88),
            (3, 92, 80, 85, 88, 95),
            (4, 70, 92, 85, 90, 80),
            (5, 88, 85, 90, 85, 90)
        ''')

        # Insert sample company qualities
        cursor.execute('''
            INSERT INTO company_qualities (company_id, leadership, creativity, problem_solver, communication, technical_skills)
            VALUES
            (1, 90, 85, 88, 92, 95),
            (2, 85, 90, 92, 88, 90),
            (3, 92, 88, 90, 85, 93),
            (4, 88, 92, 85, 90, 87),
            (5, 95, 85, 90, 88, 92)
        ''')

        # Insert sample schedules
        cursor.execute('''
            INSERT INTO schedules (company_id, applicant_id, job_id, time, date, interviewer)
            VALUES
            (1, 1, 1, '10:00', '2024-03-20', 'Alice Manager'),
            (2, 2, 2, '14:00', '2024-03-21', 'Bob Director'),
            (3, 3, 3, '11:00', '2024-03-22', 'Charlie Lead'),
            (4, 4, 4, '15:00', '2024-03-23', 'David HR'),
            (5, 5, 5, '13:00', '2024-03-24', 'Eve Recruiter')
        ''')

        # Insert sample watchlists
        cursor.execute('''
            INSERT INTO applicant_watchlist (applicant_id, company_id)
            VALUES
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 1)
        ''')

        cursor.execute('''
            INSERT INTO company_watchlist (company_id, applicant_id)
            VALUES
            (1, 2), (2, 3), (3, 4), (4, 5), (5, 1)
        ''')

        conn.commit()
        print("Database schema created and sample data inserted successfully!")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    create_db_schema()