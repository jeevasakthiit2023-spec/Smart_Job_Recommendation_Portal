from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from jobs.models import Job
from applications.models import JobApplication
from applications.forms import JobApplicationForm
from accounts.models import UserProfile
from accounts.decorators import job_seeker_required

@login_required
@job_seeker_required
def apply_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # 1. Check if job is still active and open
    if not job.is_open:
        messages.error(request, "This job vacancy has expired or is no longer accepting new applications.")
        return redirect('job_detail', job_id=job.id)

    # 2. Prevent duplicate application
    existing_app = JobApplication.objects.filter(job=job, applicant=request.user).first()
    if existing_app:
        messages.warning(request, f"You have already applied for '{job.job_title}'. Your current status is: {existing_app.get_status_display()}.")
        return redirect('my_applications')

    profile = UserProfile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES, profile=profile)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()

            messages.success(request, f"Congratulations! Your application for '{job.job_title}' at {job.company_name} was submitted successfully.")
            return redirect('my_applications')
        else:
            messages.error(request, "Please correct the errors in the application form below.")
    else:
        initial_data = {}
        if profile and profile.expected_salary:
            initial_data['expected_salary'] = profile.expected_salary
        form = JobApplicationForm(initial=initial_data, profile=profile)

    context = {
        'job': job,
        'form': form,
        'profile': profile,
    }
    return render(request, 'applications/apply.html', context)


@login_required
@job_seeker_required
def my_applications_view(request):
    applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')
    
    # Summary counts
    total = applications.count()
    pending = applications.filter(status='Pending').count()
    shortlisted = applications.filter(status='Shortlisted').count()
    selected = applications.filter(status='Selected').count()
    rejected = applications.filter(status='Rejected').count()

    context = {
        'applications': applications,
        'total': total,
        'pending': pending,
        'shortlisted': shortlisted,
        'selected': selected,
        'rejected': rejected,
    }
    return render(request, 'applications/my_applications.html', context)
