from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from accounts.models import UserProfile, RecruiterProfile
from accounts.forms import UserRegisterForm, JobSeekerProfileForm, RecruiterProfileForm
from accounts.decorators import job_seeker_required
from applications.models import JobApplication
from jobs.models import Job, SavedJob
from jobs.recommendation import get_recommended_jobs

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            role = form.cleaned_data['role']
            full_name = form.cleaned_data.get('full_name', '')
            company_name = form.cleaned_data.get('company_name', '')

            if role == 'recruiter':
                RecruiterProfile.objects.create(
                    user=user,
                    company_name=company_name or f"{user.username}'s Company"
                )
                UserProfile.objects.create(
                    user=user,
                    role='recruiter',
                    full_name=full_name
                )
            else:
                UserProfile.objects.create(
                    user=user,
                    role='job_seeker',
                    full_name=full_name
                )

            # Auto-login after registration
            login(request, user)
            messages.success(request, f"Welcome to SmartJob Portal, {user.username}! Your account has been created.")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors in the registration form.")
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard_dispatcher(request):
    """Redirects users to their specific dashboard based on role."""
    if RecruiterProfile.objects.filter(user=request.user).exists():
        return redirect('recruiter_dashboard')
    return redirect('seeker_dashboard')


@login_required
@job_seeker_required
def seeker_dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'role': 'job_seeker'})
    
    # Applications stats
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    total_applied = applications.count()
    pending_count = applications.filter(status='Pending').count()
    shortlisted_count = applications.filter(status='Shortlisted').count()
    selected_count = applications.filter(status='Selected').count()
    rejected_count = applications.filter(status='Rejected').count()

    # Saved jobs count
    saved_count = SavedJob.objects.filter(user=request.user).count()

    # Smart Recommendations (Top 4 preview)
    recommended_jobs = get_recommended_jobs(request.user, limit=4)

    context = {
        'profile': profile,
        'total_applied': total_applied,
        'pending_count': pending_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'saved_count': saved_count,
        'recent_applications': applications[:5],
        'recommended_jobs': recommended_jobs,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    is_recruiter = RecruiterProfile.objects.filter(user=request.user).exists()

    if is_recruiter:
        rec_profile, _ = RecruiterProfile.objects.get_or_create(user=request.user, defaults={'company_name': f"{request.user.username} Co."})
        if request.method == 'POST':
            form = RecruiterProfileForm(request.POST, instance=rec_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Recruiter company profile updated successfully.")
                return redirect('profile')
        else:
            form = RecruiterProfileForm(instance=rec_profile)
        return render(request, 'accounts/profile.html', {'form': form, 'is_recruiter': True, 'profile': rec_profile})
    else:
        seeker_profile, _ = UserProfile.objects.get_or_create(user=request.user, defaults={'role': 'job_seeker'})
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=seeker_profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Job seeker profile and resume updated successfully.")
                return redirect('profile')
            else:
                messages.error(request, "Please fix the errors below.")
        else:
            form = JobSeekerProfileForm(instance=seeker_profile)
        return render(request, 'accounts/profile.html', {'form': form, 'is_recruiter': False, 'profile': seeker_profile})


def custom_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

def custom_404(request, exception=None):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)
