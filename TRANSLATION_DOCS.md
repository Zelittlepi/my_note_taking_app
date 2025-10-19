# Translation Feature Documentation

## Overview
The note-taking application now includes AI-powered translation functionality that can translate English text to Chinese using GitHub Copilot's AI model.

## API Endpoints

### 1. Translate Text
**Endpoint:** `POST /api/translate`

**Description:** Translate any English text to Chinese

**Request Body:**
```json
{
    "text": "Your English text to translate"
}
```

**Response:**
```json
{
    "original_text": "Your English text to translate",
    "translated_text": "你要翻译的英文文本",
    "source_language": "en",
    "target_language": "zh"
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:5001/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, how are you today?"}'
```

### 2. Translate Note
**Endpoint:** `POST /api/notes/{note_id}/translate`

**Description:** Translate both title and content of a specific note

**Response:**
```json
{
    "note_id": 1,
    "original": {
        "title": "Original Note Title",
        "content": "Original note content..."
    },
    "translated": {
        "title": "原始笔记标题",
        "content": "原始笔记内容..."
    },
    "source_language": "en",
    "target_language": "zh"
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:5001/api/notes/1/translate
```

## Configuration

### Environment Variables
Make sure you have the following environment variable set in your `.env` file:

```
GITHUB_AI_TOKEN=your_github_copilot_token_here
```

### Dependencies
The following packages are required (already added to requirements.txt):
- `openai>=1.0.0`
- `python-dotenv>=1.0.0`

## Usage in Code

### Direct Translation
```python
from src.utils.llm import llm_client

# Translate text
translated = llm_client.translate_to_chinese("Hello, world!")
print(translated)  # Output: 你好，世界！
```

### Error Handling
The translation functions include proper error handling:

```python
try:
    translated = llm_client.translate_to_chinese(text)
    return translated
except Exception as e:
    print(f"Translation failed: {e}")
    return None
```

## Features

- **High-quality translation**: Uses GitHub Copilot's GPT-4 model for accurate translations
- **Consistent output**: Lower temperature setting (0.3) for more consistent translation results
- **Error handling**: Comprehensive error handling for API failures
- **RESTful API**: Clean REST endpoints for easy integration
- **Note integration**: Direct translation of existing notes

## Testing

Run the test script to verify the translation functionality:

```bash
python test_translation.py
```

## Limitations

- Currently supports English to Chinese translation only
- Requires valid GitHub Copilot token
- Internet connection required for API calls
- Rate limits may apply based on GitHub Copilot usage terms