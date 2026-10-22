from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )
    EXPERIENCE_CHOICES = (
        ('Fresher', 'Fresher / Entry Level (0-1 yr)'),
        ('Junior', 'Junior (1-3 yrs)'),
        ('Mid', 'Mid-Level (3-5 yrs)'),
        ('Senior', 'Senior (5-8 yrs)'),
        ('Lead', 'Lead / Principal (8+ yrs)'),
    )
    JOB_TYPE_CHOICES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    full_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    headline = models.CharField(max_length=200, blank=True, help_text="e.g. Senior Python & Django Engineer")
    education = models.CharField(max_length=255, blank=True, help_text="e.g. B.S. in Computer Science")
    skills = models.TextField(blank=True, help_text="Comma-separated skills, e.g. Python, Django, SQL, HTML, CSS")
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    preferred_job_role = models.CharField(max_length=150, blank=True, help_text="e.g. Python Developer, Full Stack Engineer")
    preferred_location = models.CharField(max_length=150, blank=True, help_text="e.g. Remote, New York, San Francisco")
    preferred_job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, blank=True)
    expected_salary = models.PositiveIntegerField(null=True, blank=True, help_text="Annual expected salary in USD")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name or self.user.username} ({self.get_role_display()})"

    @property
    def is_job_seeker(self):
        return self.role == 'job_seeker'

    @property
    def is_recruiter(self):
        return self.role == 'recruiter'

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip().lower() for s in self.skills.split(',') if s.strip()]


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=150)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True, help_text="e.g. Information Technology, FinTech")
    location = models.CharField(max_length=150, blank=True, help_text="e.g. San Francisco, CA or Remote")
    contact_number = models.CharField(max_length=25, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
