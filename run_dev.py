#!/usr/bin/env python3
"""
Local development server with environment configuration
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app

if __name__ == '__main__':
    # Set development environment
    os.environ['FLASK_ENV'] = 'development'
    
    # Create database tables
    with app.app_context():
        from src.models.user import db
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    print("🚀 Starting NoteTaker development server...")
    print("📝 App will be available at: http://localhost:5001")
    print("🔧 Environment: Development")
    print("🗄️  Database: " + app.config['SQLALCHEMY_DATABASE_URI'])
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5001)),
        debug=True,
        use_reloader=True
    )