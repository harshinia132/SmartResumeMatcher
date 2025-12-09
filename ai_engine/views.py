from django.http import JsonResponse
from resumes.models import Resume
from jobs.models import Job
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def match_resume_to_job(request, resume_id, job_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return JsonResponse({"error": "Resume not found"}, status=404)

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Job not found"}, status=404)

    if not resume.embedding or not job.embedding:
        return JsonResponse({"error": "Embeddings not found for Resume or Job"}, status=400)

    resume_vec = np.array(resume.embedding).reshape(1, -1)
    job_vec = np.array(job.embedding).reshape(1, -1)

    score = cosine_similarity(resume_vec, job_vec)[0][0]
    return JsonResponse({
        "resume_id": resume.id,
        "job_id": job.id,
        "match_score": round(float(score), 4),
        "status": "success"
    })
