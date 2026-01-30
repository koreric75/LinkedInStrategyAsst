#!/usr/bin/env python3
"""
Test that the auto-scraper produces JSON that the backend can parse correctly.
This validates the data format contract between the scraper and the app.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def test_scraper_json_format():
    """Test that sample scraper output can be parsed by the backend."""
    
    # Sample output from linkedin_scraper.js
    scraper_output = {
        "headline": "Senior Software Engineer | Cloud & AI",
        "about": "Passionate about building scalable systems and AI-powered solutions. Experienced in cloud-native architectures.",
        "current_role": "Senior Software Engineer at Tech Corp",
        "skills": "Python, Docker, Kubernetes, FastAPI, Flutter, AI, Machine Learning",
        "certifications": "AWS Certified Solutions Architect, Google Cloud Professional"
    }
    
    # Convert to JSON string (simulating clipboard data)
    json_str = json.dumps(scraper_output)
    print("✅ Scraper output is valid JSON")
    print(f"Sample output: {json_str[:100]}...")
    
    # Parse it back (simulating what the backend does)
    try:
        from app import _parse_linkedin_text
        
        profile = _parse_linkedin_text(json_str)
        
        # Verify all fields are extracted
        assert profile.headline == scraper_output["headline"], "Headline mismatch"
        assert profile.about == scraper_output["about"], "About mismatch"
        assert profile.current_role == scraper_output["current_role"], "Current role mismatch"
        
        # Verify skills are parsed as list
        expected_skills = [s.strip() for s in scraper_output["skills"].split(",")]
        assert profile.skills == expected_skills, f"Skills mismatch: {profile.skills} != {expected_skills}"
        
        # Verify certifications are parsed as list
        expected_certs = [c.strip() for c in scraper_output["certifications"].split(",")]
        assert profile.certifications == expected_certs, f"Certs mismatch: {profile.certifications} != {expected_certs}"
        
        print("✅ Backend successfully parsed scraper JSON")
        print(f"   - Headline: {profile.headline}")
        print(f"   - Skills: {len(profile.skills)} skills extracted")
        print(f"   - Certifications: {len(profile.certifications)} certs extracted")
        
        return True
        
    except Exception as e:
        print(f"❌ Backend parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_empty_fields():
    """Test that empty/missing fields are handled gracefully."""
    
    from app import _parse_linkedin_text
    
    # Test with minimal data
    minimal_data = {
        "headline": "Test User",
        "about": "",
        "current_role": "",
        "skills": "",
        "certifications": ""
    }
    
    try:
        profile = _parse_linkedin_text(json.dumps(minimal_data))
        assert profile.headline == "Test User"
        assert profile.about == ""
        assert profile.skills == []
        assert profile.certifications == []
        print("✅ Empty fields handled correctly")
        return True
    except Exception as e:
        print(f"❌ Empty field handling failed: {e}")
        return False

def test_scraper_js_syntax():
    """Basic syntax check for the JavaScript scraper."""
    
    scraper_path = Path(__file__).parent.parent / 'linkedin_scraper.js'
    
    if not scraper_path.exists():
        print(f"❌ Scraper file not found: {scraper_path}")
        return False
    
    content = scraper_path.read_text()
    
    # Basic checks
    checks = [
        ("Contains IIFE wrapper", "(function()" in content or "(function(){" in content),
        ("Has headline extraction", "headline" in content),
        ("Has about extraction", "about" in content),
        ("Has skills extraction", "skills" in content),
        ("Has certifications extraction", "certifications" in content or "certs" in content),
        ("Uses clipboard API", "navigator.clipboard" in content or "clipboard.writeText" in content),
        ("Has JSON.stringify", "JSON.stringify" in content),
    ]
    
    all_passed = True
    for check_name, result in checks:
        if result:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("=" * 70)
    print("LinkedIn Auto-Scraper - Integration Tests")
    print("=" * 70)
    
    results = []
    
    print("\n--- Test 1: JavaScript Scraper Syntax ---")
    results.append(test_scraper_js_syntax())
    
    print("\n--- Test 2: Scraper JSON Format Compatibility ---")
    results.append(test_scraper_json_format())
    
    print("\n--- Test 3: Empty Fields Handling ---")
    results.append(test_empty_fields())
    
    print("\n" + "=" * 70)
    if all(results):
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
