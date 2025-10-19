#!/usr/bin/env python3
"""
Test script for the auto-completion functionality
"""
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.llm import llm_client

def test_auto_completion():
    """Test the auto-completion function"""
    try:
        # Test with a simple note
        test_title = "Machine Learning Basics"
        test_content = """I am learning about machine learning algorithms. 
        So far I understand linear regression and decision trees. 
        I want to learn more about neural networks."""
        
        print(f"Original Title: {test_title}")
        print(f"Original Content: {test_content}")
        print("\n" + "="*50)
        print("AUTO-COMPLETION RESULTS:")
        print("="*50)
        
        completion_result = llm_client.auto_complete_note(test_title, test_content)
        
        print("\n💡 CONTENT SUGGESTIONS:")
        for i, suggestion in enumerate(completion_result.get('suggestions', []), 1):
            print(f"{i}. {suggestion}")
        
        print("\n✏️ IMPROVEMENTS:")
        for i, improvement in enumerate(completion_result.get('improvements', []), 1):
            print(f"{i}. {improvement}")
        
        print("\n📝 ADDITIONAL CONTENT:")
        additional = completion_result.get('additional_content', '')
        if additional:
            print(additional)
        else:
            print("No additional content suggested.")
        
        print("\n🏗️ STRUCTURE TIPS:")
        for i, tip in enumerate(completion_result.get('structure_tips', []), 1):
            print(f"{i}. {tip}")
        
        print("\n✅ Auto-completion test completed successfully!")
        
    except Exception as e:
        print(f"❌ Auto-completion test failed: {e}")

def test_short_note():
    """Test with a shorter note"""
    try:
        print("\n" + "="*50)
        print("TESTING SHORT NOTE:")
        print("="*50)
        
        test_title = "My thoughts"
        test_content = "Today was a good day."
        
        print(f"Title: {test_title}")
        print(f"Content: {test_content}")
        
        completion_result = llm_client.auto_complete_note(test_title, test_content)
        
        print("\n💡 SUGGESTIONS:")
        for suggestion in completion_result.get('suggestions', []):
            print(f"• {suggestion}")
        
        print("\n📝 ADDITIONAL CONTENT:")
        additional = completion_result.get('additional_content', '')
        if additional:
            print(additional)
        
        print("\n✅ Short note test completed!")
        
    except Exception as e:
        print(f"❌ Short note test failed: {e}")

if __name__ == "__main__":
    test_auto_completion()
    test_short_note()