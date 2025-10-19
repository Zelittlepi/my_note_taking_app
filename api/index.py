"""
Enhanced Vercel serverless function with gradual feature restoration
"""

import os
import sys
import json
from datetime import datetime

# Add src directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

# Try to import Flask and create basic app
try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError as e:
    print(f"Flask import failed: {e}")
    FLASK_AVAILABLE = False

if FLASK_AVAILABLE:
    # Create Flask app
    app = Flask(__name__)
    CORS(app, origins=['*'])
    
    # Try to import database models and routes
    database_available = False
    models_available = False
    routes_available = False
    
    try:
        from src.models.user import db
        from src.models.note import Note
        models_available = True
        print("✅ Database models imported successfully")
        
        # Configure database
        DATABASE_URL = os.getenv('DATABASE_URL')
        if DATABASE_URL:
            if DATABASE_URL.startswith('postgres://'):
                DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
            
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                'pool_pre_ping': True,
                'pool_recycle': 300,
                'pool_size': 3,
                'max_overflow': 5,
                'connect_args': {'sslmode': 'require', 'connect_timeout': 15}
            }
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
        
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')
        
        # Initialize database
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            print("✅ Database initialized successfully")
            database_available = True
            
    except Exception as e:
        print(f"⚠️  Database setup failed: {e}")
    
    # Try to import AI utilities
    ai_available = False
    try:
        from src.utils.llm import llm_client
        ai_available = True
        print("✅ AI utilities imported successfully")
    except Exception as e:
        print(f"⚠️  AI utilities failed: {e}")
    
    # Basic endpoints that always work
    @app.route('/')
    def root():
        return jsonify({
            'status': 'healthy',
            'message': 'NoteTaker API is running',
            'timestamp': datetime.now().isoformat(),
            'version': '4.0-enhanced',
            'features': {
                'database': database_available,
                'models': models_available,
                'ai': ai_available
            }
        })
    
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'backend': 'working',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'database': 'connected' if database_available else 'degraded',
                'models': 'loaded' if models_available else 'unavailable',
                'ai': 'ready' if ai_available else 'unavailable'
            },
            'environment': {
                'database_configured': bool(os.getenv('DATABASE_URL')),
                'secrets_configured': bool(os.getenv('SECRET_KEY')),
                'ai_configured': bool(os.getenv('GITHUB_AI_TOKEN'))
            }
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
            'database_test': test_database_connection(),
            'feature_status': {
                'database_available': database_available,
                'models_available': models_available,
                'ai_available': ai_available
            }
        })
    
    # PHASE 1: Basic Notes API (if database is available)
    if database_available and models_available:
        
        @app.route('/api/notes', methods=['GET'])
        def get_notes():
            """Get all notes"""
            try:
                notes = Note.query.order_by(Note.updated_at.desc()).all()
                return jsonify([note.to_dict() for note in notes])
            except Exception as e:
                return jsonify({'error': f'Database error: {str(e)}'}), 500
        
        @app.route('/api/notes', methods=['POST'])
        def create_note():
            """Create a new note"""
            try:
                data = request.json
                if not data or 'title' not in data or 'content' not in data:
                    return jsonify({'error': 'Title and content are required'}), 400
                
                note = Note(title=data['title'], content=data['content'])
                db.session.add(note)
                db.session.commit()
                return jsonify(note.to_dict()), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Create failed: {str(e)}'}), 500
        
        @app.route('/api/notes/<int:note_id>', methods=['GET'])
        def get_note(note_id):
            """Get a specific note"""
            try:
                note = Note.query.get_or_404(note_id)
                return jsonify(note.to_dict())
            except Exception as e:
                return jsonify({'error': f'Note not found: {str(e)}'}), 404
        
        @app.route('/api/notes/<int:note_id>', methods=['PUT'])
        def update_note(note_id):
            """Update a note"""
            try:
                note = Note.query.get_or_404(note_id)
                data = request.json
                
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                note.title = data.get('title', note.title)
                note.content = data.get('content', note.content)
                db.session.commit()
                return jsonify(note.to_dict())
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Update failed: {str(e)}'}), 500
        
        @app.route('/api/notes/<int:note_id>', methods=['DELETE'])
        def delete_note(note_id):
            """Delete a note"""
            try:
                note = Note.query.get_or_404(note_id)
                db.session.delete(note)
                db.session.commit()
                return '', 204
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f'Delete failed: {str(e)}'}), 500
        
        @app.route('/api/notes/search', methods=['GET'])
        def search_notes():
            """Search notes"""
            try:
                query = request.args.get('q', '')
                if not query:
                    return jsonify([])
                
                notes = Note.query.filter(
                    (Note.title.contains(query)) | (Note.content.contains(query))
                ).order_by(Note.updated_at.desc()).all()
                
                return jsonify([note.to_dict() for note in notes])
            except Exception as e:
                return jsonify({'error': f'Search failed: {str(e)}'}), 500
    
    else:
        # Fallback endpoints when database is not available
        @app.route('/api/notes', methods=['GET'])
        def get_notes_fallback():
            return jsonify({
                'notes': [
                    {
                        'id': 1,
                        'title': 'Welcome to NoteTaker',
                        'content': 'Database is being set up. Full functionality will be restored soon.',
                        'created_at': '2024-10-19T00:00:00'
                    }
                ],
                'status': 'fallback_mode',
                'message': 'Database not available - showing test data'
            })
    
    # PHASE 2: AI Features (if AI is available)
    if ai_available:
        
        @app.route('/api/translate', methods=['POST'])
        def translate_text():
            """Translate text using AI"""
            try:
                data = request.json
                if not data or 'text' not in data:
                    return jsonify({'error': 'Text field is required'}), 400
                
                text_to_translate = data['text']
                if not text_to_translate.strip():
                    return jsonify({'error': 'Text cannot be empty'}), 400
                
                translated_text = llm_client.translate_to_chinese(text_to_translate)
                
                return jsonify({
                    'original_text': text_to_translate,
                    'translated_text': translated_text,
                    'source_language': 'en',
                    'target_language': 'zh'
                }), 200
                
            except Exception as e:
                return jsonify({'error': f'Translation failed: {str(e)}'}), 500
        
        @app.route('/api/complete', methods=['POST'])
        def complete_text():
            """Auto-complete text using AI"""
            try:
                data = request.json
                if not data or 'title' not in data or 'content' not in data:
                    return jsonify({'error': 'Title and content fields are required'}), 400
                
                title = data['title'].strip()
                content = data['content'].strip()
                
                if not title and not content:
                    return jsonify({'error': 'Title or content must be provided'}), 400
                
                completion_result = llm_client.auto_complete_note(title, content)
                
                return jsonify({
                    'original': {'title': title, 'content': content},
                    'suggestions': completion_result.get('suggestions', []),
                    'improvements': completion_result.get('improvements', []),
                    'additional_content': completion_result.get('additional_content', ''),
                    'structure_tips': completion_result.get('structure_tips', [])
                }), 200
                
            except Exception as e:
                return jsonify({'error': f'Auto-completion failed: {str(e)}'}), 500
    
    else:
        # Fallback AI endpoints
        @app.route('/api/translate', methods=['POST'])
        def translate_fallback():
            return jsonify({'error': 'AI translation not available - check GITHUB_AI_TOKEN'}), 503
        
        @app.route('/api/complete', methods=['POST'])
        def complete_fallback():
            return jsonify({'error': 'AI completion not available - check GITHUB_AI_TOKEN'}), 503
    
    def test_database_connection():
        """Test database connection"""
        if not database_available:
            return {'status': 'unavailable', 'message': 'Database not configured'}
        
        try:
            with app.app_context():
                db.engine.execute('SELECT 1')
            return {'status': 'connected', 'message': 'Database connection successful'}
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