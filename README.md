# LinkedIn Strategy Assistant v1.1 (Cloud Run + Flutter)

**NEW in v1.1:** Manual text input for LinkedIn data - no more OCR inaccuracies! Just copy/paste from your profile for 100% fidelity.

## Backend (Python / FastAPI)
- Entry point: [src/app.py](src/app.py) (wraps pipeline logic for text input, OCR, resume parsing, gap analysis)
- **Input methods**: `linkedin_text` (JSON with profile data) OR `screenshots` (images for OCR fallback)
- Run locally: `pip install -r requirements.txt && uvicorn src.app:app --reload`
- Cloud Vision OCR: set `use_cloud_vision=true` form field; requires Vision API enabled and service account creds
- Health: `GET /health`

## Container & Deployment
- Dockerfile builds Python 3.11 + tesseract fallback; runs `uvicorn src.app:app --host 0.0.0.0 --port 8080`
- Cloud Build: [cloudbuild.yaml](cloudbuild.yaml) builds/pushes image and deploys to Cloud Run (`$LOCATION` region)
- Cloud Run runtime env:
  - `VISION_USE_AUTH=true` (example flag if you gate Vision usage)
  - Service account needs `roles/run.invoker`, `roles/storage.objectAdmin` (if using GCS), `roles/vision.user` (for Vision)

## Google Cloud Services
- **Cloud Vision API**: higher fidelity OCR for LinkedIn screenshots; enable API and provide service account key (or Workload Identity)
- **Cloud Storage**: optional persistent storage for uploads; replace temp file writes with GCS uploads if needed
- **Cloud Run**: hosts the FastAPI service
- **Firebase Auth (optional)**: protect the API; add ID token verification middleware in FastAPI

## Flutter Client
- Location: [flutter_app/](flutter_app/)
- Config: set `--dart-define API_URL=https://<cloud-run-url>/analyze` when running/building
- **UI Flow (v1.1)**: Fill in LinkedIn text fields OR upload screenshots, upload resume, select mode, submit to backend; displays formatted strategy dashboard
- **Text Input Fields**: Headline, About, Current Role, Skills (comma-separated), Certifications (comma-separated)
- **Screenshots**: Optional for visual engagement assessment

## Quickstart
1. Backend local test: `python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt && uvicorn src.app:app --reload`
2. Build & run container: `docker build -t linkedin-backend . && docker run -p 8080:8080 linkedin-backend`
3. Deploy via Cloud Build: `gcloud builds submit --substitutions=_LOCATION=us-central1`
4. Flutter web dev: `cd flutter_app && flutter pub get && flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze`

## Testing checklist
- **v1.1 Text Input**: POST /analyze with `mode`, `linkedin_text` JSON, one resume file; verify `profile_score`, `immediate_fixes`, `strategic_roadmap`
- **OCR Fallback**: POST with screenshots only (no `linkedin_text`); toggle `use_cloud_vision=true` and confirm OCR extraction
- Validate error when missing resume or both LinkedIn data sources
- Run `test_data/test_text_input.py` for text input mode testing
- Run Flutter client against local and Cloud Run endpoints
