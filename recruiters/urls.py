from django.urls import path
from recruiters import views

urlpatterns = [
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('jobs/new/', views.job_create_view, name='job_create'),
    path('jobs/<int:job_id>/edit/', views.job_edit_view, name='job_edit'),
    path('jobs/<int:job_id>/toggle/', views.job_toggle_status_view, name='job_toggle_status'),
    path('jobs/<int:job_id>/delete/', views.job_delete_view, name='job_delete'),
    path('applicants/', views.applicants_view, name='applicants_all'),
    path('applicants/<int:job_id>/', views.applicants_view, name='applicants_job'),
    path('application/<int:app_id>/update/', views.update_applicant_status_view, name='update_applicant_status'),
]
