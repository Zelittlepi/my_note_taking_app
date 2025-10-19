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

# Database configuration with error handling
DATABASE_URL = os.getenv('DATABASE_URL')
database_connected = False

if DATABASE_URL:
    try:
        # Fix common PostgreSQL URL issues
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 3,  # Reduced for serverless
            'max_overflow': 5,  # Reduced for serverless
            'connect_args': {
                'sslmode': 'require',
                'connect_timeout': 15,  # Shorter timeout for serverless
            }
        }
        database_connected = True
        print(f"✅ Database configured: {DATABASE_URL[:50]}...")
        
    except Exception as e:
        print(f"❌ Database configuration error: {e}")
        # Fallback to SQLite for development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fallback.db'
        print("🔄 Falling back to SQLite database")
        
else:
    # Fallback for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    print("🔄 Using SQLite database (no DATABASE_URL found)")
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app, 
     origins=['*'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Initialize database and routes with better error handling
db_initialized = False
routes_registered = False

try:
    if 'db' in locals():
        db.init_app(app)
        print("✅ Database initialized")
        db_initialized = True
    else:
        print("⚠️  Database models not available")
        
except Exception as e:
    print(f"❌ Database initialization error: {e}")

try:
    if 'user_bp' in locals() and 'note_bp' in locals():
        app.register_blueprint(user_bp, url_prefix='/api')
        app.register_blueprint(note_bp, url_prefix='/api')
        print("✅ Routes registered")
        routes_registered = True
    else:
        print("⚠️  Route blueprints not available")
        
except Exception as e:
    print(f"❌ Blueprint registration error: {e}")

# Initialize database tables only if everything is working
if db_initialized:
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
    except Exception as e:
        print(f"❌ Database table creation error: {e}")

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
    """Enhanced health check endpoint with diagnostics"""
    health_status = {
        'status': 'healthy',
        'message': 'NoteTaker API is running',
        'environment': {
            'database_url_set': bool(os.getenv('DATABASE_URL')),
            'secret_key_set': bool(os.getenv('SECRET_KEY')),
            'github_token_set': bool(os.getenv('GITHUB_AI_TOKEN'))
        },
        'components': {
            'database_configured': database_connected,
            'database_initialized': db_initialized if 'db_initialized' in locals() else False,
            'routes_registered': routes_registered if 'routes_registered' in locals() else False
        }
    }
    
    # Test database connection if available
    if 'db' in locals() and db_initialized:
        try:
            with app.app_context():
                # Simple query to test connection
                result = db.engine.execute('SELECT 1')
                health_status['database_test'] = 'connected'
        except Exception as e:
            health_status['database_test'] = f'failed: {str(e)}'
            health_status['status'] = 'degraded'
    
    return jsonify(health_status)

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
