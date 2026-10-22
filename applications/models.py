from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Not Selected'),
        ('Selected', 'Hired / Selected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True, help_text="Why are you a great fit for this position?")
    expected_salary = models.PositiveIntegerField(null=True, blank=True, help_text="Annual USD salary expectation")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, help_text="Internal recruiter review notes")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.job_title} ({self.status})"
