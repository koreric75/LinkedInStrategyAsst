"""
LinkedIn Profile Optimizer - Enhanced strategy generation using AI agent skills.

This module integrates the LinkedIn Profile Optimizer skill to provide more 
detailed and expert recommendations for LinkedIn profile optimization.
"""

from __future__ import annotations
from typing import List, Dict, Any


# LinkedIn Profile Optimizer best practices derived from skill
LINKEDIN_BEST_PRACTICES = {
    "headline": {
        "max_chars": 220,
        "formula": "[Role] | [Key Expertise] | [Value Proposition]",
        "keywords_priority": ["role", "expertise", "value"],
        "impact_multiplier": 21  # Profiles with optimized headlines get 21x more views
    },
    "about": {
        "min_chars": 1500,
        "max_chars": 2600,
        "recommended_chars": 1800,
        "structure": ["hook", "who_you_are", "achievements", "looking_for", "skills_list", "cta"],
        "first_line_preview": 300  # Only 300 chars show before "see more"
    },
    "skills": {
        "max_count": 50,
        "min_recommended": 5,
        "optimal_count": 50,  # Use all 50 slots
        "categories": ["job_specific", "tools", "methodologies", "soft_skills", "industry_terms"]
    },
    "completeness": {
        "all_star": ["photo", "headline", "current_position", "two_past_positions", "education", "5_skills", "industry", "postal_code", "50_connections"],
        "beyond_all_star": ["banner", "featured", "long_about", "rich_media", "500_connections", "5_recommendations", "50_skills", "volunteer", "certifications"]
    },
    "experience": {
        "description_length": "2-3 sentences",
        "bullets": "4-6 achievement bullets",
        "include": ["clear_title", "company_logo", "date_range", "location", "description", "achievements", "media"]
    }
}


def get_headline_optimization_tips(current_headline: str, skills: List[str], current_role: str) -> List[str]:
    """Generate specific tips for optimizing LinkedIn headline."""
    tips = []
    
    if not current_headline or len(current_headline) < 50:
        tips.append("Create a compelling headline using formula: [Role] | [Key Expertise] | [Value Proposition]")
    
    if current_role and current_role not in current_headline:
        tips.append(f"Include your current role '{current_role}' in headline for searchability")
    
    # Check for keywords
    if skills:
        top_skills = skills[:3]
        missing_skills = [s for s in top_skills if s.lower() not in current_headline.lower()]
        if missing_skills:
            tips.append(f"Add key skills to headline: {', '.join(missing_skills[:2])}")
    
    # Check for value proposition
    value_indicators = ["driving", "building", "leading", "growing", "transforming", "delivering"]
    has_value = any(indicator in current_headline.lower() for indicator in value_indicators)
    if not has_value:
        tips.append("Add a value proposition showing impact (e.g., 'Driving 0→1 Products to $10M ARR')")
    
    return tips


def get_about_section_optimization_tips(current_about: str, skills: List[str], achievements: List[str]) -> List[str]:
    """Generate specific tips for optimizing LinkedIn About section."""
    tips = []
    
    about_length = len(current_about) if current_about else 0
    
    if about_length == 0:
        tips.append("Write an About section (1,500-2,000 characters) using structure: Hook → Who You Are → Achievements → Skills → CTA")
    elif about_length < 1500:
        tips.append(f"Expand About section to 1,500+ characters (currently {about_length}). Add achievements and skills list")
    
    # Check for hook (compelling first line)
    if current_about and len(current_about) > 300:
        first_line = current_about.split('\n')[0] if '\n' in current_about else current_about[:300]
        # If first line is too long, suggest making it more compelling
        if len(first_line) > 150:
            tips.append("Start About section with a compelling one-liner (shows in preview before 'see more')")
    
    # Check for skills list
    if skills and current_about:
        skills_mentioned = sum(1 for skill in skills if skill.lower() in current_about.lower())
        if skills_mentioned < min(5, len(skills)):
            tips.append("Add a 'Key skills:' section at the end of About listing your core competencies")
    
    # Check for CTA
    if current_about and "email" not in current_about.lower() and "connect" not in current_about.lower():
        tips.append("Add a call-to-action at the end (e.g., 'Let's connect! Reach me at [email]')")
    
    return tips


def get_skills_optimization_tips(linkedin_skills: List[str], resume_skills: List[str]) -> List[str]:
    """Generate specific tips for optimizing LinkedIn Skills section."""
    tips = []
    
    current_count = len(linkedin_skills)
    optimal = LINKEDIN_BEST_PRACTICES["skills"]["optimal_count"]
    
    if current_count == 0:
        tips.append(f"Add skills to LinkedIn Skills section (aim for {optimal} total)")
    elif current_count < optimal:
        tips.append(f"Increase skills count from {current_count} to {optimal} (use all available slots)")
    
    # Skills missing from LinkedIn
    missing = [s for s in resume_skills if s.lower() not in [ls.lower() for ls in linkedin_skills]]
    if missing:
        tips.append(f"Transfer skills from resume to LinkedIn: {', '.join(missing[:5])}")
    
    return tips


def get_completeness_assessment(linkedin_data: Dict) -> Dict[str, Any]:
    """Assess LinkedIn profile completeness against All-Star and beyond criteria."""
    # Simple assessment based on available data
    has_headline = bool(linkedin_data.get("headline"))
    has_about = bool(linkedin_data.get("about"))
    has_skills = len(linkedin_data.get("skills", [])) >= 5
    has_50_skills = len(linkedin_data.get("skills", [])) >= 50
    has_certs = bool(linkedin_data.get("certifications"))
    
    all_star_score = sum([
        has_headline,
        has_about,
        has_skills,
    ]) / 3 * 100
    
    beyond_score = sum([
        has_headline and len(linkedin_data.get("headline", "")) > 50,
        has_about and len(linkedin_data.get("about", "")) >= 1500,
        has_50_skills,
        has_certs,
    ]) / 4 * 100
    
    return {
        "all_star_score": int(all_star_score),
        "beyond_score": int(beyond_score),
        "is_all_star": all_star_score >= 80,
        "is_beyond": beyond_score >= 80,
    }


def get_keyword_optimization_tips(linkedin_text: str, target_keywords: List[str]) -> List[str]:
    """Generate tips for keyword optimization across profile."""
    tips = []
    
    if not target_keywords:
        return tips
    
    # Check keyword presence
    linkedin_lower = linkedin_text.lower()
    missing_keywords = []
    for keyword in target_keywords[:10]:  # Check top 10
        if keyword.lower() not in linkedin_lower:
            missing_keywords.append(keyword)
    
    if missing_keywords:
        tips.append(f"Add searchable keywords throughout profile: {', '.join(missing_keywords[:5])}")
        tips.append("Place keywords in: Headline (highest weight) → About → Experience → Skills")
    
    return tips


def generate_enhanced_fixes(
    linkedin_data: Dict,
    resume_data: Dict,
    gaps: Dict
) -> List[str]:
    """Generate enhanced immediate fixes using LinkedIn Profile Optimizer best practices."""
    fixes = []
    
    # Headline optimization
    headline_tips = get_headline_optimization_tips(
        linkedin_data.get("headline", ""),
        resume_data.get("skills", []),
        linkedin_data.get("current_role", "")
    )
    fixes.extend(headline_tips[:2])
    
    # About section optimization
    about_tips = get_about_section_optimization_tips(
        linkedin_data.get("about", ""),
        resume_data.get("skills", []),
        resume_data.get("projects", [])
    )
    fixes.extend(about_tips[:2])
    
    # Skills optimization
    skills_tips = get_skills_optimization_tips(
        linkedin_data.get("skills", []),
        resume_data.get("skills", [])
    )
    fixes.extend(skills_tips[:1])
    
    # Certifications
    if gaps.get("certifications_missing_from_linkedin"):
        missing_certs = gaps["certifications_missing_from_linkedin"]
        fixes.append(f"Add certifications to LinkedIn: {', '.join(missing_certs[:3])}")
    
    return fixes[:6]  # Return top 6 most impactful fixes


def generate_enhanced_roadmap(
    mode: str,
    linkedin_data: Dict,
    resume_data: Dict,
    gaps: Dict
) -> List[str]:
    """Generate enhanced strategic roadmap using LinkedIn Profile Optimizer best practices."""
    mode_lower = mode.lower()
    completeness = get_completeness_assessment(linkedin_data)
    
    if mode_lower == "get hired":
        roadmap = [
            "Week 1: Optimize headline with target role + key skills + value proposition",
            "Week 2: Write compelling About section (1,500+ chars) with hook, achievements, skills list",
            "Week 3: Add all missing skills and certifications (aim for 50 total skills)",
            "Week 4: Add rich media to Experience section and request 5 recommendations",
        ]
        if completeness["is_all_star"]:
            roadmap.append("Week 5: Enable 'Open to Work' (recruiters only) and apply to 10 targeted roles")
        else:
            roadmap.append("Week 5: Complete All-Star profile requirements before activating 'Open to Work'")
    
    elif mode_lower == "grow connections":
        roadmap = [
            "Week 1: Optimize profile for searchability (headline, About, skills with keywords)",
            "Week 2: Identify 10 KOLs in your niche and analyze their content themes",
            "Week 3: Send 5 personalized connection requests referencing specific content",
            "Week 4: Comment daily on KOL posts with insights (not just 'Great post!')",
            "Week 5: Publish your first post sharing a professional lesson or project insight",
        ]
    
    elif mode_lower == "influence market":
        roadmap = [
            "Week 1: Optimize profile as your content portfolio (Featured section + rich media)",
            "Week 2: Create content calendar from recent projects and detected tech themes",
            "Week 3: Publish 2 posts on advanced tech topics with specific examples",
            "Week 4: Share a detailed case study with metrics and outcomes",
            "Week 5: Engage with comments and track post analytics to refine strategy",
        ]
    
    else:
        roadmap = [
            "Week 1: Assess profile completeness and set All-Star goal",
            "Week 2: Optimize headline and About section for searchability",
            "Week 3: Add all missing skills, certifications, and experience details",
            "Week 4: Request recommendations and add Featured content",
            "Week 5: Review profile analytics and iterate on improvements",
        ]
    
    return roadmap
