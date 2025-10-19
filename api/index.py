import os
import sys
import traceback

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

# Try to import the main app with better error handling
try:
    from src.main import app
    print("✅ Successfully imported main app")
except Exception as e:
    print(f"❌ Failed to import main app: {str(e)}")
    print("Traceback:", traceback.format_exc())
    
    # Create a fallback Flask app
    from flask import Flask, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def fallback_root():
        return jsonify({
            'status': 'error',
            'message': 'Main app import failed',
            'error': str(e),
            'environment_check': {
                'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Missing',
                'SECRET_KEY': 'Set' if os.getenv('SECRET_KEY') else 'Missing',
                'GITHUB_AI_TOKEN': 'Set' if os.getenv('GITHUB_AI_TOKEN') else 'Missing'
            }
        })
    
    @app.route('/health')
    def fallback_health():
        return jsonify({
            'status': 'degraded',
            'message': 'Running in fallback mode',
            'environment': dict(os.environ) if len(os.environ) < 20 else 'Too many vars to display'
        })

# Export the app for Vercel
application = app

# For compatibility with different WSGI servers
def handler(event, context=None):
    return app