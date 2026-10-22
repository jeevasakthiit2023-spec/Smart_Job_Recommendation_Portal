import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile, RecruiterProfile
from jobs.models import Job, SavedJob
from jobs.recommendation import calculate_job_match, get_recommended_jobs

class JobsRecommendationTestCase(TestCase):
    def setUp(self):
        self.recruiter_user = User.objects.create_user(username='recruiter1', password='password123')
        self.seeker_user = User.objects.create_user(username='seeker1', password='password123')

        self.seeker_profile = UserProfile.objects.create(
            user=self.seeker_user,
            role='job_seeker',
            full_name='Test Seeker',
            skills='Python, Django, SQL, Docker',
            experience_level='Mid',
            preferred_job_role='Python Developer',
            preferred_location='Remote'
        )

        today = timezone.now().date()
        self.matching_job = Job.objects.create(
            job_title='Python Developer',
            company_name='TechCorp',
            recruiter=self.recruiter_user,
            category='software_development',
            job_type='Full-Time',
            experience_level='Mid',
            location='Remote',
            is_remote=True,
            min_salary=80000,
            max_salary=100000,
            required_skills='Python, Django, SQL, Docker',
            description='Test description',
            responsibilities='Test responsibilities',
            qualifications='Test qualifications',
            application_deadline=today + datetime.timedelta(days=30),
            is_active=True
        )

        self.partial_job = Job.objects.create(
            job_title='Frontend Specialist',
            company_name='WebWorks',
            recruiter=self.recruiter_user,
            category='ui_ux',
            job_type='Contract',
            experience_level='Senior',
            location='New York, NY',
            is_remote=False,
            min_salary=70000,
            max_salary=90000,
            required_skills='JavaScript, React, CSS3',
            description='Test frontend job',
            responsibilities='Build UI',
            qualifications='Degree in CS',
            application_deadline=today + datetime.timedelta(days=30),
            is_active=True
        )

    def test_recommendation_algorithm_high_match(self):
        result = calculate_job_match(self.seeker_profile, self.matching_job)
        score = result['total_score']
        # High match should be close to 100% (50 skills + 20 role + 15 location + 15 exp = 100)
        self.assertEqual(score, 100)
        self.assertEqual(len(result['matched_skills']), 4)
        self.assertTrue(len(result['reasons']) >= 3)

    def test_recommendation_algorithm_low_match(self):
        result = calculate_job_match(self.seeker_profile, self.partial_job)
        score = result['total_score']
        # Low match: skills=0, role=0, location=0, exp=0 (Senior vs Mid diff=1 -> 8 pts)
        self.assertTrue(score < 30)

    def test_get_recommended_jobs_sorting(self):
        recommendations = get_recommended_jobs(self.seeker_user)
        self.assertTrue(len(recommendations) >= 2)
        # First recommendation must have higher score than second
        self.assertGreaterEqual(recommendations[0]['score'], recommendations[1]['score'])
        self.assertEqual(recommendations[0]['job'], self.matching_job)

    def test_saved_job_toggle(self):
        saved = SavedJob.objects.create(user=self.seeker_user, job=self.matching_job)
        self.assertTrue(SavedJob.objects.filter(user=self.seeker_user, job=self.matching_job).exists())
        
        # Test unique constraint
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            SavedJob.objects.create(user=self.seeker_user, job=self.matching_job)
