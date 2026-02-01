"""
Integration tests for FastAPI application endpoints.
"""
import pytest
import json
from pathlib import Path
from fastapi.testclient import TestClient
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.mark.integration
class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_endpoint(self, client):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


@pytest.mark.integration
class TestAnalyzeEndpoint:
    """Test /analyze endpoint."""
    
    def test_analyze_with_text_input(self, client, sample_linkedin_data, sample_resume_text, temp_dir):
        """Test analysis with manual text input."""
        # Create resume file
        resume_path = temp_dir / "test_resume.txt"
        resume_path.write_text(sample_resume_text)
        
        # Prepare request
        with open(resume_path, "rb") as resume_file:
            files = {
                "resume": ("resume.txt", resume_file, "text/plain")
            }
            data = {
                "mode": "Get Hired",
                "linkedin_text": json.dumps(sample_linkedin_data),
            }
            
            response = client.post("/analyze", files=files, data=data)
        
        # Validate response
        assert response.status_code == 200
        result = response.json()
        
        assert result["mode"] == "Get Hired"
        assert 0 <= result["profile_score"] <= 100
        assert isinstance(result["immediate_fixes"], list)
        assert isinstance(result["strategic_roadmap"], list)
        assert "gaps" in result
        assert "dashboard_markdown" in result
    
    def test_analyze_all_modes(self, client, sample_linkedin_data, sample_resume_text, temp_dir):
        """Test all three strategy modes."""
        modes = ["Get Hired", "Grow Connections", "Influence Market"]
        
        resume_path = temp_dir / "test_resume.txt"
        resume_path.write_text(sample_resume_text)
        
        for mode in modes:
            with open(resume_path, "rb") as resume_file:
                files = {"resume": ("resume.txt", resume_file, "text/plain")}
                data = {
                    "mode": mode,
                    "linkedin_text": json.dumps(sample_linkedin_data),
                }
                
                response = client.post("/analyze", files=files, data=data)
            
            assert response.status_code == 200
            result = response.json()
            assert result["mode"] == mode
    
    def test_analyze_missing_linkedin_data(self, client, sample_resume_text, temp_dir):
        """Test analysis with missing LinkedIn data."""
        resume_path = temp_dir / "test_resume.txt"
        resume_path.write_text(sample_resume_text)
        
        with open(resume_path, "rb") as resume_file:
            files = {"resume": ("resume.txt", resume_file, "text/plain")}
            data = {"mode": "Get Hired"}
            
            response = client.post("/analyze", files=files, data=data)
        
        assert response.status_code == 400
        assert "Must provide either linkedin_text or screenshots" in response.text
    
    def test_analyze_invalid_mode(self, client, sample_linkedin_data, sample_resume_text, temp_dir):
        """Test analysis with invalid mode."""
        resume_path = temp_dir / "test_resume.txt"
        resume_path.write_text(sample_resume_text)
        
        with open(resume_path, "rb") as resume_file:
            files = {"resume": ("resume.txt", resume_file, "text/plain")}
            data = {
                "mode": "Invalid Mode",
                "linkedin_text": json.dumps(sample_linkedin_data),
            }
            
            response = client.post("/analyze", files=files, data=data)
        
        assert response.status_code == 422  # Validation error
    
    def test_analyze_invalid_json(self, client, sample_resume_text, temp_dir):
        """Test analysis with invalid JSON in linkedin_text."""
        resume_path = temp_dir / "test_resume.txt"
        resume_path.write_text(sample_resume_text)
        
        with open(resume_path, "rb") as resume_file:
            files = {"resume": ("resume.txt", resume_file, "text/plain")}
            data = {
                "mode": "Get Hired",
                "linkedin_text": "not valid json",
            }
            
            response = client.post("/analyze", files=files, data=data)
        
        assert response.status_code == 400
        assert "Invalid linkedin_text JSON" in response.text
    
    def test_analyze_unsupported_resume_format(self, client, sample_linkedin_data, temp_dir):
        """Test analysis with unsupported resume format."""
        # Create a file with unsupported extension
        resume_path = temp_dir / "resume.exe"
        resume_path.write_text("Some content")
        
        with open(resume_path, "rb") as resume_file:
            files = {"resume": ("resume.exe", resume_file, "application/octet-stream")}
            data = {
                "mode": "Get Hired",
                "linkedin_text": json.dumps(sample_linkedin_data),
            }
            
            response = client.post("/analyze", files=files, data=data)
        
        assert response.status_code == 400
        assert "Unsupported resume format" in response.text


@pytest.mark.integration
class TestCORSHeaders:
    """Test CORS configuration."""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present."""
        response = client.options("/health")
        
        # Check for CORS headers
        assert "access-control-allow-origin" in response.headers


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling."""
    
    def test_404_not_found(self, client):
        """Test 404 for non-existent endpoint."""
        response = client.get("/nonexistent")
        assert response.status_code == 404
