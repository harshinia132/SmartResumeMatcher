from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_text(text):
    return model.encode([text])[0].tolist()

def match_resume_to_job(resume, job):
    if not resume.embedding or not job.embedding:
        return 0
    resume_vec = np.array(resume.embedding)
    job_vec = np.array(job.embedding)
    similarity = np.dot(resume_vec, job_vec) / (np.linalg.norm(resume_vec) * np.linalg.norm(job_vec))
    similarity = max(min(similarity, 1), -1)
    scaled_score = round((similarity + 1) / 2 * 10, 2)  # 0-10 scale
    return scaled_score
