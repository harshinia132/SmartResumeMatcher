from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job

@login_required
def upload_job(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title and description:
            # Create job first
            job = Job.objects.create(
                poster=request.user,
                title=title,
                description=description,
                required_skills=[]  # Will be filled by AI
            )
            
            # ✅ FIXED: Proper indentation
            try:
                from ai_engine.embeddings import get_embedding, store_embedding
                from ai_engine.parsers import extract_skills_enhanced
                
                # Generate embedding
                embedding = get_embedding(description)
                if embedding is not None:  # ✅ Fixed numpy array check
                    store_embedding(job, embedding)
                
                # Extract skills
                skills = extract_skills_enhanced(description)
                job.required_skills = skills
                job.save()
                
                messages.success(request, "Job posted and processed successfully!")
            except Exception as e:
                messages.error(request, f"Job posted but AI processing failed: {e}")
            
            return redirect('home')
        else:
            messages.error(request, "Please fill in both title and description")
    
    return render(request, 'frontend/upload_job.html')

@login_required
def job_list(request):
    """Simple view to list all jobs"""
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})