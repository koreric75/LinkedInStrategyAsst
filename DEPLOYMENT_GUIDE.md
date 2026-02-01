## Testing the API

### Health Check (Verified ✓)
```bash
curl https://linkedin-strategy-backend-796550517938.us-central1.run.app/health
# Response: {"status":"ok"}
```

### Test Strategy Analysis Endpoint (v1.2 - Text Input)
```bash
# Recommended: Use text input for highest accuracy
curl -X POST https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze \
  -F "mode=Get Hired" \
  -F "resume=@path/to/resume.pdf" \
  -F 'linkedin_text={"headline":"Senior Software Engineer | Cloud & AI","about":"I help organizations...","current_role":"Software Engineer at Company","skills":"Python, Docker, Kubernetes","certifications":"CompTIA Security+"}'
```

### Test Strategy Analysis Endpoint (Screenshots Fallback)
```bash
# Alternative: Use screenshots (requires OCR)
curl -X POST https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze \
  -F "mode=Get Hired" \
  -F "resume=@path/to/resume.pdf" \
  -F "screenshots=@path/to/linkedin-screenshot1.png" \
  -F "screenshots=@path/to/linkedin-screenshot2.png" \
  -F "use_cloud_vision=true"
```

### Test with Python Script (v1.2)
```powershell
cd test_data
python test_text_input.py  # Tests text input mode
python test_api.py          # Tests screenshot mode
```

## Flutter SDK Installation

1. Download Flutter SDK:
   - Visit https://docs.flutter.dev/get-started/install/windows
   - Download Flutter SDK zip
   - Extract to `C:\src\flutter` (or your preferred location)

2. Add Flutter to PATH:
   ```powershell
   $env:Path += ";C:\src\flutter\bin"
   # Or permanently via System Environment Variables
   ```

3. Run Flutter Doctor:
   ```powershell
   flutter doctor
   ```

4. Install Chrome (if not installed) for web development

5. Run the Flutter app:
   ```powershell
   cd C:\Users\korer\LinkedInStrategyAsst\flutter_app
   flutter pub get
   flutter run -d chrome --dart-define API_URL=https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze
   ```

## Production Enhancements

### 1. Firebase Auth Middleware
Add to `src/app.py`:
```python
from firebase_admin import auth, credentials, initialize_app
import os

# Initialize Firebase Admin
if os.path.exists("firebase-adminsdk.json"):
    cred = credentials.Certificate("firebase-adminsdk.json")
    initialize_app(cred)

async def verify_firebase_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.post("/analyze")
async def analyze(
    mode: str = Form(...),
    resume: UploadFile = File(...),
    screenshots: List[UploadFile] = File(...),
    use_cloud_vision: bool = Form(False),
    user: dict = Depends(verify_firebase_token)  # Add this
):
    # Existing code...
```

### 2. Cloud Vision Integration (Already in code)
Enable Cloud Vision API and set `use_cloud_vision=true` in requests for better OCR accuracy.

### 3. Cloud Storage for Persistent Files
Update `requirements.txt`:
```
google-cloud-storage>=2.16.0  # Already included
```

Add to `src/app.py`:
```python
from google.cloud import storage

def upload_to_gcs(file_path: Path, bucket_name: str, blob_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(str(file_path))
    return blob.public_url
```

## Next Steps
- Test API with sample resume + screenshots
- Install Flutter SDK for web client development
- Add Firebase project and download service account key for auth
- Enable Cloud Vision API for production OCR
