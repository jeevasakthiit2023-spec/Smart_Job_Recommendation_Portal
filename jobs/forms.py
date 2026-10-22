from django import forms
from jobs.models import Job

class JobSearchForm(forms.Form):
    q = forms.CharField(required=False, label="Keywords", widget=forms.TextInput(attrs={'placeholder': 'Job title, skills, or company...'}))
    location = forms.CharField(required=False, label="Location", widget=forms.TextInput(attrs={'placeholder': 'City, state, or Remote...'}))
    category = forms.ChoiceField(required=False, choices=[('', 'All Categories')] + list(Job.CATEGORY_CHOICES))
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Job Types')] + list(Job.JOB_TYPE_CHOICES))
    experience_level = forms.ChoiceField(required=False, choices=[('', 'All Experience Levels')] + list(Job.EXPERIENCE_CHOICES))
    sort_by = forms.ChoiceField(required=False, choices=[
        ('newest', 'Newest Openings'),
        ('salary_desc', 'Highest Salary'),
        ('deadline', 'Closing Soonest'),
    ], initial='newest')
