"""
Simplified Flask app for Vercel serverless deployment
This version focuses on core functionality without complex database initialization
"""

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Enable CORS
CORS(app, 
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

@app.route('/')
def index():
    """Main endpoint"""
    return jsonify({
        'message': 'NoteTaker API is running',
        'status': 'healthy',
        'version': '2.0',
        'endpoints': {
            'health': '/health',
            'debug': '/debug',
            'notes': '/api/notes (coming soon)',
            'translate': '/api/translate (coming soon)',
            'complete': '/api/complete (coming soon)'
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'NoteTaker API is running',
        'environment': {
            'database_url_set': bool(os.getenv('DATABASE_URL')),
            'secret_key_set': bool(os.getenv('SECRET_KEY')),
            'github_token_set': bool(os.getenv('GITHUB_AI_TOKEN')),
            'flask_env': os.getenv('FLASK_ENV', 'production')
        },
        'system': {
            'python_version': sys.version.split()[0],
            'working_directory': os.getcwd()
        }
    })

@app.route('/debug')
def debug_info():
    """Debug information endpoint"""
    try:
        return jsonify({
            'environment_variables': {
                key: 'SET' if value else 'MISSING' 
                for key, value in {
                    'DATABASE_URL': os.getenv('DATABASE_URL'),
                    'SECRET_KEY': os.getenv('SECRET_KEY'),
                    'GITHUB_AI_TOKEN': os.getenv('GITHUB_AI_TOKEN'),
                    'FLASK_ENV': os.getenv('FLASK_ENV')
                }.items()
            },
            'paths': {
                'current_dir': os.getcwd(),
                'script_dir': os.path.dirname(os.path.abspath(__file__)),
                'sys_path': sys.path[:5]  # First 5 paths only
            },
            'database_test': test_database_connection()
        })
    except Exception as e:
        return jsonify({'error': str(e)})

def test_database_connection():
    """Test database connection"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        return {'status': 'no_url', 'message': 'DATABASE_URL not set'}
    
    try:
        import psycopg2
        
        # Quick connection test with short timeout
        conn = psycopg2.connect(database_url, sslmode='require', connect_timeout=5)
        conn.close()
        
        return {'status': 'connected', 'message': 'Database connection successful'}
        
    except ImportError:
        return {'status': 'no_driver', 'message': 'psycopg2 not available'}
    except Exception as e:
        return {'status': 'failed', 'message': str(e)}

@app.route('/api/notes', methods=['GET'])
def get_notes_simple():
    """Simple notes endpoint for testing"""
    return jsonify({
        'notes': [
            {
                'id': 1,
                'title': 'Test Note',
                'content': 'This is a test note from the simplified API',
                'created_at': '2024-01-01T00:00:00'
            }
        ],
        'count': 1,
        'message': 'This is a test endpoint. Full functionality coming soon.'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'This endpoint does not exist'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=True)