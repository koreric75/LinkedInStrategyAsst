#!/usr/bin/env python3
import sys
sys.path.insert(0, 'c:/Users/korer/LinkedInStrategyAsst/src')
from pipeline import extract_linkedin_profile, parse_resume, generate_gap_analysis, generate_strategy
from pathlib import Path

# Load test data
screenshots = [Path('c:/Users/korer/LinkedInStrategyAsst/test_data/linkedin_screenshot_1.png'), Path('c:/Users/korer/LinkedInStrategyAsst/test_data/linkedin_screenshot_2.png')]
resume = Path('c:/Users/korer/LinkedInStrategyAsst/test_data/sample_resume.txt')

linkedin = extract_linkedin_profile(screenshots)
resume_data = parse_resume(resume)
gaps = generate_gap_analysis(linkedin, resume_data)
strategy = generate_strategy('Get Hired', gaps, linkedin, resume_data)

print('=== LINKEDIN PROFILE ===')
print(f'Headline: {linkedin.headline if linkedin.headline else "(empty)"}')
print(f'About: {linkedin.about[:100] if linkedin.about else "(empty)"}...')
print(f'Skills: {len(linkedin.skills)} items - {linkedin.skills[:3]}')
print(f'Certifications: {len(linkedin.certifications)} items')
print()
print('=== RESUME DATA ===')
print(f'Skills: {len(resume_data.skills)} items - {resume_data.skills[:5]}')
print(f'Certifications: {len(resume_data.certifications)} items')
print(f'Projects: {len(resume_data.projects)} items')
print()
print('=== GAP ANALYSIS ===')
print(f'Skills missing: {len(gaps.skills_missing_from_linkedin)}')
print(f'Certs missing: {len(gaps.certifications_missing_from_linkedin)}')
print(f'Projects missing: {len(gaps.projects_missing_from_linkedin)}')
print(f'Tech themes: {gaps.advanced_tech_themes}')
print()
print('=== NEW SCORE CALCULATION ===')
print(f'Baseline: 70')
print(f'LinkedIn completeness:')
print(f'  Headline: +{"5" if linkedin.headline else "0"} ({"YES" if linkedin.headline else "NO"})')
print(f'  About >100 chars: +{"10" if linkedin.about and len(linkedin.about) > 100 else "0"} ({"YES" if linkedin.about and len(linkedin.about) > 100 else "NO"})')
print(f'  Skills >5: +{"10" if linkedin.skills and len(linkedin.skills) > 5 else "0"} ({len(linkedin.skills)} skills)')
print(f'  Has certs: +{"5" if linkedin.certifications else "0"} ({"YES" if linkedin.certifications else "NO"})')
skills_gap_ratio = len(gaps.skills_missing_from_linkedin) / max(len(resume_data.skills), 1)
print(f'Skills gap: -{min(15, int(skills_gap_ratio * 20))} (ratio: {skills_gap_ratio:.2%})')
print(f'Certs gap: -{min(10, len(gaps.certifications_missing_from_linkedin) * 3)} ({len(gaps.certifications_missing_from_linkedin)} missing)')
print(f'Projects gap: -{min(10, len(gaps.projects_missing_from_linkedin) * 3)} ({len(gaps.projects_missing_from_linkedin)} missing)')
print(f'Tech themes bonus: +{min(15, len(gaps.advanced_tech_themes) * 2)} ({len(gaps.advanced_tech_themes)} themes)')
print()
print(f'FINAL SCORE: {strategy.profile_score}/100')

