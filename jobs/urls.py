from django.urls import path
from .views import upload_job, job_list

urlpatterns = [
    path('upload/', upload_job, name='upload_job'),
    path('', job_list, name='job_list'),
]
