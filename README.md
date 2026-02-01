# LinkedIn Strategy Assistant v1.2 (Cloud Run + Flutter)

[![GitHub Release](https://img.shields.io/github/v/release/koreric75/LinkedInStrategyAsst)](https://github.com/koreric75/LinkedInStrategyAsst/releases)
[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://linkedin-strategy-app.storage.googleapis.com/index.html)
[![Cost Dashboard](https://img.shields.io/badge/cost-$0.20-brightgreen)](https://koreric75.github.io/LinkedInStrategyAsst/cost-dashboard.html)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Repository:** https://github.com/koreric75/LinkedInStrategyAsst  
**🚀 Live Application:** https://linkedin-strategy-app.storage.googleapis.com/index.html  
**📊 Interactive Cost Dashboard:** https://koreric75.github.io/LinkedInStrategyAsst/cost-dashboard.html

## 🚀 NEW: Auto-Scraper for Instant Profile Import!

**Stop wasting time manually copying your LinkedIn profile!** Use our auto-scraper to extract all your profile data in **3 seconds**:

1. Copy the [linkedin_scraper.js](linkedin_scraper.js) script
2. Run it on your LinkedIn profile (press F12 → Console → Paste → Enter)
3. Click "Import from Clipboard" in the app - done!

**[📖 Full Scraper Guide →](SCRAPER_README.md)**

## What's New in v1.2

**NEW in v1.2:** LinkedIn Profile Optimizer skill integrated - expert-level recommendations based on recruiter search algorithms and profile best practices. Now includes 5-week detailed strategic roadmaps and enhanced immediate fixes.

**v1.1 Features:** Manual text input for LinkedIn data - no more OCR inaccuracies! Just copy/paste from your profile for 100% fidelity.

## Backend (Python / FastAPI)
- Entry point: [src/app.py](src/app.py) (wraps pipeline logic for text input, OCR, resume parsing, gap analysis)
- **Input methods**: `linkedin_text` (JSON with profile data) OR `screenshots` (images for OCR fallback)
- Run locally: `pip install -r requirements.txt && uvicorn src.app:app --reload`
- Health check: `GET /health`

## Integrations
For detailed information about all external service integrations, see **[INTEGRATIONS.md](INTEGRATIONS.md)**

**Quick Overview**:
- **Google Cloud Run**: Hosts the FastAPI backend service
- **Google Cloud Vision API**: Optional high-fidelity OCR (falls back to pytesseract)
- **Firebase Hosting**: Hosts Flutter web client
- **Firebase Auth**: Optional API authentication
- **AI Agent Skills**: Extensible skill system for enhanced recommendations

## Flutter Client
- Location: [flutter_app/](flutter_app/)
- Config: set `--dart-define API_URL=https://<cloud-run-url>/analyze` when running/building
- **UI Flow (v1.1)**: Fill in LinkedIn text fields OR upload screenshots, upload resume, select mode, submit to backend; displays formatted strategy dashboard
- **Text Input Fields**: Headline, About, Current Role, Skills (comma-separated), Certifications (comma-separated)
- **Screenshots**: Optional for visual engagement assessment
- See [MOBILE_GUIDE.md](flutter_app/MOBILE_GUIDE.md) for Flutter-specific documentation

## Deployment
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.

**Quick Deploy**:
```bash
# Deploy backend to Cloud Run
gcloud builds submit --substitutions=_LOCATION=us-central1

# Deploy Flutter client to Firebase Hosting
cd flutter_app && flutter build web && firebase deploy --only hosting
```

## AI Agent Skills
- Location: [skills/](skills/)
- **LinkedIn Integration**: Integrate LinkedIn with personal life OS systems for career tracking and goal alignment
- **LinkedIn Profile Optimizer**: Expert-level recommendations for headline, About section, skills optimization, and searchability
- Skills enhance strategy generation with domain-specific expertise and best practices
- See [skills/README.md](skills/README.md) for details on available skills

### Managing Skills
Add new skills from external repositories:
```bash
npm install  # First time only
npx skills add <repository-url> --skill <skill-name>
```

List installed skills:
```bash
npx skills list
```

Example:
```bash
npx skills add https://github.com/andrejones92/canifi-life-os --skill linkedin
```

## Quickstart
```bash
# 1. Backend local test
python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt
uvicorn src.app:app --reload

# 2. Build & run container
docker build -t linkedin-backend . && docker run -p 8080:8080 linkedin-backend

# 3. Deploy via Cloud Build
gcloud builds submit --substitutions=_LOCATION=us-central1

# 4. Flutter web dev
cd flutter_app && flutter pub get
flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze
```

## Documentation
- **[🏗️ ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Complete system architecture, component details, and deployment guide
- **[📚 API.md](docs/API.md)** - Comprehensive API reference with examples and error handling
- **[🔧 DEVELOPER_SETUP.md](docs/DEVELOPER_SETUP.md)** - Step-by-step developer environment setup
- **[📊 REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md)** - Summary of recent improvements and refactoring
- **[INTEGRATIONS.md](INTEGRATIONS.md)** - External service integrations guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions and configuration
- **[USER_GUIDE.md](USER_GUIDE.md)** - End-user guide for using the application
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures and validation
- **[SCRAPER_README.md](SCRAPER_README.md)** - Auto-scraper for LinkedIn profile import
- **[QUICKREF.md](QUICKREF.md)** - Quick reference guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- **[FEATURE_ROADMAP.md](FEATURE_ROADMAP.md)** - Future feature plans
- **[COST_ANALYSIS.md](COST_ANALYSIS.md)** - Detailed cost breakdown and optimization
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing to this project

### Additional Resources
- **[docs/](docs/)** - Additional documentation and HTML demos
- **[docs/archive/](docs/archive/)** - Historical documentation from previous releases
- **[skills/README.md](skills/README.md)** - AI agent skills documentation

## Testing checklist
- **v1.1 Text Input**: POST /analyze with `mode`, `linkedin_text` JSON, one resume file; verify `profile_score`, `immediate_fixes`, `strategic_roadmap`
- **OCR Fallback**: POST with screenshots only (no `linkedin_text`); toggle `use_cloud_vision=true` and confirm OCR extraction
- Validate error when missing resume or both LinkedIn data sources
- Run `test_data/test_text_input.py` for text input mode testing
- Run Flutter client against local and Cloud Run endpoints
