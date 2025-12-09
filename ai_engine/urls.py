from django.urls import path
from . import views

urlpatterns = [
    path('match/<int:resume_id>/<int:job_id>/', views.match_resume_to_job, name='match_resume_to_job'),
]
