# 🔐 Security Configuration Guide

## SECRET_KEY Explained

### What is SECRET_KEY?
The `SECRET_KEY` is a cryptographic key used by Flask for:
- **Session Security**: Encrypting user session data
- **CSRF Protection**: Preventing Cross-Site Request Forgery attacks
- **Cookie Signing**: Preventing cookie tampering
- **Token Generation**: Creating secure tokens for various purposes

### Security Requirements:
✅ **Random**: Must be cryptographically random
✅ **Long**: At least 32 characters recommended
✅ **Unique**: Different for each environment
✅ **Secret**: Never exposed in code repositories

### ❌ Bad Examples:
- `SECRET_KEY=password123`
- `SECRET_KEY=myappname`
- `SECRET_KEY=wangzeshigedashuaige` (predictable)

### ✅ Good Examples:
- `SECRET_KEY=bbece6c281325bd2846130d4c57ce20ed116a297dca89ccd58da3180dcd111a8`
- `SECRET_KEY=pOA5l*gu*!Z1NsBRG#Elf2j6tLDt1Pge`

## Environment Variables for Deployment

### Development (.env file):
```env
SECRET_KEY=bbece6c281325bd2846130d4c57ce20ed116a297dca89ccd58da3180dcd111a8
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:180031@db.vbdzzryvrsqpmdrkhvxr.supabase.co:5432/postgres?sslmode=require
GITHUB_AI_TOKEN=your_github_token_here
```

### Production (Vercel Dashboard):
**Never store production secrets in .env files!**

Set these in Vercel Dashboard → Settings → Environment Variables:
- `SECRET_KEY` = Generate a NEW random key for production
- `DATABASE_URL` = Your Supabase production URL
- `GITHUB_AI_TOKEN` = Your GitHub AI token
- `FLASK_ENV` = `production`

## Quick Secret Key Generator

```python
import secrets
import os

# Method 1: Hex-based (recommended)
secret_key = os.urandom(32).hex()
print(f"SECRET_KEY={secret_key}")

# Method 2: Mixed characters
import string
alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
secret_key = ''.join(secrets.choice(alphabet) for _ in range(32))
print(f"SECRET_KEY={secret_key}")
```

## Security Checklist

- [ ] Use cryptographically random SECRET_KEY
- [ ] Different keys for development vs production
- [ ] Keys are at least 32 characters long
- [ ] Production keys set via Vercel dashboard
- [ ] .env files added to .gitignore
- [ ] Regular key rotation (monthly/quarterly)

## Vercel Deployment Security

1. **Set Environment Variables in Vercel:**
   - Go to your project dashboard
   - Settings → Environment Variables
   - Add all required variables
   - Select "Production" environment

2. **Never Commit .env to Git:**
   - Ensure `.env` is in `.gitignore`
   - Use `.env.example` for documentation

3. **Database Security:**
   - Use Supabase connection pooling
   - Enable SSL mode (already configured)
   - Rotate database passwords regularly