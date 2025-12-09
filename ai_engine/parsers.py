import PyPDF2
import docx2txt
import spacy
import re
import os
from typing import List, Dict
import numpy as np

# Initialize spaCy
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy model loaded successfully")
except OSError:
    print("❌ Please download spaCy model: python -m spacy download en_core_web_sm")
    nlp = None

# Comprehensive skills database
SKILLS_DATABASE = {
    'programming': ['python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'php', 'html', 'css', 'typescript'],
    'web_frameworks': ['django', 'flask', 'react', 'angular', 'vue', 'spring', 'express', 'laravel', 'bootstrap', 'node.js', 'django rest framework'],
    'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql', 'nosql', 'sql server'],
    'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd', 'cloud formation'],
    'ml_ai': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision', 'neural networks', 'scikit-learn', 'opencv'],
    'tools': ['git', 'jenkins', 'linux', 'bash', 'ansible', 'jira', 'confluence', 'gitlab', 'github'],
    'electronics': ['arduino', 'raspberry pi', 'circuit design', 'embedded systems', 'pcb design', 'iot', 'microcontroller', 'sensors', 'wireless communication']
}

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF or DOCX files"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return ""
        
    try:
        if file_path.endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return extract_text_from_docx(file_path)
        else:
            # Try to read as text file
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return ""

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF with error handling"""
    try:
        text = ''
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        print(f"✅ Extracted {len(text)} characters from PDF")
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX"""
    try:
        text = docx2txt.process(file_path)
        print(f"✅ Extracted {len(text)} characters from DOCX")
        return text
    except Exception as e:
        print(f"❌ Error reading DOCX {file_path}: {e}")
        return ""

def extract_skills_enhanced(text: str) -> List[str]:
    """Enhanced skill extraction using multiple methods"""
    if not text:
        print("❌ No text provided for skill extraction")
        return []
        
    text_lower = text.lower()
    found_skills = set()
    
    # Method 1: Direct keyword matching with word boundaries
    all_skills = [skill for category in SKILLS_DATABASE.values() for skill in category]
    
    for skill in all_skills:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    
    # Method 2: NLP-based extraction if available
    if nlp and len(text) > 50:
        try:
            doc = nlp(text[:1000])  # Process first 1000 chars for efficiency
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    potential_skill = ent.text.lower()
                    if any(skill in potential_skill for skill in all_skills):
                        found_skills.add(potential_skill)
        except Exception as e:
            print(f"❌ NLP processing error: {e}")
    
    print(f"✅ Found {len(found_skills)} skills: {list(found_skills)}")
    return list(found_skills)

def parse_and_store_resume(resume_instance):
    """Main function to parse resume and store results"""
    try:
        print(f"🔄 Processing resume: {resume_instance.file.name}")
        
        # Extract text
        text = extract_text_from_file(resume_instance.file.path)
        if not text:
            print(f"❌ No text extracted from {resume_instance.file.path}")
            return False
            
        # Update resume instance
        resume_instance.text = text
        
        # Extract skills
        skills = extract_skills_enhanced(text)
        resume_instance.skills = skills
        
        # Generate embeddings
        from .embeddings import get_embedding, store_embedding
        embedding = get_embedding(text)
        if embedding is not None:
            store_embedding(resume_instance, embedding)
            print("✅ Embedding generated and stored")
        else:
            print("❌ Failed to generate embedding")
        
        # Save everything
        resume_instance.save()
        
        print(f"✅ Successfully processed resume ID {resume_instance.id}: {len(skills)} skills found")
        return True
        
    except Exception as e:
        print(f"❌ Error processing resume {resume_instance.id}: {e}")
        return False