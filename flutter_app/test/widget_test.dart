// Flutter widget tests for LinkedIn Strategy Assistant
//
// Tests the core UI functionality including the LinkedIn profile scraper integration.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:linkedin_strategy_assistant/main.dart';

void main() {
  testWidgets('App renders main screen with LinkedIn Strategy Assistant title', (WidgetTester tester) async {
    // Build the app and trigger a frame.
    await tester.pumpWidget(const StrategyApp());

    // Verify that the app bar title is displayed.
    expect(find.text('LinkedIn Strategy Assistant'), findsOneWidget);
  });

  testWidgets('Auto-Extract section is displayed with scraper buttons', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Verify the Auto-Extract section header is present
    expect(find.text('Auto-Extract from LinkedIn'), findsOneWidget);

    // Verify the Copy Scraper Script button is present
    expect(find.text('Copy Scraper Script'), findsOneWidget);

    // Verify the Import Data button is present
    expect(find.text('Import Data'), findsOneWidget);
  });

  testWidgets('LinkedIn Profile Data section has manual input fields', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Verify manual input fields are present
    expect(find.text('LinkedIn Profile Data'), findsOneWidget);
    expect(find.text('Headline'), findsOneWidget);
    expect(find.text('About Section'), findsOneWidget);
    expect(find.text('Current Role'), findsOneWidget);
    expect(find.text('Skills (comma-separated)'), findsOneWidget);
    expect(find.text('Certifications (comma-separated)'), findsOneWidget);
  });

  testWidgets('Expand/collapse instructions toggle works', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Initially the detailed instructions should be collapsed
    expect(find.text('📋 How to Auto-Extract Your Profile:'), findsNothing);

    // Find and tap the expand button
    final expandButton = find.byIcon(Icons.expand_more);
    expect(expandButton, findsOneWidget);
    await tester.tap(expandButton);
    await tester.pumpAndSettle();

    // Now the instructions should be visible
    expect(find.text('📋 How to Auto-Extract Your Profile:'), findsOneWidget);
    expect(find.text('Copy the Scraper'), findsOneWidget);
    expect(find.text('Go to LinkedIn'), findsOneWidget);
    expect(find.text('Run the Script'), findsOneWidget);
    expect(find.text('Import Here'), findsOneWidget);
  });

  testWidgets('Strategy Mode dropdown is present', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Verify the strategy mode section is present
    expect(find.text('Strategy Mode'), findsOneWidget);
    expect(find.text('Get Hired'), findsWidgets);
  });

  testWidgets('Resume upload section is present', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Verify resume section is present
    expect(find.text('Resume (PDF/DOC)'), findsOneWidget);
    expect(find.text('Select Resume'), findsOneWidget);
  });

  testWidgets('Generate Strategy button is present', (WidgetTester tester) async {
    await tester.pumpWidget(const StrategyApp());

    // Verify the generate strategy button is present
    expect(find.text('Generate Strategy'), findsOneWidget);
  });
}
