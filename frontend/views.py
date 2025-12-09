from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from resumes.models import Resume
from jobs.models import Job
from django.contrib.auth import logout
# ADD THIS IMPORT AT THE TOP
from .forms import ResumeUploadForm  # Make sure this exists

def home(request):
    return render(request, 'frontend/home.html')

@login_required
def upload_resume(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            resume_file = request.FILES['file']
            print(f"📤 DEBUG: Processing upload - {resume_file.name}")
            
            # Create resume
            resume = Resume.objects.create(user=request.user, file=resume_file)
            
            # AI processing
            try:
                from ai_engine.parsers import parse_and_store_resume
                parse_and_store_resume(resume)
            except Exception as e:
                print(f"DEBUG: AI error - {e}")
            
            # Get updated resumes and render directly
            user_resumes = Resume.objects.filter(user=request.user).order_by('-id')[:5]
            messages.success(request, f"✅ Uploaded: {resume_file.name}")
            
            print(f"📊 DEBUG: Rendering with {user_resumes.count()} resumes")
            return render(request, 'frontend/upload_resume.html', {
                'user_resumes': user_resumes
            })
    
    # GET request
    user_resumes = Resume.objects.filter(user=request.user).order_by('-id')[:5]
    print(f"📋 DEBUG: GET request - {user_resumes.count()} resumes")
    return render(request, 'frontend/upload_resume.html', {
        'user_resumes': user_resumes
    })

@login_required
def upload_job(request):
    return render(request, 'frontend/upload_job.html')



@login_required
def match_page(request):
    resumes = Resume.objects.filter(user=request.user)
    jobs = Job.objects.all()
    
    # ADD THESE 5 LINES:
    if request.method == 'POST':
        resume_id = request.POST.get('resume')
        job_id = request.POST.get('job')
        if resume_id and job_id:
            return redirect('match_result', resume_id=resume_id, job_id=job_id)
    
    return render(request, 'frontend/match_page.html', {
        'resumes': resumes,
        'jobs': jobs
    })

@login_required
def match_latest(request):
    # FIXED: Changed 'owner' to 'user'
    resume = Resume.objects.filter(user=request.user).order_by('-id').first()
    job = Job.objects.order_by('-id').first()

    if not resume:
        messages.error(request, "No resume found. Please upload a resume first.")
        return redirect('upload_resume')
    if not job:
        messages.error(request, "No jobs found. Please post a job first.")
        return redirect('upload_job')

    return redirect('match_result', resume_id=resume.id, job_id=job.id)

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'frontend/job_list.html', {'jobs': jobs})


@login_required
def match_result(request, resume_id, job_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    job = get_object_or_404(Job, id=job_id)

    print(f"Resume: {resume.file.name}")
    print(f"Job: {job.title}")
    
    match_score = None
    
    try:
        from ai_engine.embeddings import compute_match_score
        print("✓ AI engine imported successfully")
        match_score = compute_match_score(resume, job)
        print(f"✓ Match score calculated: {match_score}")
        
    except Exception as e:
        print(f"❌ Matching error: {e}")
        # Simple fallback: extract skills from description
        job_description = job.description.lower()
        common_skills = ['python', 'c++', 'arduino', 'raspberry', 'circuit', 'embedded']
        found_skills = [skill for skill in common_skills if skill in job_description]
        match_score = min(len(found_skills) * 20, 100)  # Simple scoring

    # Safe skill extraction
    resume_skills = getattr(resume, 'skills', []) or []
    
    # Extract skills from job description as fallback
    job_description = job.description.lower()
    common_tech_skills = ['python', 'c++', 'c', 'arduino', 'raspberry pi', 'circuit design', 'embedded systems', 'pcb', 'iot']
    job_skills = [skill for skill in common_tech_skills if skill in job_description]
    
    missing_skills = []
    if job_skills and resume_skills:
        resume_skills_lower = [str(s).lower() for s in resume_skills]
        job_skills_lower = [str(s).lower() for s in job_skills]
        missing_skills = [skill for skill in job_skills_lower if skill not in resume_skills_lower]

    print(f"Final match score: {match_score}")
    print(f"Resume skills: {resume_skills}")
    print(f"Job skills (extracted): {job_skills}")
    print(f"Missing skills: {missing_skills}")

    return render(request, 'frontend/match_result.html', {
        'resume': resume,
        'job': job,
        'match_score': match_score,
        'missing_skills': missing_skills,
        'resume_skills': resume_skills,
        'job_skills': job_skills,
    })


def logout_view(request):
    logout(request)
    return redirect('login')



def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'frontend/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'frontend/login.html')

@login_required
def interview_prep(request, job_id=None):
    """AI-powered interview preparation"""
    job = None
    questions = []
    
    if job_id:
        job = get_object_or_404(Job, id=job_id)
        resume = Resume.objects.filter(user=request.user).first()
        
        if resume and job:
            from ai_engine.gemini_service import generate_interview_questions
            questions = generate_interview_questions(
                job_title=job.title,
                job_description=job.description,
                resume_skills=resume.skills,
                num_questions=10
            )
    
    jobs = Job.objects.all()
    return render(request, 'frontend/interview_prep.html', {
        'job': job,
        'questions': questions,
        'jobs': jobs
    })

@login_required
def career_insights(request):
    """AI-powered personalized career insights"""
    insights = {}
    job = None
    selected_resume = None
    
    # Get user's resumes and jobs FIRST
    user_resumes = Resume.objects.filter(user=request.user).order_by('-id')
    jobs = Job.objects.all()
    
    print(f"🔍 DEBUG: Found {user_resumes.count()} resumes and {jobs.count()} jobs")
    
    # Check if parameters came from GET
    job_id = request.GET.get('job_id')
    resume_id = request.GET.get('resume_id')
    
    if job_id and resume_id:
        try:
            job = Job.objects.get(id=job_id)
            selected_resume = Resume.objects.get(id=resume_id, user=request.user)
            
            if selected_resume.skills and job:
                from ai_engine.gemini_service import generate_career_insights
                insights = generate_career_insights(
                    resume_skills=selected_resume.skills,
                    job_title=job.title,
                    job_description=job.description,
                    job_skills=job.required_skills
                )
                print(f"✅ Generated career insights for: {job.title}")
                
        except (Job.DoesNotExist, Resume.DoesNotExist) as e:
            print(f"❌ Job or Resume not found: {e}")
            messages.error(request, "Selected job or resume not found")
        except Exception as e:
            print(f"❌ Error generating insights: {e}")
            messages.error(request, f"Error generating insights: {e}")
    
    return render(request, 'frontend/career_insights.html', {
        'user_resumes': user_resumes,
        'selected_resume': selected_resume,
        'insights': insights,
        'job': job,
        'jobs': jobs
    })

@login_required
def interview_prep(request, job_id=None):
    """AI-powered interview preparation"""
    job = None
    questions_data = []  # Changed from questions to questions_data
    
    # Check if job_id came from GET parameter
    job_id_from_get = request.GET.get('job_id')
    if job_id_from_get:
        job_id = job_id_from_get
    
    if job_id:
        try:
            job = Job.objects.get(id=job_id)
            resume = Resume.objects.filter(user=request.user).first()
            
            if resume and job:
                from ai_engine.gemini_service import generate_interview_questions_with_answers
                print("🔄 Generating interview questions with answers...")
                questions_data = generate_interview_questions_with_answers(
                    job_title=job.title,
                    job_description=job.description,
                    resume_skills=resume.skills,
                    num_questions=8
                )
                print(f"✅ Generated {len(questions_data)} questions with answers")
                
        except Job.DoesNotExist:
            print(f"❌ Job with ID {job_id} not found")
            job = None
        except Exception as e:
            print(f"❌ Error: {e}")
    
    jobs = Job.objects.all()
    
    return render(request, 'frontend/interview_prep.html', {
        'job': job,
        'questions_data': questions_data,  # Changed parameter name
        'jobs': jobs
    })