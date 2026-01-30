#!/usr/bin/env python3
"""Test LinkedIn text input instead of OCR screenshots."""
import json
import requests
from pathlib import Path

# Sample LinkedIn data (copy/paste from real profile)
linkedin_data = {
    "headline": "Solutions Architect | Cloud & AI | Digital Transformation",
    "about": """I help organizations transform their operations through cloud-native solutions and AI-powered automation. 
    Specializing in Google Cloud Run, Docker containerization, and CI/CD pipelines. 
    Passionate about building scalable systems that drive business outcomes.
    
    Recent projects include LinkedIn strategy automation using OCR and LLM integration.""",
    "current_role": "Solutions Architect at Tech Company",
    "skills": "Python, Docker, Kubernetes, Cloud Run, CI/CD, Google Cloud, FastAPI, Flutter, LLM, AI, RPA, Terraform, CompTIA Security+",
    "certifications": "CompTIA Security+, Google Cloud Professional"
}

def test_text_input(api_url: str, mode: str = "Get Hired"):
    """Test analysis with manual text input."""
    print(f"\n=== Testing Text Input Mode: {mode} ===")
    print(f"API URL: {api_url}")
    
    resume_path = Path(__file__).parent / "sample_resume.txt"
    if not resume_path.exists():
        print(f"❌ Resume file not found: {resume_path}")
        return
    
    files = {
        'resume': ('sample_resume.txt', resume_path.open('rb'), 'text/plain')
    }
    
    data = {
        'mode': mode,
        'linkedin_text': json.dumps(linkedin_data)
    }
    
    print(f"\n📤 Sending request...")
    print(f"LinkedIn Data: {json.dumps(linkedin_data, indent=2)}")
    
    try:
        response = requests.post(api_url, files=files, data=data, timeout=30)
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ SUCCESS!")
            print(f"Profile Score: {result['profile_score']}/100")
            print(f"\nImmediate Fixes ({len(result['immediate_fixes'])}):")
            for i, fix in enumerate(result['immediate_fixes'], 1):
                print(f"  {i}. {fix}")
            
            print(f"\nGap Analysis:")
            gaps = result['gaps']
            print(f"  - Skills missing: {len(gaps['skills_missing_from_linkedin'])}")
            print(f"  - Certs missing: {len(gaps['certifications_missing_from_linkedin'])}")
            print(f"  - Advanced tech themes: {', '.join(gaps['advanced_tech_themes'][:5])}")
            
            print(f"\n📊 Score Analysis:")
            if result['profile_score'] >= 70:
                print(f"  🟢 GOOD - Score is in expected range (70-100)")
            elif result['profile_score'] >= 50:
                print(f"  🟡 OK - Score is acceptable (50-69)")
            else:
                print(f"  🔴 LOW - Score needs improvement (<50)")
        else:
            print(f"❌ ERROR: {response.text}")
    
    except Exception as e:
        print(f"❌ Request failed: {e}")
    finally:
        files['resume'][1].close()

if __name__ == "__main__":
    # Test against production
    prod_url = "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze"
    
    print("=" * 70)
    print("LinkedIn Strategy Assistant - Text Input Test")
    print("=" * 70)
    
    # Test all three modes
    for mode in ["Get Hired", "Grow Connections", "Influence Market"]:
        test_text_input(prod_url, mode)
        print("\n" + "=" * 70)
