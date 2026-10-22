from django import forms
from jobs.models import Job
from applications.models import JobApplication

class JobCreateUpdateForm(forms.ModelForm):
    application_deadline = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Deadline for candidate submissions"
    )

    class Meta:
        model = Job
        fields = [
            'job_title', 'company_name', 'category', 'job_type',
            'experience_level', 'location', 'is_remote',
            'min_salary', 'max_salary', 'required_skills',
            'description', 'responsibilities', 'qualifications',
            'application_deadline', 'is_active'
        ]
        widgets = {
            'job_title': forms.TextInput(attrs={'placeholder': 'e.g. Senior Python / Django Developer'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Apex Tech Innovations'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Austin, TX or Remote'}),
            'min_salary': forms.NumberInput(attrs={'placeholder': 'e.g. 75000'}),
            'max_salary': forms.NumberInput(attrs={'placeholder': 'e.g. 110000'}),
            'required_skills': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Python, Django, PostgreSQL, Docker, Git, REST APIs'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Provide an overview of the role and what makes your team unique...'}),
            'responsibilities': forms.Textarea(attrs={'rows': 4, 'placeholder': '- Architect backend APIs\n- Maintain test suites\n- Collaborate with frontend teams'}),
            'qualifications': forms.Textarea(attrs={'rows': 4, 'placeholder': '- 3+ years experience with Python & Django\n- Solid SQL skills\n- Strong team communication'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        min_salary = cleaned_data.get('min_salary')
        max_salary = cleaned_data.get('max_salary')

        if min_salary and max_salary and min_salary > max_salary:
            self.add_error('max_salary', "Maximum salary must be greater than or equal to minimum salary.")
        return cleaned_data


class ApplicantStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional internal recruiter notes (e.g. Interview scheduled for Friday)...'}),
        }
