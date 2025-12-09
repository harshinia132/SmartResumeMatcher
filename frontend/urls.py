from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('upload-job/', views.upload_job, name='upload_job'),
    path('match_page/', views.match_page, name='match_page'),
    path('match_result/<int:resume_id>/<int:job_id>/', views.match_result, name='match_result'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # ✅ Only once
    path('register/', views.register_view, name='register'),
    
    # ✅ NEW AI FEATURES - Add these lines
    path('interview-prep/', views.interview_prep, name='interview_prep'),
    path('interview-prep/<int:job_id>/', views.interview_prep, name='interview_prep_job'),
    path('career-insights/', views.career_insights, name='career_insights'),
]