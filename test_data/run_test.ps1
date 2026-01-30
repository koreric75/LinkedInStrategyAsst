# Test the LinkedIn Strategy Assistant with mock data
Write-Host "Testing LinkedIn Strategy Assistant API..." -ForegroundColor Cyan

# API endpoint
$API_URL = "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze"

# Test file paths (in test_data folder)
$testDir = "C:\Users\korer\LinkedInStrategyAsst\test_data"
$resumePath = "$testDir\sample_resume.txt"
$screenshot1 = "$testDir\linkedin_screenshot_1.png"
$screenshot2 = "$testDir\linkedin_screenshot_2.png"

# Verify files exist
Write-Host "`nVerifying test files..." -ForegroundColor Yellow
if (!(Test-Path $resumePath)) {
    Write-Host "ERROR: Resume file not found at $resumePath" -ForegroundColor Red
    exit 1
}
if (!(Test-Path $screenshot1)) {
    Write-Host "ERROR: Screenshot 1 not found at $screenshot1" -ForegroundColor Red
    exit 1
}
if (!(Test-Path $screenshot2)) {
    Write-Host "ERROR: Screenshot 2 not found at $screenshot2" -ForegroundColor Red
    exit 1
}

Write-Host "✓ All test files found" -ForegroundColor Green

# Test each strategic mode
$modes = @("Get Hired", "Grow Connections", "Influence Market")

foreach ($mode in $modes) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Testing Mode: $mode" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    try {
        $form = @{
            mode = $mode
            resume = Get-Item -Path $resumePath
            screenshots = @(
                Get-Item -Path $screenshot1
                Get-Item -Path $screenshot2
            )
            use_cloud_vision = "false"
        }

        $response = Invoke-WebRequest -Uri $API_URL -Method Post -Form $form -UseBasicParsing
        $result = $response.Content | ConvertFrom-Json
        
        Write-Host "`n📊 CAREER STRATEGY DASHBOARD" -ForegroundColor Green
        Write-Host "Mode: $($result.mode)" -ForegroundColor White
        Write-Host "Profile Score: $($result.profile_score)/100" -ForegroundColor Yellow
        
        Write-Host "`n🔧 IMMEDIATE FIXES:" -ForegroundColor Green
        foreach ($fix in $result.immediate_fixes) {
            Write-Host "  • $fix" -ForegroundColor White
        }
        
        Write-Host "`n🗓️ 30-DAY ROADMAP:" -ForegroundColor Green
        foreach ($step in $result.strategic_roadmap) {
            Write-Host "  • $step" -ForegroundColor White
        }
        
        Write-Host "`n🔍 GAP ANALYSIS:" -ForegroundColor Green
        Write-Host "  Skills missing: $($result.gaps.skills_missing_from_linkedin -join ', ')" -ForegroundColor White
        Write-Host "  Advanced tech detected: $($result.gaps.advanced_tech_themes -join ', ')" -ForegroundColor White
        
        Write-Host "`n✅ Test PASSED for mode: $mode" -ForegroundColor Green
        
    } catch {
        Write-Host "`n❌ Test FAILED for mode: $mode" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
    }
    
    Start-Sleep -Seconds 2
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "All tests completed!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
