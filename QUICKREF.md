# LinkedIn Strategy Assistant v1.2 - Quick Reference

## 🚀 Deployment Info
**Service URL:** https://linkedin-strategy-backend-796550517938.us-central1.run.app  
**Revision:** Will be updated after v1.2.0 deployment  
**Status:** ✅ Production Ready  
**Last Updated:** February 1, 2026

---

## 📊 API Endpoint

### POST /analyze

#### Text Input Mode (Recommended - v1.1+)
```bash
curl -X POST https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze \
  -F "mode=Get Hired" \
  -F "resume=@resume.pdf" \
  -F 'linkedin_text={"headline":"Senior Engineer","about":"...","current_role":"...","skills":"Python, Docker","certifications":"CompTIA Security+"}'
```

#### Screenshot Mode (Fallback)
```bash
curl -X POST https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze \
  -F "mode=Get Hired" \
  -F "resume=@resume.pdf" \
  -F "screenshots=@screenshot1.png" \
  -F "use_cloud_vision=true"
```

---

## 🎯 Strategic Modes
1. **Get Hired** - Job search optimization, resume tweaks, "Open to Work" strategies
2. **Grow Connections** - Network expansion, KOL targeting, personalized outreach
3. **Influence Market** - Thought leadership, content calendar, market positioning

---

## 📋 Input Requirements

### Required
- ✅ Resume (PDF or DOC)
- ✅ LinkedIn Data (text OR screenshots)
- ✅ Mode selection

### LinkedIn Text Format (JSON)
```json
{
  "headline": "Senior Software Engineer | Cloud & AI",
  "about": "I help organizations transform...",
  "current_role": "Software Engineer at Tech Company",
  "skills": "Python, Docker, Kubernetes, Cloud Run, CI/CD",
  "certifications": "CompTIA Security+, Google Cloud Professional"
}
```

---

## 📤 Response Format
```json
{
  "mode": "Get Hired",
  "profile_score": 80,
  "immediate_fixes": [
    "Add skills to LinkedIn: Docker, CI/CD",
    "Show certifications: CompTIA Security+"
  ],
  "strategic_roadmap": [
    "Week 1: Update headline with target role",
    "Week 2: Add missing skills and certifications",
    "Week 3: Publish project summary",
    "Week 4: Apply to 10 matching roles"
  ],
  "gaps": {
    "skills_missing_from_linkedin": ["docker", "ci/cd"],
    "certifications_missing_from_linkedin": ["comptia security+"],
    "projects_missing_from_linkedin": [],
    "advanced_tech_themes": ["docker", "cloud run", "ai", "llm"]
  },
  "dashboard_markdown": "# 📊 LinkedIn Strategy Dashboard..."
}
```

---

## 🧪 Test Commands

### Text Input Test
```bash
cd test_data
python test_text_input.py
# Expected: Profile score 70-100
```

### Screenshot Test
```bash
cd test_data
python test_api.py
# Expected: Profile score varies (OCR dependent)
```

### Flutter App Test
```bash
cd flutter_app
flutter run -d chrome
# Fill text fields → upload resume → analyze
```

---

## 📊 Performance Benchmarks

| Metric | Target | Actual (v1.2) |
|--------|--------|---------------|
| Profile Score (Text) | 70-100 | 80-90 ✅ |
| Profile Score (OCR) | 50-70 | 40-65 ⚠️ OCR inherently lossy |
| Response Time | <10s | 4-7s ✅ |
| Data Accuracy (Text) | 100% | 100% ✅ |
| Data Accuracy (OCR) | 70% | 30-50% ⚠️ OCR limitations |
| Strategic Roadmap | 4-5 weeks | 5 weeks ✅ |
| Immediate Fixes | 5-6 items | 6 items ✅ |

**Recommendation:** Use text input mode for production use.

---

## 🔍 Common Issues

### Low Profile Score (<50)
- **Cause:** OCR failed to extract LinkedIn data
- **Solution:** Use text input mode instead of screenshots

### Missing Skills/Certifications
- **Cause:** OCR parsing errors or data not in resume
- **Solution:** Verify resume contains all skills, use text input

### Error: "Must provide either linkedin_text or screenshots"
- **Cause:** Both linkedin_text and screenshots missing
- **Solution:** Provide at least one LinkedIn data source

---

## 📚 Documentation Files

- [README.md](README.md) - Architecture overview
- [USER_GUIDE.md](USER_GUIDE.md) - End-user instructions
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing procedures
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Cloud Run deployment
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [VERSION_1.1.md](VERSION_1.1.md) - Full v1.1 documentation
- [RELEASE_v1.1.md](RELEASE_v1.1.md) - Release summary
- [DEPLOYMENT_STATUS_v1.1.md](DEPLOYMENT_STATUS_v1.1.md) - Deployment status

---

## 🛠️ Tech Stack
- **Backend:** Python 3.11, FastAPI, Cloud Run
- **Frontend:** Flutter (Web, Android, iOS)
- **OCR:** Google Cloud Vision API, pytesseract
- **Parsing:** pdfplumber, python-docx
- **Infrastructure:** Cloud Build, Container Registry, Cloud Run

---

## 📞 Support
- **Issues:** Open GitHub issue with [BUG] or [FEATURE] tag
- **Questions:** Check USER_GUIDE.md first
- **Updates:** Follow CHANGELOG.md for new releases

---

**Version:** 1.2.0  
**Released:** February 1, 2026  
**Status:** ✅ Production Ready
