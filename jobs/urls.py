from django.urls import path
from jobs import views

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('saved/', views.saved_jobs_view, name='saved_jobs'),
    path('save/<int:job_id>/', views.toggle_save_job_view, name='toggle_save_job'),
]
