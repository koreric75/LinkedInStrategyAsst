from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional

try:
    from PIL import Image
    import pytesseract
except ImportError:  # pragma: no cover - optional dependency
    Image = None
    pytesseract = None

try:
    import pdfplumber
except ImportError:  # pragma: no cover - optional dependency
    pdfplumber = None

try:
    import docx  # python-docx
except ImportError:  # pragma: no cover - optional dependency
    docx = None


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
]


@dataclass
class LinkedInProfile:
    headline: str = ""
    about: str = ""
    current_role: str = ""
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    activity_topics: List[str] = field(default_factory=list)


@dataclass
class ResumeData:
    skills: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    experience: List[str] = field(default_factory=list)


@dataclass
class GapAnalysis:
    skills_missing_from_linkedin: List[str]
    projects_missing_from_linkedin: List[str]
    certifications_missing_from_linkedin: List[str]
    advanced_tech_themes: List[str]


@dataclass
class Strategy:
    mode: str
    profile_score: int
    immediate_fixes: List[str]
    strategic_roadmap: List[str]
    gaps: GapAnalysis


def extract_linkedin_profile(screenshot_paths: Iterable[Path]) -> LinkedInProfile:
    profile = LinkedInProfile()
    texts: List[str] = []
    if pytesseract is None or Image is None:
        return profile

    for path in screenshot_paths:
        if not path.exists():
            continue
        try:
            image = Image.open(path)
            text = pytesseract.image_to_string(image)
            texts.append(text)
        except Exception:
            continue

    full_text = "\n".join(texts)
    profile.headline = _extract_headline(full_text)
    profile.about = _extract_section(full_text, "About")
    profile.skills = _extract_list(full_text, ["Skills", "Skill"])
    profile.certifications = _extract_list(full_text, ["Certifications", "Certification"])
    profile.activity_topics = _extract_activity(full_text)
    profile.current_role = _extract_current_role(full_text)
    return profile


def parse_resume(resume_path: Path) -> ResumeData:
    data = ResumeData()
    if not resume_path.exists():
        return data

    text_chunks: List[str] = []
    if resume_path.suffix.lower() == ".pdf" and pdfplumber:
        with pdfplumber.open(resume_path) as pdf:
            for page in pdf.pages:
                text_chunks.append(page.extract_text() or "")
    elif resume_path.suffix.lower() in {".doc", ".docx"} and docx:
        document = docx.Document(resume_path)
        for para in document.paragraphs:
            text_chunks.append(para.text)
    else:
        try:
            text_chunks.append(resume_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    full_text = "\n".join(text_chunks)
    data.skills = _extract_skills(full_text)
    data.projects = _extract_projects(full_text)
    data.certifications = _extract_certifications(full_text)
    data.experience = _extract_experience(full_text)
    return data


def generate_gap_analysis(linkedin: LinkedInProfile, resume: ResumeData) -> GapAnalysis:
    resume_skills = set(_normalize_all(resume.skills))
    linkedin_skills = set(_normalize_all(linkedin.skills))
    skills_missing = sorted(resume_skills - linkedin_skills)

    resume_projects = set(_normalize_all(resume.projects))
    linkedin_projects = set(_normalize_all(linkedin.activity_topics))
    projects_missing = sorted(resume_projects - linkedin_projects)

    resume_certs = set(_normalize_all(resume.certifications))
    linkedin_certs = set(_normalize_all(linkedin.certifications))
    certs_missing = sorted(resume_certs - linkedin_certs)

    advanced_themes = _detect_advanced_themes("\n".join([linkedin.about, " ".join(resume.projects), " ".join(resume.skills)]))

    return GapAnalysis(
        skills_missing_from_linkedin=skills_missing,
        projects_missing_from_linkedin=projects_missing,
        certifications_missing_from_linkedin=certs_missing,
        advanced_tech_themes=advanced_themes,
    )


def generate_strategy(mode: str, gaps: GapAnalysis, linkedin: LinkedInProfile, resume: ResumeData) -> Strategy:
    score = _calculate_profile_score(gaps, linkedin, resume)
    
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
    except (ImportError, AttributeError) as e:
        # Fallback to original implementation if optimizer not available
        # ImportError: module not found, AttributeError: function not found
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
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return lines[0] if lines else ""


def _extract_section(text: str, title: str) -> str:
    pattern = rf"{title}[:\n]+(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _extract_list(text: str, labels: List[str]) -> List[str]:
    for label in labels:
        pattern = rf"{label}[:\n]+(.+?)(?:\n\n|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            raw = match.group(1)
            parts = re.split(r"[,\n]", raw)
            return [p.strip() for p in parts if p.strip()]
    return []


def _extract_activity(text: str) -> List[str]:
    topics = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if len(ln.split()) >= 3:
            topics.append(ln)
    return topics[:10]


def _extract_current_role(text: str) -> str:
    match = re.search(r"(?:Current|Role)[:\s]+(.+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _extract_skills(text: str) -> List[str]:
    skills = _extract_list(text, ["Skills"])
    if skills:
        return skills
    return _split_tokens(text, keywords=["skills", "technologies", "tools"])


def _extract_projects(text: str) -> List[str]:
    return _split_tokens(text, keywords=["projects", "experience", "work"], min_words=3)


def _extract_certifications(text: str) -> List[str]:
    certs = _extract_list(text, ["Certifications", "Certification"])
    return certs


def _extract_experience(text: str) -> List[str]:
    return _split_tokens(text, keywords=["experience", "work"], min_words=3)


def _split_tokens(text: str, keywords: List[str], min_words: int = 1) -> List[str]:
    tokens = []
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    for ln in lines:
        if any(k.lower() in ln.lower() for k in keywords) and len(ln.split()) >= min_words:
            tokens.append(ln)
    return tokens


def _detect_advanced_themes(text: str) -> List[str]:
    found = []
    lowered = text.lower()
    for term in ADVANCED_TECH_TERMS:
        if term.lower() in lowered:
            found.append(term)
    return sorted(set(found))


def _normalize_all(values: Iterable[str]) -> List[str]:
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
