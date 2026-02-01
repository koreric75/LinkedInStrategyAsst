# Testing Guide - LinkedIn Strategy Assistant v1.2

## Quick Test (API)

### 1. Test Text Input Mode (v1.2 - Recommended)
```powershell
cd test_data
python test_text_input.py
```

**Expected Output**:
- ✅ Profile Score 70-75+ (vs 36 with OCR failures)
- ✅ Accurate gap analysis (no missing skills due to OCR errors)
- ✅ All three modes tested (Get Hired, Grow Connections, Influence Market)

### 2. Test Screenshot OCR Mode (Fallback)
```powershell
cd test_data
python test_api.py
```

**Expected Output Features**:
- ✅ Executive summary with emoji score (🟢/🟡/🟠/🔴)
- ✅ Profile analysis with "Silent Wins" section
- ✅ Gap analysis table with coverage percentages
- ✅ Numbered immediate fixes with impact statements
- ✅ 30-day strategic roadmap (Week 1-4 breakdown)
- ✅ Projected outcomes (score increase, views, connections)
- ✅ Mode-specific strategies (Get Hired/Grow Connections/Influence Market)
- ✅ Quick start guide with pro tips

## Full Workflow Test (Flutter App)

### Prerequisites
1. Install Flutter SDK (see [flutter_app/MOBILE_GUIDE.md](flutter_app/MOBILE_GUIDE.md))
2. Run `flutter doctor` to verify setup

### Web Testing
```powershell
cd flutter_app
flutter pub get
flutter run -d chrome
```

**Test Steps (v1.2 - Text Input Mode)**:
1. Fill in **LinkedIn Profile Data** text fields
   - Headline: Copy from your LinkedIn profile
   - About: Paste your full About section
   - Current Role: Enter your current position
   - Skills: List comma-separated (e.g., "Python, Docker, Kubernetes")
   - Certifications: List comma-separated (e.g., "CompTIA Security+")
   
2. (Optional) Upload screenshots
   - Click **"Take Photo"** or **"From Gallery"**
   - Screenshots help assess visual engagement quality
   - Not required if text fields are filled
   
3. Upload resume
   - Click **"Select Resume"** button
   - Choose PDF or DOC file
   - Green checkmark appears with filename
   
4. Select strategy mode
   - Choose from dropdown:
     * **Get Hired** - Job search optimization
     * **Grow Connections** - Network expansion
     * **Influence Market** - Thought leadership
   
5. Generate strategy
   - Click **"Analyze Profile"** button
   - Loading spinner appears
   - Wait for API response (5-15 seconds)
   
6. Review results
   - Formatted strategy dashboard appears
   - Profile score, gap analysis, immediate fixes, 30-day roadmap
   - Score should be 70-75+ with accurate text input

### Mobile Testing (Android)

```powershell
# Connect Android device via USB
# Enable Developer Options + USB Debugging on device

flutter devices  # List connected devices
flutter run -d <device-id>
```

**Test Steps**:
1. Tap **"Take Photo"**
   - Camera opens directly
   - Capture LinkedIn profile screenshots
   - Photo added to chip list
   
2. Or tap **"From Gallery"**
   - Device gallery opens
   - Select multiple images
   - All added to chip list
   
3. Continue with upload/strategy selection as above

### Mobile Testing (iOS - macOS only)

```bash
# Connect iOS device via USB
# Trust computer on device

flutter devices  # List connected devices
flutter run -d <device-id>
```

## Verification Checklist

### Backend API
- [ ] `/health` endpoint returns `{"status":"ok"}`
- [ ] `/analyze` accepts multipart form data
- [ ] OCR extracts text from LinkedIn screenshots
- [ ] Resume parsing extracts skills/certs/projects
- [ ] Gap analysis compares resume vs LinkedIn
- [ ] Mode selection changes strategy output
- [ ] Dashboard includes all 8 sections
- [ ] Emoji indicators match score ranges
- [ ] Tables render with proper formatting
- [ ] Mode-specific content appears correctly

### Flutter App (Web)
- [ ] Camera access works in browser
- [ ] Screenshot preview displays as chips
- [ ] Remove screenshot function works
- [ ] Resume upload accepts PDF/DOC
- [ ] Mode dropdown shows all 3 options
- [ ] Loading state displays during API call
- [ ] Results render as selectable text
- [ ] Copy button works
- [ ] Scrollable result view

### Flutter App (Mobile)
- [ ] Camera permission requested on first use
- [ ] Take Photo opens native camera
- [ ] From Gallery opens native picker
- [ ] Multi-select works in gallery
- [ ] Chips display correctly on mobile
- [ ] Resume picker opens file manager
- [ ] API call works over mobile network
- [ ] Results responsive on small screens
- [ ] Markdown formatting preserved

## Performance Targets

### API Response Times
- OCR (per image): < 2 seconds
- Resume parsing: < 1 second
- Gap analysis: < 0.5 seconds
- Strategy generation: < 1 second
- **Total /analyze**: < 10 seconds for 2 images + resume

### Mobile App
- Camera launch: < 500ms
- Photo capture: < 1 second
- Upload progress: Visible feedback
- Results render: < 2 seconds after API response

## Troubleshooting

### API Errors
**"Missing screenshots or resume"**
- Ensure both file types uploaded
- Check Content-Type: multipart/form-data

**"OCR failed"**
- Verify screenshot clarity
- Check tesseract-ocr installation in Docker

**"Gap analysis empty"**
- Resume may lack structured data
- LinkedIn screenshots may be low quality

### Flutter App Errors
**Camera not working**
- Check permissions in AndroidManifest.xml/Info.plist
- Grant camera access in device settings
- Use physical device (not all emulators have camera)

**File picker crashes**
- Run `flutter clean && flutter pub get`
- Check file_picker and image_picker versions

**API timeout**
- Increase timeout in http package
- Check network connectivity
- Verify Cloud Run service is running

## Next Steps After Testing

1. **Collect Feedback**
   - Note UX pain points
   - Record feature requests
   - Document bugs

2. **Performance Optimization**
   - Profile slow API endpoints
   - Optimize OCR quality vs speed
   - Add caching for repeat users

3. **Feature Additions**
   - HTML report generation
   - Email delivery of strategy
   - History tracking
   - Progress dashboard

4. **Production Readiness**
   - Enable Cloud Vision API (better OCR)
   - Add Firebase Analytics
   - Implement rate limiting
   - Set up monitoring/alerting

## Support

- **API Logs**: https://console.cloud.google.com/run/detail/us-central1/linkedin-strategy-backend/logs
- **Build Logs**: https://console.cloud.google.com/cloud-build/builds
- **Flutter Issues**: https://github.com/flutter/flutter/issues
- **Project Docs**: See ENHANCEMENTS_SUMMARY.md, FEATURE_ROADMAP.md, MOBILE_GUIDE.md
