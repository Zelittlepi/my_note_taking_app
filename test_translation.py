#!/usr/bin/env python3
"""
Test script for the translation functionality
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.llm import llm_client

def test_translation():
    """Test the translation function"""
    try:
        # Test with a simple sentence
        test_text = "Hello, this is a test note for translation."
        print(f"Original text: {test_text}")
        
        translated = llm_client.translate_to_chinese(test_text)
        print(f"Translated text: {translated}")
        
        # Test with a longer text
        longer_text = """This is a note-taking application that allows users to create, read, update, and delete notes. 
        The application provides a simple and intuitive interface for managing personal notes and thoughts."""
        
        print(f"\nOriginal longer text: {longer_text}")
        translated_longer = llm_client.translate_to_chinese(longer_text)
        print(f"Translated longer text: {translated_longer}")
        
        print("\n✅ Translation test completed successfully!")
        
    except Exception as e:
        print(f"❌ Translation test failed: {e}")

if __name__ == "__main__":
    test_translation()