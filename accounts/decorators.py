from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from accounts.models import RecruiterProfile, UserProfile

def job_seeker_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to access this page.")
            return redirect('login')
        
        # If recruiter tries to access job seeker specific page
        if RecruiterProfile.objects.filter(user=request.user).exists():
            messages.warning(request, "This area is designed for job seekers. Recruiter dashboard is shown below.")
            return redirect('recruiter_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def recruiter_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log in with a recruiter account.")
            return redirect('login')
        
        if not RecruiterProfile.objects.filter(user=request.user).exists():
            messages.error(request, "Access restricted. You need a verified recruiter account.")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
