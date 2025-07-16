# AI Recruitment Helper (Conexio)

Conexio is an AI-powered platform designed to streamline the recruitment process for both job seekers and recruiters. It aims to reduce inefficiencies and human bias in hiring by leveraging cutting-edge AI technologies for intelligent matching, performance analysis, and automated tasks.

## Key Features

### For Job Seekers:

  * **Personalized Performance Dashboard**: Visualize your skills (communication, technical, creativity, leadership, problem-solving) with a radar chart. Get detailed insights into your strengths and weaknesses, along with actionable recommendations for improvement.
  * **Intelligent Job Matching**: Discover job opportunities that align with your skills and career goals through AI-driven matching. Receive real-time comparisons between your profile and job requirements.
  * **Resume Analysis**: Upload your resume for in-depth analysis, receiving skill scores, identified strengths, and areas for improvement.
  * **Profile Management**: Easily manage your personal information, upload resumes, and connect your LinkedIn and GitHub profiles.

### For Recruiters:

  * **Recruiter Dashboard**: Gain quick insights into active job postings, total applicants, and scheduled interviews.
  * **Candidate Scouting**: Efficiently browse and filter a comprehensive list of applicants based on various criteria.
  * **Automated Interview Question Generation**: Generate technical, behavioral, and gap-filling interview questions tailored to a candidate's resume and a specific job description.
  * **Hiring Analysis**: Analyze hiring data to optimize strategies and improve recruitment outcomes.

## Technologies Used

  * **Frontend**: HTML, CSS, JavaScript
      * **Frameworks/Libraries**: Bootstrap, Chart.js, Font Awesome
      * **Templating**: EJS (potentially for some dynamic content generation in older versions)
  * **Backend**: Python (FastAPI)
      * **Database**: SQLite (`dummy_data.db`, `recruitment.db`), Supabase (PostgreSQL-based for authentication and core data storage)
      * **AI/ML**: Google Gemini API (`google.generativeai`), `PyPDF2` (for PDF resume parsing)
  * **Deployment (Conceptual)**: Uvicorn (for FastAPI applications)

## Installation and Setup

### Prerequisites

  * Python 3.8+
  * Node.js and npm (if developing frontend locally)
  * Git

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/WebDevWAI-main.git
    cd WebDevWAI-main
    ```

2.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install backend dependencies:**

    ```bash
    pip install -r requirements.txt # (Assuming a requirements.txt exists with FastAPI, uvicorn, python-dotenv, PyPDF2, supabase, google-generativeai)
    ```

    (If `requirements.txt` is not available, install them manually):

    ```bash
    pip install fastapi uvicorn python-dotenv PyPDF2 supabase google-generativeai
    ```

4.  **Database Setup:**
    The project uses SQLite for local development and Supabase for more robust data storage and authentication.

      * **SQLite:** The `recruitment_db_generator.py` or `db.py` script can be used to create and populate the `dummy_data.db` or `recruitment.db` SQLite databases.
        ```bash
        python WebDevWAI-main/older/old/recruitment_db_generator.py
        # OR
        python WebDevWAI-main/notebooks/recruitment_db.py
        ```
      * **Supabase (Recommended):**
          * Create a Supabase project.
          * Update `SUPA_URL` and `SUPA_SERVICE_KEY` in `WebDevWAI-main/backend/main.py` with your Supabase project URL and service role key.
          * Set up your database schema in Supabase according to the models defined in `WebDevWAI-main/backend/main.py` (Applicants, Companies, JobProfiles, ApplicantProfiles, ApplicantSkills, ApplicantQualities, CompanyQualities, Schedules, ApplicantWatchlist, CompanyWatchlist).

5.  **Google Gemini API Key:**

      * Obtain a Google Gemini API key.
      * Update the `genai.configure(api_key='YOUR_GEMINI_API_KEY')` line in `WebDevWAI-main/backend/main.py` (or set it as an environment variable `GEMINI_API_KEY`).

### Frontend Setup

The frontend consists of static HTML, CSS, and JavaScript files. No specific build process is required for basic setup.

## Usage

### Running the Backend

1.  Navigate to the `WebDevWAI-main/backend` directory (if not already there).
2.  Run the FastAPI application:
    ```bash
    uvicorn main:router --reload --port 8000
    ```
    This will start the backend server, typically accessible at `http://127.0.0.1:8000`.

### Viewing the Frontend

You can open the HTML files directly in your web browser. For full functionality (e.g., API calls to the backend, correct pathing for `main.css`), you might need to serve them via a simple local HTTP server or integrate them with the FastAPI application if it's configured to serve static files.

  * Open `WebDevWAI-main/html/landing.html` in your web browser to start.
  * Navigate through the various pages (`login.html`, `signup.html`, `perf.html`, `jobs.html`, `scout.html`) to explore the application.

## Project Structure

```
WebDevWAI-main/
├── backend/
│   ├── main.py                     # Main FastAPI backend application
│   ├── main copy.py                # Copy of main.py
│   ├── perfecto_ml.py              # ML-related scripts
│   ├── recruitment_db_generator.py # Script to generate SQLite DB
│   ├── resume_analysis.json        # Placeholder for resume analysis output
│   ├── hiring_analysis.json        # Placeholder for hiring analysis output
│   ├── test_resume_analysis.py     # Tests for resume analysis
│   └── watchlist.json              # Watchlist data (JSON)
├── doc/
│   ├── 17th.docx                   # Progress report document
│   ├── AI Recruitment Helper.docx  # Project description document
│   ├── changes.docx                # Document detailing changes/updates
│   └── prompt.docx                 # Document related to prompt engineering
├── html/
│   ├── acc_info.html               # Account information page (user/applicant)
│   ├── config.yaml                 # Configuration file (API keys etc.)
│   ├── jobs.html                   # Job listings page (for applicants)
│   ├── jobs_safe.html              # Safe version of job listings
│   ├── landing.html                # Main landing page
│   ├── login.html                  # User login page
│   ├── main.css                    # Main CSS stylesheet for the frontend
│   ├── perf.html                   # Performance dashboard (for applicants)
│   ├── recruit.html                # Recruiter dashboard
│   ├── scout.html                  # Candidate scouting page (for recruiters)
│   ├── signup.html                 # User signup page
│   ├── test.html                   # Test HTML file (possibly for Supabase integration)
│   └── user_info.html              # User information form
├── notebooks/
│   ├── db.ipynb                    # Jupyter notebook for database interaction/testing
│   ├── db.py                       # Python script for database operations
│   ├── design.ipynb                # Jupyter notebook for design ideas/code generation
│   ├── reasoning.ipynb             # Jupyter notebook for AI reasoning/analysis
│   ├── recruitment_db.py           # Python script for recruitment database schema
│   └── Resume-SoumyaPandey.pdf     # Sample resume (PDF)
└── older/                          # Older versions/iterations of project files
    ├── backend/
    │   ├── main.py
    │   └── watchlist.json
    ├── doc/
    │   ├── 17th.docx
    │   ├── AI Recruitment Helper.docx
    │   ├── changes.docx
    │   └── prompt.docx
    ├── html/
    │   ├── index_account.html
    │   ├── index_info2.html
    │   ├── index_login.html
    │   ├── index_recruiter_2.html
    │   ├── index_scout.html
    │   ├── jobs.html
    │   ├── landing.html
    │   ├── main.css
    │   ├── perf.html
    │   └── signup.html
    ├── new/
    │   └── notebooks/
    │       ├── config.yaml
    │       ├── db.ipynb
    │       ├── db.py
    │       ├── design.ipynb
    │       └── recruitment_db.py
    └── old/
        ├── config.yaml
        ├── db.ipynb
        ├── design.ipynb
        ├── home.html
        ├── index_info.html
        ├── index_info2.html
        ├── index_login.html
        ├── info2.html
        ├── jobs.html
        ├── landing.html
        ├── main.css
        ├── nyan.html
        ├── nyan3.html
        ├── perf.html
        ├── performance.html
        ├── recruitment_db_generator.py
        ├── signup.html
        └── old/
            ├── fill.py
            ├── fill2.py
            ├── home.html
            ├── index.html
            ├── index_2.html
            ├── index_account2.html
            ├── index_integrate.html
            ├── index_integrate.py
            ├── index_integrate2.html
            ├── index_recruiter.html
            ├── index_try.html
            ├── jobs_2.html
            ├── marketing_sample_for_naukri_com-jobs__20190701_20190830__30k_data.csv
            ├── nyan.html
            ├── nyan3.html
            ├── ollama.ipynb
            ├── recruiters.html
            └── test.py
```

## Future Enhancements (Based on Project Files)

  * Further development of the conversational AI for real-time support.
  * More advanced features using RAG for deeper insights and workflow optimization.
  * Comprehensive integration with Supabase for all data storage and retrieval, moving away from local SQLite for production.
  * Improving the frontend with a full-fledged React.js implementation instead of in-line scripts for complex interactions.
  * Enhancing security measures, especially for sensitive data like resumes and user credentials.
  * Adding more sophisticated analytics and reporting features for both applicants and recruiters.
