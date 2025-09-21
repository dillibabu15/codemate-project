#!/usr/bin/env python3
"""
AI Natural Language Interpreter for PyTerminal
Converts natural language commands to shell commands using LLM
"""

import os
import json
import requests
from typing import List, Optional, Dict, Any
from config import PyTerminalConfig

class AIInterpreter:
    """AI-driven natural language command interpreter using LLM"""
    
    def __init__(self, api_key: str = None, api_url: str = None, model: str = None):
        """
        Initialize AI interpreter with LLM API
        
        Args:
            api_key: API key for the LLM service
            api_url: API endpoint URL (defaults to OpenAI)
            model: Model name to use
        """
        self.config = PyTerminalConfig()
        self.api_key = api_key or self.config.api_key
        self.api_url = api_url or self.config.api_url
        self.model = model or self.config.model
        
        # Available commands in PyTerminal
        self.available_commands = {
            'ls': 'List files and directories',
            'cd': 'Change directory',
            'pwd': 'Print current directory',
            'mkdir': 'Create directory',
            'rm': 'Remove file or directory',
            'cat': 'Display file contents',
            'touch': 'Create empty file',
            'cp': 'Copy file or directory',
            'mv': 'Move/rename file or directory',
            'rmdir': 'Remove empty directory',
            'echo': 'Display text or write to file',
            'cpu': 'Show CPU usage',
            'mem': 'Show memory usage',
            'ps': 'List running processes',
            'disk': 'Show disk usage',
            'help': 'Show help',
            'history': 'Show command history',
            'clear': 'Clear screen',
            'exit': 'Exit terminal'
        }
    
    def interpret(self, command: str) -> Optional[List[str]]:
        """
        Interpret natural language command and return equivalent shell commands using LLM
        """
        if not self.api_key:
            return self._fallback_interpret(command)
        
        try:
            return self._llm_interpret(command)
        except Exception as e:
            print(f"LLM interpretation failed: {str(e)}")
            return self._fallback_interpret(command)
    
    def _llm_interpret(self, command: str) -> Optional[List[str]]:
        """Use LLM to interpret natural language command"""
        system_prompt = self._create_system_prompt()
        user_prompt = f"Convert this natural language command to PyTerminal shell commands: '{command}'"
        
        # Check if this is a Google AI API
        if self.api_key.startswith('AIza'):
            return self._google_ai_interpret(system_prompt, user_prompt)
        else:
            return self._openai_interpret(system_prompt, user_prompt)
    
    def _openai_interpret(self, system_prompt: str, user_prompt: str) -> Optional[List[str]]:
        """Use OpenAI API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'max_tokens': self.config.max_tokens,
            'temperature': self.config.temperature
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content'].strip()
        
        return self._parse_llm_response(content)
    
    def _google_ai_interpret(self, system_prompt: str, user_prompt: str) -> Optional[List[str]]:
        """Use Google AI API"""
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Google AI API uses different format
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        data = {
            'contents': [{
                'parts': [{'text': full_prompt}]
            }],
            'generationConfig': {
                'maxOutputTokens': self.config.max_tokens,
                'temperature': self.config.temperature
            }
        }
        
        # Add API key as query parameter for Google AI
        url = f"{self.api_url}?key={self.api_key}"
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        content = result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        return self._parse_llm_response(content)
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for the LLM"""
        commands_desc = "\n".join([f"  {cmd}: {desc}" for cmd, desc in self.available_commands.items()])
        
        return f"""You are a helpful assistant that converts natural language commands to PyTerminal shell commands.

Available PyTerminal commands:
{commands_desc}

Rules:
1. Return ONLY the shell commands, one per line
2. Do not include explanations or additional text
3. Use exact command names from the available commands
4. For complex operations, break them into multiple commands
5. If the request is unclear or impossible, return "ERROR: [reason]"

Examples:
User: "create a folder called test"
Assistant: mkdir test

User: "show me the files"
Assistant: ls

User: "create a folder called backup and move file.txt into it"
Assistant: mkdir backup
mv file.txt backup/

User: "what's my CPU usage"
Assistant: cpu

Return only the shell commands:"""
    
    def _parse_llm_response(self, response: str) -> Optional[List[str]]:
        """Parse LLM response to extract commands"""
        if response.startswith("ERROR:"):
            return None
        
        lines = response.strip().split('\n')
        commands = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                # Extract command (first word should be a valid command)
                parts = line.split()
                if parts and parts[0] in self.available_commands:
                    commands.append(line)
        
        return commands if commands else None
    
    def _fallback_interpret(self, command: str) -> Optional[List[str]]:
        """Fallback interpretation using simple patterns when LLM is not available"""
        command = command.lower().strip()
        
        # Simple pattern matching as fallback
        if any(word in command for word in ['create', 'make', 'new']):
            if any(word in command for word in ['folder', 'directory']):
                # Extract folder name
                words = command.split()
                for i, word in enumerate(words):
                    if word in ['folder', 'directory'] and i + 1 < len(words):
                        folder_name = words[i + 1]
                        return [f"mkdir {folder_name}"]
        
        if any(word in command for word in ['show', 'display', 'list']):
            if any(word in command for word in ['file', 'files']):
                return ["ls"]
            elif any(word in command for word in ['cpu', 'processor']):
                return ["cpu"]
            elif any(word in command for word in ['memory', 'ram']):
                return ["mem"]
            elif any(word in command for word in ['process', 'processes']):
                return ["ps"]
            elif any(word in command for word in ['disk', 'storage']):
                return ["disk"]
        
        return None
