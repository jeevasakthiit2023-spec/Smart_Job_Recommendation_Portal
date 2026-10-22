import re
from django.utils import timezone
from accounts.models import UserProfile
from jobs.models import Job
from applications.models import JobApplication

EXP_SCALE = {
    'Fresher': 1,
    'Junior': 2,
    'Mid': 3,
    'Senior': 4,
    'Lead': 5,
}

def normalize_text(text):
    if not text:
        return ''
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower()).strip()

def calculate_job_match(profile, job):
    """
    Rule-matching and scoring algorithm:
    - Skills match: 50%
    - Preferred job role/category match: 20%
    - Preferred location match: 15%
    - Experience-level match: 15%
    Total: 0 - 100 points
    """
    reasons = []
    
    # 1. Skills match (50%)
    job_skills = job.get_normalized_skills()
    seeker_skills = profile.get_skills_list() if profile else []
    
    matched_skills = []
    missing_skills = []
    
    if job_skills and seeker_skills:
        for js in job_skills:
            # Check for direct match or substring match (e.g. 'python' in 'python 3')
            is_matched = any(
                js == ss or js in ss or ss in js 
                for ss in seeker_skills
            )
            if is_matched:
                matched_skills.append(js)
            else:
                missing_skills.append(js)
        
        ratio = len(matched_skills) / max(len(job_skills), 1)
        skills_score = round(ratio * 50.0, 1)
        if matched_skills:
            reasons.append(f"Matched {len(matched_skills)} of {len(job_skills)} required skills ({', '.join(s.title() for s in matched_skills[:4])})")
    elif not job_skills:
        skills_score = 30.0  # Job requires generalist knowledge
    else:
        skills_score = 0.0
        missing_skills = job_skills

    # 2. Preferred job role / category match (20%)
    role_score = 0.0
    pref_role = normalize_text(profile.preferred_job_role if profile else '')
    job_title_norm = normalize_text(job.job_title)
    category_norm = normalize_text(job.get_category_display())
    
    if pref_role:
        pref_words = set(pref_role.split())
        title_words = set(job_title_norm.split())
        category_words = set(category_norm.split())
        
        overlap_title = pref_words.intersection(title_words)
        overlap_cat = pref_words.intersection(category_words)
        
        if pref_role in job_title_norm or job_title_norm in pref_role:
            role_score = 20.0
            reasons.append(f"Direct role alignment with your target '{profile.preferred_job_role}'")
        elif overlap_title:
            role_score = 15.0
            reasons.append(f"Strong role similarity in keywords ({', '.join(w.title() for w in overlap_title)})")
        elif overlap_cat:
            role_score = 10.0
            reasons.append(f"Category alignment with {job.get_category_display()}")
        else:
            role_score = 0.0
    else:
        role_score = 5.0  # neutral if unselected

    # 3. Preferred location match (15%)
    loc_score = 0.0
    pref_loc = normalize_text(profile.preferred_location if profile else '')
    job_loc = normalize_text(job.location)
    
    if job.is_remote or 'remote' in job_loc:
        loc_score = 15.0
        reasons.append("Remote-friendly position matching flexible workplace preference")
    elif pref_loc:
        if 'remote' in pref_loc:
            # Seeker wants remote, but job is non-remote
            loc_score = 5.0
        elif pref_loc in job_loc or job_loc in pref_loc:
            loc_score = 15.0
            reasons.append(f"Location match with '{profile.preferred_location}'")
        else:
            loc_score = 0.0
    else:
        loc_score = 7.5  # Neutral if preference not set

    # 4. Experience-level match (15%)
    exp_score = 0.0
    seeker_exp = profile.experience_level if profile else None
    job_exp = job.experience_level
    
    if seeker_exp and job_exp in EXP_SCALE and seeker_exp in EXP_SCALE:
        diff = abs(EXP_SCALE[seeker_exp] - EXP_SCALE[job_exp])
        if diff == 0:
            exp_score = 15.0
            reasons.append(f"Exact experience match for {job.get_experience_level_display()}")
        elif diff == 1:
            exp_score = 8.0
            reasons.append(f"Close experience compatibility ({job.get_experience_level_display()})")
        else:
            exp_score = 0.0
    elif not seeker_exp:
        exp_score = 7.5
    else:
        exp_score = 0.0

    total_score = min(100, max(0, round(skills_score + role_score + loc_score + exp_score)))
    
    return {
        'total_score': total_score,
        'skills_score': skills_score,
        'role_score': role_score,
        'loc_score': loc_score,
        'exp_score': exp_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'reasons': reasons,
    }


def get_recommended_jobs(user, limit=None):
    """
    Returns recommendations sorted by match score descending.
    Excludes expired, inactive, or already-applied jobs.
    """
    if not user.is_authenticated:
        return []

    profile = UserProfile.objects.filter(user=user).first()
    
    # Exclude applied jobs
    applied_job_ids = JobApplication.objects.filter(applicant=user).values_list('job_id', flat=True)
    
    # Active and non-expired jobs
    today = timezone.now().date()
    eligible_jobs = Job.objects.filter(
        is_active=True,
        application_deadline__gte=today
    ).exclude(id__in=applied_job_ids).select_related('recruiter')
    
    scored_jobs = []
    for job in eligible_jobs:
        match_info = calculate_job_match(profile, job)
        scored_jobs.append({
            'job': job,
            'score': match_info['total_score'],
            'breakdown': match_info,
            'reasons': match_info['reasons'],
        })

    # Sort descending by match score, then newest
    scored_jobs.sort(key=lambda x: (x['score'], x['job'].created_at), reverse=True)

    if limit:
        return scored_jobs[:limit]
    return scored_jobs
