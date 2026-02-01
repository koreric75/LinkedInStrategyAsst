"""
FastAPI application for LinkedIn Strategy Assistant.

Provides REST API endpoints for analyzing LinkedIn profiles and resumes
to generate career growth strategies.
"""
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

from config import Config
from logger import setup_logger
from pipeline import (
    extract_linkedin_profile,
    parse_resume,
    generate_gap_analysis,
    generate_strategy,
    format_dashboard,
)

# Set up module logger
logger = setup_logger(__name__)

try:
    from google.cloud import vision  # type: ignore
    HAS_VISION_API = True
except Exception:  # pragma: no cover - optional
    vision = None
    HAS_VISION_API = False
    logger.warning("Google Cloud Vision API not available")

app = FastAPI(
    title=Config.APP_TITLE,
    version=Config.APP_VERSION,
    description="Analyze LinkedIn profiles and resumes to generate career growth strategies"
)

# Enable CORS for Flutter web client
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=Config.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info(f"CORS configured with origins: {Config.CORS_ORIGINS}")

# Optional: Initialize Firebase Admin (requires firebase-adminsdk.json)
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth, credentials
    
    if not firebase_admin._apps and Config.FIREBASE_ADMIN_SDK_PATH.exists():
        cred = credentials.Certificate(str(Config.FIREBASE_ADMIN_SDK_PATH))
        firebase_admin.initialize_app(cred)
        Config.FIREBASE_ENABLED = True
        logger.info("Firebase Admin SDK initialized")
    else:
        Config.FIREBASE_ENABLED = False
        logger.info("Firebase Admin SDK not configured")
except ImportError:
    Config.FIREBASE_ENABLED = False
    logger.warning("Firebase Admin SDK not available")


async def verify_firebase_token(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """
    Optional Firebase auth verification. Skipped if Firebase not configured.
    
    Args:
        authorization: Authorization header with Bearer token
    
    Returns:
        Decoded token dict if authentication successful, None if Firebase not enabled
    
    Raises:
        HTTPException: If token is invalid or missing (when Firebase enabled)
    """
    if not Config.FIREBASE_ENABLED:
        return None  # Skip auth if Firebase not configured
    
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Missing or invalid authorization header")
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.split("Bearer ")[1]
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        logger.info(f"Firebase token verified for user: {decoded_token.get('uid')}")
        return decoded_token
    except Exception as e:
        logger.error(f"Firebase token verification failed: {e}")
        raise HTTPException(
            status_code=401,
            detail=f"Invalid Firebase token: {str(e)}"
        )


@app.post("/analyze")
async def analyze(
    mode: str = Form(..., pattern=r"^(Get Hired|Grow Connections|Influence Market)$"),
    resume: UploadFile = File(...),
    screenshots: List[UploadFile] = File(default=[]),
    linkedin_text: Optional[str] = Form(None),  # JSON string with LinkedIn data
    use_cloud_vision: bool = Form(True),  # Default to Cloud Vision for production
    user: Optional[dict] = Depends(verify_firebase_token),  # Optional Firebase auth
):
    """
    Analyze LinkedIn profile and resume to generate career strategy.
    
    Args:
        mode: Strategic mode - "Get Hired", "Grow Connections", or "Influence Market"
        resume: Resume file (PDF, DOCX, or TXT)
        screenshots: Optional LinkedIn profile screenshots for OCR
        linkedin_text: Optional manual LinkedIn data as JSON string (preferred over OCR)
        use_cloud_vision: Use Google Cloud Vision API for OCR (default: True)
        user: Optional Firebase user data (if authentication enabled)
    
    Returns:
        JSONResponse with strategy dashboard and recommendations
    
    Raises:
        HTTPException: For validation errors or processing failures
    """
    logger.info(f"Received analysis request - mode: {mode}, user: {user.get('uid') if user else 'anonymous'}")
    
    # Validate inputs
    if not linkedin_text and not screenshots:
        logger.warning("No LinkedIn data provided")
        raise HTTPException(
            status_code=400,
            detail="Must provide either linkedin_text or screenshots"
        )
    
    # Validate resume file
    resume_ext = Path(resume.filename).suffix.lower()
    if resume_ext not in Config.ALLOWED_RESUME_EXTENSIONS:
        logger.warning(f"Invalid resume format: {resume_ext}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported resume format: {resume_ext}. Allowed: {Config.ALLOWED_RESUME_EXTENSIONS}"
        )
    
    # Validate screenshot files if provided
    for screenshot in screenshots:
        img_ext = Path(screenshot.filename).suffix.lower()
        if img_ext not in Config.ALLOWED_IMAGE_EXTENSIONS:
            logger.warning(f"Invalid screenshot format: {img_ext}")
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format: {img_ext}. Allowed: {Config.ALLOWED_IMAGE_EXTENSIONS}"
            )
    
    try:
        # Save uploads to temp files
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Save resume
            resume_path = tmpdir_path / resume.filename
            resume_bytes = await resume.read()
            
            # Validate file size
            if len(resume_bytes) > Config.MAX_UPLOAD_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"Resume file too large. Max size: {Config.MAX_UPLOAD_SIZE} bytes"
                )
            
            resume_path.write_bytes(resume_bytes)
            logger.info(f"Saved resume: {resume.filename} ({len(resume_bytes)} bytes)")

            # Save screenshots if provided
            screenshot_paths: List[Path] = []
            for file in screenshots:
                shot_bytes = await file.read()
                if len(shot_bytes) > Config.MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Screenshot file too large. Max size: {Config.MAX_UPLOAD_SIZE} bytes"
                    )
                shot_path = tmpdir_path / file.filename
                shot_path.write_bytes(shot_bytes)
                screenshot_paths.append(shot_path)
                logger.info(f"Saved screenshot: {file.filename} ({len(shot_bytes)} bytes)")

            # Prioritize manual text input over OCR
            if linkedin_text:
                logger.info("Using manual LinkedIn text input")
                linkedin_profile = _parse_linkedin_text(linkedin_text)
            elif screenshot_paths:
                logger.info(f"Using OCR extraction from {len(screenshot_paths)} screenshots")
                linkedin_profile = await _extract_linkedin(screenshot_paths, use_cloud_vision)
            else:
                # This should not happen due to earlier validation
                raise HTTPException(
                    status_code=400,
                    detail="Must provide either linkedin_text or screenshots"
                )

            # Parse resume and generate strategy
            logger.info("Parsing resume")
            resume_data = parse_resume(resume_path)
            
            logger.info("Generating gap analysis")
            gaps = generate_gap_analysis(linkedin_profile, resume_data)
            
            logger.info(f"Generating strategy for mode: {mode}")
            strategy = generate_strategy(mode, gaps, linkedin_profile, resume_data)
            
            logger.info(f"Strategy generated - score: {strategy.profile_score}/100")

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
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Unexpected error during analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


def _parse_linkedin_text(linkedin_json: str):
    """
    Parse manual LinkedIn text input from Flutter form.
    
    Args:
        linkedin_json: JSON string with LinkedIn profile data
    
    Returns:
        LinkedInProfile object
    
    Raises:
        HTTPException: If JSON is invalid or missing required fields
    """
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
        
        logger.info(f"Parsed LinkedIn text - headline: {bool(profile.headline)}, "
                   f"skills: {len(profile.skills)}, certs: {len(profile.certifications)}")
        
        return profile
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in linkedin_text: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid linkedin_text JSON: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Failed to parse linkedin_text: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse linkedin_text: {str(e)}"
        )


async def _extract_linkedin(paths: List[Path], use_cloud_vision: bool):
    """
    Extract LinkedIn profile data from screenshots using OCR.
    
    Args:
        paths: List of screenshot file paths
        use_cloud_vision: Whether to use Google Cloud Vision API
    
    Returns:
        LinkedInProfile object with extracted data
    
    Raises:
        HTTPException: If OCR extraction fails or Vision API unavailable
    """
    if use_cloud_vision:
        if not HAS_VISION_API:
            logger.error("Cloud Vision API requested but not available")
            raise HTTPException(
                status_code=500,
                detail="Cloud Vision API not available. Install google-cloud-vision or set use_cloud_vision=false"
            )
        
        try:
            logger.info(f"Using Cloud Vision API for {len(paths)} screenshots")
            client = vision.ImageAnnotatorClient()
            texts: List[str] = []
            
            for path in paths:
                with path.open("rb") as f:
                    content = f.read()
                
                image = vision.Image(content=content)
                response = client.document_text_detection(image=image)
                
                if response.error.message:
                    logger.error(f"Vision API error: {response.error.message}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Vision API error: {response.error.message}"
                    )
                
                if response.full_text_annotation and response.full_text_annotation.text:
                    text = response.full_text_annotation.text
                    texts.append(text)
                    logger.info(f"Extracted {len(text)} chars from {path.name} via Vision API")
            
            if not texts:
                logger.warning("No text extracted from screenshots via Vision API")
                raise HTTPException(
                    status_code=400,
                    detail="No text extracted from screenshots. Please ensure images contain visible text."
                )
            
            # Write merged text to temp to reuse pipeline parsing
            merged = "\n".join(texts)
            tmp = Path(tempfile.mkstemp(suffix=".txt")[1])
            tmp.write_text(merged, encoding="utf-8")
            profile = extract_linkedin_profile([tmp])
            tmp.unlink()  # Clean up temp file
            return profile
            
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"OCR extraction failed with Cloud Vision: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"OCR extraction failed: {str(e)}"
            )
    
    # Fallback to pytesseract (local only)
    logger.info(f"Using pytesseract for {len(paths)} screenshots")
    return extract_linkedin_profile(paths)


@app.get("/health")
async def health():
    """
    Health check endpoint for monitoring and load balancing.
    
    Returns:
        Health status and version information
    """
    return {
        "status": "ok",
        "version": Config.APP_VERSION,
        "firebase_enabled": Config.FIREBASE_ENABLED,
        "vision_api_available": HAS_VISION_API,
    }


def get_app() -> FastAPI:
    """Get FastAPI application instance."""
    return app


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {Config.APP_TITLE} v{Config.APP_VERSION}")
    logger.info(f"Server: {Config.HOST}:{Config.PORT}")
    
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level=Config.LOG_LEVEL.lower()
    )
