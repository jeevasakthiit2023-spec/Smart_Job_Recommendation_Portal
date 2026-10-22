from django.contrib import admin
from jobs.models import Job, SavedJob

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'category', 'experience_level', 'job_type', 'is_active', 'application_deadline', 'created_at')
    list_filter = ('is_active', 'category', 'job_type', 'experience_level')
    search_fields = ('job_title', 'company_name', 'required_skills', 'location')
    date_hierarchy = 'created_at'

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'saved_at')
    search_fields = ('user__username', 'job__job_title', 'job__company_name')
