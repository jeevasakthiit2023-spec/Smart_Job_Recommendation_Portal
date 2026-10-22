import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from jobs.models import Job
from applications.models import JobApplication

class ApplicationsTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username='rec_app', password='password123')
        self.seeker = User.objects.create_user(username='seek_app', password='password123')
        
        self.job = Job.objects.create(
            job_title='Backend Developer',
            company_name='AppCorp',
            recruiter=self.recruiter,
            location='Remote',
            min_salary=70000,
            max_salary=90000,
            required_skills='Python, SQL',
            description='Test description',
            responsibilities='Test responsibilities',
            qualifications='Test qualifications',
            application_deadline=timezone.now().date() + datetime.timedelta(days=15),
            is_active=True
        )

    def test_application_creation(self):
        fake_resume = SimpleUploadedFile("resume.pdf", b"dummy pdf content", content_type="application/pdf")
        app = JobApplication.objects.create(
            job=self.job,
            applicant=self.seeker,
            resume=fake_resume,
            expected_salary=80000,
            cover_letter="I am very excited about this role."
        )
        self.assertEqual(app.status, 'Pending')
        self.assertEqual(JobApplication.objects.filter(job=self.job).count(), 1)

    def test_duplicate_application_prevented(self):
        from django.db import IntegrityError
        fake_resume1 = SimpleUploadedFile("resume1.pdf", b"dummy pdf 1", content_type="application/pdf")
        fake_resume2 = SimpleUploadedFile("resume2.pdf", b"dummy pdf 2", content_type="application/pdf")
        
        JobApplication.objects.create(job=self.job, applicant=self.seeker, resume=fake_resume1)
        
        with self.assertRaises(IntegrityError):
            JobApplication.objects.create(job=self.job, applicant=self.seeker, resume=fake_resume2)
