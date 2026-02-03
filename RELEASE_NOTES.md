# Release Notes

This document contains the release notes for the current and recent versions of LinkedIn Strategy Assistant.

---

## [1.2.0] - 2026-02-01

**Release Tag:** v1.2.0  
**Previous Version:** v1.1.0

### 🎉 What's New

#### LinkedIn Profile Optimizer Enhancement

v1.2.0 brings **expert-level LinkedIn optimization** to your career strategy! Our new LinkedIn Profile Optimizer skill provides recommendations based on recruiter search algorithms and profile best practices.

### Key Features

#### 1. Enhanced Strategic Roadmaps (5-Week Plans)
- Extended from 4 weeks to **5 weeks** of detailed guidance
- Mode-specific recommendations for Get Hired, Grow Connections, and Influence Market
- Week-by-week actionable tasks with clear milestones

#### 2. Improved Immediate Fixes (Up to 6 Items)
- Increased from 5 to **6 immediate action items**
- More specific, actionable recommendations
- Prioritized based on impact to profile visibility

#### 3. LinkedIn Profile Optimization
- **Headline Optimization**: Formula-based recommendations: `[Role] | [Key Expertise] | [Value Proposition]`
- **About Section**: Structure guidance (1,500-2,000 characters recommended)
- **Skills Maximization**: Guidance to use all 50 LinkedIn skill slots for better searchability
- **Profile Completeness**: Assessment against All-Star and Beyond All-Star criteria
- **Keyword Optimization**: Strategic placement aligned with LinkedIn's search algorithm

### 🚀 Improvements

#### Better Recommendations
- Specific formula-based headline recommendations vs generic "add headline"
- Detailed About section structure (hook, achievements, skills list, CTA)
- Skills recommendations push users to maximize all 50 LinkedIn skill slots
- Keyword placement strategy for better recruiter visibility

#### Enhanced Strategy Generation
- **Get Hired Mode**: Focus on headline, About section, skills, recommendations, and 'Open to Work' setup
- **Grow Connections Mode**: Profile optimization, KOL identification, personalized outreach, content engagement
- **Influence Market Mode**: Portfolio setup, content calendar, tech posts, case studies, analytics

### 📋 Technical Details

#### New Components
- `src/linkedin_optimizer.py` - LinkedIn Profile Optimizer module (10,941 bytes)
- `skills/linkedin-profile-optimizer/SKILL.md` - Skill documentation from https://github.com/paramchoudhary/resumeskills
- Skills directory structure for AI agent skill management

#### Compatibility
- **Backward Compatible**: No breaking changes
- **Graceful Fallback**: If optimizer is unavailable, falls back to original strategy generation
- **No New Dependencies**: Pure Python implementation using existing libraries

#### Testing
- All 27 core tests passing
- New test coverage for optimizer module
- Profile scores now range 80-90 (improved from 70-80)

### 📊 Performance Metrics

| Metric | v1.1.0 | v1.2.0 | Change |
|--------|--------|--------|--------|
| Profile Score (Text) | 70-80 | 80-90 | +10 points |
| Strategic Roadmap | 4 weeks | 5 weeks | +1 week |
| Immediate Fixes | 5 items | 6 items | +1 item |
| Response Time | 5-8s | 4-7s | Faster |

### 🔄 Upgrade Path

#### From v1.1.0
1. Pull latest code from repository
2. No configuration changes required
3. Redeploy backend to Cloud Run
4. Rebuild Flutter client (optional - version only)

#### Deployment Commands
```bash
# Backend deployment
gcloud builds submit --substitutions=_LOCATION=us-central1

# Flutter client (optional)
cd flutter_app && flutter build web && firebase deploy --only hosting
```

### 🎯 Impact

#### For Users
- Better profile optimization recommendations
- More actionable strategies
- Enhanced recruiter visibility guidance
- Clearer roadmap for career growth

#### For Developers
- Extensible skills framework
- Modular optimizer architecture
- Improved code organization
- Better test coverage

### 📝 Notes
- Text input mode remains the recommended method for highest accuracy
- Screenshots mode continues to work as OCR fallback
- All existing features from v1.1.0 are preserved
- No changes to API endpoints or parameters

### 🔗 Resources
- **GitHub Repository**: https://github.com/koreric75/LinkedInStrategyAsst
- **Live Demo**: https://linkedin-strategy-app.storage.googleapis.com/index.html
- **Full Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **User Guide**: [USER_GUIDE.md](USER_GUIDE.md)

---

## [1.1.0] - 2026-01-28

### Added
- **Manual Text Input Feature** - Users can now copy/paste LinkedIn profile data directly into text fields for 100% accuracy
  - Headline text field
  - About section text field (multi-line)
  - Current role text field
  - Skills text field (comma-separated)
  - Certifications text field (comma-separated)
- **Backend `linkedin_text` Parameter** - Accepts JSON string with LinkedIn profile data
- **Hybrid Data Input** - Backend prioritizes text input over OCR; screenshots now optional
- **Test Script for Text Input** - Added `test_data/test_text_input.py` for testing manual input mode
- **Updated Documentation** - All guides updated with v1.1 text input instructions

### Changed
- **Screenshots Now Optional** - Screenshots only required if no text input provided
- **Flutter UI Redesign** - LinkedIn data input section now shows text fields prominently with screenshots as optional
- **Backend API** - `/analyze` endpoint now accepts either `linkedin_text` OR `screenshots` (or both)
- **Error Handling** - Improved validation to require at least one LinkedIn data source
- **Scoring Algorithm** - Balanced penalties to prevent over-penalization from incomplete data (base 70, capped penalties)

### Fixed
- **OCR Data Loss** - OCR extraction was failing, causing profile scores to drop from 75 to 36
- **Data Fidelity** - Text input eliminates OCR inaccuracies and layout parsing issues
- **Score Accuracy** - Profile scores now correctly reflect 70-75 range with proper data

---

## [1.0.0] - 2026-01-27

### Initial Release
- FastAPI backend with OCR-based LinkedIn profile analysis
- Resume parsing (PDF/DOCX support via pdfplumber, python-docx)
- Gap analysis comparing LinkedIn vs resume
- Three strategic modes: Get Hired, Grow Connections, Influence Market
- Profile scoring algorithm (0-100)
- Cloud Vision API integration for OCR
- Flutter web/mobile client with file upload
- Formatted dashboard report with markdown output
- Cloud Run deployment via Cloud Build
- Optional Firebase Authentication
- Test suite with sample data

---

For the complete version history, see [CHANGELOG.md](CHANGELOG.md).

For detailed release documentation, see [docs/archive/](docs/archive/).
