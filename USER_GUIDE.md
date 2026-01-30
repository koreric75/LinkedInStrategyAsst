# LinkedIn Strategy Assistant - User Guide (v1.1)

## NEW in v1.1: Text Input Mode

For **highest accuracy**, simply copy/paste your LinkedIn profile data into text fields - no screenshots needed! This eliminates OCR errors and gives you perfect gap analysis.

## How to Use the App

### What You Need

1. **Your Resume** (PDF or Word format)
   - Should include your skills, projects, certifications, and work experience
   
2. **LinkedIn Profile Data** (Choose ONE method):
   
   **Method A: Manual Text Input (Recommended for Accuracy)**
   - Copy your LinkedIn headline
   - Copy your "About" section text
   - Copy your current role
   - List your skills (comma-separated)
   - List your certifications (comma-separated)
   
   **Method B: Screenshots (Optional - for Visual Assessment)**
   - Screenshot of your LinkedIn headline
   - Screenshot of your "About" section
   - Screenshot of your Skills section
   - Screenshot of any recent activity/posts (optional)

3. **Choose Your Goal** (Strategic Mode):
   - **Get Hired** - Optimize for job applications
   - **Grow Connections** - Build your professional network
   - **Influence Market** - Establish thought leadership

### Method 1: Using the Web API (No Installation Required)

#### Step 1: Prepare Your Data
Have your resume file ready and copy your LinkedIn profile data.

#### Step 2: Make an API Request

**Using PowerShell (v1.1 Text Input - Recommended):**
```powershell
# Replace these with your actual data
$resumePath = "C:\Users\YourName\Documents\resume.pdf"

$linkedinData = @{
    headline = "Senior Software Engineer | Cloud & AI"
    about = "I help organizations transform through cloud-native solutions..."
    current_role = "Software Engineer at Tech Company"
    skills = "Python, Docker, Kubernetes, Cloud Run, CI/CD"
    certifications = "CompTIA Security+, Google Cloud Professional"
} | ConvertTo-Json

$form = @{
    mode = "Get Hired"  # Or "Grow Connections" or "Influence Market"
    resume = Get-Item -Path $resumePath
    linkedin_text = $linkedinData
}

$response = Invoke-WebRequest -Uri "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze" -Method Post -Form $form -UseBasicParsing
$result = $response.Content | ConvertFrom-Json
$result.dashboard_markdown
```

**Using PowerShell (Screenshots Fallback):**
```powershell
# Replace these paths with your actual file locations
$resumePath = "C:\Users\YourName\Documents\resume.pdf"
$screenshot1 = "C:\Users\YourName\Pictures\linkedin-headline.png"
$screenshot2 = "C:\Users\YourName\Pictures\linkedin-about.png"

$form = @{
    mode = "Get Hired"  # Or "Grow Connections" or "Influence Market"
    resume = Get-Item -Path $resumePath
    screenshots = @(
        Get-Item -Path $screenshot1
        Get-Item -Path $screenshot2
    )
    use_cloud_vision = "true"
}

$response = Invoke-WebRequest -Uri "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze" -Method Post -Form $form -UseBasicParsing
$result = $response.Content | ConvertFrom-Json
$result.dashboard_markdown
```

**Using Postman:**
1. Open Postman
2. Create a new POST request to: `https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze`
3. Go to "Body" → select "form-data"
4. Add fields:
   - `mode` (text): `Get Hired`
   - `resume` (file): Select your resume PDF
   - `screenshots` (file): Select first screenshot
   - `screenshots` (file): Select second screenshot (add more as needed)
   - `use_cloud_vision` (text): `false`
5. Click "Send"

### What You'll Get Back

The app returns a **Career Strategy Dashboard** with:

#### 1. Profile Score (0-100)
- Tailored to your selected mode
- Shows how well your LinkedIn profile aligns with your resume

#### 2. Immediate Fixes (3-5 action items)
Examples:
- "Add these skills to LinkedIn: Docker, CI/CD, LLM integration"
- "Add certification badges: CompTIA Security+"
- "Populate About section with top projects and outcomes"

#### 3. 30-Day Strategic Roadmap
Based on your mode:

**Get Hired:**
- Week 1: Update headline with target role keywords
- Week 2: Add missing skills and certifications to LinkedIn
- Week 3: Publish one project summary highlighting outcomes
- Week 4: Apply to 10 roles matching your tech stack

**Grow Connections:**
- Week 1: Identify 10 KOLs in your niche
- Week 2: Send 5 personalized connection requests
- Week 3: Comment daily on KOL posts with specific insights
- Week 4: Host a short post summarizing a project lesson

**Influence Market:**
- Week 1: Draft content calendar from recent projects
- Week 2: Publish 2 posts on your advanced tech themes
- Week 3: Share a case study with metrics
- Week 4: Run a poll and synthesize learnings

#### 4. Gap Analysis Summary
Shows what's missing:
- Skills in resume but not on LinkedIn
- Projects/achievements not mentioned on LinkedIn
- Certifications present in resume but not shown on LinkedIn
- Advanced tech themes detected (LLM, RPA, Docker, Kubernetes, etc.)

### Method 2: Using Flutter Web Client (Optional)

If you have Flutter SDK installed:

```powershell
cd C:\Users\korer\LinkedInStrategyAsst\flutter_app
flutter pub get
flutter run -d chrome --dart-define API_URL=https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze
```

This opens a web UI where you can:
1. Upload screenshots using file picker
2. Upload resume
3. Select strategic mode from dropdown
4. Click "Generate Strategy"
5. View results in the browser

### Tips for Best Results

1. **Resume Quality:**
   - Include specific technologies (Docker, Kubernetes, CI/CD, LLM, RPA)
   - List certifications with full names
   - Describe projects with technical details

2. **LinkedIn Screenshots:**
   - Take clear, full-screen screenshots
   - Include all visible skills
   - Capture your complete "About" section
   - For better OCR, use `use_cloud_vision=true` (requires Cloud Vision API enabled)

3. **Choose the Right Mode:**
   - **Get Hired**: Best if actively job searching
   - **Grow Connections**: Best for career networking
   - **Influence Market**: Best for establishing authority

### Example Output

```json
{
  "mode": "Get Hired",
  "profile_score": 72,
  "immediate_fixes": [
    "Add skills to LinkedIn: docker, kubernetes, ci/cd",
    "Show certifications on LinkedIn: CompTIA Security+",
    "Populate About section with top projects and outcomes"
  ],
  "strategic_roadmap": [
    "Week 1: Update headline with target role and key skills",
    "Week 2: Add missing skills and certifications to LinkedIn",
    "Week 3: Publish one project summary highlighting outcomes",
    "Week 4: Apply to 10 roles matching stack and location"
  ],
  "gaps": {
    "skills_missing_from_linkedin": ["docker", "kubernetes", "ci/cd"],
    "projects_missing_from_linkedin": [],
    "certifications_missing_from_linkedin": ["comptia security+"],
    "advanced_tech_themes": ["Docker", "Kubernetes", "CI/CD", "LLM"]
  }
}
```

### Troubleshooting

**"No results" or empty gaps:**
- Ensure screenshots are clear and readable
- Check that resume has technical skills listed
- Try `use_cloud_vision=true` for better OCR

**API errors:**
- Verify file formats (PDF/DOCX for resume, PNG/JPG for screenshots)
- Ensure mode is exactly: "Get Hired", "Grow Connections", or "Influence Market"
- Check file sizes (Cloud Run has upload limits)

**Need help?**
- Health check: https://linkedin-strategy-backend-796550517938.us-central1.run.app/health
- Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for technical details
