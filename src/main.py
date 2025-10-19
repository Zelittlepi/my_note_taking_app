import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

try:
    from flask import Flask, send_from_directory, jsonify
    from flask_cors import CORS
    from src.models.user import db
    from src.routes.user import user_bp  
    from src.routes.note import note_bp
    from src.models.note import Note
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports for Vercel
    from flask import Flask, send_from_directory, jsonify
    from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Fix common PostgreSQL URL issues
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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
else:
    # Fallback for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app, 
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Initialize database and routes if available
try:
    db.init_app(app)
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(note_bp, url_prefix='/api')
    
    # Initialize database tables
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database initialization error: {e}")
            
except Exception as e:
    print(f"Blueprint registration error: {e}")

@app.route('/')
def index():
    """Serve the main application"""
    try:
        static_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
        if os.path.exists(static_path):
            return send_from_directory(os.path.join(os.path.dirname(__file__), 'static'), 'index.html')
        else:
            return jsonify({
                'message': 'NoteTaker API is running',
                'status': 'healthy',
                'endpoints': {
                    'health': '/health',
                    'notes': '/api/notes',
                    'translate': '/api/translate',
                    'complete': '/api/complete'
                }
            })
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'NoteTaker API is running',
        'database': 'connected' if DATABASE_URL else 'local'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create tables for local development
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
        except Exception as e:
            print(f"Database error: {e}")
    
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=os.getenv('FLASK_ENV') == 'development')
