# LinkedIn Strategy Assistant - Flutter Client (v1.1)

**NEW in v1.1:** Manual text input for LinkedIn data - just copy/paste from your profile!

## Features
- **Text Input Mode (v1.1)** - Copy/paste LinkedIn profile data for 100% accuracy
- **Screenshot Upload** - Optional camera/gallery integration for visual assessment
- **Resume Upload** - PDF/DOC support via file picker
- **Strategic Modes** - Get Hired, Grow Connections, Influence Market
- **Formatted Dashboard** - Profile score, gap analysis, immediate fixes, 30-day roadmap
- **Cross-Platform** - Web (Chrome), Android, iOS support

## Quick Start

### Web (Chrome)
```bash
flutter pub get
flutter run -d chrome --dart-define API_URL=https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze
```

### Android
```bash
flutter pub get
flutter run -d <device-id>
```

### iOS (macOS only)
```bash
flutter pub get
flutter run -d <device-id>
```

## How to Use (v1.1)

1. **Fill LinkedIn Profile Data (Recommended)**
   - Copy headline from LinkedIn → paste into Headline field
   - Copy About section → paste into About field
   - Enter current role
   - List skills (comma-separated)
   - List certifications (comma-separated)

2. **OR Upload Screenshots (Optional)**
   - Tap "Take Photo" to capture LinkedIn profile
   - Or "From Gallery" to select existing screenshots
   - Screenshots used for visual engagement assessment

3. **Upload Resume**
   - Tap "Select Resume"
   - Choose PDF or DOC file

4. **Select Strategic Mode**
   - Get Hired - Job search optimization
   - Grow Connections - Network expansion
   - Influence Market - Thought leadership

5. **Analyze**
   - Tap "Analyze Profile"
   - View formatted strategy dashboard
   - Profile score 70-75+ with accurate text input!

## Configuration

### API URL (Development)

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
