"""
Test configuration and fixtures for LinkedIn Strategy Assistant.
"""
import pytest
from pathlib import Path
from typing import Generator
import tempfile
import sys

# Add src to Python path
SRC_PATH = Path(__file__).parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_resume_text() -> str:
    """Sample resume text for testing."""
    return """
John Doe
Senior Software Engineer

EXPERIENCE
Senior Software Engineer at Tech Corp (2020-Present)
- Led development of cloud-native microservices using Docker and Kubernetes
- Implemented CI/CD pipelines using Terraform and Cloud Run
- Built AI-powered automation tools using LLM and RPA

Software Engineer at StartupXYZ (2018-2020)
- Developed FastAPI backend services
- Created Flutter mobile applications
- Implemented Machine Learning models for data analysis

SKILLS
Python, Docker, Kubernetes, Cloud Run, FastAPI, Flutter, Terraform, 
CI/CD, AI, Machine Learning, RPA, LLM, PostgreSQL, Redis, Git

CERTIFICATIONS
CompTIA Security+
Google Cloud Professional Architect
AWS Solutions Architect

PROJECTS
LinkedIn Strategy Assistant - AI-powered career growth platform
Built with FastAPI, Flutter, Google Cloud Run, and Vision API

Cloud Migration Tool - Automated migration of legacy apps to cloud
Technologies: Docker, Kubernetes, Terraform, CI/CD
"""


@pytest.fixture
def sample_linkedin_data() -> dict:
    """Sample LinkedIn profile data for testing."""
    return {
        "headline": "Senior Software Engineer | Cloud & AI Specialist",
        "about": """Passionate software engineer specializing in cloud-native solutions 
        and AI-powered automation. Expert in Docker, Kubernetes, and modern CI/CD practices.
        
        Currently building innovative solutions at Tech Corp.""",
        "current_role": "Senior Software Engineer at Tech Corp",
        "skills": "Python, Docker, Kubernetes, FastAPI, Cloud Run, AI",
        "certifications": "Google Cloud Professional Architect"
    }


@pytest.fixture
def sample_resume_file(temp_dir: Path, sample_resume_text: str) -> Path:
    """Create a sample resume file for testing."""
    resume_path = temp_dir / "sample_resume.txt"
    resume_path.write_text(sample_resume_text)
    return resume_path


@pytest.fixture
def mock_vision_response():
    """Mock Google Cloud Vision API response."""
    class MockTextAnnotation:
        def __init__(self, text: str):
            self.text = text
    
    class MockError:
        message = ""
    
    class MockResponse:
        def __init__(self, text: str):
            self.full_text_annotation = MockTextAnnotation(text)
            self.error = MockError()
    
    return MockResponse
