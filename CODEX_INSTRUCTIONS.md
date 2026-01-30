# Google Codex Max – Implementation Instructions
**Project:** LinkedIn Strategy Assistant (Opal Workflow)  
**Reference:** [.github/copilot-instructions.md](.github/copilot-instructions.md) | [Untitled-1.md](Untitled-1.md)

## Application Architecture
Build a multi-step Opal application that processes LinkedIn profiles and resumes to generate career growth strategies.

### Step 1: User Input Collection
Create three input components on the left panel:

```python
# Input 1: LinkedIn Profile Screenshots
linkedin_screenshots = opal.upload(
    label="LinkedIn Profile Screenshots",
    accept=[".png", ".jpg", ".jpeg"],
    multiple=True,
    description="Upload screenshots of your headline, About section, and activity"
)

# Input 2: Resume File  
resume_file = opal.upload(
    label="Resume File",
    accept=[".pdf", ".docx", ".doc"],
    description="Upload your current resume (PDF or Word)"
)

# Input 3: Strategic Mode Selection
strategic_mode = opal.select(
    label="Strategic Mode",
    options=["Get Hired", "Grow Connections", "Influence Market"],
    description="Select your primary career goal"
)
```

### Step 2: Extract LinkedIn Profile Information
**Objective:** Perform OCR and layout analysis on screenshots to extract structured data.

```python
def extract_linkedin_profile(screenshots):
    """
    Use OCR (pytesseract/Google Vision API) to extract:
    - Headline text
    - About section content
    - Current position & company
    - Skills listed
    - Recent activity/posts
    - Certifications visible
    
    Return: dict with structured fields
    """
    profile_data = {
        "headline": "",
        "about": "",
        "current_role": "",
        "skills": [],
        "certifications": [],
        "activity_topics": []
    }
    
    for screenshot in screenshots:
        # OCR extraction logic
        # Layout detection to identify section types
        # Text extraction per section
        pass
    
    return profile_data
```

**Key Requirements:**
- Detect sections by layout patterns (headline at top, About has paragraph text)
- Extract skills as list items or comma-separated values
- Identify certification badges/text (e.g., "CompTIA Security+")

### Step 3: Parse Resume File
**Objective:** Extract skills, projects, and certifications from PDF/Word documents.

```python
def parse_resume(resume_file):
    """
    Parse PDF/DOCX to extract:
    - Technical skills (CI/CD, Docker, Cloud Run, LLM integration, RPA)
    - Project descriptions with technologies used
    - Certifications with dates
    - Work experience with achievements
    
    Return: dict with structured fields
    """
    resume_data = {
        "skills": [],
        "projects": [],
        "certifications": [],
        "experience": []
    }
    
    # Use PyPDF2/pdfplumber for PDFs, python-docx for Word
    # Regex patterns to detect:
    # - "Skills:" sections → extract as list
    # - "Projects:" or "Experience:" → extract with bullet points
    # - Certification names and dates
    
    # Advanced tech detection (LLM, RPA, cloud-native, Docker, Kubernetes)
    advanced_techs = ["LLM", "RPA", "Docker", "Kubernetes", "Cloud Run", 
                     "CI/CD", "Terraform", "AI", "Machine Learning"]
    
    return resume_data
```

### Step 4: Generate Strategy and Gap Analysis Report
**Objective:** Compare resume vs LinkedIn to find "silent wins" and tailor to selected mode.

```python
def generate_gap_analysis(linkedin_data, resume_data, strategic_mode):
    """
    Perform gap analysis:
    1. Skills in resume but missing from LinkedIn profile
    2. Projects/achievements in resume not mentioned on LinkedIn
    3. Certifications present in one but not the other
    4. Advanced tech themes (LLM, RPA, cloud) to highlight
    
    Mode-specific recommendations:
    - Get Hired: Map to job descriptions, suggest resume tweaks, "Open to Work" headline
    - Grow Connections: Identify KOLs in user's niche, draft connection requests
    - Influence Market: Build content calendar from GitHub projects & expertise
    """
    
    gaps = {
        "skills_missing_from_linkedin": [],
        "projects_missing_from_linkedin": [],
        "certifications_missing_from_linkedin": [],
        "advanced_tech_themes": []
    }
    
    # Set operations to find differences
    resume_skills = set(resume_data["skills"])
    linkedin_skills = set(linkedin_data["skills"])
    gaps["skills_missing_from_linkedin"] = list(resume_skills - linkedin_skills)
    
    # Identify advanced tech themes
    all_text = str(resume_data) + str(linkedin_data)
    for tech in advanced_techs:
        if tech.lower() in all_text.lower():
            gaps["advanced_tech_themes"].append(tech)
    
    # Generate mode-specific strategy
    strategy = generate_mode_strategy(strategic_mode, gaps, linkedin_data, resume_data)
    
    return {
        "gaps": gaps,
        "strategy": strategy,
        "mode": strategic_mode
    }
```

### Step 5: Generate Strategy Dashboard
**Objective:** Output the final dashboard with score, immediate fixes, and 30-day roadmap.

```python
def generate_dashboard(analysis_report):
    """
    Create Dashboard View with:
    1. Profile Score (0-100) tuned to selected intent
    2. Immediate Fixes (3-5 high-priority changes)
    3. Strategic Roadmap (30-day action plan)
    """
    
    mode = analysis_report["mode"]
    gaps = analysis_report["gaps"]
    
    # Calculate Profile Score
    score = calculate_profile_score(analysis_report)
    
    # Generate Immediate Fixes (3-5 items)
    fixes = []
    if gaps["skills_missing_from_linkedin"]:
        fixes.append(f"Add these skills to LinkedIn: {', '.join(gaps['skills_missing_from_linkedin'][:3])}")
    if gaps["certifications_missing_from_linkedin"]:
        fixes.append(f"Add certification badges: {', '.join(gaps['certifications_missing_from_linkedin'])}")
    # Add 3-5 total fixes based on gaps
    
    # Generate 30-Day Roadmap
    roadmap = generate_roadmap(mode, gaps, analysis_report)
    
    return {
        "profile_score": score,
        "immediate_fixes": fixes[:5],
        "strategic_roadmap": roadmap
    }

def calculate_profile_score(analysis_report):
    """Score 0-100 based on mode and profile completeness"""
    base_score = 50
    
    # Deduct points for gaps
    base_score -= len(analysis_report["gaps"]["skills_missing_from_linkedin"]) * 2
    base_score -= len(analysis_report["gaps"]["projects_missing_from_linkedin"]) * 3
    
    # Bonus for advanced tech themes
    base_score += len(analysis_report["gaps"]["advanced_tech_themes"]) * 5
    
    return max(0, min(100, base_score))

def generate_roadmap(mode, gaps, analysis):
    """30-day action plan specific to mode"""
    if mode == "Get Hired":
        return [
            "Week 1: Update LinkedIn headline with target role keywords",
            "Week 2: Rewrite About section highlighting silent wins from resume",
            "Week 3: Add missing skills and enable 'Open to Work'",
            "Week 4: Apply to 10 jobs matching your tech stack"
        ]
    elif mode == "Grow Connections":
        return [
            "Week 1: Identify 10 KOLs in [user's niche from advanced_tech_themes]",
            "Week 2: Send personalized connection requests (5 per week)",
            "Week 3: Engage with KOL posts daily",
            "Week 4: Share your own insights on trending topics"
        ]
    elif mode == "Influence Market":
        return [
            "Week 1: Create content calendar from GitHub projects",
            "Week 2: Write 2 posts on [advanced_tech_themes]",
            "Week 3: Share case study from resume projects",
            "Week 4: Engage with 20 relevant posts, build thought leadership"
        ]
```

## Output Display
Format the dashboard as a clean UI component:

```python
opal.display(f"""
### 📊 Career Strategy Dashboard
**Mode:** {mode}  
**Profile Score:** {score}/100

#### 🔧 Immediate Fixes
{'\n'.join([f'- {fix}' for fix in fixes])}

#### 🗓️ 30-Day Strategic Roadmap
{'\n'.join([f'{i+1}. {step}' for i, step in enumerate(roadmap)])}

#### 🔍 Gap Analysis Summary
**Skills missing from LinkedIn:** {', '.join(gaps['skills_missing_from_linkedin'])}  
**Advanced Tech Themes Detected:** {', '.join(gaps['advanced_tech_themes'])}
""")
```

## Key Implementation Notes
1. **OCR Libraries:** Use `pytesseract` or Google Cloud Vision API for screenshot text extraction
2. **Resume Parsing:** Use `PyPDF2`/`pdfplumber` for PDFs, `python-docx` for Word files
3. **Error Handling:** If LinkedIn screenshots or resume are missing, request them with clear messages
4. **Tech Detection:** Maintain a list of advanced technologies (LLM, RPA, Docker, Kubernetes, CI/CD, Terraform) and scan both inputs
5. **Mode-Specific Logic:** Each strategic mode should produce distinct outputs—job mapping for Get Hired, KOL lists for Grow Connections, content calendars for Influence Market
6. **Evidence-Based:** Always cite specific extracted data when making recommendations (e.g., "Your resume mentions Docker but LinkedIn doesn't")

## Dependencies
```python
# requirements.txt
pytesseract>=0.3.10
Pillow>=10.0.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
python-docx>=1.0.0
# google-cloud-vision  # Optional for better OCR
```

## Testing Checklist
- [ ] Upload multiple LinkedIn screenshots → extract headline, About, skills
- [ ] Upload PDF resume → parse skills, projects, certifications
- [ ] Select each mode → verify mode-specific roadmap generated
- [ ] Verify gap analysis identifies skills in resume but not LinkedIn
- [ ] Confirm dashboard shows score, 3-5 fixes, 30-day plan
- [ ] Test with advanced tech (LLM, RPA) → ensure detection in output
