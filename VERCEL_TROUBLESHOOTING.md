# 🔧 Vercel Deployment Troubleshooting Guide

## Common 500 Internal Server Error Causes

### 1. **Import Errors**
❌ **Problem**: Python modules not found in serverless environment
✅ **Solution**: Fixed with proper path management in `api/index.py`

### 2. **Database Connection Issues**
❌ **Problem**: PostgreSQL connection fails in serverless function
✅ **Solution**: Added connection pooling and timeout configuration

### 3. **Environment Variable Issues**
❌ **Problem**: Missing or incorrect environment variables
✅ **Solution**: Added fallback configurations and better error handling

## 🚀 Deployment Steps (Updated)

### Step 1: Verify Environment Variables in Vercel
Go to your Vercel project dashboard → Settings → Environment Variables:

**Required Variables:**
```
DATABASE_URL = your_supabase_database_url_here
SECRET_KEY = your_secure_random_secret_key_here
GITHUB_AI_TOKEN = your_github_copilot_token_here
```

**Example formats:**
```
DATABASE_URL = postgresql://postgres:your_password@db.abc123xyz.supabase.co:5432/postgres?sslmode=require
SECRET_KEY = a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
GITHUB_AI_TOKEN = github_pat_11ABC123_example_token_xyz789
```

⚠️ **Important**: Replace these with your actual values from:
- Supabase: Your project's database connection string
- GitHub: Your personal access token for Copilot
- Secret Key: Generate a secure random key (32+ characters)

### Step 2: Check Database Connection
1. **Test Supabase Connection:**
   - Go to your Supabase dashboard
   - Verify project is active
   - Test connection string

2. **Create Tables in Supabase:**
   ```sql
   CREATE TABLE IF NOT EXISTS note (
       id SERIAL PRIMARY KEY,
       title VARCHAR(200) NOT NULL,
       content TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### Step 3: Deploy with Fixed Configuration
1. **Push Changes to GitHub:**
   ```bash
   git add .
   git commit -m "Fix serverless deployment issues"
   git push
   ```

2. **Vercel will auto-deploy** the updated configuration

### Step 4: Test Deployment
Visit these endpoints to verify:
- `https://your-app.vercel.app/` - Main app
- `https://your-app.vercel.app/health` - Health check
- `https://your-app.vercel.app/api/debug` - Debug info

## 🔍 Debugging Commands

### Check Vercel Logs:
```bash
# Install Vercel CLI
npm install -g vercel

# View function logs
vercel logs

# View real-time logs
vercel logs --follow
```

### Test Locally Before Deployment:
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python run_dev.py
```

## 🛠️ Changes Made to Fix Issues

### 1. **Fixed API Entry Point** (`api/index.py`)
- Proper path management for imports
- Fallback error handling
- Better module loading

### 2. **Updated Main App** (`src/main.py`)
- Removed `@app.before_first_request` (deprecated in Flask 2.2+)
- Added try/catch for imports
- Better database configuration
- Improved error handling

### 3. **Simplified Dependencies** (`requirements.txt`)
- Removed unnecessary packages
- Kept only essential dependencies for serverless

### 4. **Updated Vercel Config** (`vercel.json`)
- Changed build source to `api/index.py`
- Simplified routing
- Removed conflicting configuration

## 🚨 If Still Getting Errors

### 1. Check Vercel Function Logs:
- Go to Vercel Dashboard → Your Project → Functions tab
- Click on the failed function to see error logs

### 2. Test Debug Endpoint:
Visit: `https://your-app.vercel.app/api/debug`

### 3. Common Error Solutions:

**Error: "Module not found"**
- Check that all files are properly committed to Git
- Verify import paths are correct

**Error: "Database connection failed"**
- Verify DATABASE_URL is set correctly in Vercel
- Check Supabase project is active
- Test connection string format

**Error: "Environment variables not set"**
- Go to Vercel Dashboard → Settings → Environment Variables
- Ensure all required variables are set for "Production" environment
- Redeploy after adding variables

### 4. Force Fresh Deployment:
```bash
# Clear Vercel cache and redeploy
vercel --prod --force
```

## ✅ Success Indicators

When deployment is successful, you should see:
- ✅ Health endpoint returns JSON response
- ✅ Main page loads without errors  
- ✅ API endpoints respond correctly
- ✅ Database operations work
- ✅ No 500 errors in Vercel logs

## 📞 Still Need Help?

If issues persist:
1. Check the Vercel function logs for specific error messages
2. Test the debug endpoint for environment information
3. Verify all environment variables are correctly set
4. Ensure database tables exist in Supabase