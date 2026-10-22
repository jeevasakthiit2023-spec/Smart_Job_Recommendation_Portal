from django.contrib import admin
from applications.models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'expected_salary', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__job_title', 'job__company_name', 'applicant__username', 'applicant__email')
    list_editable = ('status',)
