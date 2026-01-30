
import 'dart:convert';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const StrategyApp());
}

class StrategyApp extends StatelessWidget {
  const StrategyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LinkedIn Strategy Assistant',
      theme: ThemeData.dark(),
      home: const StrategyForm(),
    );
  }
}

class StrategyForm extends StatefulWidget {
  const StrategyForm({super.key});

  @override
  State<StrategyForm> createState() => _StrategyFormState();
}

class _StrategyFormState extends State<StrategyForm> {
  List<PlatformFile> screenshots = [];
  PlatformFile? resume;
  String mode = 'Get Hired';
  bool loading = false;
  Map<String, dynamic>? strategyData;
  final ImagePicker _picker = ImagePicker();
  
  // LinkedIn text input controllers
  final TextEditingController _headlineController = TextEditingController();
  final TextEditingController _aboutController = TextEditingController();
  final TextEditingController _currentRoleController = TextEditingController();
  final TextEditingController _skillsController = TextEditingController();
  final TextEditingController _certificationsController = TextEditingController();
  
  @override
  void dispose() {
    _headlineController.dispose();
    _aboutController.dispose();
    _currentRoleController.dispose();
    _skillsController.dispose();
    _certificationsController.dispose();
    super.dispose();
  }

  Future<void> importFromClipboard() async {
    try {
      final clipboardData = await Clipboard.getData(Clipboard.kTextPlain);
      if (clipboardData == null || clipboardData.text == null || clipboardData.text!.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Clipboard is empty. Please run the LinkedIn scraper first.'),
              backgroundColor: Colors.orange,
            ),
          );
        }
        return;
      }

      final jsonData = jsonDecode(clipboardData.text!) as Map<String, dynamic>;
      
      setState(() {
        _headlineController.text = jsonData['headline']?.toString() ?? '';
        _aboutController.text = jsonData['about']?.toString() ?? '';
        _currentRoleController.text = jsonData['current_role']?.toString() ?? '';
        _skillsController.text = jsonData['skills']?.toString() ?? '';
        _certificationsController.text = jsonData['certifications']?.toString() ?? '';
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('✅ Successfully imported LinkedIn data from clipboard!'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 3),
          ),
        );
      }
    } catch (e) {
      // Log technical details for developers
      debugPrint('Error importing clipboard data: $e');
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'The clipboard data is not in the expected format.\n\nPlease make sure you ran the LinkedIn scraper script successfully before clicking "Import from Clipboard".',
            ),
            backgroundColor: Colors.red,
            duration: Duration(seconds: 5),
          ),
        );
      }
    }
  }

  Future<void> openScraperInstructions() async {
    // Try GitHub Pages first, fallback to showing dialog
    const url = 'https://koreric75.github.io/LinkedInStrategyAsst/scraper-guide.html';
    final uri = Uri.parse(url);
    
    bool launched = false;
    try {
      if (await canLaunchUrl(uri)) {
        launched = await launchUrl(uri, mode: LaunchMode.externalApplication);
      }
    } catch (e) {
      launched = false;
    }
    
    // Show fallback dialog if URL couldn't be launched
    if (!launched && mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('LinkedIn Profile Scraper'),
            content: SingleChildScrollView(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Auto-extract your LinkedIn profile in 3 steps:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  const Text('1. Go to github.com/koreric75/LinkedInStrategyAsst'),
                  const SizedBox(height: 8),
                  const Text('2. Open linkedin_scraper.js, click "Raw", and copy all code (Ctrl+A, Ctrl+C)'),
                  const SizedBox(height: 8),
                  const Text('3. Go to your LinkedIn profile, press F12, click Console tab, paste the script, press Enter'),
                  const SizedBox(height: 8),
                  const Text('4. Return here and click "Import from Clipboard"'),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      '💡 The scraper runs locally in your browser and is 100% private. No data is sent to any server.',
                      style: TextStyle(fontSize: 13, fontStyle: FontStyle.italic),
                    ),
                  ),
                ],
              ),
            ),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Got it'),
              ),
            ],
          ),
        );
      }
    }
  }

  Future<void> pickScreenshots() async {
    final res = await FilePicker.platform.pickFiles(
      allowMultiple: true,
      type: FileType.image,
      withData: true,
    );
    if (res != null) {
      setState(() => screenshots = res.files);
    }
  }

  Future<void> takePhoto() async {
    final XFile? photo = await _picker.pickImage(source: ImageSource.camera);
    if (photo != null) {
      final bytes = await photo.readAsBytes();
      final file = PlatformFile(
        name: photo.name,
        size: bytes.length,
        bytes: bytes,
        path: photo.path,
      );
      setState(() => screenshots.add(file));
    }
  }

  Future<void> pickFromGallery() async {
    final List<XFile> images = await _picker.pickMultiImage();
    for (final image in images) {
      final bytes = await image.readAsBytes();
      final file = PlatformFile(
        name: image.name,
        size: bytes.length,
        bytes: bytes,
        path: image.path,
      );
      setState(() => screenshots.add(file));
    }
  }

  Future<void> pickResume() async {
    final res = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'doc', 'docx'],
      withData: true,
    );
    if (res != null && res.files.isNotEmpty) {
      setState(() => resume = res.files.first);
    }
  }

  Future<http.MultipartFile> _toMultipartFile(String field, PlatformFile file) async {
    if (file.bytes != null) {
      return http.MultipartFile.fromBytes(
        field,
        file.bytes!,
        filename: file.name,
      );
    }
    if (file.path != null) {
      return http.MultipartFile.fromPath(field, file.path!);
    }
    throw Exception('Missing file data for ${file.name}');
  }

  void removeScreenshot(int index) {
    setState(() => screenshots.removeAt(index));
  }

  Future<void> submit() async {
    if (resume == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please upload a resume')),
      );
      return;
    }

    // Require either screenshots OR manual text input
    final hasLinkedInData = screenshots.isNotEmpty ||
        _headlineController.text.isNotEmpty ||
        _aboutController.text.isNotEmpty ||
        _skillsController.text.isNotEmpty;
    
    if (!hasLinkedInData) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please provide LinkedIn data via screenshots or text fields')),
      );
      return;
    }

    setState(() {
      loading = true;
      strategyData = null;
    });

    const apiUrl = String.fromEnvironment(
      'API_URL',
      defaultValue: 'https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze',
    );
    final uri = Uri.parse(apiUrl);
    final request = http.MultipartRequest('POST', uri)
      ..fields['mode'] = mode;

    // Add LinkedIn text data if provided
    if (_headlineController.text.isNotEmpty ||
        _aboutController.text.isNotEmpty ||
        _currentRoleController.text.isNotEmpty ||
        _skillsController.text.isNotEmpty ||
        _certificationsController.text.isNotEmpty) {
      final linkedinText = jsonEncode({
        'headline': _headlineController.text.trim(),
        'about': _aboutController.text.trim(),
        'current_role': _currentRoleController.text.trim(),
        'skills': _skillsController.text.trim(),
        'certifications': _certificationsController.text.trim(),
      });
      request.fields['linkedin_text'] = linkedinText;
    }

    request.files.add(await _toMultipartFile('resume', resume!));
    for (final shot in screenshots) {
      request.files.add(await _toMultipartFile('screenshots', shot));
    }

    try {
      final response = await request.send();
      final body = await response.stream.bytesToString();

      final data = jsonDecode(body) as Map<String, dynamic>;
      
      setState(() {
        loading = false;
        strategyData = data;
      });
    } catch (e) {
      setState(() => loading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LinkedIn Strategy Assistant'),
        backgroundColor: Colors.blueAccent,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Text(
                          'LinkedIn Profile Data',
                          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(width: 8),
                        Tooltip(
                          message: 'For better accuracy, use the auto-scraper or copy/paste from your LinkedIn profile',
                          child: Icon(Icons.info_outline, size: 20, color: Colors.grey[400]),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [Colors.blue.shade700, Colors.blue.shade900],
                        ),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        children: [
                          const Row(
                            children: [
                              Icon(Icons.auto_awesome, color: Colors.white, size: 24),
                              SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  'Auto-Extract from LinkedIn',
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          const Text(
                            'Automatically scrape your LinkedIn profile in seconds! No manual copying required.',
                            style: TextStyle(color: Colors.white70, fontSize: 13),
                          ),
                          const SizedBox(height: 16),
                          Row(
                            children: [
                              Expanded(
                                child: ElevatedButton.icon(
                                  onPressed: openScraperInstructions,
                                  icon: const Icon(Icons.help_outline),
                                  label: const Text('How to Scrape'),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.white,
                                    foregroundColor: Colors.blue.shade900,
                                    padding: const EdgeInsets.symmetric(vertical: 12),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 12),
                              Expanded(
                                child: ElevatedButton.icon(
                                  onPressed: importFromClipboard,
                                  icon: const Icon(Icons.content_paste),
                                  label: const Text('Import from Clipboard'),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.green,
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(vertical: 12),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    const Divider(),
                    const SizedBox(height: 8),
                    const Text(
                      'Or manually enter your LinkedIn data below:',
                      style: TextStyle(fontSize: 13, color: Colors.grey, fontStyle: FontStyle.italic),
                    ),
                    const SizedBox(height: 16),
                    TextField(
                      controller: _headlineController,
                      decoration: const InputDecoration(
                        labelText: 'Headline',
                        hintText: 'e.g., Senior Software Engineer | Cloud & AI',
                        border: OutlineInputBorder(),
                        helperText: 'Copy from your LinkedIn profile headline',
                      ),
                      maxLines: 2,
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _aboutController,
                      decoration: const InputDecoration(
                        labelText: 'About Section',
                        hintText: 'Paste your full About/Summary section',
                        border: OutlineInputBorder(),
                        helperText: 'Your LinkedIn "About" text',
                      ),
                      maxLines: 6,
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _currentRoleController,
                      decoration: const InputDecoration(
                        labelText: 'Current Role',
                        hintText: 'e.g., Software Engineer at Google',
                        border: OutlineInputBorder(),
                      ),
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _skillsController,
                      decoration: const InputDecoration(
                        labelText: 'Skills (comma-separated)',
                        hintText: 'e.g., Python, Docker, Kubernetes, CI/CD, Cloud Run',
                        border: OutlineInputBorder(),
                        helperText: 'List your LinkedIn skills',
                      ),
                      maxLines: 3,
                    ),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _certificationsController,
                      decoration: const InputDecoration(
                        labelText: 'Certifications (comma-separated)',
                        hintText: 'e.g., AWS Certified, Google Cloud Professional',
                        border: OutlineInputBorder(),
                      ),
                      maxLines: 2,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'LinkedIn Profile Screenshots (Optional)',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      'Screenshots help assess visual engagement quality',
                      style: TextStyle(fontSize: 14, color: Colors.grey),
                    ),
                    const SizedBox(height: 12),
                    Wrap(
                      spacing: 8,
                      runSpacing: 8,
                      children: [
                        ElevatedButton.icon(
                          onPressed: takePhoto,
                          icon: const Icon(Icons.camera_alt),
                          label: const Text('Take Photo'),
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
                        ),
                        ElevatedButton.icon(
                          onPressed: pickFromGallery,
                          icon: const Icon(Icons.photo_library),
                          label: const Text('From Gallery'),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    if (screenshots.isNotEmpty)
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: screenshots.asMap().entries.map((entry) {
                          return Chip(
                            avatar: const Icon(Icons.image, size: 18),
                            label: Text(entry.value.name),
                            deleteIcon: const Icon(Icons.close, size: 18),
                            onDeleted: () => removeScreenshot(entry.key),
                          );
                        }).toList(),
                      ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Resume (PDF/DOC)',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    ElevatedButton.icon(
                      onPressed: pickResume,
                      icon: const Icon(Icons.upload_file),
                      label: Text(resume == null ? 'Select Resume' : 'Change Resume'),
                    ),
                    if (resume != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 12),
                        child: Row(
                          children: [
                            const Icon(Icons.check_circle, color: Colors.green, size: 20),
                            const SizedBox(width: 8),
                            Expanded(child: Text(resume!.name, style: const TextStyle(color: Colors.green))),
                          ],
                        ),
                      ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Strategy Mode',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 12),
                    DropdownButton<String>(
                      value: mode,
                      isExpanded: true,
                      items: const [
                        DropdownMenuItem(
                          value: 'Get Hired',
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Get Hired', style: TextStyle(fontWeight: FontWeight.bold)),
                              Text('Optimize for job search', style: TextStyle(fontSize: 12, color: Colors.grey)),
                            ],
                          ),
                        ),
                        DropdownMenuItem(
                          value: 'Grow Connections',
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Grow Connections', style: TextStyle(fontWeight: FontWeight.bold)),
                              Text('Expand your network', style: TextStyle(fontSize: 12, color: Colors.grey)),
                            ],
                          ),
                        ),
                        DropdownMenuItem(
                          value: 'Influence Market',
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Influence Market', style: TextStyle(fontWeight: FontWeight.bold)),
                              Text('Build thought leadership', style: TextStyle(fontSize: 12, color: Colors.grey)),
                            ],
                          ),
                        ),
                      ],
                      onChanged: (val) => setState(() => mode = val ?? 'Get Hired'),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: loading ? null : submit,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                backgroundColor: Colors.blueAccent,
                disabledBackgroundColor: Colors.grey,
              ),
              child: loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                    )
                  : const Text(
                      'Generate Strategy',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
            ),
            if (strategyData != null) ...[
              const SizedBox(height: 24),
              _buildStrategyReport(strategyData!),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStrategyReport(Map<String, dynamic> data) {
    final score = data['profile_score'] as int? ?? 0;
    final fixes = (data['immediate_fixes'] as List?)?.cast<String>() ?? [];
    final roadmap = (data['strategic_roadmap'] as List?)?.cast<String>() ?? [];
    final gaps = data['gaps'] as Map<String, dynamic>? ?? {};
    final mode = data['mode'] as String? ?? 'Unknown';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Header
        Card(
          elevation: 8,
          color: Colors.blue.shade900,
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.green.shade400.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Colors.green.shade400),
                  ),
                  child: Text(
                    'STRATEGIC MODE: $mode',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'AI Career Strategist Report',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'A data-driven roadmap to optimize your professional identity',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey.shade300,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Profile Score
        Card(
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                Stack(
                  alignment: Alignment.center,
                  children: [
                    SizedBox(
                      width: 160,
                      height: 160,
                      child: CircularProgressIndicator(
                        value: score / 100,
                        strokeWidth: 12,
                        backgroundColor: Colors.grey.shade200,
                        valueColor: AlwaysStoppedAnimation<Color>(
                          score >= 80 ? Colors.green : score >= 60 ? Colors.orange : Colors.red,
                        ),
                      ),
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          '$score',
                          style: const TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        Text(
                          'out of 100',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey.shade600,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                const Text(
                  'YOUR PROFILE STRENGTH',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  _getScoreDescription(score),
                  style: TextStyle(color: Colors.grey.shade700),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Gap Analysis
        Card(
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.orange.shade100,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(Icons.lightbulb, color: Colors.orange.shade700),
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      'Gap Analysis',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                _buildGapSection('Skills Missing from LinkedIn', gaps['skills_missing_from_linkedin']),
                _buildGapSection('Certifications Missing', gaps['certifications_missing_from_linkedin']),
                _buildGapSection('Projects Missing', gaps['projects_missing_from_linkedin']),
                _buildGapSection('Advanced Tech Themes Detected', gaps['advanced_tech_themes']),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // Immediate Fixes
        Card(
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.red.shade100,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Icon(Icons.build, color: Colors.red.shade700),
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      'Immediate Fixes',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                ...fixes.asMap().entries.map((entry) => Padding(
                  padding: const EdgeInsets.only(bottom: 12),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        width: 28,
                        height: 28,
                        decoration: BoxDecoration(
                          color: Colors.green.shade600,
                          shape: BoxShape.circle,
                        ),
                        child: Center(
                          child: Text(
                            '${entry.key + 1}',
                            style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                              fontSize: 14,
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          entry.value,
                          style: const TextStyle(fontSize: 15, height: 1.5),
                        ),
                      ),
                    ],
                  ),
                )),
              ],
            ),
          ),
        ),
        const SizedBox(height: 16),

        // 30-Day Roadmap
        Card(
          elevation: 4,
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.grey.shade800,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(Icons.calendar_month, color: Colors.white),
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      '30-DAY STRATEGIC ROADMAP',
                      style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, letterSpacing: 0.5),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                ...roadmap.asMap().entries.map((entry) {
                  final weekNum = entry.key + 1;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 20),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(
                          width: 50,
                          height: 50,
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [Colors.blue.shade600, Colors.blue.shade800],
                            ),
                            shape: BoxShape.circle,
                          ),
                          child: Center(
                            child: Text(
                              'W$weekNum',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Week $weekNum',
                                style: const TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blue,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                entry.value,
                                style: const TextStyle(fontSize: 15, height: 1.5),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                }),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildGapSection(String title, dynamic items) {
    final itemList = items is List ? items.cast<String>() : <String>[];
    if (itemList.isEmpty) return const SizedBox.shrink();

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Colors.blue,
            ),
          ),
          const SizedBox(height: 6),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: itemList.take(10).map((item) => Chip(
              label: Text(
                item,
                style: const TextStyle(fontSize: 11),
              ),
              backgroundColor: Colors.blue.shade50,
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            )).toList(),
          ),
          if (itemList.length > 10)
            Padding(
              padding: const EdgeInsets.only(top: 6),
              child: Text(
                '...and ${itemList.length - 10} more',
                style: TextStyle(fontSize: 12, color: Colors.grey.shade600, fontStyle: FontStyle.italic),
              ),
            ),
        ],
      ),
    );
  }

  String _getScoreDescription(int score) {
    if (score >= 80) {
      return 'Your profile is strong and well-optimized for your strategic goals.';
    } else if (score >= 60) {
      return 'Your profile has solid foundations but needs focused improvements.';
    } else if (score >= 40) {
      return 'Your profile needs significant optimization to stand out.';
    } else {
      return 'Your profile requires immediate attention to showcase your value.';
    }
  }
}

