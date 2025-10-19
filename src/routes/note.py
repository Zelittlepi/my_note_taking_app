from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.utils.llm import llm_client

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
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
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
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
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/translate', methods=['POST'])
def translate_text():
    """Translate English text to Chinese using AI"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text_to_translate = data['text']
        if not text_to_translate.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Use the LLM client to translate
        translated_text = llm_client.translate_to_chinese(text_to_translate)
        
        return jsonify({
            'original_text': text_to_translate,
            'translated_text': translated_text,
            'source_language': 'en',
            'target_language': 'zh'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Translation failed: {str(e)}'}), 500

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a specific note's content from English to Chinese"""
    try:
        note = Note.query.get_or_404(note_id)
        
        # Translate both title and content
        translated_title = llm_client.translate_to_chinese(note.title)
        translated_content = llm_client.translate_to_chinese(note.content)
        
        return jsonify({
            'note_id': note_id,
            'original': {
                'title': note.title,
                'content': note.content
            },
            'translated': {
                'title': translated_title,
                'content': translated_content
            },
            'source_language': 'en',
            'target_language': 'zh'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Note translation failed: {str(e)}'}), 500

@note_bp.route('/complete', methods=['POST'])
def complete_text():
    """Auto-complete and enhance text content using AI"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content fields are required'}), 400
        
        title = data['title'].strip()
        content = data['content'].strip()
        
        if not title and not content:
            return jsonify({'error': 'Title or content must be provided'}), 400
        
        # Use the LLM client to auto-complete
        completion_result = llm_client.auto_complete_note(title, content)
        
        return jsonify({
            'original': {
                'title': title,
                'content': content
            },
            'suggestions': completion_result.get('suggestions', []),
            'improvements': completion_result.get('improvements', []),
            'additional_content': completion_result.get('additional_content', ''),
            'structure_tips': completion_result.get('structure_tips', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Auto-completion failed: {str(e)}'}), 500

@note_bp.route('/notes/<int:note_id>/complete', methods=['POST'])
def complete_note(note_id):
    """Auto-complete and enhance a specific note using AI"""
    try:
        note = Note.query.get_or_404(note_id)
        
        # Use the LLM client to auto-complete
        completion_result = llm_client.auto_complete_note(note.title, note.content)
        
        return jsonify({
            'note_id': note_id,
            'original': {
                'title': note.title,
                'content': note.content
            },
            'suggestions': completion_result.get('suggestions', []),
            'improvements': completion_result.get('improvements', []),
            'additional_content': completion_result.get('additional_content', ''),
            'structure_tips': completion_result.get('structure_tips', [])
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Note auto-completion failed: {str(e)}'}), 500

