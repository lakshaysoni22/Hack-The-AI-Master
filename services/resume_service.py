import os
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None
import time
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Configure Gemini API if available
api_key = os.environ.get("GEMINI_API_KEY")
if api_key and genai:
    genai.configure(api_key=api_key)

def extract_text_from_pdf(file_stream):
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def analyze_resume(resume_text, user_stats=None):
    """
    Sends the resume text to the AI model to evaluate against cybersecurity internship requirements.
    Falls back to a mock response if API key is missing.
    """
    if not api_key:
        print("GEMINI_API_KEY not found. Using mock AI response.")
        time.sleep(2) # Simulate API latency
        
        # Mock logic based on keywords
        text_lower = resume_text.lower()
        has_security = 'security' in text_lower or 'cyber' in text_lower or 'ctf' in text_lower
        
        if has_security:
            return {
                "success": True,
                "eligible": True,
                "feedback": "Your resume shows a strong foundation in cybersecurity concepts and practical experience.\n\nStrengths: \n- Relevant domain knowledge\n- Practical experience (CTF/Labs)\n\nWe recommend you apply for the Junior Penetration Tester Internship."
            }
        else:
            return {
                "success": True,
                "eligible": False,
                "feedback": "While your background is solid, we noticed a lack of specific cybersecurity experience.\n\nAreas to Improve:\n- Complete the 'Web Exploitation' labs on this platform.\n- Gain practical experience with tools like Burp Suite and Nmap.\n- Familiarize yourself with the OWASP Top 10.\n\nKeep learning and check back in a few weeks!"
            }

    prompt = f"""
    You are an expert technical recruiter for a top-tier cybersecurity firm. 
    Analyze the following resume text and evaluate if the candidate is eligible for a cybersecurity internship.
    
    Candidate Stats from CTF Platform: {user_stats}
    
    Resume Text:
    {resume_text}
    
    Respond STRICTLY in JSON format with exactly these three keys:
    "success": boolean (true),
    "eligible": boolean (true if they have strong cyber skills, false otherwise),
    "feedback": string (Provide a concise, professional 3-paragraph feedback. If eligible, encourage them to apply. If not, list specific labs/skills they need to work on.)
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Parse JSON from response
        import json
        import re
        
        text_resp = response.text
        # Extract json block if wrapped in markdown
        json_match = re.search(r'```json\n(.*?)\n```', text_resp, re.DOTALL)
        if json_match:
            text_resp = json_match.group(1)
            
        data = json.loads(text_resp)
        return data
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "success": False,
            "message": "AI analysis temporarily unavailable."
        }
