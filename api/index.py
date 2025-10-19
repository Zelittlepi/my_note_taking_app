import os
import sys

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

try:
    from src.main import app
except ImportError:
    # Fallback if import fails
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def fallback():
        return jsonify({'error': 'Import failed', 'message': 'Check deployment configuration'})

# Export the app for Vercel
application = app

# For compatibility with different WSGI servers
def handler(event, context=None):
    return app