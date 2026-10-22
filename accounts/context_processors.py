from accounts.models import UserProfile, RecruiterProfile
from jobs.models import SavedJob
from applications.models import JobApplication

def user_role_context(request):
    context = {
        'is_seeker': False,
        'is_recruiter': False,
        'current_profile': None,
        'saved_jobs_count': 0,
        'applications_count': 0,
    }
    if request.user.is_authenticated:
        try:
            r_profile = RecruiterProfile.objects.filter(user=request.user).first()
            if r_profile:
                context['is_recruiter'] = True
                context['current_profile'] = r_profile
        except Exception:
            pass

        try:
            s_profile = UserProfile.objects.filter(user=request.user).first()
            if s_profile and s_profile.role == 'job_seeker':
                context['is_seeker'] = True
                context['current_profile'] = s_profile
                context['saved_jobs_count'] = SavedJob.objects.filter(user=request.user).count()
                context['applications_count'] = JobApplication.objects.filter(applicant=request.user).count()
            elif not context['is_recruiter']:
                context['is_seeker'] = True
                context['saved_jobs_count'] = SavedJob.objects.filter(user=request.user).count()
                context['applications_count'] = JobApplication.objects.filter(applicant=request.user).count()
        except Exception:
            pass
            
    return context
