#!/bin/bash
# Quick deployment script for NoteTaker App

echo "🚀 NoteTaker App - Quick Deployment to Vercel"
echo "============================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "📦 Adding files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy NoteTaker app to Vercel"
fi
git commit -m "$commit_msg"

echo ""
echo "✅ Ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub:"
echo "   git remote add origin https://github.com/yourusername/notetaker-app.git"
echo "   git push -u origin main"
echo ""
echo "2. Connect to Vercel:"
echo "   - Go to vercel.com"
echo "   - Import your GitHub repository"
echo "   - Add environment variables (DATABASE_URL, GITHUB_AI_TOKEN, SECRET_KEY)"
echo "   - Deploy!"
echo ""
echo "📖 See VERCEL_DEPLOYMENT_GUIDE.md for detailed instructions"