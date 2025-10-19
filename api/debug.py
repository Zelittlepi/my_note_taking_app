"""
Debug endpoint for Vercel deployment troubleshooting
"""
import os
import sys
from flask import Flask, jsonify

debug_app = Flask(__name__)

@debug_app.route('/debug')
def debug_info():
    """Debug information for troubleshooting"""
    try:
        return jsonify({
            'status': 'running',
            'python_version': sys.version,
            'python_path': sys.path[:5],  # Show first 5 paths
            'current_directory': os.getcwd(),
            'environment_variables': {
                'DATABASE_URL': 'Set' if os.getenv('DATABASE_URL') else 'Not set',
                'SECRET_KEY': 'Set' if os.getenv('SECRET_KEY') else 'Not set',
                'GITHUB_AI_TOKEN': 'Set' if os.getenv('GITHUB_AI_TOKEN') else 'Not set'
            },
            'files_in_directory': os.listdir('.') if os.path.exists('.') else 'Directory not accessible'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'type': type(e).__name__
        }), 500

if __name__ == '__main__':
    debug_app.run(debug=True)