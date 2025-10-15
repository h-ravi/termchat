"""
Universal LLM API client module for TermChat
Supports multiple LLM providers
"""
import requests
from typing import List, Dict, Any

class UniversalLLMClient:
    """Universal client for interacting with multiple LLM providers"""
    
    def __init__(self, provider_config: Dict[str, str]):
        """
        Initialize the LLM client
        
        Args:
            provider_config: Dictionary containing provider configuration
                - name: Provider name
                - api_key: API key
                - api_url: API endpoint URL
                - model: Model identifier
                - env_key: Environment variable key
        """
        self.provider_name = provider_config['name']
        self.api_key = provider_config['api_key']
        self.base_url = provider_config['api_url']
        self.model = provider_config['model']
        
        # Setup headers based on provider
        self._setup_headers()
    
    def _setup_headers(self) -> None:
        """Setup HTTP headers based on the provider"""
        if "OpenRouter" in self.provider_name:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/termchat",
                "X-Title": "TermChat"
            }
        elif "Anthropic" in self.provider_name:
            self.headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
        elif "HuggingFace" in self.provider_name:
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
        else:
            # Default header format (OpenAI, xAI, DeepSeek, etc.)
            self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
    
    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get a response from the AI
        
        Args:
            messages: List of message objects with role and content
            
        Returns:
            The AI's response text
        """
        # Format request based on provider
        if "Anthropic" in self.provider_name:
            return self._get_anthropic_response(messages)
        elif "Google" in self.provider_name:
            return self._get_google_response(messages)
        elif "HuggingFace" in self.provider_name:
            return self._get_huggingface_response(messages)
        else:
            # Default OpenAI-compatible format
            return self._get_openai_compatible_response(messages)
    
    def _get_openai_compatible_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from OpenAI-compatible APIs"""
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    def _get_anthropic_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Anthropic Claude API"""
        # Convert messages to Anthropic format
        system_message = ""
        user_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                user_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        payload = {
            "model": self.model,
            "messages": user_messages,
            "max_tokens": 4096
        }
        
        if system_message:
            payload["system"] = system_message
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"]
    
    def _get_google_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from Google Gemini API"""
        # Convert messages to Google Gemini format
        # Gemini expects alternating user/model roles
        contents = []
        for msg in messages:
            # Convert 'assistant' role to 'model' for Gemini
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        # Correct Gemini API endpoint format
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": contents
        }
        
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        
        # Extract response with error handling
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            # Better error message
            if "error" in data:
                raise Exception(f"Google API Error: {data['error'].get('message', str(data['error']))}")
            raise Exception(f"Unexpected response format: {data}")
    
    def _get_huggingface_response(self, messages: List[Dict[str, str]]) -> str:
        """Get response from HuggingFace API"""
        # Combine messages into a single prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        url = f"{self.base_url}{self.model}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7
            }
        }
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()
        data = response.json()
        
        # HuggingFace returns different formats
        if isinstance(data, list) and len(data) > 0:
            if "generated_text" in data[0]:
                return data[0]["generated_text"]
        
        return str(data)
    
    def set_model(self, model: str) -> None:
        """
        Change the AI model
        
        Args:
            model: The model identifier to use
        """
        self.model = model