# Contributing to LinkedIn Strategy Assistant

Thank you for your interest in contributing to the LinkedIn Strategy Assistant! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Contributions](#making-contributions)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

This project follows a standard code of conduct. Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/LinkedInStrategyAsst.git
   cd LinkedInStrategyAsst
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/koreric75/LinkedInStrategyAsst.git
   ```

## Development Setup

### Backend (Python/FastAPI)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.app:app --reload
```

### Frontend (Flutter)

```bash
cd flutter_app

# Install dependencies
flutter pub get

# Run on web (Chrome)
flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze

# Run on mobile emulator
flutter run
```

### Skills CLI (Node.js)

```bash
# Install dependencies
npm install

# List skills
npx skills list

# Add new skill
npx skills add <repository-url> --skill <skill-name>
```

## Making Contributions

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes** - Fix identified bugs or issues
2. **Features** - Implement new features or enhancements
3. **Documentation** - Improve or update documentation
4. **Tests** - Add or improve test coverage
5. **Integrations** - Add support for new services or APIs
6. **Skills** - Contribute new AI agent skills

### Contribution Workflow

1. **Create a branch** for your contribution:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following the coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** with clear commit messages:
   ```bash
   git add .
   git commit -m "feat: add new LinkedIn scraping feature"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub

### Commit Message Guidelines

Follow conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or modifications
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements

Examples:
```
feat: add support for Cloud Storage file persistence
fix: resolve OCR extraction error with Cloud Vision API
docs: update INTEGRATIONS.md with new service details
test: add integration tests for text input mode
```

## Pull Request Process

1. **Update documentation** if needed (README, INTEGRATIONS.md, etc.)
2. **Add tests** for new functionality
3. **Ensure all tests pass**:
   ```bash
   # Backend tests
   python test_data/test_text_input.py
   python test_data/test_api.py
   
   # Flutter tests
   cd flutter_app && flutter test
   ```
4. **Update CHANGELOG.md** with your changes under "Unreleased" section
5. **Request review** from maintainers
6. **Address review feedback** if any
7. **Squash commits** if requested

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All tests pass
```

## Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Use Google-style docstrings
- **Line Length**: Maximum 100 characters
- **Formatting**: Consider using `black` for auto-formatting

Example:
```python
from typing import List, Optional

def extract_skills(profile_text: str, max_skills: int = 50) -> List[str]:
    """Extract skills from LinkedIn profile text.
    
    Args:
        profile_text: The raw profile text to parse
        max_skills: Maximum number of skills to extract (default: 50)
        
    Returns:
        List of extracted skill names
        
    Raises:
        ValueError: If profile_text is empty
    """
    if not profile_text:
        raise ValueError("Profile text cannot be empty")
    
    # Implementation here
    return []
```

### Dart (Flutter)

- **Style**: Follow Dart style guide
- **Formatting**: Use `dart format`
- **Linting**: Follow `analysis_options.yaml` rules
- **Null Safety**: Always use null safety features

Example:
```dart
class ProfileData {
  final String headline;
  final String about;
  final List<String> skills;
  
  const ProfileData({
    required this.headline,
    required this.about,
    required this.skills,
  });
  
  Map<String, dynamic> toJson() => {
    'headline': headline,
    'about': about,
    'skills': skills.join(', '),
  };
}
```

### JavaScript (Skills CLI)

- **Style**: Use ES6+ features
- **Formatting**: Use 2-space indentation
- **Error Handling**: Always handle errors gracefully

## Testing Guidelines

### Backend Tests

Place tests in `test_data/` directory:

```python
# test_data/test_new_feature.py
import requests
import json

def test_new_feature():
    url = "http://localhost:8080/analyze"
    
    data = {
        "mode": "Get Hired",
        "linkedin_text": json.dumps({
            "headline": "Test Headline",
            "about": "Test About",
            "skills": "Python, Docker"
        })
    }
    
    files = {
        "resume": ("resume.txt", open("test_data/sample_resume.txt", "rb"))
    }
    
    response = requests.post(url, data=data, files=files)
    assert response.status_code == 200
    assert "profile_score" in response.json()
```

### Integration Tests

Test the full workflow:
- API endpoint integration
- File upload handling
- Response formatting
- Error cases

### Manual Testing Checklist

- [ ] Test with text input mode
- [ ] Test with screenshot OCR mode
- [ ] Test all three strategic modes (Get Hired, Grow Connections, Influence Market)
- [ ] Test error handling (missing files, invalid mode, etc.)
- [ ] Test Flutter client against local backend
- [ ] Test Flutter client against deployed backend

## Documentation

### When to Update Documentation

Update documentation when you:
- Add new features
- Change existing behavior
- Add new integrations or services
- Modify API endpoints or parameters
- Update configuration options

### Documentation Files

- **README.md** - Main project overview and quick start
- **INTEGRATIONS.md** - External service integrations
- **DEPLOYMENT_GUIDE.md** - Deployment instructions
- **USER_GUIDE.md** - End-user documentation
- **TESTING_GUIDE.md** - Testing procedures
- **CHANGELOG.md** - Version history
- **Code comments** - Inline documentation for complex logic

### Documentation Style

- Use clear, concise language
- Include code examples where helpful
- Add screenshots for UI changes
- Keep documentation up-to-date with code changes
- Use proper markdown formatting

## Adding New Skills

To contribute a new AI agent skill:

1. Create skill directory: `skills/your-skill-name/`
2. Add `SKILL.md` with skill instructions
3. Update `skills/README.md` to list the new skill
4. Test the skill with the strategy generation pipeline
5. Submit PR with skill documentation

## Questions or Issues?

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Contact**: Reach out to maintainers via GitHub

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to LinkedIn Strategy Assistant! 🚀
