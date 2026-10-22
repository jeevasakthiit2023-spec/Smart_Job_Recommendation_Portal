# Smart Job Recommendation Portal

An intelligent, full-stack recruitment portal built with **Python 3**, **Django 5**, **HTML5**, **CSS3 (Vanilla)**, and **JavaScript**. The platform features an explainable rule-matching recommendation engine that pairs candidate profiles with engineering vacancies based on skills alignment, target role, workplace preferences, and experience tier.

---

## 🚀 Key Features

### 1. Smart Recommendation Engine (`jobs/recommendation.py`)
- **Skills Match (50% weight):** Normalizes and parses technical competencies (e.g. `Python, Django, PostgreSQL, Docker`), rewarding direct and substring skill overlaps.
- **Preferred Role Match (20% weight):** Evaluates semantic keyword alignment between seeker target title and job title/category.
- **Workplace & Location Match (15% weight):** Prioritizes remote-friendly roles and geographical preferences.
- **Experience Level Match (15% weight):** Maps career tiers (`Fresher`, `Junior`, `Mid`, `Senior`, `Lead`) with calibrated proximity scoring.
- **Explainability:** Generates transparent bullet-point rationale for each recommendation with a clear indicator disclaimer.
- **Exclusion Filters:** Automatically hides expired jobs, paused vacancies, and already-applied positions.

### 2. User Roles & Security
- **Job Seeker Module:** Maintain resume document uploads (`.pdf`, `.doc`, `.docx` up to 5MB), skills inventory, salary expectations, application tracker, and saved jobs bookmarks.
- **Recruiter Module:** Organization branding, publish vacancies with deadline tracking, review candidates per opening, view cover letters, download candidate resumes securely, and update hiring statuses (`Pending`, `Shortlisted`, `Selected`, `Rejected`).
- **Django Built-in Auth:** Secure salted SHA-256 password hashing, CSRF token verification across all forms, role-enforcing decorators (`@job_seeker_required`, `@recruiter_required`).
- **Custom Error Handling:** Styled 403, 404, and 500 error pages.

### 3. Modern Vanilla UI Design
- Tailored color palette: Deep Navy (`#0f172a`), Vibrant Teal (`#0d9488`, `#14b8a6`), Crisp White (`#ffffff`), and Slate accents.
- Responsive CSS Grid and Flexbox layouts.
- Interactive alerts with auto-dismissal.
- High-contrast typography via Google Fonts (Plus Jakarta Sans) and FontAwesome 6 icons.

---

## 📂 Project Architecture

```
Smart_Job_Recommendation_Portal/
│
├── manage.py                          # Django CLI utility
├── requirements.txt                   # Production dependencies
├── README.md                          # Documentation and instructions
├── .gitignore                         # Version control exclusions
├── run.bat                            # Windows one-click server starter
├── db.sqlite3                         # Local SQLite database
│
├── config/                            # Core Django project configuration
│   ├── __init__.py
│   ├── settings.py                   # App config, media/static paths, security
│   ├── urls.py                       # Root URL routing & custom error handlers
│   ├── wsgi.py                       # WSGI entrypoint
│   └── asgi.py                       # ASGI entrypoint
│
├── accounts/                          # Authentication & user profiles
│   ├── models.py                     # UserProfile & RecruiterProfile
│   ├── forms.py                      # Registration & Profile forms with validators
│   ├── views.py                      # Login, Register, Profile, Dashboard dispatcher
│   ├── urls.py
│   ├── admin.py
│   ├── decorators.py                 # Role-based access control decorators
│   ├── context_processors.py         # Global template role context
│   └── tests.py                      # Auth & profile test cases
│
├── jobs/                              # Job postings & recommendation engine
│   ├── models.py                     # Job & SavedJob models
│   ├── recommendation.py             # Weighted rule-matching scoring algorithm
│   ├── forms.py                      # Search & filtering forms
│   ├── views.py                      # Catalog, Detail, Recommendations, Saved jobs
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py                      # Scoring algorithm & filtering test cases
│   └── management/commands/
│       └── populate_jobs.py          # Sample data generator
│
├── applications/                      # Job applications & candidate pipeline
│   ├── models.py                     # JobApplication model
│   ├── forms.py                      # Application submission form with file validation
│   ├── views.py                      # Apply view & candidate application history
│   ├── urls.py
│   ├── admin.py
│   └── tests.py                      # Duplicate prevention & application tests
│
├── recruiters/                        # Recruiter management module
│   ├── forms.py                      # Job vacancy create/update & status forms
│   ├── views.py                      # Recruiter hub, job CRUD, candidate pipeline
│   ├── urls.py
│   └── tests.py                      # Ownership enforcement & permission tests
│
├── templates/                         # HTML5 templates
│   ├── base.html                     # Main layout & navigation
│   ├── home.html                     # Hero, search, latest jobs, specializations
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   ├── accounts/
│   │   ├── dashboard.html
│   │   └── profile.html
│   ├── jobs/
│   │   ├── job_list.html
│   │   ├── job_detail.html
│   │   ├── recommendations.html
│   │   └── saved_jobs.html
│   ├── applications/
│   │   ├── apply.html
│   │   └── my_applications.html
│   ├── recruiters/
│   │   ├── dashboard.html
│   │   ├── job_form.html
│   │   ├── job_confirm_delete.html
│   │   └── applicants.html
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       └── 500.html
│
├── static/                            # Static assets
│   ├── css/style.css                 # 100% Vanilla CSS design system
│   └── js/main.js                    # Mobile nav, dismissible alerts, confirmation dialogs
│
└── media/                             # Upload storage
    └── resumes/                      # Uploaded candidate resumes
```

---

## 🛠️ Installation & Setup (PowerShell on Windows)

### 1. Navigate to Project Directory
```powershell
cd C:\Users\Jeevasakthi\Documents\Smart_Job_Recommendation_Portal
```

### 2. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell script execution is restricted, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```powershell
python manage.py migrate
```

### 5. Generate Realistic Sample Data
```powershell
python manage.py populate_jobs
```

### 6. Run Test Suite
```powershell
python manage.py test
```

### 7. Start the Development Server
```powershell
python manage.py runserver
```
Or simply double-click `run.bat` in the project directory.

---

## 🌐 Default Access & Credentials

Once the server is running, open your web browser to:
- **Application Portal:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Administration:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### Pre-Configured Demonstration Accounts

| Role | Username | Password | Features to Test |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin12345` | Django Admin portal, inspecting all tables, permissions |
| **Recruiter Account** | `recruiter_demo` | `demo12345` | Recruiter Hub, posting vacancies, reviewing candidate resumes, updating statuses |
| **Job Seeker Account** | `seeker_demo` | `demo12345` | Smart recommendation matches (Python Developer: 100% match), applying for jobs, bookmarking |

---

## 🔑 Creating a New Superuser

To create your own custom administrative account:
```powershell
python manage.py createsuperuser
```
Follow the interactive prompts to set your preferred username, email, and password.
