"""
Ollama Chat Client Application Package.

A professional chat client for Ollama with Tkinter UI,
following best practices for modular architecture and cohesion.
"""

__version__ = "1.0.0"
__author__ = "Chat Client Developer"

from app.llm_client import OllamaClient
from app.ui import ChatAppUI

__all__ = ["OllamaClient", "ChatAppUI"]
