# LinkedIn Strategy Assistant - Integrations

This document provides a comprehensive overview of all external service integrations used by the LinkedIn Strategy Assistant.

## Architecture Overview

The LinkedIn Strategy Assistant is a hybrid application consisting of:
- **Backend**: Python FastAPI service deployed on Google Cloud Run
- **Frontend**: Flutter web/mobile client
- **Skills System**: Node.js CLI for managing AI agent skills

## Google Cloud Platform Integrations

### 1. Cloud Run (Required)

**Purpose**: Hosts the FastAPI backend service

**Configuration**:
- Service name: `linkedin-strategy-backend`
- Region: `us-central1` (configurable via `_LOCATION` substitution)
- Port: `8080`
- Authentication: Public (--allow-unauthenticated)

**Deployment**:
```bash
gcloud builds submit --substitutions=_LOCATION=us-central1
```

**Environment Variables**:
- `VISION_USE_AUTH=true` - Example flag for gating Vision API usage
- `PORT` - Runtime port (default: 8080)

**Required IAM Roles**:
- `roles/run.invoker` - For service invocation

**Files**:
- `cloudbuild.yaml` - Build and deployment configuration
- `Dockerfile` - Container image definition

### 2. Cloud Vision API (Optional)

**Purpose**: High-fidelity OCR for LinkedIn profile screenshots

**Status**: Optional - Falls back to pytesseract if not enabled

**Configuration**:
- Enabled via `use_cloud_vision=true` form field in API requests
- Requires Vision API enabled in GCP project
- Uses Application Default Credentials or service account key

**Required IAM Roles**:
- `roles/vision.user` - For Vision API access

**Code Reference**: `src/app.py` - `_extract_linkedin` function for Cloud Vision integration

**Fallback**: Local pytesseract OCR when Cloud Vision is unavailable

### 3. Cloud Storage (Planned)

**Purpose**: Persistent storage for uploaded files

**Status**: Not yet implemented

**Current Implementation**: Uses temporary in-memory/tmpdir storage

**Planned Enhancement**: Replace temp file handling with GCS uploads

**Required IAM Roles (when implemented)**:
- `roles/storage.objectAdmin` - For object read/write operations

**Code Reference**: `src/app.py` - temporary file handling in `analyze` endpoint

### 4. Cloud Build (Required for Deployment)

**Purpose**: Automated container builds and Cloud Run deployments

**Configuration**:
- Builds Docker image from repository
- Pushes to Container Registry
- Deploys to Cloud Run

**Files**: `cloudbuild.yaml`

## Firebase Integrations

### 1. Firebase Hosting (Active)

**Purpose**: Hosts the Flutter web client

**Configuration**:
```json
{
  "hosting": {
    "public": "flutter_app/build/web",
    "rewrites": [{"source": "**", "destination": "/index.html"}]
  }
}
```

**Deployment**:
```bash
cd flutter_app
flutter build web
firebase deploy --only hosting
```

**Files**:
- `firebase.json` - Hosting configuration
- `.firebaserc` - Project configuration (project: `linkedin-strategy-ai-assistant`)

### 2. Firebase Authentication (Optional)

**Purpose**: Optional API authentication via Firebase ID tokens

**Status**: Optional - Only enabled if `firebase-adminsdk.json` exists

**Implementation**:
- Token verification in FastAPI via `verify_firebase_token` dependency
- Authorization header: `Bearer <firebase-id-token>`
- Gracefully disabled if Firebase not configured

**Code Reference**: `src/app.py` - `verify_firebase_token` function and Firebase initialization

**Required Package**: `firebase-admin>=6.5.0`

## Flutter Client Integration

### Configuration

**API Endpoint**: Configured via Dart defines at build/run time
```bash
flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze
```

**Dependencies**:
- `http: ^1.2.0` - HTTP client for API calls
- `file_picker: ^6.1.1` - Resume file selection
- `image_picker: ^1.0.7` - Screenshot/camera capture
- `url_launcher: ^6.2.0` - External link handling

**Data Flow**:
1. User inputs LinkedIn data (text or screenshots) + resume
2. Client sends multipart POST to `/analyze` endpoint
3. Backend processes and returns JSON strategy
4. Client displays formatted dashboard

**Code Reference**: `flutter_app/lib/main.dart`

## AI Agent Skills System

### Overview

Custom skills extend the AI agent's capabilities with domain-specific expertise.

**Implementation**: Node.js CLI tool for managing skills

**Installation**:
```bash
npm install  # Install CLI dependencies
npx skills add <repository-url> --skill <skill-name>
```

### Installed Skills

#### 1. LinkedIn Integration
- **Source**: https://github.com/andrejones92/canifi-life-os
- **Location**: `skills/linkedin/`
- **Purpose**: Integrate LinkedIn with personal life OS systems

#### 2. LinkedIn Profile Optimizer
- **Source**: https://github.com/paramchoudhary/resumeskills
- **Location**: `skills/linkedin-profile-optimizer/`
- **Purpose**: Expert profile optimization recommendations

### Skills CLI

**Commands**:
```bash
npx skills list          # List installed skills
npx skills add <url>     # Add new skill
```

**Files**:
- `package.json` - NPM package configuration with CLI bindings
- `scripts/skills-cli.js` - CLI implementation
- `skills/README.md` - Skills documentation

## Third-Party Libraries

### Python Backend

**OCR & Document Processing**:
- `pytesseract>=0.3.10` - Local OCR fallback
- `Pillow>=10.0.0` - Image processing
- `pdfplumber>=0.10.0` - PDF resume parsing
- `python-docx>=1.0.0` - Word document parsing

**Web Framework**:
- `fastapi>=0.110.0` - API framework
- `uvicorn[standard]>=0.29.0` - ASGI server
- `python-multipart>=0.0.9` - File upload handling

**Google Cloud**:
- `google-cloud-vision>=3.7.0` - Vision API client
- `google-cloud-storage>=2.16.0` - Cloud Storage client (not yet used)
- `firebase-admin>=6.5.0` - Firebase authentication

### Node.js (Skills CLI)

- `commander: ^11.1.0` - CLI framework
- `node-fetch: ^2.7.0` - HTTP requests

## Input Methods

### 1. Text Input (v1.1+) - Primary Method

**Preferred Method**: Highest fidelity, no OCR required

**Format**: JSON string with LinkedIn profile data
```json
{
  "headline": "Software Engineer | AI Specialist",
  "about": "Passionate about...",
  "current_role": "Senior Developer at Company",
  "skills": "Python, FastAPI, Cloud Run, Docker",
  "certifications": "AWS Certified, CompTIA Security+"
}
```

**API Parameter**: `linkedin_text` (form field)

### 2. Screenshot OCR - Fallback Method

**Purpose**: Extract profile data from screenshots when text input unavailable

**Supported Formats**: JPEG, PNG

**OCR Options**:
- Cloud Vision API (high quality) - when `use_cloud_vision=true`
- pytesseract (local fallback) - when Cloud Vision unavailable

**API Parameter**: `screenshots` (multipart file array)

## API Endpoints

### POST /analyze

**Purpose**: Process LinkedIn profile and resume to generate career strategy

**Required Parameters**:
- `mode`: Strategic mode - `"Get Hired"`, `"Grow Connections"`, or `"Influence Market"`
- `resume`: Resume file (PDF, DOCX, or TXT)

**Optional Parameters**:
- `linkedin_text`: JSON string with LinkedIn profile data (preferred)
- `screenshots`: Screenshot files for OCR (fallback)
- `use_cloud_vision`: Boolean - use Cloud Vision API (default: true)

**Authentication**: Optional Firebase ID token via `Authorization: Bearer <token>` header

**Response**:
```json
{
  "mode": "Get Hired",
  "profile_score": 85,
  "immediate_fixes": ["Fix 1", "Fix 2", "Fix 3"],
  "strategic_roadmap": ["Week 1: ...", "Week 2: ..."],
  "gaps": {...},
  "dashboard_markdown": "..."
}
```

### GET /health

**Purpose**: Health check endpoint

**Response**: `{"status": "ok"}`

## Development Setup

### Local Backend
```bash
python -m venv .venv
.venv/Scripts/activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn src.app:app --reload
```

### Local Docker
```bash
docker build -t linkedin-backend .
docker run -p 8080:8080 linkedin-backend
```

### Flutter Client
```bash
cd flutter_app
flutter pub get
flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze
```

## Security Considerations

### Credentials Management

**Excluded from Git** (via `.gitignore`):
- `firebase-adminsdk.json` - Firebase service account key
- `*service-account*.json` - GCP service account keys
- `.env` files - Environment variables

**Production Best Practices**:
- Use Google Cloud Workload Identity instead of service account keys
- Restrict Cloud Vision API access with IAM policies
- Implement rate limiting for public API endpoints
- Use Firebase Authentication in production

### CORS Configuration

**Current**: Allows all origins (`allow_origins=["*"]`)

**Production Recommendation**: Specify exact Flutter client origins
```python
allow_origins=[
    "https://linkedin-strategy-app.storage.googleapis.com",
    "https://yourdomain.web.app"
]
```

## Testing Integrations

### Text Input Mode
```bash
python test_data/test_text_input.py
```

### Screenshot OCR Mode
```bash
python test_data/test_api.py
```

### Cloud Vision Toggle
Test with both `use_cloud_vision=true` and `use_cloud_vision=false` to verify fallback behavior.

### Flutter Client
Test against both local (port 8080) and Cloud Run endpoints to verify API compatibility.

## Troubleshooting

### Cloud Vision API Errors

**Issue**: "Cloud Vision API not available"
- **Solution**: Install `google-cloud-vision` and set `GOOGLE_APPLICATION_CREDENTIALS` environment variable, or use `use_cloud_vision=false`

### Firebase Authentication Disabled

**Issue**: Firebase auth not working
- **Solution**: Add `firebase-adminsdk.json` to root directory or remove the dependency to use public API

### CORS Errors in Flutter Client

**Issue**: CORS blocked requests
- **Solution**: Verify backend CORS configuration includes client origin

### Build Failures

**Issue**: Cloud Build fails
- **Solution**: Verify GCP project ID matches in `cloudbuild.yaml` and ensure required APIs are enabled

## Future Integration Opportunities

1. **Cloud Storage**: Persistent file storage for uploads
2. **Cloud Logging**: Centralized logging and monitoring
3. **Cloud Secret Manager**: Secure credential management
4. **Vertex AI**: Enhanced AI-powered recommendations
5. **Cloud Tasks**: Asynchronous job processing
6. **Firestore**: Store user profiles and analysis history

## References

- [README.md](README.md) - Main project documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment instructions
- [USER_GUIDE.md](USER_GUIDE.md) - End-user documentation
- [skills/README.md](skills/README.md) - Skills system documentation
