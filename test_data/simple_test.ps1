# Simple test of LinkedIn Strategy Assistant
$API_URL = "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze"

Write-Host "Testing Get Hired mode..." -ForegroundColor Cyan

$form = @{
    mode = "Get Hired"
    resume = Get-Item "C:\Users\korer\LinkedInStrategyAsst\test_data\sample_resume.txt"
    screenshots = @(
        Get-Item "C:\Users\korer\LinkedInStrategyAsst\test_data\linkedin_screenshot_1.png"
        Get-Item "C:\Users\korer\LinkedInStrategyAsst\test_data\linkedin_screenshot_2.png"
    )
    use_cloud_vision = "false"
}

$response = Invoke-WebRequest -Uri $API_URL -Method Post -Form $form -UseBasicParsing
$result = $response.Content | ConvertFrom-Json

Write-Host "`nProfile Score: $($result.profile_score)/100" -ForegroundColor Yellow
Write-Host "`nImmediate Fixes:" -ForegroundColor Green
$result.immediate_fixes | ForEach-Object { Write-Host "  - $_" }

Write-Host "`n30-Day Roadmap:" -ForegroundColor Green
$result.strategic_roadmap | ForEach-Object { Write-Host "  - $_" }

Write-Host "`nGap Analysis:" -ForegroundColor Green
Write-Host "Skills missing from LinkedIn: $($result.gaps.skills_missing_from_linkedin -join ', ')"
Write-Host "Advanced tech themes: $($result.gaps.advanced_tech_themes -join ', ')"

Write-Host "`n✅ Test completed successfully!" -ForegroundColor Green
