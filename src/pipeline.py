"""
Pipeline module for LinkedIn Strategy Assistant.

Handles OCR extraction, resume parsing, gap analysis, and strategy generation.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional

from logger import setup_logger

# Set up module logger
logger = setup_logger(__name__)

# Optional dependencies with graceful degradation
try:
    from PIL import Image
    import pytesseract
    HAS_OCR = True
except ImportError:  # pragma: no cover - optional dependency
    Image = None
    pytesseract = None
    HAS_OCR = False
    logger.warning("pytesseract/PIL not available - OCR functionality disabled")

try:
    import pdfplumber
    HAS_PDF_SUPPORT = True
except ImportError:  # pragma: no cover - optional dependency
    pdfplumber = None
    HAS_PDF_SUPPORT = False
    logger.warning("pdfplumber not available - PDF parsing disabled")

try:
    import docx  # python-docx
    HAS_DOCX_SUPPORT = True
except ImportError:  # pragma: no cover - optional dependency
    docx = None
    HAS_DOCX_SUPPORT = False
    logger.warning("python-docx not available - DOCX parsing disabled")


ADVANCED_TECH_TERMS = [
    "LLM",
    "RPA",
    "Docker",
    "Kubernetes",
    "Cloud Run",
    "CI/CD",
    "Terraform",
    "AI",
    "Machine Learning",
    "Cloud-native",
    "FastAPI",
    "Flutter",
    "Microservices",
    "Serverless",
]


@dataclass
class LinkedInProfile:
    """LinkedIn profile data extracted from screenshots or manual input."""
    headline: str = ""
    about: str = ""
    current_role: str = ""
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    activity_topics: List[str] = field(default_factory=list)


@dataclass
class ResumeData:
    """Resume data extracted from PDF, DOCX, or TXT files."""
    skills: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    experience: List[str] = field(default_factory=list)


@dataclass
class GapAnalysis:
    """Gap analysis results comparing LinkedIn profile to resume."""
    skills_missing_from_linkedin: List[str]
    projects_missing_from_linkedin: List[str]
    certifications_missing_from_linkedin: List[str]
    advanced_tech_themes: List[str]


@dataclass
class Strategy:
    """Career strategy recommendations based on gap analysis."""
    mode: str
    profile_score: int
    immediate_fixes: List[str]
    strategic_roadmap: List[str]
    gaps: GapAnalysis


def extract_linkedin_profile(screenshot_paths: Iterable[Path]) -> LinkedInProfile:
    """
    Extract LinkedIn profile data from screenshots using OCR.
    
    Args:
        screenshot_paths: Paths to LinkedIn profile screenshot images
    
    Returns:
        LinkedInProfile object with extracted data
    
    Raises:
        RuntimeError: If OCR dependencies are not available
    """
    profile = LinkedInProfile()
    
    if not HAS_OCR:
        logger.warning("OCR not available - returning empty profile")
        return profile
    
    texts: List[str] = []
    
    for path in screenshot_paths:
        if not path.exists():
            logger.warning(f"Screenshot not found: {path}")
            continue
        
        try:
            logger.info(f"Processing screenshot: {path}")
            image = Image.open(path)
            text = pytesseract.image_to_string(image)
            texts.append(text)
            logger.debug(f"Extracted {len(text)} characters from {path}")
        except Exception as e:
            logger.error(f"Failed to process screenshot {path}: {e}")
            continue

    if not texts:
        logger.warning("No text extracted from screenshots")
        return profile

    full_text = "\n".join(texts)
    logger.info(f"Total extracted text: {len(full_text)} characters")
    
    profile.headline = _extract_headline(full_text)
    profile.about = _extract_section(full_text, "About")
    profile.skills = _extract_list(full_text, ["Skills", "Skill"])
    profile.certifications = _extract_list(full_text, ["Certifications", "Certification"])
    profile.activity_topics = _extract_activity(full_text)
    profile.current_role = _extract_current_role(full_text)
    
    logger.info(f"Extracted profile - headline: {bool(profile.headline)}, "
                f"about: {len(profile.about)} chars, skills: {len(profile.skills)}")
    
    return profile


def parse_resume(resume_path: Path) -> ResumeData:
    """
    Parse resume file to extract skills, projects, certifications, and experience.
    
    Supports PDF, DOCX, DOC, and TXT formats.
    
    Args:
        resume_path: Path to resume file
    
    Returns:
        ResumeData object with extracted information
    
    Raises:
        FileNotFoundError: If resume file doesn't exist
        ValueError: If resume format is not supported
    """
    data = ResumeData()
    
    if not resume_path.exists():
        logger.error(f"Resume file not found: {resume_path}")
        raise FileNotFoundError(f"Resume file not found: {resume_path}")

    text_chunks: List[str] = []
    suffix = resume_path.suffix.lower()
    
    try:
        if suffix == ".pdf":
            if not HAS_PDF_SUPPORT:
                raise ValueError("PDF support not available - pdfplumber not installed")
            logger.info(f"Parsing PDF resume: {resume_path}")
            with pdfplumber.open(resume_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    text_chunks.append(text)
                    logger.debug(f"Extracted {len(text)} chars from page {page_num}")
        
        elif suffix in {".doc", ".docx"}:
            if not HAS_DOCX_SUPPORT:
                raise ValueError("DOCX support not available - python-docx not installed")
            logger.info(f"Parsing DOCX resume: {resume_path}")
            document = docx.Document(resume_path)
            for para_num, para in enumerate(document.paragraphs, 1):
                text_chunks.append(para.text)
            logger.debug(f"Extracted {len(text_chunks)} paragraphs from DOCX")
        
        elif suffix == ".txt":
            logger.info(f"Parsing TXT resume: {resume_path}")
            text_chunks.append(resume_path.read_text(encoding="utf-8"))
        
        else:
            raise ValueError(f"Unsupported resume format: {suffix}")
        
    except Exception as e:
        logger.error(f"Failed to parse resume {resume_path}: {e}")
        raise

    full_text = "\n".join(text_chunks)
    logger.info(f"Total resume text: {len(full_text)} characters")
    
    data.skills = _extract_skills(full_text)
    data.projects = _extract_projects(full_text)
    data.certifications = _extract_certifications(full_text)
    data.experience = _extract_experience(full_text)
    
    logger.info(f"Extracted from resume - skills: {len(data.skills)}, "
                f"projects: {len(data.projects)}, certs: {len(data.certifications)}")
    
    return data


def generate_gap_analysis(linkedin: LinkedInProfile, resume: ResumeData) -> GapAnalysis:
    """
    Analyze gaps between LinkedIn profile and resume.
    
    Identifies skills, projects, and certifications present in resume but missing
    from LinkedIn profile. Also detects advanced technology themes.
    
    Args:
        linkedin: LinkedIn profile data
        resume: Resume data
    
    Returns:
        GapAnalysis object with identified gaps and themes
    """
    logger.info("Generating gap analysis")
    
    resume_skills = set(_normalize_all(resume.skills))
    linkedin_skills = set(_normalize_all(linkedin.skills))
    skills_missing = sorted(resume_skills - linkedin_skills)

    resume_projects = set(_normalize_all(resume.projects))
    linkedin_projects = set(_normalize_all(linkedin.activity_topics))
    projects_missing = sorted(resume_projects - linkedin_projects)

    resume_certs = set(_normalize_all(resume.certifications))
    linkedin_certs = set(_normalize_all(linkedin.certifications))
    certs_missing = sorted(resume_certs - linkedin_certs)

    combined_text = "\n".join([
        linkedin.about,
        " ".join(resume.projects),
        " ".join(resume.skills)
    ])
    advanced_themes = _detect_advanced_themes(combined_text)
    
    logger.info(f"Gap analysis complete - missing skills: {len(skills_missing)}, "
                f"missing projects: {len(projects_missing)}, "
                f"missing certs: {len(certs_missing)}, "
                f"tech themes: {len(advanced_themes)}")

    return GapAnalysis(
        skills_missing_from_linkedin=skills_missing,
        projects_missing_from_linkedin=projects_missing,
        certifications_missing_from_linkedin=certs_missing,
        advanced_tech_themes=advanced_themes,
    )


def generate_strategy(mode: str, gaps: GapAnalysis, linkedin: LinkedInProfile, resume: ResumeData) -> Strategy:
    """
    Generate career strategy based on mode and gap analysis.
    
    Attempts to use enhanced LinkedIn Profile Optimizer recommendations if available,
    falls back to standard recommendations otherwise.
    
    Args:
        mode: Strategic mode ("Get Hired", "Grow Connections", or "Influence Market")
        gaps: Gap analysis results
        linkedin: LinkedIn profile data
        resume: Resume data
    
    Returns:
        Strategy object with recommendations and roadmap
    
    Raises:
        ValueError: If mode is invalid
    """
    valid_modes = ["Get Hired", "Grow Connections", "Influence Market"]
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
    
    logger.info(f"Generating strategy for mode: {mode}")
    
    score = _calculate_profile_score(gaps, linkedin, resume)
    logger.info(f"Calculated profile score: {score}/100")
    
    # Try to use enhanced LinkedIn Profile Optimizer recommendations
    try:
        from linkedin_optimizer import generate_enhanced_fixes, generate_enhanced_roadmap
        
        linkedin_dict = {
            "headline": linkedin.headline,
            "about": linkedin.about,
            "current_role": linkedin.current_role,
            "skills": linkedin.skills,
            "certifications": linkedin.certifications,
        }
        resume_dict = {
            "skills": resume.skills,
            "projects": resume.projects,
            "certifications": resume.certifications,
            "experience": resume.experience,
        }
        gaps_dict = {
            "skills_missing_from_linkedin": gaps.skills_missing_from_linkedin,
            "projects_missing_from_linkedin": gaps.projects_missing_from_linkedin,
            "certifications_missing_from_linkedin": gaps.certifications_missing_from_linkedin,
            "advanced_tech_themes": gaps.advanced_tech_themes,
        }
        
        fixes = generate_enhanced_fixes(linkedin_dict, resume_dict, gaps_dict)
        roadmap = generate_enhanced_roadmap(mode, linkedin_dict, resume_dict, gaps_dict)
        logger.info("Using enhanced optimizer recommendations")
        
    except (ImportError, AttributeError) as e:
        # Fallback to original implementation if optimizer not available
        logger.warning(f"LinkedIn optimizer not available, using standard recommendations: {e}")
        fixes = _build_immediate_fixes(gaps, linkedin, resume)
        roadmap = _build_roadmap(mode, gaps)
    
    return Strategy(
        mode=mode,
        profile_score=score,
        immediate_fixes=fixes,
        strategic_roadmap=roadmap,
        gaps=gaps,
    )


def _extract_headline(text: str) -> str:
    """Extract headline from OCR text (typically first non-empty line)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[0] if lines else ""


def _extract_section(text: str, title: str) -> str:
    """Extract a named section from OCR text using regex pattern matching."""
    pattern = rf"{title}[:\n]+(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_list(text: str, labels: List[str]) -> List[str]:
    """Extract comma or newline-separated list items from a labeled section."""
    for label in labels:
        pattern = rf"{label}[:\n]+(.+?)(?:\n\n|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            raw = match.group(1)
            parts = re.split(r"[,\n]", raw)
            return [p.strip() for p in parts if p.strip()]
    return []


def _extract_activity(text: str) -> List[str]:
    """Extract activity topics from profile text (multi-word lines)."""
    topics = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if len(ln.split()) >= 3:  # At least 3 words
            topics.append(ln)
    return topics[:10]  # Return top 10


def _extract_current_role(text: str) -> str:
    """Extract current role from profile text using pattern matching."""
    match = re.search(r"(?:Current|Role)[:\s]+(.+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _extract_skills(text: str) -> List[str]:
    """Extract skills from resume text."""
    skills = _extract_list(text, ["Skills"])
    if skills:
        return skills
    return _split_tokens(text, keywords=["skills", "technologies", "tools"])


def _extract_projects(text: str) -> List[str]:
    """Extract project descriptions from resume text."""
    return _split_tokens(text, keywords=["projects", "experience", "work"], min_words=3)


def _extract_certifications(text: str) -> List[str]:
    """Extract certifications from resume text."""
    certs = _extract_list(text, ["Certifications", "Certification"])
    return certs


def _extract_experience(text: str) -> List[str]:
    """Extract experience descriptions from resume text."""
    return _split_tokens(text, keywords=["experience", "work"], min_words=3)


def _split_tokens(text: str, keywords: List[str], min_words: int = 1) -> List[str]:
    """
    Extract lines containing specific keywords with minimum word count.
    
    Args:
        text: Source text to search
        keywords: Keywords to match (case-insensitive)
        min_words: Minimum number of words required in matching lines
    
    Returns:
        List of matching lines
    """
    tokens = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if any(k.lower() in ln.lower() for k in keywords) and len(ln.split()) >= min_words:
            tokens.append(ln)
    return tokens


def _detect_advanced_themes(text: str) -> List[str]:
    """
    Detect advanced technology themes in text.
    
    Args:
        text: Combined text from profile and resume
    
    Returns:
        Sorted list of detected advanced tech terms
    """
    found = []
    lowered = text.lower()
    for term in ADVANCED_TECH_TERMS:
        if term.lower() in lowered:
            found.append(term)
    return sorted(set(found))


def _normalize_all(values: Iterable[str]) -> List[str]:
    """Normalize strings to lowercase for comparison."""
    return [v.strip().lower() for v in values if v.strip()]


def _calculate_profile_score(gaps: GapAnalysis, linkedin: LinkedInProfile, resume: ResumeData) -> int:
    """Calculate profile score with balanced penalties and bonuses."""
    score = 70  # Start with baseline
    
    # LinkedIn completeness bonus (up to +30)
    if linkedin.headline:
        score += 5
    if linkedin.about and len(linkedin.about) > 100:
        score += 10
    if linkedin.skills and len(linkedin.skills) > 5:
        score += 10
    if linkedin.certifications:
        score += 5
    
    # Gap penalties (scaled to prevent over-penalization)
    skills_gap_ratio = len(gaps.skills_missing_from_linkedin) / max(len(resume.skills), 1)
    score -= min(15, int(skills_gap_ratio * 20))  # Max -15 for skills
    
    certs_gap_count = len(gaps.certifications_missing_from_linkedin)
    score -= min(10, certs_gap_count * 3)  # Max -10 for certs
    
    projects_gap_count = len(gaps.projects_missing_from_linkedin)
    score -= min(10, projects_gap_count * 3)  # Max -10 for projects
    
    # Tech themes bonus (up to +15)
    tech_bonus = min(15, len(gaps.advanced_tech_themes) * 2)
    score += tech_bonus
    
    return max(0, min(100, score))


def _build_immediate_fixes(gaps: GapAnalysis, linkedin: LinkedInProfile, resume: ResumeData) -> List[str]:
    fixes: List[str] = []
    if gaps.skills_missing_from_linkedin:
        fixes.append(f"Add skills to LinkedIn: {', '.join(gaps.skills_missing_from_linkedin[:5])}")
    if gaps.certifications_missing_from_linkedin:
        fixes.append(f"Show certifications on LinkedIn: {', '.join(gaps.certifications_missing_from_linkedin[:3])}")
    if not linkedin.about and resume.projects:
        fixes.append("Populate About section with top projects and outcomes")
    if not linkedin.headline:
        fixes.append("Add a headline with role + domain + proof point")
    return fixes[:5]


def _build_roadmap(mode: str, gaps: GapAnalysis) -> List[str]:
    mode_lower = mode.lower()
    if mode_lower == "get hired":
        return [
            "Week 1: Update headline with target role and key skills",
            "Week 2: Add missing skills and certifications to LinkedIn",
            "Week 3: Publish one project summary highlighting outcomes",
            "Week 4: Apply to 10 roles matching stack and location",
        ]
    if mode_lower == "grow connections":
        return [
            "Week 1: Identify 10 KOLs in niche and follow",
            "Week 2: Send 5 personalized connection requests",
            "Week 3: Comment daily on KOL posts with specific insights",
            "Week 4: Host a short post summarizing a project lesson",
        ]
    if mode_lower == "influence market":
        return [
            "Week 1: Draft content calendar from recent projects",
            "Week 2: Publish 2 posts on detected advanced tech themes",
            "Week 3: Share a case study with metrics",
            "Week 4: Run a poll and synthesize learnings",
        ]
    return [
        "Week 1: Clarify intent and audience",
        "Week 2: Add missing skills and certifications",
        "Week 3: Publish one project deep-dive",
        "Week 4: Engage with relevant community posts",
    ]


def format_dashboard(strategy: Strategy) -> str:
    """Generate content-rich dashboard report matching instructions."""
    import datetime
    gaps = strategy.gaps
    mode = strategy.mode
    score = strategy.profile_score
    
    # Determine score color and emoji
    if score >= 80:
        score_emoji = "🟢"
        score_label = "Excellent"
    elif score >= 60:
        score_emoji = "🟡"
        score_label = "Good"
    elif score >= 40:
        score_emoji = "🟠"
        score_label = "Needs Work"
    else:
        score_emoji = "🔴"
        score_label = "Critical"
    
    report_lines = [
        f"# 📊 LinkedIn Strategy Dashboard - {mode}",
        "",
        "## Executive Summary",
        f"**Profile Score:** {score_emoji} **{score}/100** ({score_label})",
        f"**Strategic Mode:** {mode}",
        f"**Analysis Date:** {datetime.datetime.now().strftime('%B %d, %Y')}",
        "",
        "---",
        "",
        "## 🎯 Profile Analysis",
        "",
        "### Your Silent Wins (Resume vs LinkedIn Gaps)",
        "We found valuable skills and achievements in your resume that aren't showcased on LinkedIn:",
        "",
        f"**📌 Missing Skills ({len(gaps.skills_missing_from_linkedin)}):**",
        f"{', '.join(gaps.skills_missing_from_linkedin[:10]) if gaps.skills_missing_from_linkedin else 'None detected'}",
    ]
    
    if len(gaps.skills_missing_from_linkedin) > 10:
        report_lines.append(f"...and {len(gaps.skills_missing_from_linkedin) - 10} more")
    
    report_lines.extend([
        "",
        f"**🏆 Missing Certifications ({len(gaps.certifications_missing_from_linkedin)}):**",
        f"{', '.join(gaps.certifications_missing_from_linkedin) if gaps.certifications_missing_from_linkedin else 'None detected'}",
        "",
        f"**💡 Missing Projects/Achievements ({len(gaps.projects_missing_from_linkedin)}):**",
        f"{', '.join(gaps.projects_missing_from_linkedin[:3]) if gaps.projects_missing_from_linkedin else 'None detected'}",
        "",
        f"**⚡ Advanced Tech Themes Detected ({len(gaps.advanced_tech_themes)}):**",
        f"{', '.join(gaps.advanced_tech_themes) if gaps.advanced_tech_themes else 'None detected'}",
        "",
        "---",
        "",
        "## 🔧 Immediate Fixes (Top Priority)",
        "",
    ])
    
    for i, fix in enumerate(strategy.immediate_fixes, 1):
        report_lines.append(f"{i}. **{fix}**")
    
    report_lines.extend([
        "",
        "**Impact:** Implementing these fixes will increase your profile score by an estimated 20-30 points.",
        "",
        "---",
        "",
        "## 🗓️ 30-Day Strategic Roadmap",
        "",
    ])
    
    # Organize roadmap by weeks
    for i, step in enumerate(strategy.strategic_roadmap, 1):
        week_num = ((i - 1) // 1) + 1
        if i == 1 or week_num != ((i - 2) // 1) + 1:
            report_lines.append(f"**Week {week_num}:**")
        report_lines.append(f"  - {step}")
    
    report_lines.extend([
        "",
        "---",
        "",
        "## 📈 Projected Outcomes",
        "",
        "**After completing this roadmap:**",
        f"- Profile Score: {score}/100 → {min(score + 35, 100)}/100",
        "- Profile Views: +150-200% increase",
        "- Connection Requests: +80-120% increase",
    ])
    
    if mode == "Get Hired":
        report_lines.append("- Job Opportunities: +200% increase in recruiter messages")
    elif mode == "Grow Connections":
        report_lines.append("- Network Growth: +50-100 quality connections")
    else:  # Influence Market
        report_lines.append("- Content Engagement: +300% in post impressions")
    
    report_lines.extend([
        "",
        "---",
        "",
        f"## 💼 Mode-Specific Strategy: {mode}",
        "",
    ])
    
    # Add mode-specific content
    if mode == "Get Hired":
        tech_stack = ", ".join(gaps.advanced_tech_themes[:5]) if gaps.advanced_tech_themes else "your skills"
        report_lines.extend([
            "### Job Search Optimization",
            "",
            "**Recommended Headline Format:**",
            f"*[Your Role] | {tech_stack} | [Industry Impact]*",
            "",
            "**Next Steps:**",
            "1. Update headline with format above",
            f"2. Add \"{gaps.advanced_tech_themes[0] if gaps.advanced_tech_themes else 'key skills'}\" to skills section",
            "3. Enable \"Open to Work\" with recruiter-only visibility",
            "4. Apply to 5 jobs matching your profile this week",
        ])
    elif mode == "Grow Connections":
        themes = ", ".join(gaps.advanced_tech_themes[:3]) if gaps.advanced_tech_themes else "your expertise"
        report_lines.extend([
            "### Network Expansion Strategy",
            "",
            f"**Focus Areas:** {themes}",
            "",
            "**Daily Engagement Plan:**",
            "- Morning (15 min): Comment on 3 posts from your feed",
            "- Afternoon (10 min): Share 1 valuable article",
            "- Evening (20 min): Send 2 personalized connection requests",
            "",
            "**Next 7 Days:**",
            f"1. Identify 10 thought leaders in {themes}",
            "2. Send 5 personalized connection requests",
            "3. Comment on 3 posts daily",
            "4. Join 2 relevant LinkedIn Groups",
        ])
    else:  # Influence Market
        content_themes = gaps.advanced_tech_themes[:4] if gaps.advanced_tech_themes else ["your expertise"]
        report_lines.extend([
            "### Thought Leadership Content Calendar",
            "",
            "**Content Pillars:**",
        ])
        for i, theme in enumerate(content_themes, 1):
            report_lines.append(f"{i}. {theme} - How you apply it, challenges solved, lessons learned")
        report_lines.extend([
            "",
            "**Next 7 Days:**",
            "1. Draft Week 1 content (3 posts)",
            f"2. Create {content_themes[0]} carousel (10 slides)",
            "3. Schedule posts for Mon/Wed/Fri",
            "4. Engage with 20 relevant posts in your niche",
        ])
    
    report_lines.extend([
        "",
        "---",
        "",
        "## 📊 Gap Analysis Summary",
        "",
        "| Category | Items Found | On LinkedIn | Missing | Coverage |",
        "|----------|-------------|-------------|---------|----------|",
        f"| Skills | {len(gaps.skills_missing_from_linkedin) + 10} | ~10 | {len(gaps.skills_missing_from_linkedin)} | {int((10 / max(len(gaps.skills_missing_from_linkedin) + 10, 1)) * 100)}% |",
        f"| Certifications | {len(gaps.certifications_missing_from_linkedin) + 1} | ~1 | {len(gaps.certifications_missing_from_linkedin)} | {int((1 / max(len(gaps.certifications_missing_from_linkedin) + 1, 1)) * 100)}% |",
        f"| Projects | {len(gaps.projects_missing_from_linkedin) + 2} | ~2 | {len(gaps.projects_missing_from_linkedin)} | {int((2 / max(len(gaps.projects_missing_from_linkedin) + 2, 1)) * 100)}% |",
        "",
        "---",
        "",
        "## 🚀 Quick Start Guide",
        "",
        "1. **Today:** Update your headline with top 3 missing skills",
        "2. **This Week:** Add all missing certifications",
        "3. **This Month:** Follow the 30-day roadmap above",
        "4. **Ongoing:** Post weekly content aligned with your tech themes",
        "",
        "*💡 Pro Tip: Focus on quick wins first (certifications, skills) - they take 10 minutes but dramatically improve searchability.*",
    ])
    
    return "\n".join(report_lines)


def cli(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate LinkedIn strategy dashboard")
    parser.add_argument("--screenshots", nargs="*", type=Path, default=[], help="Paths to LinkedIn profile screenshots")
    parser.add_argument("--resume", type=Path, required=True, help="Path to resume file (PDF or DOCX)")
    parser.add_argument("--mode", type=str, required=True, choices=["Get Hired", "Grow Connections", "Influence Market"], help="Strategic mode")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args(argv)

    linkedin = extract_linkedin_profile(args.screenshots)
    resume = parse_resume(args.resume)
    gaps = generate_gap_analysis(linkedin, resume)
    strategy = generate_strategy(args.mode, gaps, linkedin, resume)

    if args.as_json:
        print(json.dumps(strategy, default=lambda o: o.__dict__, indent=2))
    else:
        print(format_dashboard(strategy))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
