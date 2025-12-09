from django import forms
from .models import Job

class JobUploadForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Job Description', 'rows': 6}),
        }


