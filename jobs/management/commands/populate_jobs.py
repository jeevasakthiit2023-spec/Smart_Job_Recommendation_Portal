import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile, RecruiterProfile
from jobs.models import Job

class Command(BaseCommand):
    help = "Populate database with demonstration recruiters, job seekers, and realistic job openings."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Initializing sample data generation..."))

        # 1. Create or get Demo Recruiter
        recruiter_user, created = User.objects.get_or_create(
            username="recruiter_demo",
            defaults={"email": "recruiter@demo-jobs.local", "first_name": "Sarah", "last_name": "Jenkins"}
        )
        if created:
            recruiter_user.set_password("demo12345")
            recruiter_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo recruiter user: 'recruiter_demo' / 'demo12345'"))

        rec_profile, _ = RecruiterProfile.objects.get_or_create(
            user=recruiter_user,
            defaults={
                "company_name": "Apex Cloud & Software Labs",
                "company_website": "https://apexcloud.example.org",
                "industry": "Cloud Software & Enterprise SaaS",
                "location": "San Francisco, CA / Remote",
                "contact_number": "+1 (415) 555-0199",
                "company_description": "Apex Cloud is an enterprise SaaS innovator developing resilient cloud infrastructure and developer productivity platforms."
            }
        )

        UserProfile.objects.get_or_create(
            user=recruiter_user,
            defaults={"role": "recruiter", "full_name": "Sarah Jenkins"}
        )

        # 2. Create or get Demo Job Seeker
        seeker_user, created = User.objects.get_or_create(
            username="seeker_demo",
            defaults={"email": "seeker@demo-jobs.local", "first_name": "Alex", "last_name": "Morgan"}
        )
        if created:
            seeker_user.set_password("demo12345")
            seeker_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo job seeker user: 'seeker_demo' / 'demo12345'"))

        UserProfile.objects.get_or_create(
            user=seeker_user,
            defaults={
                "role": "job_seeker",
                "full_name": "Alex Morgan",
                "headline": "Mid-Level Python & Django Backend Engineer",
                "phone": "+1 (555) 234-5678",
                "education": "B.S. in Computer Science - State University (2021)",
                "skills": "Python, Django, SQL, PostgreSQL, REST APIs, Git, Docker, Linux",
                "experience_level": "Mid",
                "years_of_experience": 3,
                "preferred_job_role": "Python Developer",
                "preferred_location": "Remote",
                "preferred_job_type": "Full-Time",
                "expected_salary": 92000,
                "bio": "Passionate backend software engineer with 3+ years of experience building secure, scalable web APIs and database systems using Python, Django, and PostgreSQL."
            }
        )

        # 3. Create Second Recruiter for Company Diversity
        recruiter_user2, created2 = User.objects.get_or_create(
            username="techhire_recruiter",
            defaults={"email": "hiring@techhire-global.local", "first_name": "Marcus", "last_name": "Vance"}
        )
        if created2:
            recruiter_user2.set_password("demo12345")
            recruiter_user2.save()

        RecruiterProfile.objects.get_or_create(
            user=recruiter_user2,
            defaults={
                "company_name": "NexGen Data Dynamics",
                "company_website": "https://nexgendata.example.org",
                "industry": "Data Analytics & AI",
                "location": "New York, NY",
                "contact_number": "+1 (212) 555-8741",
                "company_description": "NexGen provides real-time analytics platforms, business intelligence dashboards, and distributed data pipelines."
            }
        )
        UserProfile.objects.get_or_create(
            user=recruiter_user2,
            defaults={"role": "recruiter", "full_name": "Marcus Vance"}
        )

        # 4. Realistic Job Openings
        today = timezone.now().date()
        future_deadline = today + datetime.timedelta(days=45)

        sample_jobs_data = [
            {
                "job_title": "Python Developer [Sample Demo]",
                "company_name": "Apex Cloud & Software Labs",
                "recruiter": recruiter_user,
                "category": "software_development",
                "job_type": "Full-Time",
                "experience_level": "Mid",
                "location": "Remote",
                "is_remote": True,
                "min_salary": 85000,
                "max_salary": 110000,
                "required_skills": "Python, Django, REST APIs, PostgreSQL, Docker, Git",
                "description": "We are seeking a talented Python Developer to join our backend architecture team. You will build resilient microservices, design performant database schemas, and integrate core third-party APIs.",
                "responsibilities": "- Design, build, and maintain high-performance Python services.\n- Implement RESTful endpoints and clean architecture.\n- Write comprehensive automated unit and integration tests.\n- Optimize database queries and caching layers.",
                "qualifications": "- 2-4 years of professional Python programming experience.\n- Demonstrated experience with Django or Flask frameworks.\n- Solid knowledge of SQL (PostgreSQL preferred).\n- Experience with Docker containerization and Git version control.",
                "application_deadline": future_deadline,
                "is_active": True,
            },
            {
                "job_title": "Django Developer [Sample Demo]",
                "company_name": "NexGen Data Dynamics",
                "recruiter": recruiter_user2,
                "category": "web_development",
                "job_type": "Full-Time",
                "experience_level": "Mid",
                "location": "Remote / New York, NY",
                "is_remote": True,
                "min_salary": 90000,
                "max_salary": 120000,
                "required_skills": "Python, Django, Django REST Framework, Celery, Redis, SQL",
                "description": "NexGen is looking for a senior Django Developer to drive the expansion of our web applications and customer analytics portal. You will take ownership of full-cycle feature delivery from database models to REST endpoints.",
                "responsibilities": "- Develop robust web modules using Django and Django REST Framework.\n- Manage asynchronous task processing using Celery and Redis.\n- Ensure high availability, data security, and compliance.\n- Collaborate with frontend engineers and UX designers.",
                "qualifications": "- 3+ years experience developing production web apps with Django.\n- Strong foundation in relational database design and ORM optimization.\n- Understanding of caching, background queues, and cloud deployments.",
                "application_deadline": future_deadline + datetime.timedelta(days=10),
                "is_active": True,
            },
            {
                "job_title": "Web Developer [Sample Demo]",
                "company_name": "Apex Cloud & Software Labs",
                "recruiter": recruiter_user,
                "category": "web_development",
                "job_type": "Full-Time",
                "experience_level": "Junior",
                "location": "Austin, TX",
                "is_remote": False,
                "min_salary": 65000,
                "max_salary": 85000,
                "required_skills": "HTML5, CSS3, JavaScript, Python, Django, Responsive Design",
                "description": "Join our interactive web development team to craft modern, accessible, and responsive user interfaces powered by a Python web backend.",
                "responsibilities": "- Build modular, responsive web pages adhering to modern HTML5 and CSS3 standards.\n- Integrate backend template tags and REST API data.\n- Maintain cross-browser compatibility and mobile responsiveness.\n- Participate in agile sprint planning and code reviews.",
                "qualifications": "- 1-2 years experience building web applications.\n- Strong understanding of semantic HTML5, CSS Grid/Flexbox, and modern JavaScript.\n- Familiarity with Python web frameworks like Django.",
                "application_deadline": future_deadline + datetime.timedelta(days=20),
                "is_active": True,
            },
            {
                "job_title": "Frontend Developer [Sample Demo]",
                "company_name": "NexGen Data Dynamics",
                "recruiter": recruiter_user2,
                "category": "ui_ux",
                "job_type": "Full-Time",
                "experience_level": "Mid",
                "location": "San Francisco, CA",
                "is_remote": True,
                "min_salary": 85000,
                "max_salary": 115000,
                "required_skills": "JavaScript, HTML5, CSS3, UI/UX, REST APIs, Web Accessibility",
                "description": "Are you passionate about beautiful typography, micro-interactions, and blazing-fast client interfaces? We are hiring a Frontend Developer to modernize our user portals.",
                "responsibilities": "- Translate UI/UX wireframes into pixel-perfect web pages.\n- Optimize frontend asset delivery, DOM rendering, and accessibility.\n- Implement dynamic client-side interactions and form validations.",
                "qualifications": "- 2+ years of hands-on frontend web development experience.\n- In-depth knowledge of modern Vanilla JavaScript and CSS3 architecture.\n- Passion for clean design and intuitive user experience.",
                "application_deadline": future_deadline + datetime.timedelta(days=15),
                "is_active": True,
            },
            {
                "job_title": "Software Engineer [Sample Demo]",
                "company_name": "Apex Cloud & Software Labs",
                "recruiter": recruiter_user,
                "category": "software_development",
                "job_type": "Full-Time",
                "experience_level": "Senior",
                "location": "Seattle, WA",
                "is_remote": True,
                "min_salary": 120000,
                "max_salary": 160000,
                "required_skills": "Python, System Design, Algorithms, SQL, Docker, Microservices",
                "description": "We are seeking an experienced Software Engineer to tackle challenging scaling problems in distributed systems and data processing.",
                "responsibilities": "- Architect distributed software systems capable of processing millions of daily transactions.\n- Lead technical architecture discussions and mentor junior teammates.\n- Enforce code quality, testing standards, and continuous integration.",
                "qualifications": "- 5+ years of software engineering experience.\n- Proven track record with large-scale backend systems in Python.\n- Strong command of computer science fundamentals, data structures, and algorithms.",
                "application_deadline": future_deadline + datetime.timedelta(days=30),
                "is_active": True,
            },
            {
                "job_title": "SQL Developer & Database Specialist [Sample Demo]",
                "company_name": "NexGen Data Dynamics",
                "recruiter": recruiter_user2,
                "category": "database_sql",
                "job_type": "Full-Time",
                "experience_level": "Mid",
                "location": "Chicago, IL",
                "is_remote": False,
                "min_salary": 80000,
                "max_salary": 105000,
                "required_skills": "SQL, PostgreSQL, Query Optimization, Database Indexing, ETL, Python",
                "description": "Join our data infrastructure squad as a dedicated SQL Developer. You will oversee query optimization, database partitioning, schema migrations, and ETL reporting pipelines.",
                "responsibilities": "- Write complex, high-efficiency SQL queries and stored procedures.\n- Diagnose query bottlenecks, design indexing strategies, and analyze execution plans.\n- Build automated data ingestion scripts with Python.\n- Maintain database backup schedules, data integrity, and disaster recovery.",
                "qualifications": "- 3+ years of intensive SQL and relational database engineering (PostgreSQL / MySQL).\n- Solid understanding of normalization, indexing, and transactional isolation.\n- Working knowledge of scripting in Python.",
                "application_deadline": future_deadline + datetime.timedelta(days=25),
                "is_active": True,
            },
            {
                "job_title": "Junior Software Developer [Sample Demo]",
                "company_name": "Apex Cloud & Software Labs",
                "recruiter": recruiter_user,
                "category": "software_development",
                "job_type": "Full-Time",
                "experience_level": "Fresher",
                "location": "Remote",
                "is_remote": True,
                "min_salary": 55000,
                "max_salary": 72000,
                "required_skills": "Python, SQL, HTML, CSS, Git, Basic Algorithms",
                "description": "Kickstart your software engineering career with our supportive, mentorship-focused development program. Junior developers receive guided onboarding, pair programming, and career growth pathways.",
                "responsibilities": "- Collaborate with senior engineers on application bug fixes and feature tickets.\n- Write clean, documented Python code and unit tests.\n- Participate in daily standups and agile sprint retrospectives.",
                "qualifications": "- Degree in Computer Science, Software Engineering, or equivalent coding experience.\n- Foundational proficiency in Python and basic database concepts.\n- Eagerness to learn, ask thoughtful questions, and grow as an engineer.",
                "application_deadline": future_deadline + datetime.timedelta(days=12),
                "is_active": True,
            },
            {
                "job_title": "Cloud & DevOps Engineer [Sample Demo]",
                "company_name": "Apex Cloud & Software Labs",
                "recruiter": recruiter_user,
                "category": "cloud_devops",
                "job_type": "Full-Time",
                "experience_level": "Mid",
                "location": "Denver, CO / Remote",
                "is_remote": True,
                "min_salary": 95000,
                "max_salary": 130000,
                "required_skills": "Docker, Kubernetes, Linux, CI/CD, Python, Cloud Infrastructure",
                "description": "Manage our containerized cloud environments, automate deployment pipelines, and maintain 99.99% system uptime across global regions.",
                "responsibilities": "- Maintain automated CI/CD deployment pipelines.\n- Monitor infrastructure health, alert thresholds, and system logs.\n- Automate operational runbooks using Python and shell scripts.",
                "qualifications": "- 3+ years working in DevOps or Systems Administration.\n- Strong Linux command-line, Docker container, and networking expertise.",
                "application_deadline": future_deadline + datetime.timedelta(days=35),
                "is_active": True,
            },
            {
                "job_title": "Data Analyst & Business Intelligence [Sample Demo]",
                "company_name": "NexGen Data Dynamics",
                "recruiter": recruiter_user2,
                "category": "data_ai",
                "job_type": "Contract",
                "experience_level": "Junior",
                "location": "Boston, MA",
                "is_remote": True,
                "min_salary": 60000,
                "max_salary": 80000,
                "required_skills": "SQL, Python, Data Visualization, Excel, Statistics",
                "description": "Transform raw business metrics into actionable visual intelligence for executive stakeholders and product leaders.",
                "responsibilities": "- Query multi-table relational databases to extract KPI metrics.\n- Produce weekly visual dashboards and executive performance summaries.\n- Analyze candidate-to-hire conversion funnels.",
                "qualifications": "- Strong SQL query writing skills.\n- Experience with data visualization in Python or BI tools.\n- Clear written and verbal communication.",
                "application_deadline": future_deadline + datetime.timedelta(days=18),
                "is_active": True,
            }
        ]

        created_count = 0
        for item in sample_jobs_data:
            job, created = Job.objects.get_or_create(
                job_title=item["job_title"],
                company_name=item["company_name"],
                defaults=item
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {created_count} realistic demonstration job openings."))
        self.stdout.write(self.style.SUCCESS("Demo credentials:\n- Recruiter: username 'recruiter_demo' / password 'demo12345'\n- Seeker: username 'seeker_demo' / password 'demo12345'"))
