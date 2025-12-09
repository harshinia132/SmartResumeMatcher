


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from jobs.models import Job
from resumes.models import Resume
#from resumes.models import Resume
#from jobs.models import Job  # ✅ Correct import

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

class JobUploadForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']