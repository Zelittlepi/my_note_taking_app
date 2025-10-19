#!/usr/bin/env python3
"""
Database Connection Diagnostic Tool
Tests connection to Supabase PostgreSQL database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_connection():
    """Test database connection with detailed diagnostics"""
    
    print("🔍 Database Connection Diagnostics")
    print("=" * 50)
    
    # 1. Check environment variables
    print("\n1. Environment Variables:")
    database_url = os.getenv('DATABASE_URL')
    print(f"   DATABASE_URL exists: {'✅' if database_url else '❌'}")
    
    if database_url:
        # Parse URL components (safely)
        if database_url.startswith('postgresql://'):
            parts = database_url.replace('postgresql://', '').split('@')
            if len(parts) >= 2:
                host_part = parts[1].split(':')[0] if ':' in parts[1] else parts[1].split('/')[0]
                print(f"   Host: {host_part}")
                print(f"   URL length: {len(database_url)} characters")
            else:
                print("   ⚠️  URL format appears malformed")
        else:
            print(f"   ⚠️  URL doesn't start with postgresql:// (starts with: {database_url[:20]}...)")
    
    # 2. Test basic connectivity
    print("\n2. Testing Database Libraries:")
    try:
        import psycopg2
        print("   psycopg2: ✅ Available")
    except ImportError as e:
        print(f"   psycopg2: ❌ Not available - {e}")
        
    try:
        import sqlalchemy
        print(f"   SQLAlchemy: ✅ Available (v{sqlalchemy.__version__})")
    except ImportError as e:
        print(f"   SQLAlchemy: ❌ Not available - {e}")
        return False
        
    if not database_url:
        print("\n❌ No DATABASE_URL found. Please check your .env file.")
        return False
    
    # 3. Test SQLAlchemy connection
    print("\n3. Testing SQLAlchemy Connection:")
    try:
        from sqlalchemy import create_engine, text
        
        # Fix postgres:// URL if needed
        if database_url.startswith('postgres://'):
            fixed_url = database_url.replace('postgres://', 'postgresql://')
            print("   🔧 Fixed URL scheme: postgres:// -> postgresql://")
        else:
            fixed_url = database_url
            
        # Create engine with connection options
        engine = create_engine(
            fixed_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=5,
            max_overflow=10,
            connect_args={
                'sslmode': 'require',
                'connect_timeout': 30,
            }
        )
        
        print("   🔧 Engine created successfully")
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   ✅ Connection successful!")
            print(f"   📊 PostgreSQL version: {version[:50]}...")
            
            # Test table creation capability
            conn.execute(text("CREATE TABLE IF NOT EXISTS test_connection (id SERIAL PRIMARY KEY, test_col TEXT)"))
            conn.execute(text("DROP TABLE IF EXISTS test_connection"))
            print("   ✅ Table creation/deletion works")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        
        # Common error diagnostics
        error_str = str(e).lower()
        if 'timeout' in error_str:
            print("   💡 Suggestion: Network timeout - check firewall/VPN")
        elif 'authentication' in error_str or 'password' in error_str:
            print("   💡 Suggestion: Check username/password in DATABASE_URL")
        elif 'connection refused' in error_str:
            print("   💡 Suggestion: Check host and port in DATABASE_URL")
        elif 'ssl' in error_str:
            print("   💡 Suggestion: SSL connection issue - check sslmode parameter")
        elif 'does not exist' in error_str:
            print("   💡 Suggestion: Database name might be incorrect")
            
        return False

def test_flask_integration():
    """Test Flask-SQLAlchemy integration"""
    print("\n4. Testing Flask Integration:")
    
    try:
        # Add src to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_dir)
        
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        app = Flask(__name__)
        
        database_url = os.getenv('DATABASE_URL')
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://')
            
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 5,
            'max_overflow': 10,
            'connect_args': {
                'sslmode': 'require',
                'connect_timeout': 30,
            }
        }
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            # Test database connection
            db.engine.execute('SELECT 1')
            print("   ✅ Flask-SQLAlchemy connection successful!")
            
            # Try importing models
            try:
                from models.note import Note
                from models.user import User
                print("   ✅ Models imported successfully")
                
                # Test table creation
                db.create_all()
                print("   ✅ Tables created successfully")
                
            except Exception as e:
                print(f"   ⚠️  Model/table issue: {e}")
                
        return True
        
    except Exception as e:
        print(f"   ❌ Flask integration failed: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("🚀 Starting Database Diagnostics...\n")
    
    success = test_connection()
    
    if success:
        test_flask_integration()
        print("\n🎉 Diagnostics Complete!")
        print("\n💡 If your app is still having issues, check:")
        print("   - Vercel environment variables are set correctly")
        print("   - Supabase database is running and accessible")
        print("   - No firewall blocking the connection")
    else:
        print("\n❌ Database connection failed. Please fix the issues above.")
        print("\n🔧 Common solutions:")
        print("   1. Verify DATABASE_URL in .env file")
        print("   2. Check Supabase dashboard for connection details")
        print("   3. Ensure your IP is whitelisted in Supabase")
        print("   4. Install required packages: pip install psycopg2-binary")

if __name__ == "__main__":
    main()