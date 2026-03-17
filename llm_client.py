"""
Ollama LLM Client Module.

Handles all communication with the Ollama API.
High cohesion: focused solely on API interaction.
Low coupling: uses only standard library + requests.
"""

import json
import requests
import time
from typing import Generator, Tuple


class OllamaClient:
    """
    Client for interacting with the Ollama API.
    
    Responsible for:
    - Connecting to Ollama API endpoint
    - Sending prompts and receiving responses
    - Measuring response times
    - Handling errors gracefully
    """
    
    DEFAULT_HOST = "http://localhost"
    DEFAULT_PORT = 11434
    API_ENDPOINT = "/api/generate"
    
    # Available models
    AVAILABLE_MODELS = [
        "minyOllama",
        "gemma2:2b",
        "llama3.2:3b",
        "llama3.1:8b"
    ]
    
    # Default model if none specified
    DEFAULT_MODEL = "minyOllama"
    
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT):
        """
        Initialize the Ollama client.
        
        Args:
            host: Ollama server host (default: http://localhost)
            port: Ollama server port (default: 11434)
        """
        self.host = host
        self.port = port
        self.base_url = f"{host}:{port}"
        self.api_url = f"{self.base_url}{self.API_ENDPOINT}"
        self.timeout = 300  # 5 minutes timeout for long responses
    
    def is_available(self) -> bool:
        """
        Check if Ollama server is available.
        
        Returns:
            True if server is reachable, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available models from server.
        
        Returns:
            List of model names, or predefined list if unavailable
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                return [m.get("name", m) for m in models] if models else self.AVAILABLE_MODELS
        except (requests.RequestException, json.JSONDecodeError):
            pass
        
        return self.AVAILABLE_MODELS
    
    def generate_response(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        stream: bool = False
    ) -> Tuple[str, float]:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: Input prompt for the model
            model: Model name to use
            stream: Whether to stream the response (not used in this version)
        
        Returns:
            Tuple of (response_text, response_time_in_seconds)
        
        Raises:
            requests.RequestException: If API call fails
            ValueError: If model is invalid or prompt is empty
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        if not model:
            model = self.DEFAULT_MODEL
        
        payload = {
            "model": model,
            "prompt": prompt.strip(),
            "stream": False,
        }
        
        start_time = time.time()
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=self.timeout
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code != 200:
                error_msg = f"API Error {response.status_code}: {response.text[:100]}"
                raise requests.RequestException(error_msg)
            
            data = response.json()
            response_text = data.get("response", "")
            
            return response_text, elapsed_time
        
        except requests.Timeout:
            elapsed_time = time.time() - start_time
            raise requests.RequestException(
                f"Request timeout after {elapsed_time:.2f}s. "
                "Ollama might be processing a large model."
            )
        except requests.ConnectionError:
            raise requests.RequestException(
                f"Cannot connect to Ollama at {self.api_url}. "
                "Make sure Ollama is running."
            )
        except json.JSONDecodeError as e:
            raise requests.RequestException(
                f"Invalid response format from Ollama: {str(e)}"
            )
    
    def get_server_info(self) -> dict:
        """
        Get information about the Ollama server.
        
        Returns:
            Dictionary with server information
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except (requests.RequestException, json.JSONDecodeError):
            pass
        
        return {"status": "unavailable"}
