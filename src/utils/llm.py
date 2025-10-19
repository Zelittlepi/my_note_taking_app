import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_AI_TOKEN")
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1-mini"
        
        if not self.token:
            raise ValueError("GITHUB_AI_TOKEN environment variable is required")
        
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )
    
    def translate_to_chinese(self, text: str) -> str:
        """
        Translate English text to Chinese using GitHub Copilot AI model
        
        Args:
            text (str): The English text to translate
            
        Returns:
            str: The translated Chinese text
        """
        try:
            system_prompt = """You are a professional translator specializing in English to Chinese translation. 
            Please translate the given English text to Chinese (Simplified Chinese). 
            Maintain the original meaning, tone, and style as much as possible. 
            Only return the translated text without any additional explanations or comments."""
            
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Please translate the following English text to Chinese:\n\n{text}",
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent translations
                top_p=1,
                model=self.model
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
    
    def generate_response(self, prompt: str, system_message: str = "") -> str:
        """
        General purpose AI response generation
        
        Args:
            prompt (str): The user prompt
            system_message (str): Optional system message for context
            
        Returns:
            str: The AI response
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_message,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=1,
                top_p=1,
                model=self.model
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"AI response generation failed: {str(e)}")

# Create a global instance for easy importing
llm_client = LLMClient()