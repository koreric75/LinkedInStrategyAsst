# Architecture Documentation

## System Overview

The LinkedIn Strategy Assistant is a cloud-native AI-powered career growth platform built with modern microservices architecture.

### Technology Stack

**Backend:**
- **Language:** Python 3.11
- **Framework:** FastAPI (async web framework)
- **Deployment:** Google Cloud Run (serverless containers)
- **OCR:** Google Cloud Vision API / Tesseract (fallback)
- **Authentication:** Firebase Admin SDK (optional)

**Frontend:**
- **Framework:** Flutter (web/mobile)
- **Hosting:** Firebase Hosting

**Infrastructure:**
- **Container Registry:** Google Container Registry (GCR)
- **CI/CD:** GitHub Actions
- **Build:** Cloud Build

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Flutter Web/Mobile App                                      │
│  - File Upload (Resume, Screenshots)                         │
│  - Manual Text Input Form                                    │
│  - Strategy Dashboard Display                                │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Application (Cloud Run)                             │
│  - POST /analyze (main endpoint)                             │
│  - GET /health (health check)                                │
│  - CORS Middleware                                           │
│  - Firebase Auth (optional)                                  │
│  - Input Validation                                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                     Processing Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Pipeline Module (src/pipeline.py)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. LinkedIn Profile Extraction                       │   │
│  │    - Manual Text Input (preferred)                   │   │
│  │    - OCR from Screenshots (Vision API/Tesseract)     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 2. Resume Parsing                                    │   │
│  │    - PDF (pdfplumber)                                │   │
│  │    - DOCX (python-docx)                              │   │
│  │    - TXT (plain text)                                │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 3. Gap Analysis                                      │   │
│  │    - Skills Comparison                               │   │
│  │    - Certifications Comparison                       │   │
│  │    - Projects Detection                              │   │
│  │    - Advanced Tech Themes                            │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 4. Strategy Generation                               │   │
│  │    - LinkedIn Optimizer (enhanced)                   │   │
│  │    - Mode-specific recommendations                   │   │
│  │    - Profile Scoring                                 │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
├─────────────────────────────────────────────────────────────┤
│  - Google Cloud Vision API (OCR)                             │
│  - Firebase Auth (authentication)                            │
│  - Firebase Hosting (static web hosting)                     │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Layer (src/app.py)

**Responsibilities:**
- HTTP request handling
- Input validation and sanitization
- File upload management
- Authentication (optional Firebase)
- Error handling and logging

**Key Features:**
- Async request processing
- CORS support for cross-origin requests
- Configurable file size limits
- Comprehensive error responses

### 2. Configuration (src/config.py)

**Responsibilities:**
- Centralized configuration management
- Environment variable support
- Validation of configuration values

**Configurable Parameters:**
- Server settings (host, port)
- CORS origins
- File upload limits
- OCR settings
- Logging levels

### 3. Processing Pipeline (src/pipeline.py)

**Responsibilities:**
- LinkedIn profile extraction (OCR or manual)
- Resume parsing (multiple formats)
- Gap analysis between LinkedIn and resume
- Strategy generation based on career mode

**Supported File Formats:**
- Resume: PDF, DOCX, DOC, TXT
- Screenshots: PNG, JPG, JPEG

### 4. LinkedIn Optimizer (src/linkedin_optimizer.py)

**Responsibilities:**
- Enhanced recommendation generation
- LinkedIn best practices application
- Keyword optimization
- Profile completeness assessment

**Best Practices Applied:**
- Headline optimization (220 char limit)
- About section structure (1500-2600 chars)
- Skills maximization (50 skills)
- Keyword placement strategy

### 5. Logging (src/logger.py)

**Responsibilities:**
- Structured logging across application
- Configurable log levels
- Consistent log formatting

## Data Flow

### Analyze Request Flow

1. **Client Request:**
   - User uploads resume file
   - User provides LinkedIn data (text or screenshots)
   - User selects career mode

2. **API Validation:**
   - Validate file formats and sizes
   - Validate mode parameter
   - Optional Firebase authentication

3. **Profile Extraction:**
   - If `linkedin_text` provided: parse JSON
   - If `screenshots` provided: OCR extraction
   - Cloud Vision API (preferred) or Tesseract (fallback)

4. **Resume Parsing:**
   - Detect file format
   - Extract skills, projects, certifications, experience
   - Text normalization

5. **Gap Analysis:**
   - Compare LinkedIn skills vs resume skills
   - Identify missing certifications
   - Detect advanced technology themes
   - Generate completeness metrics

6. **Strategy Generation:**
   - Calculate profile score (0-100)
   - Generate immediate fixes (top 5-6 items)
   - Create 4-5 week strategic roadmap
   - Mode-specific customization

7. **Response:**
   - JSON with analysis results
   - Markdown-formatted dashboard
   - Gap details and metrics

## Deployment Architecture

### Google Cloud Run

**Benefits:**
- Auto-scaling (0 to N instances)
- Pay-per-use pricing
- Serverless (no infrastructure management)
- Global availability

**Configuration:**
- Region: us-central1
- Max instances: Auto-scaled
- Port: 8080
- Memory: 512MB - 2GB (configurable)

### CI/CD Pipeline

**GitHub Actions Workflow:**
1. **Test:** Unit tests, integration tests
2. **Build:** Docker image build
3. **Security Scan:** Trivy, Bandit
4. **Deploy:** Cloud Build → Cloud Run

## Security Considerations

### Input Validation
- File type validation (whitelist approach)
- File size limits (10MB default)
- JSON schema validation
- SQL injection prevention (no SQL used)

### Authentication
- Optional Firebase authentication
- Bearer token validation
- User context logging

### CORS
- Configurable allowed origins
- Credentials support
- Preflight handling

### Data Privacy
- No persistent storage of uploaded files
- Temporary directory cleanup
- No logging of sensitive data

## Performance Characteristics

### Latency
- Manual text input: ~2-5 seconds
- Screenshot OCR (Cloud Vision): ~5-10 seconds
- Screenshot OCR (Tesseract): ~10-20 seconds

### Throughput
- Concurrent requests: Limited by Cloud Run instances
- Auto-scaling based on load

### Optimization Opportunities
- [ ] Caching of resume parse results
- [ ] Parallel OCR processing
- [ ] Async strategy generation
- [ ] Result memoization

## Monitoring and Observability

### Logging
- Structured JSON logs
- Request/response logging
- Error tracking with stack traces
- Performance metrics

### Health Checks
- `/health` endpoint
- Service status
- Dependency availability checks

### Metrics (Recommended)
- Request count
- Response time (p50, p95, p99)
- Error rate
- OCR processing time
- File upload sizes

## Scalability

### Horizontal Scaling
- Cloud Run auto-scales instances
- Stateless design (no session storage)
- Concurrent request handling

### Vertical Scaling
- Configurable memory limits
- CPU allocation per request

### Bottlenecks
- OCR processing (CPU-intensive)
- Large file uploads (network I/O)
- Resume parsing (file I/O)

## Error Handling

### HTTP Status Codes
- **200:** Successful analysis
- **400:** Invalid input (bad request)
- **401:** Authentication failure
- **422:** Validation error
- **500:** Internal server error

### Error Responses
```json
{
  "detail": "Descriptive error message"
}
```

### Logging
- All errors logged with stack traces
- Request context included
- User ID (if authenticated)

## Configuration Management

### Environment Variables

Required:
- None (all have defaults)

Optional:
- `PORT`: Server port (default: 8080)
- `HOST`: Server host (default: 0.0.0.0)
- `DEBUG`: Debug mode (default: false)
- `CORS_ORIGINS`: Allowed CORS origins (default: *)
- `LOG_LEVEL`: Logging level (default: INFO)
- `USE_CLOUD_VISION_DEFAULT`: Default OCR method (default: true)

### Secrets Management
- Firebase Admin SDK: `firebase-adminsdk.json`
- Google Cloud credentials: Service account JSON

## Testing Strategy

### Unit Tests
- Pipeline functions
- Data models
- Text extraction
- Gap analysis logic

### Integration Tests
- API endpoints
- File upload handling
- Error scenarios
- CORS headers

### Test Coverage
- Target: >80% code coverage
- Critical paths: 100% coverage

## Future Enhancements

### Performance
- Redis caching layer
- Async OCR processing
- Background job queue

### Features
- Profile analytics dashboard
- Historical tracking
- A/B testing of strategies
- Multi-language support

### Infrastructure
- Database for user history
- Cloud Storage for file caching
- CDN for static assets
- Rate limiting

## Maintenance

### Dependencies
- Update requirements.txt monthly
- Security patches within 48 hours
- Python version: Follow Google Cloud Run support

### Monitoring
- Set up alerting for errors
- Track response time degradation
- Monitor cost metrics

### Backups
- No database (stateless)
- Configuration in version control
- Container images in registry
