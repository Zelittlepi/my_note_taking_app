# 🚀 Vercel Deployment Guide for NoteTaker App

## Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Supabase Account** - Sign up at [supabase.com](https://supabase.com)

## 📋 Step-by-Step Deployment Guide

### Step 1: Set up Supabase Database

1. **Create a Supabase Project:**
   - Go to [supabase.com](https://supabase.com)
   - Click "New Project"
   - Choose your organization
   - Enter project name: `notetaker-db`
   - Set a strong database password
   - Choose a region close to your users
   - Click "Create new project"

2. **Get Database Connection String:**
   - Go to Settings → Database
   - Find "Connection string" section
   - Copy the "URI" connection string
   - It looks like: `postgresql://postgres.abcdefg:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres`

3. **Configure Database Security:**
   - Go to Settings → API
   - Note your `anon` and `service_role` keys (you won't need them for this Flask app)
   - Go to Authentication → Settings
   - Disable "Enable email confirmations" for now (optional)

### Step 2: Prepare Your Code for Deployment

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - NoteTaker app"
   git branch -M main
   git remote add origin https://github.com/yourusername/notetaker-app.git
   git push -u origin main
   ```

### Step 3: Deploy to Vercel

1. **Connect GitHub to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Select your `notetaker-app` repository

2. **Configure Environment Variables:**
   - In the Vercel dashboard, go to your project
   - Click "Settings" → "Environment Variables"
   - Add the following variables:

   ```
   DATABASE_URL = postgresql://postgres.abcdefg:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   GITHUB_AI_TOKEN = your_github_copilot_token
   SECRET_KEY = your-random-secret-key-here
   FLASK_ENV = production
   ```

3. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-app-name.vercel.app`

### Step 4: Initialize Database Tables

After deployment, you need to create the database tables:

1. **Option A: Use Supabase SQL Editor:**
   - Go to your Supabase project
   - Click "SQL Editor"
   - Run this SQL to create the tables:

   ```sql
   -- Create notes table
   CREATE TABLE note (
       id SERIAL PRIMARY KEY,
       title VARCHAR(200) NOT NULL,
       content TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Create update trigger for updated_at
   CREATE OR REPLACE FUNCTION update_updated_at_column()
   RETURNS TRIGGER AS $$
   BEGIN
       NEW.updated_at = CURRENT_TIMESTAMP;
       RETURN NEW;
   END;
   $$ language 'plpgsql';

   CREATE TRIGGER update_note_updated_at BEFORE UPDATE
   ON note FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
   ```

2. **Option B: Use the API endpoint:**
   - Visit: `https://your-app-name.vercel.app/health`
   - This will trigger table creation automatically

### Step 5: Test Your Deployment

1. **Visit your app:** `https://your-app-name.vercel.app`
2. **Test functionality:**
   - Create a new note
   - Edit and save notes
   - Test translation feature
   - Test auto-completion feature
   - Delete notes

## 🔧 Configuration Details

### Environment Variables Explained

- **DATABASE_URL**: Your Supabase PostgreSQL connection string
- **GITHUB_AI_TOKEN**: Your GitHub Copilot API token for AI features
- **SECRET_KEY**: Flask secret key for sessions (generate a random string)
- **FLASK_ENV**: Set to "production" for Vercel deployment

### Files Created for Vercel

- `vercel.json` - Vercel deployment configuration
- `runtime.txt` - Python version specification
- `api/index.py` - Vercel serverless function entry point
- `.vercelignore` - Files to ignore during deployment
- `src/config.py` - Database configuration for different environments

## 🔍 Troubleshooting

### Common Issues:

1. **Database Connection Errors:**
   - Verify DATABASE_URL is correct
   - Check Supabase project is active
   - Ensure database password is correct

2. **Import Errors:**
   - Check all dependencies are in `requirements.txt`
   - Verify Python path configuration

3. **Static Files Not Loading:**
   - Check `vercel.json` routing configuration
   - Verify static files are in `src/static/`

4. **AI Features Not Working:**
   - Verify GITHUB_AI_TOKEN is set correctly
   - Check API quota limits

### Deployment Commands

```bash
# Install Vercel CLI (optional)
npm install -g vercel

# Deploy from command line
vercel

# Set environment variables via CLI
vercel env add DATABASE_URL
vercel env add GITHUB_AI_TOKEN
vercel env add SECRET_KEY
```

## 🔄 Updating Your App

To update your deployed app:

1. Make changes to your code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Vercel will automatically redeploy

## 📊 Monitoring

- **Vercel Dashboard**: Monitor deployments, logs, and analytics
- **Supabase Dashboard**: Monitor database usage and performance
- **Logs**: Check Vercel function logs for debugging

## 💡 Production Tips

1. **Database Backup**: Supabase provides automatic backups
2. **Monitoring**: Set up alerts for errors and performance
3. **Scaling**: Vercel and Supabase auto-scale based on usage
4. **Security**: Regularly rotate your SECRET_KEY and API tokens
5. **Performance**: Consider adding Redis caching for frequent queries

Your NoteTaker app is now ready for production! 🎉