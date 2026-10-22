import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from accounts.models import RecruiterProfile
from jobs.models import Job
from applications.models import JobApplication

class RecruitersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.recruiter1 = User.objects.create_user(username='rec1', password='password123')
        self.recruiter2 = User.objects.create_user(username='rec2', password='password123')

        RecruiterProfile.objects.create(user=self.recruiter1, company_name='Company One')
        RecruiterProfile.objects.create(user=self.recruiter2, company_name='Company Two')

        self.job1 = Job.objects.create(
            job_title='Lead Architect',
            company_name='Company One',
            recruiter=self.recruiter1,
            location='Remote',
            min_salary=110000,
            max_salary=140000,
            required_skills='Python, AWS',
            description='Test',
            responsibilities='Test',
            qualifications='Test',
            application_deadline=timezone.now().date() + datetime.timedelta(days=20),
            is_active=True
        )

    def test_recruiter_cannot_edit_others_job(self):
        # Log in as recruiter2, attempt to edit recruiter1's job
        self.client.login(username='rec2', password='password123')
        response = self.client.get(reverse('job_edit', kwargs={'job_id': self.job1.id}))
        self.assertEqual(response.status_code, 403)

    def test_recruiter_can_edit_own_job(self):
        self.client.login(username='rec1', password='password123')
        response = self.client.get(reverse('job_edit', kwargs={'job_id': self.job1.id}))
        self.assertEqual(response.status_code, 200)
