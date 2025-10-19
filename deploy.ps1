# PowerShell deployment script for NoteTaker App
Write-Host "🚀 NoteTaker App - Quick Deployment to Vercel" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if git is initialized
if (!(Test-Path ".git")) {
    Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# Add all files
Write-Host "📦 Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit changes
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
$commitMsg = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Deploy NoteTaker app to Vercel"
}
git commit -m $commitMsg

Write-Host ""
Write-Host "✅ Ready for deployment!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Push to GitHub:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/yourusername/notetaker-app.git" -ForegroundColor Gray
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Connect to Vercel:" -ForegroundColor White
Write-Host "   - Go to vercel.com" -ForegroundColor Gray
Write-Host "   - Import your GitHub repository" -ForegroundColor Gray
Write-Host "   - Add environment variables (DATABASE_URL, GITHUB_AI_TOKEN, SECRET_KEY)" -ForegroundColor Gray
Write-Host "   - Deploy!" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 See VERCEL_DEPLOYMENT_GUIDE.md for detailed instructions" -ForegroundColor Cyan

Pause