from django.contrib import admin
from accounts.models import UserProfile, RecruiterProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'role', 'experience_level', 'preferred_location', 'created_at')
    list_filter = ('role', 'experience_level', 'preferred_job_type')
    search_fields = ('user__username', 'full_name', 'skills', 'preferred_job_role')

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'location', 'created_at')
    search_fields = ('company_name', 'user__username', 'industry', 'location')
