import os
from django import forms
from django.core.exceptions import ValidationError
from applications.models import JobApplication

ALLOWED_RESUME_EXTENSIONS = ['.pdf', '.doc', '.docx']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def validate_resume_file(file):
    if file:
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_RESUME_EXTENSIONS:
            raise ValidationError("Unsupported file format. Please upload a PDF, DOC, or DOCX resume.")
        if file.size > MAX_FILE_SIZE:
            raise ValidationError("File size exceeds 5MB limit. Please upload a smaller file.")
    return file

class JobApplicationForm(forms.ModelForm):
    resume = forms.FileField(
        required=False,
        validators=[validate_resume_file],
        help_text="Upload your latest resume (PDF, DOC, DOCX - max 5MB)"
    )

    class Meta:
        model = JobApplication
        fields = ['resume', 'expected_salary', 'cover_letter']
        widgets = {
            'expected_salary': forms.NumberInput(attrs={'placeholder': 'e.g. 75000'}),
            'cover_letter': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Explain why your skills, experience, and accomplishments make you a top candidate for this role...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        resume = cleaned_data.get('resume')
        
        # If no new file uploaded, check if profile already has resume
        if not resume:
            if self.profile and self.profile.resume:
                cleaned_data['resume'] = self.profile.resume
            else:
                self.add_error('resume', "A resume file is mandatory. Please upload one.")
        return cleaned_data
