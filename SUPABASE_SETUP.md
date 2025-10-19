# 🚀 Supabase Setup Guide for NoteTaker App

## Step 1: Create New Supabase Project

1. **Go to**: https://supabase.com/dashboard
2. **Click**: "New Project"
3. **Fill in**:
   - Organization: Your organization
   - Name: `notetaker-app` (or any name you prefer)
   - Database Password: Create a strong password (save it!)
   - Region: Choose closest to you (e.g., US East, US West, Europe)

## Step 2: Get Database Connection String

After project creation:
1. **Go to**: Settings → Database
2. **Find**: "Connection pooling" section
3. **Copy**: The URI that looks like:
   ```
   postgresql://postgres.abcdefghijklmnop:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
   ```

## Step 3: Update Your .env File

Replace the current DATABASE_URL in your .env file with the new one:

```bash
# Replace this line:
DATABASE_URL=postgresql://postgres:180031@db.vbdzzryvrsqpmdrkhvxr.supabase.co:5432/postgres?sslmode=require

# With your new connection string:
DATABASE_URL=postgresql://postgres.abcdefghijklmnop:[YOUR-PASSWORD]@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

## Step 4: Test Connection

Run this command to test:
```bash
python test_db_connection.py
```

## Step 5: Update Vercel Environment Variables

1. Go to Vercel dashboard
2. Find your project
3. Settings → Environment Variables
4. Update DATABASE_URL with the new connection string
5. Redeploy

## 📋 Connection String Format

Standard Supabase format:
```
postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

## 🔧 Troubleshooting

If you still have issues:
1. **Check password**: Ensure no special characters that need URL encoding
2. **Check region**: Make sure the region matches your project
3. **Check firewall**: Some networks block database connections
4. **Check project status**: Ensure project is not paused in Supabase dashboard

## ✅ Success Indicators

You'll know it's working when:
- DNS resolution works for your hostname
- Connection test passes
- Flask app starts without database errors
- Tables are created successfully