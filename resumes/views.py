from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm
from .models import Resume




@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            
            # ✅ ADD ONLY THESE 2 LINES:
            from ai_engine.parsers import parse_and_store_resume
            parse_and_store_resume(resume)
            
            return redirect('home')
    else:
        form = ResumeUploadForm()
    return render(request, 'frontend/upload_resume.html', {'form': form})