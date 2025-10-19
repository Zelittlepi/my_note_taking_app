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
    
    def auto_complete_note(self, title: str, content: str) -> dict:
        """
        Auto-complete and enhance note content with AI assistance
        
        Args:
            title (str): The note title
            content (str): The existing note content
            
        Returns:
            dict: Enhanced content with suggestions, corrections, and associations
        """
        try:
            system_prompt = """You are an intelligent note-taking assistant that helps users enhance their notes. 
            Your task is to analyze the existing note content and provide:
            1. Content suggestions and associations related to the topic
            2. Grammar and style improvements
            3. Additional relevant information or ideas
            4. Structure improvements
            
            Return your response in a structured JSON format with the following keys:
            - "suggestions": Array of content suggestions and related ideas
            - "improvements": Array of grammar/style improvement suggestions
            - "additional_content": Suggested additional paragraphs or sections
            - "structure_tips": Tips for better organization
            
            Be helpful, constructive, and maintain the original tone and intent of the note."""
            
            user_prompt = f"""Please analyze and help enhance this note:

Title: {title}

Current Content:
{content}

Please provide suggestions for improvement, related content ideas, grammar corrections, and structural enhancements."""

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                temperature=0.7,  # Moderate temperature for creativity while maintaining relevance
                top_p=0.9,
                model=self.model
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to structured text if needed
            try:
                import json
                result = json.loads(ai_response)
                
                # Ensure all required keys exist with proper data types
                normalized_result = {
                    "suggestions": [],
                    "improvements": [],
                    "additional_content": "",
                    "structure_tips": []
                }
                
                # Normalize suggestions
                if "suggestions" in result:
                    if isinstance(result["suggestions"], list):
                        normalized_result["suggestions"] = [str(s) for s in result["suggestions"] if s]
                    elif isinstance(result["suggestions"], str):
                        normalized_result["suggestions"] = [result["suggestions"]]
                
                # Normalize improvements
                if "improvements" in result:
                    if isinstance(result["improvements"], list):
                        normalized_result["improvements"] = [str(i) for i in result["improvements"] if i]
                    elif isinstance(result["improvements"], str):
                        normalized_result["improvements"] = [result["improvements"]]
                
                # Normalize additional_content
                if "additional_content" in result:
                    if isinstance(result["additional_content"], str):
                        normalized_result["additional_content"] = result["additional_content"]
                    elif isinstance(result["additional_content"], list):
                        normalized_result["additional_content"] = "\n".join(str(c) for c in result["additional_content"] if c)
                
                # Normalize structure_tips
                if "structure_tips" in result:
                    if isinstance(result["structure_tips"], list):
                        normalized_result["structure_tips"] = [str(t) for t in result["structure_tips"] if t]
                    elif isinstance(result["structure_tips"], str):
                        normalized_result["structure_tips"] = [result["structure_tips"]]
                        
                return normalized_result
                
            except json.JSONDecodeError:
                # Fallback: parse as structured text
                return self._parse_completion_response(ai_response)
            
        except Exception as e:
            raise Exception(f"Auto-completion failed: {str(e)}")
    
    def _parse_completion_response(self, response_text: str) -> dict:
        """
        Fallback parser for AI response when JSON parsing fails
        
        Args:
            response_text (str): The AI response text
            
        Returns:
            dict: Parsed response with structured data
        """
        lines = response_text.split('\n')
        result = {
            "suggestions": [],
            "improvements": [],
            "additional_content": "",
            "structure_tips": []
        }
        
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if any(keyword in line.lower() for keyword in ['suggestion', 'idea', 'related']):
                if current_section and current_content:
                    if current_section == 'suggestions':
                        result['suggestions'].extend(current_content)
                    current_content = []
                current_section = 'suggestions'
            elif any(keyword in line.lower() for keyword in ['improvement', 'correction', 'grammar']):
                if current_section and current_content:
                    if current_section == 'suggestions':
                        result['suggestions'].extend(current_content)
                    current_content = []
                current_section = 'improvements'
            elif any(keyword in line.lower() for keyword in ['additional', 'expand', 'add']):
                if current_section and current_content:
                    if current_section in ['suggestions', 'improvements']:
                        result[current_section].extend(current_content)
                    current_content = []
                current_section = 'additional_content'
            elif any(keyword in line.lower() for keyword in ['structure', 'organization', 'format']):
                if current_section and current_content:
                    if current_section == 'additional_content':
                        result['additional_content'] = '\n'.join(current_content)
                    elif current_section in ['suggestions', 'improvements']:
                        result[current_section].extend(current_content)
                    current_content = []
                current_section = 'structure_tips'
            else:
                # Add content to current section
                if line.startswith(('-', '•', '*', '1.', '2.', '3.')):
                    current_content.append(line)
                elif current_section == 'additional_content':
                    current_content.append(line)
                elif line:
                    current_content.append(line)
        
        # Add remaining content
        if current_section and current_content:
            if current_section == 'additional_content':
                result['additional_content'] = '\n'.join(current_content)
            elif current_section in ['suggestions', 'improvements', 'structure_tips']:
                result[current_section].extend(current_content)
        
        # If no structured content found, put everything in suggestions
        if not any(result.values()):
            result['suggestions'] = [response_text]
        
        return result

# Create a global instance for easy importing
llm_client = LLMClient()