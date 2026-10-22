from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403, handler404, handler500
from jobs.views import home_view
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('applications/', include('applications.urls')),
    path('recruiters/', include('recruiters.urls')),
    
    # Global shortcut dashboard
    path('dashboard/', account_views.dashboard_dispatcher, name='dashboard'),
]

handler403 = 'accounts.views.custom_403'
handler404 = 'accounts.views.custom_404'
handler500 = 'accounts.views.custom_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
