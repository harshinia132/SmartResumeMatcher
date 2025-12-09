from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

# Initialize model
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Embedding model loaded successfully")
except Exception as e:
    print(f"❌ Error loading embedding model: {e}")
    model = None

def get_embedding(text):
    """Generate embedding for text"""
    if not model or not text:
        print("❌ No model or text for embedding")
        return None
    
    # Clean and prepare text
    clean_text = ' '.join(text.split()[:512])  # Limit text length
    
    try:
        embedding = model.encode(clean_text)
        print(f"✅ Generated embedding of shape: {embedding.shape}")
        return embedding
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return None

def store_embedding(model_instance, embedding):
    """Store embedding in model instance"""
    if embedding is not None:
        try:
            model_instance.embedding = pickle.dumps(embedding)  # ✅ FIXED: singular 'embedding'
            print("✅ Embedding stored in model instance")
        except Exception as e:
            print(f"❌ Error storing embedding: {e}")

def load_embedding(serialized):
    """Load embedding from serialized data"""
    if serialized:
        try:
            embedding = pickle.loads(serialized)
            print("✅ Embedding loaded from serialized data")
            return embedding
        except Exception as e:
            print(f"❌ Error loading embedding: {e}")
    return None

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors"""
    if a is None or b is None:
        print("❌ One or both embeddings are None")
        return 0.0
    
    a = np.array(a)
    b = np.array(b)
    
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        print("❌ Zero vector in similarity calculation")
        return 0.0
    
    similarity = dot_product / (norm_a * norm_b)
    print(f"✅ Cosine similarity: {similarity:.4f}")
    return float(similarity)

def compute_match_score(resume, job):
    """Compute match score between resume and job"""
    try:
        print(f"🔍 Computing match between Resume {resume.id} and Job {job.id}")
        
        # ✅ FIXED: Use singular 'embedding' instead of 'embeddings'
        r_emb = load_embedding(resume.embedding)
        j_emb = load_embedding(job.embedding)
        
        if r_emb is None or j_emb is None:
            print("❌ Missing embeddings for match calculation")
            return 0.0
            
        similarity = cosine_similarity(r_emb, j_emb)
        # Convert to percentage (0-100)
        score = max(0.0, min(100.0, (similarity + 1) * 50))
        print(f"✅ Match score: {score:.2f}%")
        return round(score, 2)
        
    except Exception as e:
        print(f"❌ Error computing match score: {e}")
        return 0.0

def get_missing_skills(resume_skills, job_skills):
    """Find skills missing from resume that are required for job"""
    if not resume_skills or not job_skills:
        return []
    
    resume_skills_lower = [str(s).lower() for s in resume_skills]
    job_skills_lower = [str(s).lower() for s in job_skills]
    
    missing_skills = [skill for skill in job_skills_lower if skill not in resume_skills_lower]
    print(f"✅ Missing skills analysis: {len(missing_skills)} skills missing")
    return missing_skills