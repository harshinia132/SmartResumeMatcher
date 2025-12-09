import google.generativeai as genai
import os
from django.conf import settings

# Configure Gemini
def configure_gemini():
    """Configure Gemini AI with API key"""
    try:
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("⚠️ GEMINI_API_KEY not found. AI features will be disabled.")
            return False
        
        genai.configure(api_key=api_key)
        print("✅ Gemini AI configured successfully")
        return True
    except Exception as e:
        print(f"❌ Gemini configuration failed: {e}")
        return False

def generate_interview_questions_with_answers(job_title, job_description, resume_skills, num_questions=8):
    """Generate interview questions with suggested answers and keywords"""
    if not configure_gemini():
        return [{
            "question": "AI service unavailable. Please check your API key.",
            "suggested_answer": "",
            "keywords": []
        }]
    
    try:
        model_names = [
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-001', 
            'models/gemini-pro-latest',
        ]
        
        model = None
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                test_response = model.generate_content("Say 'OK'")
                if test_response.text:
                    print(f"✅ Using model: {model_name}")
                    break
            except Exception:
                continue
        
        if not model:
            return [{
                "question": "No compatible AI model found.",
                "suggested_answer": "",
                "keywords": []
            }]
        
        prompt = f"""
        Generate {num_questions} interview questions for a {job_title} position.
        
        Job Description: {job_description[:800]}
        Candidate Skills: {', '.join(resume_skills[:15])}
        
        FORMAT REQUIREMENTS:
        For each question, provide:
        QUESTION: [The interview question]
        SUGGESTED_ANSWER: [A concise model answer - 3-4 sentences max]
        KEYWORDS: [comma,separated,keywords,expected,in,answer]
        
        Example:
        QUESTION: What experience do you have with microcontroller programming?
        SUGGESTED_ANSWER: I have hands-on experience with Arduino and Raspberry Pi, where I developed projects involving sensor integration and data processing. For example, I created a temperature monitoring system using Arduino Uno that collected data from DHT22 sensors and displayed it on an LCD. I also optimized code for memory constraints and implemented power-saving features.
        KEYWORDS: Arduino,Raspberry Pi,sensor integration,data processing,memory optimization,power saving
        
        Make questions specific to embedded systems, IoT, and electronics.
        """
        
        response = model.generate_content(prompt)
        print(f"✅ Raw AI response with answers: {response.text[:300]}...")
        
        return parse_questions_with_answers(response.text, num_questions)
        
    except Exception as e:
        print(f"❌ Question generation with answers failed: {e}")
        return [{
            "question": f"Error: {str(e)}",
            "suggested_answer": "",
            "keywords": []
        }]

def parse_questions_with_answers(raw_text, expected_count=8):
    """Parse questions with suggested answers and keywords"""
    if not raw_text:
        return generate_fallback_questions_with_answers(expected_count)
    
    sections = raw_text.split('QUESTION:')
    questions_data = []
    
    for section in sections[1:]:  # Skip first empty section
        try:
            lines = section.strip().split('\n')
            question = ""
            suggested_answer = ""
            keywords = []
            
            for line in lines:
                line = line.strip()
                if line.startswith('QUESTION:'):
                    question = line.replace('QUESTION:', '').strip()
                elif line.startswith('SUGGESTED_ANSWER:'):
                    suggested_answer = line.replace('SUGGESTED_ANSWER:', '').strip()
                elif line.startswith('KEYWORDS:'):
                    keywords_str = line.replace('KEYWORDS:', '').strip()
                    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                
                # If we have a question line without prefix
                elif not question and line and '?' in line and len(line) > 10:
                    question = line
                
                # Stop if we hit the next QUESTION (in case of formatting issues)
                if line.startswith('QUESTION:') and question:
                    break
            
            if question and len(question) > 10:
                questions_data.append({
                    "question": question,
                    "suggested_answer": suggested_answer,
                    "keywords": keywords
                })
                
        except Exception as e:
            print(f"❌ Error parsing question section: {e}")
            continue
    
    # Add fallback if we didn't get enough
    if len(questions_data) < expected_count:
        print(f"⚠️ Only got {len(questions_data)} questions with answers, adding fallbacks")
        questions_data.extend(generate_fallback_questions_with_answers(expected_count - len(questions_data)))
    
    return questions_data[:expected_count]

def generate_fallback_questions_with_answers(count):
    """Generate fallback questions with answers"""
    fallbacks = [
        {
            "question": "What experience do you have with microcontroller programming?",
            "suggested_answer": "I have practical experience with Arduino and Raspberry Pi, developing projects that involve sensor integration, data processing, and communication protocols. I've worked on IoT projects collecting sensor data and implementing control algorithms.",
            "keywords": ["Arduino", "Raspberry Pi", "sensors", "data processing", "IoT", "communication protocols"]
        },
        {
            "question": "Describe a challenging circuit design problem you solved.",
            "suggested_answer": "I once designed a power supply circuit that was experiencing noise issues. I used oscilloscope measurements to identify the noise source, added proper filtering capacitors, and implemented better grounding techniques. This reduced noise by 80% and improved circuit reliability.",
            "keywords": ["circuit design", "noise reduction", "filtering", "oscilloscope", "troubleshooting", "power supply"]
        },
        {
            "question": "How do you approach debugging embedded software issues?",
            "suggested_answer": "I follow a systematic approach: first reproducing the issue, then using debuggers and serial print statements to isolate the problem area. I check hardware-software interactions, review timing issues, and validate sensor readings. For complex issues, I use logic analyzers to monitor signal timing.",
            "keywords": ["debugging", "systematic approach", "debuggers", "hardware-software interaction", "timing analysis", "logic analyzer"]
        }
    ]
    return fallbacks[:count]

def generate_career_insights(resume_skills, job_title=None, job_description=None, job_skills=None, job_market_trends=None):
    """Generate personalized career insights using Gemini"""
    if not configure_gemini():
        return {"error": "🤖 AI service is currently unavailable. Please check your API key."}
    
    try:
        # ✅ USE ACTUAL AVAILABLE MODELS FROM YOUR LIST
        model_names = [
            'models/gemini-2.0-flash',
            'models/gemini-2.0-flash-001', 
            'models/gemini-pro-latest',
            'models/gemini-flash-latest',
        ]
        
        model = None
        successful_model = None
        
        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                # Test with a simple prompt
                test_response = model.generate_content("Say 'OK'")
                if test_response.text:
                    successful_model = model_name
                    print(f"✅ Using model: {model_name}")
                    break
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
        
        if not model:
            return {"error": "❌ No compatible AI model found"}
        
        # Build dynamic prompt based on available job info
        prompt = f"""
        Analyze this skill set and provide career insights for an Electronics/Computer Engineering student:
        Skills: {', '.join(resume_skills[:20])}
        """
        
        # Add job-specific context if available
        if job_title:
            prompt += f"\nTarget Job Role: {job_title}"
        if job_description:
            prompt += f"\nJob Description: {job_description[:300]}"
        if job_skills:
            prompt += f"\nRequired Skills for Job: {', '.join(job_skills)}"
        
        prompt += """
        
        Provide insights in this structured format:
        
        Career Paths:
        1. [First career path suggestion]
        2. [Second career path suggestion] 
        3. [Third career path suggestion]
        
        Skill Gaps:
        - [First high-demand skill to learn]
        - [Second high-demand skill to learn]
        - [Third high-demand skill to learn]
        
        Learning Recommendations:
        - [First specific technology/course]
        - [Second specific technology/course]
        - [Third specific technology/course]
        
        Market Outlook: [Brief analysis of job market opportunities]
        
        Salary Expectations: [Entry-level and short-term projections]
        
        Keep it concise, practical, and actionable. Focus on electronics and computer engineering fields.
        """
        
        # If job info is provided, make it more targeted
        if job_title:
            prompt += f"\n\nFocus specifically on preparing for the {job_title} role and bridging any skill gaps."
        
        response = model.generate_content(prompt)
        return parse_career_insights(response.text)
        
    except Exception as e:
        print(f"❌ Career insights generation failed: {e}")
        return {"error": f"AI service error: {str(e)}"}

def parse_career_insights(insights_text):
    """Parse Gemini response into structured data"""
    sections = {
        "career_paths": [],
        "skill_gaps": [],
        "learning_recommendations": [],
        "market_outlook": "Information not available",
        "salary_expectations": "Information not available"
    }
    
    # Fallback content in case parsing fails
    fallback_content = [
        "Embedded Systems Engineer",
        "IoT Developer", 
        "Hardware Design Engineer",
        "Learn PCB design and advanced embedded systems",
        "Gain experience with IoT protocols",
        "Master C++ and real-time operating systems",
        "Strong demand for ECE professionals in automation and IoT",
        "Entry-level: ₹4-6 LPA, 2-year experience: ₹8-12 LPA"
    ]
    
    try:
        lines = insights_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if any(phrase in line.lower() for phrase in ["career path", "career paths"]) and ":" in line.lower():
                current_section = "career_paths"
            elif any(phrase in line.lower() for phrase in ["skill gap", "skill gaps", "skills to learn"]) and ":" in line.lower():
                current_section = "skill_gaps" 
            elif any(phrase in line.lower() for phrase in ["learning", "recommendations", "courses"]) and ":" in line.lower():
                current_section = "learning_recommendations"
            elif any(phrase in line.lower() for phrase in ["market", "outlook", "opportunities"]) and ":" in line.lower():
                current_section = "market_outlook"
            elif any(phrase in line.lower() for phrase in ["salary", "compensation"]) and ":" in line.lower():
                current_section = "salary_expectations"
            
            # Add content to sections
            elif current_section:
                if current_section in ["career_paths", "skill_gaps", "learning_recommendations"]:
                    if (line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•', '*')) and len(line) > 3) or (line[0].isdigit() and '.' in line[:3]):
                        clean_line = line.lstrip('12345.-•* ').strip()
                        if clean_line and len(clean_line) > 5:
                            sections[current_section].append(clean_line)
                else:
                    # For single-line sections, replace the content
                    if line and len(line) > 10 and not any(phrase in line.lower() for phrase in ["career", "skill", "learning", "market", "salary"]):
                        sections[current_section] = line
        
        # Ensure we have at least some content
        if not any(sections.values()):
            sections["career_paths"] = fallback_content[:3]
            sections["skill_gaps"] = fallback_content[3:6]
            sections["market_outlook"] = fallback_content[6]
            sections["salary_expectations"] = fallback_content[7]
            
    except Exception as e:
        print(f"❌ Error parsing insights: {e}")
        # Use fallback content
        sections["career_paths"] = fallback_content[:3]
        sections["skill_gaps"] = fallback_content[3:6]
        sections["market_outlook"] = fallback_content[6]
        sections["salary_expectations"] = fallback_content[7]
    
    return sections