from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from jobs.models import Job, SavedJob
from jobs.forms import JobSearchForm
from jobs.recommendation import get_recommended_jobs, calculate_job_match
from applications.models import JobApplication
from accounts.models import UserProfile, RecruiterProfile
from accounts.decorators import job_seeker_required

def home_view(request):
    today = timezone.now().date()
    featured_jobs = Job.objects.filter(is_active=True, application_deadline__gte=today).order_by('-created_at')[:6]
    total_jobs = Job.objects.filter(is_active=True, application_deadline__gte=today).count()
    total_companies = RecruiterProfile.objects.count() + 15  # Includes partner companies
    
    # Categories counts
    categories_data = []
    for cat_key, cat_name in Job.CATEGORY_CHOICES:
        cnt = Job.objects.filter(category=cat_key, is_active=True, application_deadline__gte=today).count()
        categories_data.append({'key': cat_key, 'name': cat_name, 'count': cnt})

    context = {
        'featured_jobs': featured_jobs,
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'categories_data': categories_data,
        'search_form': JobSearchForm(),
    }
    return render(request, 'home.html', context)


def job_list_view(request):
    form = JobSearchForm(request.GET or None)
    today = timezone.now().date()
    jobs = Job.objects.filter(is_active=True, application_deadline__gte=today)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')
        experience_level = form.cleaned_data.get('experience_level')
        sort_by = form.cleaned_data.get('sort_by')

        if q:
            jobs = jobs.filter(
                Q(job_title__icontains=q) |
                Q(company_name__icontains=q) |
                Q(required_skills__icontains=q) |
                Q(description__icontains=q)
            )
        if location:
            jobs = jobs.filter(Q(location__icontains=location) | (Q(is_remote=True) if 'remote' in location.lower() else Q()))
        if category:
            jobs = jobs.filter(category=category)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)

        if sort_by == 'salary_desc':
            jobs = jobs.order_by('-max_salary')
        elif sort_by == 'deadline':
            jobs = jobs.order_by('application_deadline')
        else:
            jobs = jobs.order_by('-created_at')
    else:
        jobs = jobs.order_by('-created_at')

    # Paginate results
    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Saved jobs tracking for current user
    saved_job_ids = set()
    applied_job_ids = set()
    if request.user.is_authenticated:
        saved_job_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))
        applied_job_ids = set(JobApplication.objects.filter(applicant=request.user).values_list('job_id', flat=True))

    context = {
        'page_obj': page_obj,
        'form': form,
        'total_results': jobs.count(),
        'saved_job_ids': saved_job_ids,
        'applied_job_ids': applied_job_ids,
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    is_saved = False
    has_applied = False
    match_score = None
    breakdown = None

    if request.user.is_authenticated:
        is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
        has_applied = JobApplication.objects.filter(applicant=request.user, job=job).exists()
        
        # Calculate score for seeker
        profile = UserProfile.objects.filter(user=request.user).first()
        if profile and profile.role == 'job_seeker':
            res = calculate_job_match(profile, job)
            match_score = res['total_score']
            breakdown = res

    # Similar jobs in same category
    similar_jobs = Job.objects.filter(
        category=job.category,
        is_active=True,
        application_deadline__gte=timezone.now().date()
    ).exclude(id=job.id)[:3]

    context = {
        'job': job,
        'is_saved': is_saved,
        'has_applied': has_applied,
        'match_score': match_score,
        'breakdown': breakdown,
        'similar_jobs': similar_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
@job_seeker_required
def recommendations_view(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    recommended_jobs = get_recommended_jobs(request.user)

    # Filter by minimum match score if requested
    min_score = request.GET.get('min_score')
    if min_score and min_score.isdigit():
        min_val = int(min_score)
        recommended_jobs = [r for r in recommended_jobs if r['score'] >= min_val]

    saved_job_ids = set(SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True))

    context = {
        'profile': profile,
        'recommended_jobs': recommended_jobs,
        'saved_job_ids': saved_job_ids,
        'total_recommendations': len(recommended_jobs),
    }
    return render(request, 'jobs/recommendations.html', context)


@login_required
@job_seeker_required
def toggle_save_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    saved = SavedJob.objects.filter(user=request.user, job=job).first()

    if saved:
        saved.delete()
        messages.info(request, f"Removed '{job.job_title}' from your saved jobs.")
    else:
        SavedJob.objects.create(user=request.user, job=job)
        messages.success(request, f"Saved '{job.job_title}' to your saved jobs!")

    next_url = request.META.get('HTTP_REFERER') or 'saved_jobs'
    return redirect(next_url)


@login_required
@job_seeker_required
def saved_jobs_view(request):
    saved_records = SavedJob.objects.filter(user=request.user).select_related('job').order_by('-saved_at')
    
    # Check applied status
    applied_job_ids = set(JobApplication.objects.filter(applicant=request.user).values_list('job_id', flat=True))

    context = {
        'saved_records': saved_records,
        'applied_job_ids': applied_job_ids,
    }
    return render(request, 'jobs/saved_jobs.html', context)
