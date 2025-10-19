"""
Ultra-reliable Vercel serverless function
This version prioritizes reliability over features
"""

import os
import sys
import json
from datetime import datetime

# Minimal imports to reduce failure points
try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError as e:
    print(f"Flask import failed: {e}")
    FLASK_AVAILABLE = False

if FLASK_AVAILABLE:
    # Create minimal Flask app
    app = Flask(__name__)
    CORS(app, origins=['*'])
    
    @app.route('/')
    def root():
        return jsonify({
            'status': 'healthy',
            'message': 'NoteTaker API is running',
            'timestamp': datetime.now().isoformat(),
            'version': '3.0-stable'
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'backend': 'working',
            'timestamp': datetime.now().isoformat(),
            'environment': {
                'database_configured': bool(os.getenv('DATABASE_URL')),
                'secrets_configured': bool(os.getenv('SECRET_KEY')),
                'ai_configured': bool(os.getenv('GITHUB_AI_TOKEN'))
            }
        })
    
    @app.route('/status')
    def status():
        return jsonify({
            'frontend': 'deployed',
            'backend': 'working',
            'database': 'testing_required',
            'deployment_time': datetime.now().isoformat()
        })
    
    @app.route('/debug')
    def debug():
        return jsonify({
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'environment_vars': {
                'DATABASE_URL': 'configured' if os.getenv('DATABASE_URL') else 'missing',
                'SECRET_KEY': 'configured' if os.getenv('SECRET_KEY') else 'missing',
                'GITHUB_AI_TOKEN': 'configured' if os.getenv('GITHUB_AI_TOKEN') else 'missing'
            },
            'sys_path': sys.path[:3],
            'database_test': test_database_simple()
        })
    
    @app.route('/api/notes')
    def get_notes():
        # Return test data if database is not available
        return jsonify({
            'notes': [
                {
                    'id': 1,
                    'title': 'Welcome to NoteTaker',
                    'content': 'Your note-taking app is working! The backend is responding correctly.',
                    'created_at': '2024-10-19T00:00:00'
                }
            ],
            'status': 'test_data',
            'message': 'Backend is working. Database integration pending.'
        })
    
    def test_database_simple():
        """Simple database test without complex dependencies"""
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            return {'status': 'no_config', 'message': 'DATABASE_URL not configured'}
        
        try:
            # Try minimal connection test
            import psycopg2
            conn = psycopg2.connect(database_url, connect_timeout=5)
            conn.close()
            return {'status': 'connected', 'message': 'Database connection successful'}
        except ImportError:
            return {'status': 'no_driver', 'message': 'psycopg2 not available'}
        except Exception as e:
            return {'status': 'failed', 'message': str(e)[:100]}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error', 'message': str(error)}), 500

else:
    # Fallback if Flask fails to import
    def app(environ, start_response):
        response_body = json.dumps({
            'error': 'Flask import failed',
            'message': 'Critical dependency missing'
        }).encode('utf-8')
        
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [response_body]

# Export for Vercel
application = app