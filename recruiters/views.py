from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponseForbidden

from accounts.decorators import recruiter_required
from accounts.models import RecruiterProfile, UserProfile
from jobs.models import Job
from applications.models import JobApplication
from recruiters.forms import JobCreateUpdateForm, ApplicantStatusForm

@login_required
@recruiter_required
def recruiter_dashboard(request):
    profile = get_object_or_404(RecruiterProfile, user=request.user)
    
    # Recruiter's jobs
    my_jobs = Job.objects.filter(recruiter=request.user).annotate(
        app_count=Count('applications')
    ).order_by('-created_at')

    today = timezone.now().date()
    total_jobs = my_jobs.count()
    active_jobs = my_jobs.filter(is_active=True, application_deadline__gte=today).count()
    
    total_applicants = JobApplication.objects.filter(job__recruiter=request.user).count()
    shortlisted_applicants = JobApplication.objects.filter(job__recruiter=request.user, status='Shortlisted').count()

    context = {
        'profile': profile,
        'my_jobs': my_jobs,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applicants': total_applicants,
        'shortlisted_applicants': shortlisted_applicants,
    }
    return render(request, 'recruiters/dashboard.html', context)


@login_required
@recruiter_required
def job_create_view(request):
    profile = RecruiterProfile.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = JobCreateUpdateForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            if not job.company_name and profile:
                job.company_name = profile.company_name
            job.save()
            messages.success(request, f"Job posting '{job.job_title}' created successfully!")
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        initial = {}
        if profile:
            initial['company_name'] = profile.company_name
            initial['location'] = profile.location
        form = JobCreateUpdateForm(initial=initial)

    return render(request, 'recruiters/job_form.html', {'form': form, 'is_edit': False})


@login_required
@recruiter_required
def job_edit_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.recruiter != request.user:
        return HttpResponseForbidden("You are not authorized to edit this job posting.")

    if request.method == 'POST':
        form = JobCreateUpdateForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job posting '{job.job_title}' updated successfully.")
            return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = JobCreateUpdateForm(instance=job)

    return render(request, 'recruiters/job_form.html', {'form': form, 'is_edit': True, 'job': job})


@login_required
@recruiter_required
def job_toggle_status_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.recruiter != request.user:
        return HttpResponseForbidden("You do not own this job posting.")

    job.is_active = not job.is_active
    job.save()
    status_str = "activated" if job.is_active else "deactivated"
    messages.info(request, f"Job '{job.job_title}' has been {status_str}.")
    return redirect('recruiter_dashboard')


@login_required
@recruiter_required
def job_delete_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.recruiter != request.user:
        return HttpResponseForbidden("You do not own this job posting.")

    if request.method == 'POST':
        title = job.job_title
        job.delete()
        messages.success(request, f"Job posting '{title}' was permanently deleted.")
        return redirect('recruiter_dashboard')

    return render(request, 'recruiters/job_confirm_delete.html', {'job': job})


@login_required
@recruiter_required
def applicants_view(request, job_id=None):
    recruiter_jobs = Job.objects.filter(recruiter=request.user)

    if job_id:
        selected_job = get_object_or_404(Job, id=job_id, recruiter=request.user)
        applications = JobApplication.objects.filter(job=selected_job)
    else:
        selected_job = None
        applications = JobApplication.objects.filter(job__recruiter=request.user)

    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    applications = applications.select_related('job', 'applicant', 'applicant__user_profile').order_by('-applied_at')

    context = {
        'selected_job': selected_job,
        'recruiter_jobs': recruiter_jobs,
        'applications': applications,
        'current_status': status_filter or 'All',
        'status_choices': JobApplication.STATUS_CHOICES,
    }
    return render(request, 'recruiters/applicants.html', context)


@login_required
@recruiter_required
def update_applicant_status_view(request, app_id):
    application = get_object_or_404(JobApplication, id=app_id)
    if application.job.recruiter != request.user:
        return HttpResponseForbidden("Unauthorized application access.")

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')

        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.notes = notes
            application.save()
            messages.success(request, f"Candidate {application.applicant.username} updated to '{application.get_status_display()}'.")
        else:
            messages.error(request, "Invalid status choice.")

    next_url = request.META.get('HTTP_REFERER') or 'applicants_all'
    return redirect(next_url)
