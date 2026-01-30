# Mobile Development Guide

## Flutter App - LinkedIn Strategy Assistant

### Features
✅ **Mobile Camera Integration** - Capture LinkedIn screenshots directly from the app  
✅ **Gallery Upload** - Select multiple screenshots from device gallery  
✅ **Resume Upload** - PDF/DOC support for resume parsing  
✅ **Strategy Modes** - Get Hired, Grow Connections, Influence Market  
✅ **Rich Dashboard** - Content-rich markdown reports with emojis and tables

### Prerequisites

1. **Install Flutter SDK** (Windows)
   ```powershell
   # Download Flutter SDK
   # Visit: https://docs.flutter.dev/get-started/install/windows
   
   # Extract to C:\src\flutter (or your preferred location)
   
   # Add to PATH
   $env:Path += ";C:\src\flutter\bin"
   [System.Environment]::SetEnvironmentVariable('Path', $env:Path, [System.EnvironmentVariableTarget]::User)
   
   # Verify installation
   flutter doctor
   ```

2. **Install Android Studio** (for Android development)
   - Download from https://developer.android.com/studio
   - Install Android SDK and accept licenses:
     ```powershell
     flutter doctor --android-licenses
     ```

3. **Install Xcode** (for iOS development - macOS only)
   - Download from Mac App Store
   - Install CocoaPods:
     ```bash
     sudo gem install cocoapods
     ```

### Setup

1. **Navigate to Flutter app directory**
   ```powershell
   cd flutter_app
   ```

2. **Install dependencies**
   ```powershell
   flutter pub get
   ```

3. **Verify setup**
   ```powershell
   flutter doctor -v
   ```

### Running the App

#### Web (Chrome)
```powershell
flutter run -d chrome
```

#### Android Emulator
```powershell
# List available devices
flutter devices

# Run on emulator
flutter run -d emulator-5554
```

#### iOS Simulator (macOS only)
```bash
# Open simulator
open -a Simulator

# Run on simulator
flutter run -d "iPhone 15 Pro"
```

#### Physical Device
```powershell
# Connect device via USB
# Enable USB debugging (Android) or Developer Mode (iOS)

# Run on device
flutter run
```

### Building for Production

#### Android APK
```powershell
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

#### Android App Bundle (Google Play)
```powershell
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
```

#### iOS (macOS only)
```bash
flutter build ios --release
# Then use Xcode to archive and distribute
```

### Mobile-Specific Features

#### Camera Permissions
- **Android**: Configured in `android/app/src/main/AndroidManifest.xml`
- **iOS**: Configured in `ios/Runner/Info.plist`

#### Screenshot Capture Flow
1. Tap "Take Photo" button → Camera opens
2. Capture LinkedIn profile sections:
   - Headline and profile picture
   - About section
   - Activity/Experience section
3. Review captured screenshots (displayed as chips)
4. Remove unwanted screenshots with X button
5. Upload resume (PDF/DOC)
6. Select strategy mode
7. Tap "Generate Strategy"

#### Gallery Upload Flow
1. Tap "From Gallery" button
2. Select multiple screenshots from device
3. Continue with same flow as camera capture

### API Configuration

The app is pre-configured to use the production Cloud Run endpoint:
```dart
const apiUrl = 'https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze';
```

For local development, change to:
```dart
const apiUrl = 'http://localhost:8080/analyze';
```

### Troubleshooting

#### Camera not working on Android
- Check permissions in device settings
- Verify `AndroidManifest.xml` has camera permissions
- Ensure physical device (not emulator) or emulator has camera support

#### File picker not working
```powershell
flutter clean
flutter pub get
```

#### Build errors
```powershell
# Clear build cache
flutter clean

# Update dependencies
flutter pub upgrade

# Regenerate platform files
flutter create --platforms=android,ios,web .
```

### Project Structure
```
flutter_app/
├── lib/
│   └── main.dart           # Main UI with camera integration
├── android/
│   └── app/src/main/AndroidManifest.xml  # Android permissions
├── ios/
│   └── Runner/Info.plist   # iOS permissions
├── pubspec.yaml            # Dependencies
└── README.md               # This file
```

### Dependencies
- `file_picker: ^6.1.1` - File system access
- `http: ^1.2.0` - API communication
- `image_picker: ^1.0.7` - Camera and gallery integration

### Next Steps
- [ ] Install Flutter SDK
- [ ] Run `flutter doctor` to verify setup
- [ ] Run `flutter pub get` to install dependencies
- [ ] Test on web: `flutter run -d chrome`
- [ ] Test on Android device/emulator
- [ ] Deploy to Google Play Store / Apple App Store
