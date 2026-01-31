# API Documentation

## Base URL

**Production:** `https://linkedin-strategy-backend-796550517938.us-central1.run.app`  
**Local Development:** `http://localhost:8080`

## Interactive Documentation

FastAPI provides automatic interactive documentation:
- **Swagger UI:** `http://localhost:8080/docs`
- **ReDoc:** `http://localhost:8080/redoc`

## Authentication

Authentication is optional and configured via Firebase Admin SDK.

**Header:**
```
Authorization: Bearer <firebase-id-token>
```

If Firebase is not configured, authentication is skipped and all requests are allowed.

## Endpoints

### 1. Health Check

Check if the service is running and view service status.

**Endpoint:** `GET /health`

**Response:** `200 OK`

```json
{
  "status": "ok",
  "version": "1.1.0",
  "firebase_enabled": false,
  "vision_api_available": true
}
```

---

### 2. Analyze Profile

Analyze LinkedIn profile and resume to generate career strategy recommendations.

**Endpoint:** `POST /analyze`

**Content-Type:** `multipart/form-data`

#### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `mode` | string | **Yes** | Strategic mode: `"Get Hired"`, `"Grow Connections"`, or `"Influence Market"` |
| `resume` | file | **Yes** | Resume file (PDF, DOCX, DOC, or TXT). Max size: 10MB |
| `linkedin_text` | string | No* | Manual LinkedIn profile data as JSON string (preferred method) |
| `screenshots` | file[] | No* | LinkedIn profile screenshots for OCR (PNG, JPG, JPEG) |
| `use_cloud_vision` | boolean | No | Use Google Cloud Vision API for OCR. Default: `true` |

*Either `linkedin_text` OR `screenshots` must be provided.

#### LinkedIn Text Format (JSON)

When using `linkedin_text` (recommended for accuracy):

```json
{
  "headline": "Senior Software Engineer | Cloud & AI Specialist",
  "about": "Long description of your professional background...",
  "current_role": "Senior Software Engineer at Tech Company",
  "skills": "Python, Docker, Kubernetes, CI/CD, AWS, FastAPI",
  "certifications": "AWS Solutions Architect, Google Cloud Professional"
}
```

**Fields:**
- `headline`: LinkedIn headline (220 chars max)
- `about`: About/Summary section (1500-2600 chars recommended)
- `current_role`: Current job title and company
- `skills`: Comma-separated list of skills
- `certifications`: Comma-separated list of certifications

#### Example Request (cURL)

**With Manual Text Input (Recommended):**

```bash
curl -X POST "http://localhost:8080/analyze" \
  -F "mode=Get Hired" \
  -F "resume=@/path/to/resume.pdf" \
  -F 'linkedin_text={"headline":"Software Engineer | Python & Cloud","about":"Experienced developer...","skills":"Python,Docker,Kubernetes","certifications":"AWS Solutions Architect"}'
```

**With Screenshots (OCR):**

```bash
curl -X POST "http://localhost:8080/analyze" \
  -F "mode=Grow Connections" \
  -F "resume=@/path/to/resume.pdf" \
  -F "screenshots=@/path/to/screenshot1.png" \
  -F "screenshots=@/path/to/screenshot2.png" \
  -F "use_cloud_vision=true"
```

#### Example Request (Python)

```python
import requests
import json

url = "http://localhost:8080/analyze"

# LinkedIn data
linkedin_data = {
    "headline": "Senior Software Engineer | Cloud Specialist",
    "about": "Building scalable cloud-native solutions...",
    "current_role": "Senior Engineer at TechCorp",
    "skills": "Python, Docker, Kubernetes, FastAPI, Cloud Run",
    "certifications": "Google Cloud Professional, AWS Solutions Architect"
}

# Files
files = {
    "resume": ("resume.pdf", open("resume.pdf", "rb"), "application/pdf")
}

# Form data
data = {
    "mode": "Get Hired",
    "linkedin_text": json.dumps(linkedin_data)
}

# Send request
response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print(f"Profile Score: {result['profile_score']}/100")
    print("\nImmediate Fixes:")
    for fix in result['immediate_fixes']:
        print(f"  - {fix}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
```

#### Response

**Success:** `200 OK`

```json
{
  "mode": "Get Hired",
  "profile_score": 78,
  "immediate_fixes": [
    "Add skills to LinkedIn: Terraform, RPA, Machine Learning",
    "Add certifications to LinkedIn: CompTIA Security+",
    "Write compelling About section (1,500+ chars) with hook, achievements, skills list"
  ],
  "strategic_roadmap": [
    "Week 1: Optimize headline with target role + key skills + value proposition",
    "Week 2: Write compelling About section (1,500+ chars) with hook, achievements, skills list",
    "Week 3: Add all missing skills and certifications (aim for 50 total skills)",
    "Week 4: Add rich media to Experience section and request 5 recommendations"
  ],
  "gaps": {
    "skills_missing_from_linkedin": ["terraform", "machine learning", "rpa"],
    "projects_missing_from_linkedin": ["linkedin strategy assistant"],
    "certifications_missing_from_linkedin": ["comptia security+"],
    "advanced_tech_themes": ["Docker", "Kubernetes", "LLM", "CI/CD", "Cloud Run"]
  },
  "dashboard_markdown": "# 📊 LinkedIn Strategy Dashboard - Get Hired\n\n..."
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `mode` | string | Selected strategic mode |
| `profile_score` | integer | Overall profile score (0-100) |
| `immediate_fixes` | string[] | Top 5-6 actionable improvements |
| `strategic_roadmap` | string[] | 4-5 week strategic plan |
| `gaps` | object | Detailed gap analysis |
| `gaps.skills_missing_from_linkedin` | string[] | Skills in resume but not on LinkedIn |
| `gaps.projects_missing_from_linkedin` | string[] | Projects/achievements missing |
| `gaps.certifications_missing_from_linkedin` | string[] | Certifications missing |
| `gaps.advanced_tech_themes` | string[] | Detected advanced technologies |
| `dashboard_markdown` | string | Formatted markdown report |

#### Error Responses

**400 Bad Request** - Invalid input

```json
{
  "detail": "Must provide either linkedin_text or screenshots"
}
```

**400 Bad Request** - Invalid file format

```json
{
  "detail": "Unsupported resume format: .exe. Allowed: ['.pdf', '.docx', '.doc', '.txt']"
}
```

**400 Bad Request** - File too large

```json
{
  "detail": "Resume file too large. Max size: 10485760 bytes"
}
```

**422 Validation Error** - Invalid mode

```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "mode"],
      "msg": "String should match pattern '^(Get Hired|Grow Connections|Influence Market)$'",
      "input": "Invalid Mode"
    }
  ]
}
```

**500 Internal Server Error** - Processing failure

```json
{
  "detail": "Internal server error: ..."
}
```

## Strategic Modes

### Get Hired

**Focus:** Job search optimization and recruiter visibility

**Strategy Includes:**
- Headline optimization for target roles
- Skills alignment with job descriptions
- "Open to Work" setup guidance
- Application tracking recommendations

**Best For:**
- Active job seekers
- Career changers
- Recent graduates

---

### Grow Connections

**Focus:** Network expansion and relationship building

**Strategy Includes:**
- KOL (Key Opinion Leader) identification
- Engagement tactics
- Personalized connection requests
- Community participation

**Best For:**
- Building professional network
- Industry relationships
- Thought leadership preparation

---

### Influence Market

**Focus:** Thought leadership and personal brand building

**Strategy Includes:**
- Content calendar creation
- Tech theme-based posting
- Case study development
- Engagement analytics

**Best For:**
- Industry experts
- Content creators
- Consultants and freelancers
- Building personal brand

## Rate Limiting

Currently, no rate limiting is enforced. For production use, consider implementing:
- Per-IP rate limits
- Per-user rate limits (if authenticated)
- Burst protection

## Data Privacy

- **No Persistent Storage:** Uploaded files are processed in memory and temporary directories
- **Automatic Cleanup:** Temporary files deleted after request completion
- **No Logging of Sensitive Data:** Personal information not logged
- **Stateless:** No session data stored

## Performance Tips

### For Best Performance:

1. **Use Manual Text Input** instead of screenshots
   - 2-3x faster processing
   - Higher accuracy
   - No OCR overhead

2. **Optimize File Sizes:**
   - Compress PDFs before upload
   - Use TXT format when possible
   - Limit screenshot resolution

3. **Use Cloud Vision API:**
   - Set `use_cloud_vision=true`
   - Much better OCR accuracy
   - Faster than Tesseract

## Error Handling Best Practices

```python
import requests

def analyze_profile(linkedin_data, resume_path, mode="Get Hired"):
    """Analyze LinkedIn profile with error handling."""
    url = "http://localhost:8080/analyze"
    
    try:
        with open(resume_path, 'rb') as resume_file:
            files = {'resume': resume_file}
            data = {
                'mode': mode,
                'linkedin_text': json.dumps(linkedin_data)
            }
            
            response = requests.post(url, files=files, data=data, timeout=30)
            response.raise_for_status()
            
            return response.json()
    
    except requests.exceptions.Timeout:
        print("Request timed out. Try again.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(f"Details: {e.response.json().get('detail')}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except FileNotFoundError:
        print(f"Resume file not found: {resume_path}")
    
    return None
```

## Changelog

### v1.1.0 (Current)
- Added manual text input support
- Enhanced LinkedIn Profile Optimizer integration
- Improved error handling and validation
- Added comprehensive logging
- Configuration management system

### v1.0.0
- Initial release
- Screenshot OCR support
- Resume parsing (PDF, DOCX, TXT)
- Three strategic modes
- Gap analysis engine

---

**Questions or Issues?**  
Please file an issue on [GitHub](https://github.com/koreric75/LinkedInStrategyAsst/issues).
