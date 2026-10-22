from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import UserProfile, RecruiterProfile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testseeker', email='seeker@test.com', password='password123')
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='job_seeker',
            full_name='Test Seeker',
            skills='Python, Django, SQL',
            experience_level='Mid',
            preferred_job_role='Python Developer',
            preferred_location='Remote'
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testseeker',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        # Dashboard dispatcher redirects to seeker_dashboard
        self.assertRedirects(response, reverse('dashboard'), target_status_code=302)
        
        # Follow to seeker dashboard
        dash_response = self.client.get(reverse('seeker_dashboard'))
        self.assertEqual(dash_response.status_code, 200)

    def test_registration_seeker(self):
        response = self.client.post(reverse('register'), {
            'username': 'newseeker',
            'email': 'newseeker@test.com',
            'full_name': 'New Seeker',
            'role': 'job_seeker',
            'password': 'secretpassword123',
            'confirm_password': 'secretpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newseeker').exists())
        new_profile = UserProfile.objects.get(user__username='newseeker')
        self.assertEqual(new_profile.role, 'job_seeker')

    def test_registration_recruiter(self):
        response = self.client.post(reverse('register'), {
            'username': 'newrecruiter',
            'email': 'newrecruiter@test.com',
            'full_name': 'Recruiter Person',
            'company_name': 'Apex Corp',
            'role': 'recruiter',
            'password': 'secretpassword123',
            'confirm_password': 'secretpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RecruiterProfile.objects.filter(company_name='Apex Corp').exists())

    def test_duplicate_email_fails(self):
        response = self.client.post(reverse('register'), {
            'username': 'anotheruser',
            'email': 'seeker@test.com',  # already taken
            'full_name': 'Another User',
            'role': 'job_seeker',
            'password': 'secretpassword123',
            'confirm_password': 'secretpassword123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'An account with this email address already exists.')
