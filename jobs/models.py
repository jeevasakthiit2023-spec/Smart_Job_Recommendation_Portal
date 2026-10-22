from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Job(models.Model):
    CATEGORY_CHOICES = (
        ('software_development', 'Software Development'),
        ('web_development', 'Web & Full Stack'),
        ('data_ai', 'Data Science & AI'),
        ('cloud_devops', 'Cloud & DevOps'),
        ('database_sql', 'Database & SQL Engineering'),
        ('qa_testing', 'QA & Automation Testing'),
        ('ui_ux', 'UI / UX & Frontend'),
        ('cybersecurity', 'Cybersecurity & Infrastructure'),
    )

    JOB_TYPE_CHOICES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    EXPERIENCE_CHOICES = (
        ('Fresher', 'Fresher / Entry Level (0-1 yr)'),
        ('Junior', 'Junior (1-3 yrs)'),
        ('Mid', 'Mid-Level (3-5 yrs)'),
        ('Senior', 'Senior (5-8 yrs)'),
        ('Lead', 'Lead / Principal (8+ yrs)'),
    )

    job_title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='software_development')
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='Full-Time')
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES, default='Mid')
    location = models.CharField(max_length=150)
    is_remote = models.BooleanField(default=False)
    min_salary = models.PositiveIntegerField(help_text="Annual salary in USD (e.g. 60000)")
    max_salary = models.PositiveIntegerField(help_text="Annual salary in USD (e.g. 95000)")
    required_skills = models.TextField(help_text="Comma-separated skills (e.g. Python, Django, SQL, REST APIs, Git)")
    description = models.TextField()
    responsibilities = models.TextField()
    qualifications = models.TextField()
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

    @property
    def is_expired(self):
        return self.application_deadline < timezone.now().date()

    @property
    def is_open(self):
        return self.is_active and not self.is_expired

    def get_skills_list(self):
        if not self.required_skills:
            return []
        return [s.strip() for s in self.required_skills.split(',') if s.strip()]

    def get_normalized_skills(self):
        return [s.strip().lower() for s in self.required_skills.split(',') if s.strip()]


class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by_users')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.job.job_title}"
