#!/usr/bin/env python3
"""Test the LinkedIn Profile Optimizer integration."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from linkedin_optimizer import (
    get_headline_optimization_tips,
    get_about_section_optimization_tips,
    get_skills_optimization_tips,
    get_completeness_assessment,
    generate_enhanced_fixes,
    generate_enhanced_roadmap,
)

def test_headline_tips():
    print("\n=== Testing Headline Optimization ===")
    
    # Test weak headline
    tips = get_headline_optimization_tips(
        current_headline="Looking for opportunities",
        skills=["Python", "Docker", "Kubernetes"],
        current_role="Senior Engineer"
    )
    print(f"Weak headline tips ({len(tips)}):")
    for tip in tips:
        print(f"  - {tip}")
    
    # Test good headline
    tips = get_headline_optimization_tips(
        current_headline="Senior Engineer | Python, Docker, Kubernetes | Building Scalable Systems",
        skills=["Python", "Docker", "Kubernetes"],
        current_role="Senior Engineer"
    )
    print(f"\nGood headline tips ({len(tips)}):")
    for tip in tips:
        print(f"  - {tip}")

def test_about_tips():
    print("\n=== Testing About Section Optimization ===")
    
    # Test empty about
    tips = get_about_section_optimization_tips(
        current_about="",
        skills=["Python", "Docker"],
        achievements=["Built system", "Led team"]
    )
    print(f"Empty about tips ({len(tips)}):")
    for tip in tips:
        print(f"  - {tip}")

def test_skills_tips():
    print("\n=== Testing Skills Optimization ===")
    
    tips = get_skills_optimization_tips(
        linkedin_skills=["Python", "Docker"],
        resume_skills=["Python", "Docker", "Kubernetes", "Terraform", "CI/CD"]
    )
    print(f"Skills tips ({len(tips)}):")
    for tip in tips:
        print(f"  - {tip}")

def test_completeness():
    print("\n=== Testing Completeness Assessment ===")
    
    linkedin_data = {
        "headline": "Senior Engineer | Cloud & DevOps",
        "about": "I help teams build scalable systems. " * 50,  # Long enough
        "skills": ["Python", "Docker", "Kubernetes"],
        "certifications": ["AWS Certified"],
    }
    
    assessment = get_completeness_assessment(linkedin_data)
    print(f"All-Star Score: {assessment['all_star_score']}%")
    print(f"Beyond All-Star Score: {assessment['beyond_score']}%")
    print(f"Is All-Star: {assessment['is_all_star']}")

def test_enhanced_fixes():
    print("\n=== Testing Enhanced Fixes Generation ===")
    
    linkedin_data = {
        "headline": "Looking for opportunities",
        "about": "I'm a developer.",
        "current_role": "Senior Engineer",
        "skills": ["Python"],
        "certifications": [],
    }
    
    resume_data = {
        "skills": ["Python", "Docker", "Kubernetes", "Terraform"],
        "projects": ["Built CI/CD pipeline", "Migrated to cloud"],
        "certifications": ["AWS Certified"],
        "experience": ["5 years experience"],
    }
    
    gaps = {
        "skills_missing_from_linkedin": ["Docker", "Kubernetes", "Terraform"],
        "projects_missing_from_linkedin": ["Built CI/CD pipeline"],
        "certifications_missing_from_linkedin": ["AWS Certified"],
        "advanced_tech_themes": ["Docker", "Kubernetes"],
    }
    
    fixes = generate_enhanced_fixes(linkedin_data, resume_data, gaps)
    print(f"Enhanced fixes ({len(fixes)}):")
    for i, fix in enumerate(fixes, 1):
        print(f"  {i}. {fix}")

def test_enhanced_roadmap():
    print("\n=== Testing Enhanced Roadmap Generation ===")
    
    linkedin_data = {
        "headline": "Senior Engineer",
        "about": "Developer with 5 years experience",
        "skills": ["Python", "Docker"],
        "certifications": [],
    }
    
    resume_data = {
        "skills": ["Python", "Docker", "Kubernetes"],
        "projects": ["Project 1", "Project 2"],
    }
    
    gaps = {
        "skills_missing_from_linkedin": ["Kubernetes"],
        "advanced_tech_themes": ["Docker", "Kubernetes"],
    }
    
    for mode in ["Get Hired", "Grow Connections", "Influence Market"]:
        roadmap = generate_enhanced_roadmap(mode, linkedin_data, resume_data, gaps)
        print(f"\n{mode} Roadmap ({len(roadmap)} weeks):")
        for week in roadmap:
            print(f"  - {week}")

if __name__ == "__main__":
    print("=" * 70)
    print("LinkedIn Profile Optimizer - Module Tests")
    print("=" * 70)
    
    test_headline_tips()
    test_about_tips()
    test_skills_tips()
    test_completeness()
    test_enhanced_fixes()
    test_enhanced_roadmap()
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)
