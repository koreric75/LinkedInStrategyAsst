# Developer Setup Guide

## Prerequisites

### Required Software
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Docker** (optional, for containerized development) - [Download](https://www.docker.com/get-started)

### Optional Software
- **Flutter SDK** (for frontend development) - [Install Guide](https://docs.flutter.dev/get-started/install)
- **Google Cloud SDK** (for deployment) - [Install Guide](https://cloud.google.com/sdk/docs/install)
- **Node.js & npm** (for skills management) - [Download](https://nodejs.org/)

### System Dependencies (for OCR)
- **Tesseract OCR:**
  - **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr libtesseract-dev`
  - **macOS:** `brew install tesseract`
  - **Windows:** [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/koreric75/LinkedInStrategyAsst.git
cd LinkedInStrategyAsst
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment (Optional)

Create a `.env` file in the project root (optional):

```bash
# Server Configuration
PORT=8080
HOST=0.0.0.0
DEBUG=false
LOG_LEVEL=INFO

# CORS Configuration (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# File Upload
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes

# OCR Configuration
USE_CLOUD_VISION_DEFAULT=false  # Use tesseract locally
TESSERACT_CMD=tesseract

# Google Cloud (if using Cloud Vision API)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
```

### 4. Run the Application Locally

```bash
# Start the FastAPI server
uvicorn src.app:app --reload --host 0.0.0.0 --port 8080

# Server will be available at:
# http://localhost:8080
# API docs: http://localhost:8080/docs
# Health check: http://localhost:8080/health
```

### 5. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run specific test file
pytest tests/test_pipeline.py -v

# View coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
# or
xdg-open htmlcov/index.html  # Linux
```

## Development Workflow

### Project Structure

```
LinkedInStrategyAsst/
├── src/                       # Python backend source code
│   ├── app.py                # FastAPI application
│   ├── pipeline.py           # Processing pipeline
│   ├── linkedin_optimizer.py # Enhanced recommendations
│   ├── config.py             # Configuration management
│   └── logger.py             # Logging setup
├── tests/                     # Test suite
│   ├── conftest.py           # Test fixtures
│   ├── test_pipeline.py      # Pipeline unit tests
│   └── test_api.py           # API integration tests
├── flutter_app/              # Flutter frontend
│   ├── lib/                  # Dart source code
│   └── pubspec.yaml         # Flutter dependencies
├── docs/                      # Documentation
│   └── ARCHITECTURE.md       # Architecture guide
├── test_data/                # Test scripts and data
│   ├── test_api.py          # API test script
│   └── test_text_input.py   # Text input test
├── .github/                   # GitHub configuration
│   └── workflows/           # CI/CD workflows
│       └── ci-cd.yml        # Main CI/CD pipeline
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── Dockerfile               # Docker container definition
├── cloudbuild.yaml          # Cloud Build configuration
└── README.md                # Project overview
```

### Code Style

We follow PEP 8 Python style guidelines with some modifications:

```bash
# Install code quality tools
pip install black flake8 mypy

# Format code with Black
black src/ tests/

# Check code with flake8
flake8 src/ tests/ --max-line-length=120

# Type checking with mypy
mypy src/
```

### Pre-commit Hooks (Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Set up git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8080/health

# Analyze with text input
curl -X POST http://localhost:8080/analyze \
  -F "mode=Get Hired" \
  -F "resume=@test_data/sample_resume.txt" \
  -F "linkedin_text={\"headline\":\"Software Engineer\",\"about\":\"...\",\"skills\":\"Python,Docker\",\"certifications\":\"AWS\"}"
```

### Using Python

```bash
# Run test script
python test_data/test_text_input.py
```

### Using Swagger UI

Visit http://localhost:8080/docs for interactive API documentation.

## Docker Development

### Build Docker Image

```bash
docker build -t linkedin-strategy-backend:dev .
```

### Run Container Locally

```bash
docker run -p 8080:8080 \
  -e LOG_LEVEL=DEBUG \
  linkedin-strategy-backend:dev
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8080:8080"
    environment:
      - LOG_LEVEL=INFO
      - DEBUG=false
    volumes:
      - ./src:/app/src  # Hot reload during development
```

Run with:
```bash
docker-compose up
```

## Flutter Frontend Development

### Setup

```bash
cd flutter_app

# Install dependencies
flutter pub get

# Run in Chrome (web)
flutter run -d chrome --dart-define API_URL=http://localhost:8080/analyze

# Run on mobile simulator
flutter run -d ios  # iOS
flutter run -d android  # Android

# Build for web
flutter build web

# Build for mobile
flutter build apk  # Android
flutter build ios  # iOS
```

### Configuration

Set API endpoint in Flutter:

```dart
// In main.dart or config
const String apiUrl = String.fromEnvironment(
  'API_URL',
  defaultValue: 'http://localhost:8080/analyze',
);
```

## Google Cloud Development

### Prerequisites

```bash
# Install Google Cloud SDK
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project linkedin-strategy-ai-assistant
```

### Deploy to Cloud Run

```bash
# Build and deploy
gcloud builds submit --substitutions=_LOCATION=us-central1

# Or use Cloud Build directly
gcloud builds submit

# Check deployment
gcloud run services describe linkedin-strategy-backend --region=us-central1
```

### Enable Required APIs

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable vision.googleapis.com
gcloud services enable firebasehosting.googleapis.com
```

## Common Development Tasks

### Add a New Dependency

```bash
# Add to requirements.txt
echo "package-name>=1.0.0" >> requirements.txt

# Install
pip install -r requirements.txt

# For testing dependencies, add with comment:
echo "pytest-mock>=3.0.0  # Testing" >> requirements.txt
```

### Add a New Endpoint

1. Open `src/app.py`
2. Add endpoint function:

```python
@app.get("/new-endpoint")
async def new_endpoint():
    """Endpoint description."""
    return {"message": "Hello"}
```

3. Add tests in `tests/test_api.py`
4. Run tests: `pytest tests/test_api.py::test_new_endpoint`

### Update Configuration

1. Edit `src/config.py`
2. Add new config variable
3. Update `.env` template in this guide
4. Update documentation

### Debug Issues

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
uvicorn src.app:app --reload --log-level debug

# Python debugger
# Add to code:
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Ensure you're in the project root
pwd

# Check virtual environment is activated
which python  # Should show .venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### Tesseract Not Found

**Problem:** `pytesseract.pytesseract.TesseractNotFound`

**Solution:**
```bash
# Install tesseract (see Prerequisites section)
# Then set path:
export TESSERACT_CMD=/usr/bin/tesseract  # Linux
export TESSERACT_CMD=/usr/local/bin/tesseract  # macOS
```

### Port Already in Use

**Problem:** `Error: [Errno 48] Address already in use`

**Solution:**
```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn src.app:app --reload --port 8081
```

### Docker Build Fails

**Problem:** `Docker build` fails with dependency errors

**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t linkedin-strategy-backend:dev .
```

## CI/CD Pipeline

Our GitHub Actions workflow runs on every push and PR:

1. **Test:** Runs unit and integration tests
2. **Docker Build:** Builds and tests Docker image
3. **Security Scan:** Trivy and Bandit security scans
4. **Lint:** Code style and documentation checks

View workflow runs: https://github.com/koreric75/LinkedInStrategyAsst/actions

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run tests: `pytest`
4. Format code: `black src/ tests/`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Create Pull Request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidelines.

## Getting Help

- **Documentation:** Check `/docs` directory
- **Issues:** [GitHub Issues](https://github.com/koreric75/LinkedInStrategyAsst/issues)
- **Architecture:** See `docs/ARCHITECTURE.md`

## Next Steps

- [ ] Set up local development environment
- [ ] Run all tests successfully
- [ ] Make a small change and test it
- [ ] Review architecture documentation
- [ ] Try deploying to Cloud Run (optional)
- [ ] Contribute your first feature!

---

**Happy Coding! 🚀**
