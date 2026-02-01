# Changelog

All notable changes to LinkedIn Strategy Assistant will be documented in this file.

## [1.2.0] - 2026-02-01

### Added
- **LinkedIn Profile Optimizer Skill Integration** - Enhanced recommendations based on expert-level LinkedIn optimization best practices
  - Added `skills/linkedin-profile-optimizer/SKILL.md` from https://github.com/paramchoudhary/resumeskills
  - New `src/linkedin_optimizer.py` module with optimization logic
  - Headline optimization tips with formula: [Role] | [Key Expertise] | [Value Proposition]
  - About section optimization with structure guidance (1,500-2,000 characters recommended)
  - Skills optimization (aim for all 50 LinkedIn skill slots)
  - Profile completeness assessment (All-Star and Beyond criteria)
  - Keyword optimization strategies for recruiter searchability
- **Enhanced Strategy Generation** - Mode-specific roadmaps now include 5-week detailed plans
  - Get Hired mode: Focus on headline, About section, skills, recommendations, and 'Open to Work' setup
  - Grow Connections mode: Profile optimization, KOL identification, personalized outreach, content engagement
  - Influence Market mode: Portfolio setup, content calendar, tech posts, case studies, analytics
- **Skills Directory Structure** - Added `/skills` directory for AI agent skill management
  - Skills README with usage documentation
  - Extensible framework for adding more optimization skills

### Changed
- **Immediate Fixes** - Now up to 6 fixes (was 5) with more specific, actionable recommendations
- **Strategic Roadmap** - Extended to 5 weeks (was 4) with more granular week-by-week guidance
- **Pipeline Integration** - `generate_strategy()` function now uses enhanced optimizer with fallback to original
- **Documentation** - Updated README.md with LinkedIn Profile Optimizer feature highlight

### Technical Details
- New dependency: None (pure Python implementation using existing libraries)
- Module: `src/linkedin_optimizer.py` (10,941 bytes)
- Skill file: `skills/linkedin-profile-optimizer/SKILL.md` (10,171 bytes from source)
- Integration: Backward compatible with graceful fallback if optimizer unavailable
- Test coverage: Added `test_data/test_optimizer.py` for module validation

### Impact
- **Better Headline Guidance**: Specific formula-based recommendations vs generic "add headline"
- **About Section Structure**: Detailed guidance on hook, achievements, skills list, and CTA
- **Skills Maximization**: Pushes users to use all 50 LinkedIn skill slots for better searchability
- **Recruiter Visibility**: Keyword placement strategy aligned with LinkedIn's search algorithm
- **Profile Completeness**: Assessment against All-Star and Beyond All-Star criteria

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

### Technical Details
- Backend revision: `linkedin-strategy-backend-00004-5zd`
- Deployed to: `https://linkedin-strategy-backend-796550517938.us-central1.run.app`
- Flutter UI: Added 5 TextEditingController fields with dispose() cleanup
- API change: `screenshots` parameter changed from required to optional
- Pipeline: Maintains `LinkedInProfile` dataclass structure for both input methods

### Migration Notes
- **API Compatibility**: Existing screenshot-based requests still work (backwards compatible)
- **Recommended**: Switch to text input mode for highest accuracy
- **Testing**: Use `test_text_input.py` for text mode, `test_api.py` for screenshot mode

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

### Features
- OCR extraction from LinkedIn screenshots (pytesseract local, Cloud Vision remote)
- Advanced tech detection (LLM, RPA, Docker, Kubernetes, CI/CD, etc.)
- Mode-specific immediate fixes and 30-day strategic roadmaps
- Content-rich dashboard with emojis, tables, progress indicators
- Multi-platform Flutter support (web, Android, iOS)
