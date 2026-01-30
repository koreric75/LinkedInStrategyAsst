#!/usr/bin/env python3
"""Test the LinkedIn Strategy Assistant API with mock data"""
import requests
from pathlib import Path

API_URL = "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze"

# Test files
test_dir = Path("C:/Users/korer/LinkedInStrategyAsst/test_data")
resume_path = test_dir / "sample_resume.txt"
screenshot1 = test_dir / "linkedin_screenshot_1.png"
screenshot2 = test_dir / "linkedin_screenshot_2.png"

print("🧪 Testing LinkedIn Strategy Assistant API\n")

# Test each mode
modes = ["Get Hired", "Grow Connections", "Influence Market"]

for mode in modes:
    print(f"\n{'='*50}")
    print(f"Testing Mode: {mode}")
    print('='*50)
    
    try:
        with open(resume_path, 'rb') as resume_file, \
             open(screenshot1, 'rb') as shot1, \
             open(screenshot2, 'rb') as shot2:
            
            files = {
                'resume': ('resume.txt', resume_file, 'text/plain'),
                'screenshots': ('screenshot1.png', shot1, 'image/png'),
            }
            
            # Add second screenshot separately
            files_list = [
                ('resume', ('resume.txt', open(resume_path, 'rb'), 'text/plain')),
                ('screenshots', ('screenshot1.png', open(screenshot1, 'rb'), 'image/png')),
                ('screenshots', ('screenshot2.png', open(screenshot2, 'rb'), 'image/png')),
            ]
            
            data = {
                'mode': mode,
                'use_cloud_vision': 'false'
            }
            
            response = requests.post(API_URL, files=files_list, data=data)
            response.raise_for_status()
            
            result = response.json()
            
            print(f"\n📊 CAREER STRATEGY DASHBOARD")
            print(f"Mode: {result['mode']}")
            print(f"Profile Score: {result['profile_score']}/100")
            
            print(f"\n🔧 IMMEDIATE FIXES:")
            for fix in result['immediate_fixes']:
                print(f"  • {fix}")
            
            print(f"\n🗓️ 30-DAY ROADMAP:")
            for step in result['strategic_roadmap']:
                print(f"  • {step}")
            
            print(f"\n🔍 GAP ANALYSIS:")
            gaps = result['gaps']
            print(f"  Skills missing from LinkedIn: {', '.join(gaps['skills_missing_from_linkedin']) or 'None'}")
            print(f"  Projects missing from LinkedIn: {', '.join(gaps['projects_missing_from_linkedin']) or 'None'}")
            print(f"  Certifications missing: {', '.join(gaps['certifications_missing_from_linkedin']) or 'None'}")
            print(f"  Advanced tech themes: {', '.join(gaps['advanced_tech_themes']) or 'None'}")
            
            print(f"\n✅ Test PASSED for mode: {mode}")
            
            # Close files
            for _, (_, f, _) in files_list:
                f.close()
                
    except Exception as e:
        print(f"\n❌ Test FAILED for mode: {mode}")
        print(f"Error: {str(e)}")

print(f"\n{'='*50}")
print("All tests completed!")
print('='*50)
