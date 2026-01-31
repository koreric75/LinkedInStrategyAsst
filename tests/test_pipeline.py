"""
Unit tests for pipeline.py functions.
"""
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pipeline import (
    LinkedInProfile,
    ResumeData,
    GapAnalysis,
    Strategy,
    parse_resume,
    generate_gap_analysis,
    generate_strategy,
    _extract_headline,
    _extract_section,
    _extract_list,
    _normalize_all,
    _detect_advanced_themes,
    _calculate_profile_score,
)


@pytest.mark.unit
class TestDataModels:
    """Test data model classes."""
    
    def test_linkedin_profile_initialization(self):
        """Test LinkedInProfile creation."""
        profile = LinkedInProfile()
        assert profile.headline == ""
        assert profile.about == ""
        assert profile.skills == []
        assert profile.certifications == []
    
    def test_resume_data_initialization(self):
        """Test ResumeData creation."""
        resume = ResumeData()
        assert resume.skills == []
        assert resume.projects == []
        assert resume.certifications == []
        assert resume.experience == []
    
    def test_gap_analysis_initialization(self):
        """Test GapAnalysis creation."""
        gaps = GapAnalysis(
            skills_missing_from_linkedin=["Python"],
            projects_missing_from_linkedin=["Project X"],
            certifications_missing_from_linkedin=["Cert A"],
            advanced_tech_themes=["Docker", "Kubernetes"]
        )
        assert len(gaps.skills_missing_from_linkedin) == 1
        assert len(gaps.advanced_tech_themes) == 2


@pytest.mark.unit
class TestResumeParser:
    """Test resume parsing functionality."""
    
    def test_parse_resume_txt(self, sample_resume_file):
        """Test parsing TXT resume."""
        resume = parse_resume(sample_resume_file)
        
        assert isinstance(resume, ResumeData)
        assert len(resume.skills) > 0
        assert "Python" in " ".join(resume.skills)
        assert len(resume.certifications) > 0
    
    def test_parse_resume_missing_file(self, temp_dir):
        """Test parsing non-existent resume."""
        with pytest.raises(FileNotFoundError):
            parse_resume(temp_dir / "nonexistent.txt")


@pytest.mark.unit
class TestTextExtraction:
    """Test text extraction helper functions."""
    
    def test_extract_headline(self):
        """Test headline extraction."""
        text = "Senior Software Engineer\nMore text here\nAnd more"
        headline = _extract_headline(text)
        assert headline == "Senior Software Engineer"
    
    def test_extract_headline_empty(self):
        """Test headline extraction from empty text."""
        headline = _extract_headline("")
        assert headline == ""
    
    def test_extract_section(self):
        """Test section extraction."""
        text = "About:\nThis is the about section\nIt has multiple lines\n\nNext Section"
        about = _extract_section(text, "About")
        assert "about section" in about.lower()
    
    def test_extract_list(self):
        """Test list extraction."""
        text = "Skills:\nPython, Docker, Kubernetes\n\n"
        skills = _extract_list(text, ["Skills"])
        assert len(skills) == 3
        assert "Python" in skills
        assert "Docker" in skills
    
    def test_extract_list_newline_separated(self):
        """Test list extraction with newlines."""
        text = "Certifications:\nCert A\nCert B\nCert C\n\n"
        certs = _extract_list(text, ["Certifications"])
        assert len(certs) == 3


@pytest.mark.unit
class TestGapAnalysis:
    """Test gap analysis functionality."""
    
    def test_generate_gap_analysis(self):
        """Test gap analysis generation."""
        linkedin = LinkedInProfile()
        linkedin.skills = ["Python", "Docker"]
        linkedin.certifications = ["Google Cloud"]
        
        resume = ResumeData()
        resume.skills = ["Python", "Docker", "Kubernetes", "Terraform"]
        resume.certifications = ["Google Cloud", "AWS Solutions Architect"]
        
        gaps = generate_gap_analysis(linkedin, resume)
        
        assert isinstance(gaps, GapAnalysis)
        assert "kubernetes" in gaps.skills_missing_from_linkedin
        assert "terraform" in gaps.skills_missing_from_linkedin
        assert "aws solutions architect" in gaps.certifications_missing_from_linkedin
    
    def test_detect_advanced_themes(self):
        """Test advanced tech theme detection."""
        text = "I work with Docker, Kubernetes, and LLM technology"
        themes = _detect_advanced_themes(text)
        
        assert "Docker" in themes
        assert "Kubernetes" in themes
        assert "LLM" in themes
    
    def test_normalize_all(self):
        """Test value normalization."""
        values = ["Python", " Docker ", "KUBERNETES"]
        normalized = _normalize_all(values)
        
        assert normalized == ["python", "docker", "kubernetes"]


@pytest.mark.unit
class TestStrategyGeneration:
    """Test strategy generation functionality."""
    
    def test_generate_strategy_get_hired(self):
        """Test strategy generation for Get Hired mode."""
        linkedin = LinkedInProfile()
        linkedin.headline = "Software Engineer"
        linkedin.skills = ["Python"]
        
        resume = ResumeData()
        resume.skills = ["Python", "Docker", "Kubernetes"]
        resume.certifications = ["AWS"]
        
        gaps = generate_gap_analysis(linkedin, resume)
        strategy = generate_strategy("Get Hired", gaps, linkedin, resume)
        
        assert strategy.mode == "Get Hired"
        assert 0 <= strategy.profile_score <= 100
        assert len(strategy.immediate_fixes) > 0
        assert len(strategy.strategic_roadmap) > 0
    
    def test_generate_strategy_grow_connections(self):
        """Test strategy generation for Grow Connections mode."""
        linkedin = LinkedInProfile()
        linkedin.headline = "Software Engineer"
        
        resume = ResumeData()
        resume.skills = ["Python"]
        
        gaps = generate_gap_analysis(linkedin, resume)
        strategy = generate_strategy("Grow Connections", gaps, linkedin, resume)
        
        assert strategy.mode == "Grow Connections"
        assert isinstance(strategy.strategic_roadmap, list)
    
    def test_generate_strategy_influence_market(self):
        """Test strategy generation for Influence Market mode."""
        linkedin = LinkedInProfile()
        resume = ResumeData()
        
        gaps = generate_gap_analysis(linkedin, resume)
        strategy = generate_strategy("Influence Market", gaps, linkedin, resume)
        
        assert strategy.mode == "Influence Market"
    
    def test_generate_strategy_invalid_mode(self):
        """Test strategy generation with invalid mode."""
        linkedin = LinkedInProfile()
        resume = ResumeData()
        gaps = generate_gap_analysis(linkedin, resume)
        
        with pytest.raises(ValueError):
            generate_strategy("Invalid Mode", gaps, linkedin, resume)
    
    def test_calculate_profile_score(self):
        """Test profile score calculation."""
        linkedin = LinkedInProfile()
        linkedin.headline = "Software Engineer | Cloud Specialist"
        linkedin.about = "A" * 150  # Long about section
        linkedin.skills = ["Python", "Docker", "Kubernetes", "AI", "Cloud Run", "CI/CD"]
        linkedin.certifications = ["AWS"]
        
        resume = ResumeData()
        resume.skills = ["Python", "Docker", "Kubernetes", "AI", "Cloud Run", "CI/CD", "Terraform"]
        resume.certifications = ["AWS", "GCP"]
        
        gaps = generate_gap_analysis(linkedin, resume)
        score = _calculate_profile_score(gaps, linkedin, resume)
        
        assert 0 <= score <= 100
        assert score > 50  # Should have decent score with this profile


@pytest.mark.unit
class TestDashboardFormatting:
    """Test dashboard formatting."""
    
    def test_format_dashboard(self):
        """Test dashboard markdown generation."""
        from pipeline import format_dashboard
        
        linkedin = LinkedInProfile()
        linkedin.headline = "Software Engineer"
        
        resume = ResumeData()
        resume.skills = ["Python", "Docker"]
        
        gaps = generate_gap_analysis(linkedin, resume)
        strategy = generate_strategy("Get Hired", gaps, linkedin, resume)
        
        dashboard = format_dashboard(strategy)
        
        assert isinstance(dashboard, str)
        assert "LinkedIn Strategy Dashboard" in dashboard
        assert "Get Hired" in dashboard
        assert "Profile Score" in dashboard
        assert "Immediate Fixes" in dashboard
        assert "Strategic Roadmap" in dashboard
