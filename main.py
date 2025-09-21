#!/usr/bin/env python3
"""
PyTerminal - A Python-based command terminal
Main entry point for the terminal application
"""

import sys
import os
from terminal import PyTerminal

def main():
    """Main entry point for PyTerminal"""
    print("Welcome to PyTerminal - A Python Command Terminal")
    print("Type 'help' for available commands or 'exit' to quit")
    print("For AI commands, set OPENAI_API_KEY or LLM_API_KEY environment variable")
    print("-" * 50)
    
    # Get API key from environment or user input
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('LLM_API_KEY')
    if not api_key:
        print("Note: AI interpreter requires an API key. Set OPENAI_API_KEY environment variable.")
    
    # Initialize and run the terminal
    terminal = PyTerminal(ai_api_key=api_key)
    terminal.run()

if __name__ == "__main__":
    main()
