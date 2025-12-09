from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/users/', include('users.urls')),
    path('api/resumes/', include('resumes.urls')),
    path('api/jobs/', include('jobs.urls')),
    path('api/ai/', include('ai_engine.urls')),
    path('jobs/', include('jobs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


