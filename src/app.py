from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import List, Optional

# Ensure src directory is on sys.path for local/dev execution
import sys
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pipeline import (
    extract_linkedin_profile,
    parse_resume,
    generate_gap_analysis,
    generate_strategy,
    format_dashboard,
)

try:
    from google.cloud import vision  # type: ignore
except Exception:  # pragma: no cover - optional
    vision = None

app = FastAPI(title="LinkedIn Strategy Assistant", version="1.0")

# Enable CORS for Flutter web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Initialize Firebase Admin (requires firebase-adminsdk.json)
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth, credentials
    if not firebase_admin._apps and os.path.exists("firebase-adminsdk.json"):
        cred = credentials.Certificate("firebase-adminsdk.json")
        firebase_admin.initialize_app(cred)
        FIREBASE_ENABLED = True
    else:
        FIREBASE_ENABLED = False
except ImportError:
    FIREBASE_ENABLED = False


async def verify_firebase_token(authorization: Optional[str] = Header(None)):
    """Optional Firebase auth verification. Skipped if Firebase not configured."""
    if not FIREBASE_ENABLED:
        return None  # Skip auth if Firebase not configured
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")


@app.post("/analyze")
async def analyze(
    mode: str = Form(..., pattern=r"^(Get Hired|Grow Connections|Influence Market)$"),
    resume: UploadFile = File(...),
    screenshots: List[UploadFile] = File(default=[]),
    linkedin_text: Optional[str] = Form(None),  # JSON string with LinkedIn data
    use_cloud_vision: bool = Form(True),  # Default to Cloud Vision for production
    user: Optional[dict] = Depends(verify_firebase_token),  # Optional Firebase auth
):
    # Save uploads to temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        resume_path = tmpdir_path / resume.filename
        resume_bytes = await resume.read()
        resume_path.write_bytes(resume_bytes)

        screenshot_paths: List[Path] = []
        for file in screenshots:
            shot_path = tmpdir_path / file.filename
            shot_path.write_bytes(await file.read())
            screenshot_paths.append(shot_path)

        # Prioritize manual text input over OCR
        if linkedin_text:
            linkedin_profile = _parse_linkedin_text(linkedin_text)
        elif screenshot_paths:
            linkedin_profile = await _extract_linkedin(screenshot_paths, use_cloud_vision)
        else:
            raise HTTPException(status_code=400, detail="Must provide either linkedin_text or screenshots")

        resume_data = parse_resume(resume_path)
        gaps = generate_gap_analysis(linkedin_profile, resume_data)
        strategy = generate_strategy(mode, gaps, linkedin_profile, resume_data)

        return JSONResponse(
            {
                "mode": strategy.mode,
                "profile_score": strategy.profile_score,
                "immediate_fixes": strategy.immediate_fixes,
                "strategic_roadmap": strategy.strategic_roadmap,
                "gaps": strategy.gaps.__dict__,
                "dashboard_markdown": format_dashboard(strategy),
            }
        )


def _parse_linkedin_text(linkedin_json: str):
    """Parse manual LinkedIn text input from Flutter form."""
    import json
    from pipeline import LinkedInProfile
    
    try:
        data = json.loads(linkedin_json)
        profile = LinkedInProfile()
        profile.headline = data.get("headline", "").strip()
        profile.about = data.get("about", "").strip()
        profile.current_role = data.get("current_role", "").strip()
        
        # Parse comma-separated skills and certifications
        skills_str = data.get("skills", "").strip()
        profile.skills = [s.strip() for s in skills_str.split(",") if s.strip()]
        
        certs_str = data.get("certifications", "").strip()
        profile.certifications = [c.strip() for c in certs_str.split(",") if c.strip()]
        
        return profile
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid linkedin_text JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse linkedin_text: {str(e)}")


async def _extract_linkedin(paths: List[Path], use_cloud_vision: bool):
    if use_cloud_vision:
        if not vision:
            raise HTTPException(
                status_code=500,
                detail="Cloud Vision API not available. Install google-cloud-vision or set use_cloud_vision=false"
            )
        try:
            client = vision.ImageAnnotatorClient()
            texts: List[str] = []
            for path in paths:
                with path.open("rb") as f:
                    content = f.read()
                image = vision.Image(content=content)
                response = client.document_text_detection(image=image)
                if response.error.message:
                    raise HTTPException(status_code=500, detail=f"Vision API error: {response.error.message}")
                if response.full_text_annotation and response.full_text_annotation.text:
                    texts.append(response.full_text_annotation.text)
            
            if not texts:
                raise HTTPException(status_code=400, detail="No text extracted from screenshots. Please ensure images contain visible text.")
            
            # Write merged text to temp to reuse pipeline parsing
            merged = "\n".join(texts)
            tmp = Path(tempfile.mkstemp(suffix=".txt")[1])
            tmp.write_text(merged, encoding="utf-8")
            return extract_linkedin_profile([tmp])
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")
    
    # Fallback to pytesseract (local only)
    return extract_linkedin_profile(paths)


@app.get("/health")
async def health():
    return {"status": "ok"}


def get_app() -> FastAPI:
    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
