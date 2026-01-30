# Test API with PowerShell
$API_URL = "https://linkedin-strategy-backend-796550517938.us-central1.run.app/analyze"

# Create sample test files (replace with actual paths)
$resumePath = "C:\path\to\your\resume.pdf"
$screenshot1 = "C:\path\to\linkedin-screenshot1.png"
$screenshot2 = "C:\path\to\linkedin-screenshot2.png"

# Test API endpoint
$form = @{
    mode = "Get Hired"
    resume = Get-Item -Path $resumePath
    screenshots = @(
        Get-Item -Path $screenshot1
        Get-Item -Path $screenshot2
    )
    use_cloud_vision = "false"
}

$response = Invoke-WebRequest -Uri $API_URL -Method Post -Form $form -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Alternative: Test with curl (if available)
# curl -X POST $API_URL `
#   -F "mode=Get Hired" `
#   -F "resume=@$resumePath" `
#   -F "screenshots=@$screenshot1" `
#   -F "screenshots=@$screenshot2" `
#   -F "use_cloud_vision=false"
