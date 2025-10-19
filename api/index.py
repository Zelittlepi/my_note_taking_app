import os
import sys
import traceback
import json

print("🚀 Starting Vercel function...")

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

print(f"📁 Paths added: {parent_dir}, {src_dir}")

# Create a minimal Flask app first
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({
        'status': 'running',
        'message': 'Vercel function is working',
        'environment': {
            'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Missing',
            'SECRET_KEY': 'Set' if os.getenv('SECRET_KEY') else 'Missing',
            'GITHUB_AI_TOKEN': 'Set' if os.getenv('GITHUB_AI_TOKEN') else 'Missing'
        },
        'python_version': sys.version,
        'working_directory': os.getcwd(),
        'available_modules': [name for name in sys.modules.keys() if not name.startswith('_')][:10]
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Basic function works'})

@app.route('/debug')
def debug():
    try:
        debug_info = {
            'environment_variables': dict(os.environ),
            'sys_path': sys.path,
            'current_dir': current_dir,
            'parent_dir': parent_dir,
            'src_dir': src_dir,
            'src_dir_exists': os.path.exists(src_dir),
            'files_in_src': os.listdir(src_dir) if os.path.exists(src_dir) else 'src dir not found'
        }
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

# Now try to import and integrate the main app
main_app_loaded = False

try:
    print("🔄 Attempting to import main app...")
    from src.main import app as main_app
    print("✅ Main app imported successfully")
    
    # Replace our minimal app with the main app
    app = main_app
    main_app_loaded = True
    
except Exception as e:
    print(f"❌ Failed to import main app: {str(e)}")
    print("Traceback:", traceback.format_exc())
    
    # Try to import simplified app as fallback
    try:
        print("🔄 Attempting to import simplified app...")
        sys.path.append(current_dir)
        from simple_app import app as simple_app
        app = simple_app
        print("✅ Simplified app loaded as fallback")
        
    except Exception as fallback_error:
        print(f"❌ Simplified app also failed: {fallback_error}")
        
        # Add error endpoint to minimal app
        @app.route('/error')
        def show_error():
            return jsonify({
                'error': 'All app imports failed',
                'main_app_error': str(e),
                'fallback_error': str(fallback_error),
                'traceback': traceback.format_exc()
            })

@app.route('/status')
def deployment_status():
    return jsonify({
        'main_app_loaded': main_app_loaded,
        'deployment_time': '2024-10-19',
        'status': 'running'
    })

print("🏁 Vercel function setup complete")

# Export the app for Vercel
application = app

# For compatibility with different WSGI servers
def handler(event, context=None):
    return app