# LinkedIn Strategy Assistant - AI Agent Instructions

## Architecture Overview
This is a FastAPI + Flutter hybrid app that performs **manual text input** or OCR-based LinkedIn profile analysis and resume parsing to generate career growth strategies. The core prompt defining the AI strategist's behavior lives in [Untitled-1.md](../Untitled-1.md).

**Stack**: Python 3.11 FastAPI backend (Cloud Run) + Flutter web/mobile client + Google Cloud Vision (optional OCR upgrade)

**Data flow**:
1. User provides LinkedIn data via **text fields** (headline, about, skills, certifications) OR screenshots (JPEG/PNG) + resume (PDF/DOCX/TXT) via Flutter UI or direct API
2. Backend prioritizes text input over OCR for higher fidelity; falls back to Cloud Vision/tesseract for screenshots
3. Pipeline in [src/pipeline.py](../src/pipeline.py) performs gap analysis comparing LinkedIn vs resume content
4. Generates mode-specific strategy (Get Hired | Grow Connections | Influence Market)
5. Returns JSON dashboard: `profile_score`, `immediate_fixes`, `strategic_roadmap`

## File Structure & Responsibilities
- `src/app.py`: FastAPI entry point; handles multipart file uploads, optional Firebase auth, CORS for web client
- `src/pipeline.py`: Core logic—OCR extraction (headline/about/skills), resume parsing, gap detection, strategy generation
- `flutter_app/lib/main.dart`: Mobile UI with file pickers (ImagePicker for camera, FilePicker for resume/gallery)
- `cloudbuild.yaml`: Builds Docker image → deploys to Cloud Run (region=us-central1, service=linkedin-strategy-backend)
- `test_data/test_api.py`: Python script for POST /analyze tests against dev/prod endpoints

## Dev Workflows
**Local backend**:
```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app:app --reload  # runs on http://localhost:8000
```

**Docker build/test**:
```bash
docker build -t linkedin-backend .
docker run -p 8080:8080 linkedin-backend
```

**Deploy to Cloud Run**: `gcloud builds submit` (uses cloudbuild.yaml; requires GCP project 'linkedin-strategy-ai-assistant')

**Flutter client**:
```bash
cd flutter_app && flutter pub get
flutter run -d chrome --dart-define API_URL=http://localhost:8000/analyze
```

## Critical Conventions
- **Mode validation**: The `/analyze` endpoint enforces exact match for `mode` param: `"Get Hired"`, `"Grow Connections"`, or `"Influence Market"` (no typos, case-sensitive)
- **Data input methods**: Backend accepts `linkedin_text` (JSON with headline/about/skills/certifications) OR `screenshots` (multipart files). Text input is prioritized for accuracy.
- **LinkedIn text format**: JSON string with keys: `headline`, `about`, `current_role`, `skills` (comma-separated), `certifications` (comma-separated)
- **Tech detection**: `ADVANCED_TECH_TERMS` in pipeline.py (line 28) defines terms used for gap analysis—update this list to detect new tech (e.g., add "Kubernetes", "Terraform")
- **OCR fallback**: Local mode uses pytesseract; Cloud Vision requires `use_cloud_vision=true` form field + Vision API enabled + service account creds
- **Testing**: Always test with `test_data/test_text_input.py` for text input or `test_api.py` for screenshots; includes sample resume/screenshot files
- **Firebase auth**: Optional—only enabled if `firebase-adminsdk.json` exists in root; enforced via `verify_firebase_token` dependency in app.py

## Integration Points
- **Google Cloud Vision API**: Higher fidelity OCR for screenshots; needs `roles/vision.user` IAM permission
- **Cloud Storage**: Not implemented yet—temp file storage in memory/tmpdir; see pipeline.py line 80 for upload handling
- **Firebase Auth**: Optional token verification via `Authorization: Bearer <token>` header; skipped if Firebase not initialized

## Common Tasks
**Add new strategic advice for a mode**: Edit `generate_strategy()` in pipeline.py (line 289); each mode has a distinct scoring/recommendation template

**Enable Cloud Vision locally**: Set env var `GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json`, then pass `use_cloud_vision=true` in API request

**Update Flutter API URL**: Pass `--dart-define API_URL=<new-url>` to flutter run/build commands

**Add new resume format support**: Install parser library in requirements.txt, then extend `parse_resume()` function in pipeline.py (line 218)

## Testing Checklist
- POST /analyze with all 3 modes + verify distinct `immediate_fixes` per mode
- Test with `use_cloud_vision=true` vs `false` and confirm OCR quality difference
- Validate error handling: missing resume, missing screenshots, invalid mode string
- Run Flutter client against local (port 8000) and Cloud Run endpoints

---

## AI Strategist Behavior (from Untitled-1.md)
When implementing new features or modifying the analysis logic, preserve these core behaviors:
- Perform gap analysis between resume and LinkedIn to surface "silent wins" (skills/projects present in one but missing in the other)
- Detect advanced tech themes (LLM integration, RPA, cloud-native development) to avoid generic advice
- Map experience to specific job descriptions for Get Hired mode
- Identify niche KOLs for Grow Connections mode
- Build content calendars grounded in GitHub projects for Influence Market mode
- Always tailor recommendations to detected technologies and domains
