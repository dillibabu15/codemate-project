#!/usr/bin/env python3
"""
Configuration file for PyTerminal
Handles API keys and settings
"""

import os
from typing import Optional

# Try to import dotenv for .env file support
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

class PyTerminalConfig:
    """Configuration management for PyTerminal"""
    
    def __init__(self):
        # Load .env file if available
        self._load_env_file()
        
        self.api_key = self._get_api_key()
        
        # Auto-detect API type based on key format
        if self.api_key and self.api_key.startswith('AIza'):
            # Google AI API key
            self.model = os.getenv('PYTERMINAL_MODEL', 'gemini-1.5-flash')
            self.api_url = os.getenv('PYTERMINAL_API_URL', 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent')
        else:
            # Default to OpenAI
            self.model = os.getenv('PYTERMINAL_MODEL', 'gpt-3.5-turbo')
            self.api_url = os.getenv('PYTERMINAL_API_URL', 'https://api.openai.com/v1/chat/completions')
        self.max_tokens = int(os.getenv('PYTERMINAL_MAX_TOKENS', '500'))
        self.temperature = float(os.getenv('PYTERMINAL_TEMPERATURE', '0.1'))
    
    def _load_env_file(self):
        """Load .env file if available"""
        if HAS_DOTENV:
            # Try to load from current directory
            if os.path.exists('.env'):
                load_dotenv('.env')
            # Also try to load from home directory
            elif os.path.exists(os.path.expanduser('~/.env')):
                load_dotenv(os.path.expanduser('~/.env'))
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from various sources"""
        # Check environment variables (including from .env file)
        api_key = (os.getenv('OPENAI_API_KEY') or 
                  os.getenv('LLM_API_KEY') or 
                  os.getenv('API_KEY'))  # Support your specific variable name
        if api_key:
            return api_key
        
        # Check for config file
        config_file = os.path.expanduser('~/.pyterminal_config')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    for line in f:
                        if line.startswith('API_KEY='):
                            return line.split('=', 1)[1].strip()
            except Exception:
                pass
        
        return None
    
    def save_api_key(self, api_key: str) -> bool:
        """Save API key to config file"""
        try:
            config_file = os.path.expanduser('~/.pyterminal_config')
            with open(config_file, 'w') as f:
                f.write(f'API_KEY={api_key}\n')
                f.write(f'MODEL={self.model}\n')
                f.write(f'API_URL={self.api_url}\n')
            return True
        except Exception:
            return False
    
    def is_configured(self) -> bool:
        """Check if API key is configured"""
        return self.api_key is not None
