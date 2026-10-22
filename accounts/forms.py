import os
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import UserProfile, RecruiterProfile

ALLOWED_RESUME_EXTENSIONS = ['.pdf', '.doc', '.docx']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_resume_file(file):
    if file:
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_RESUME_EXTENSIONS:
            raise ValidationError("Unsupported file format. Please upload PDF, DOC, or DOCX documents.")
        if file.size > MAX_FILE_SIZE:
            raise ValidationError("File size exceeds 5MB limit. Please upload a smaller resume.")
    return file

class UserRegisterForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker (Browse, Apply & Get Recommendations)'),
        ('recruiter', 'Recruiter (Post Jobs & Manage Candidates)'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='job_seeker')
    full_name = forms.CharField(max_length=150, required=True, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'e.g. John Doe'}))
    company_name = forms.CharField(max_length=150, required=False, label="Company Name (For Recruiters)", widget=forms.TextInput(attrs={'placeholder': 'e.g. Acme Technologies'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Choose a strong password'}), label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a unique username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        role = cleaned_data.get('role')
        company_name = cleaned_data.get('company_name')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        if len(password or '') < 6:
            self.add_error('password', "Password must be at least 6 characters long.")

        if role == 'recruiter' and not company_name:
            self.add_error('company_name', "Company name is required for recruiter registration.")

        return cleaned_data


class JobSeekerProfileForm(forms.ModelForm):
    resume = forms.FileField(required=False, validators=[validate_resume_file], help_text="Upload PDF, DOC, or DOCX (max 5MB)")

    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'phone', 'headline', 'education',
            'skills', 'experience_level', 'years_of_experience',
            'preferred_job_role', 'preferred_location', 'preferred_job_type',
            'expected_salary', 'resume', 'bio'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full legal name'}),
            'phone': forms.TextInput(attrs={'placeholder': '+1 (555) 012-3456'}),
            'headline': forms.TextInput(attrs={'placeholder': 'e.g. Senior Python Developer | Django & Cloud Specialist'}),
            'education': forms.TextInput(attrs={'placeholder': 'e.g. Bachelor of Science in Computer Science, 2022'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter comma-separated skills: Python, Django, REST API, SQL, JavaScript, Docker'}),
            'preferred_job_role': forms.TextInput(attrs={'placeholder': 'e.g. Python Developer, Full Stack Engineer'}),
            'preferred_location': forms.TextInput(attrs={'placeholder': 'e.g. Remote, San Francisco, New York'}),
            'expected_salary': forms.NumberInput(attrs={'placeholder': 'Annual salary in USD e.g. 85000'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share a summary of your professional background and career goals...'}),
        }


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = [
            'company_name', 'company_website', 'industry',
            'location', 'contact_number', 'company_description'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Company name'}),
            'company_website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'industry': forms.TextInput(attrs={'placeholder': 'e.g. FinTech, SaaS, Cloud Services'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Austin, TX or Remote'}),
            'contact_number': forms.TextInput(attrs={'placeholder': '+1 (555) 987-6543'}),
            'company_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Brief description of your company, team, and hiring culture...'}),
        }
