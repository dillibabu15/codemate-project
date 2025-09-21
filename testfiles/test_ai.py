#!/usr/bin/env python3
"""
Test script for PyTerminal AI Interpreter
Tests various natural language commands
"""

import os
import sys
from ai_interpreter import AIInterpreter
from config import PyTerminalConfig

def test_ai_commands():
    """Test various AI commands"""
    print("Testing PyTerminal AI Interpreter")
    print("=" * 35)
    
    config = PyTerminalConfig()
    if not config.is_configured():
        print("❌ No API key configured. Run 'python setup_ai.py' first.")
        return
    
    ai = AIInterpreter()
    
    # Test commands
    test_commands = [
        "create a folder called test",
        "show me the files",
        "what's my CPU usage",
        "display memory information",
        "list running processes",
        "create a directory called backup and move file.txt into it",
        "delete the file test.txt",
        "go to the home directory",
        "copy file1.txt to file2.txt",
        "show disk usage"
    ]
    
    print(f"API Key: {'✅ Configured' if ai.api_key else '❌ Not configured'}")
    print(f"Model: {ai.model}")
    print(f"API URL: {ai.api_url}")
    print()
    
    for i, command in enumerate(test_commands, 1):
        print(f"{i:2d}. Testing: '{command}'")
        try:
            result = ai.interpret(command)
            if result:
                print(f"    ✅ Generated: {result}")
            else:
                print(f"    ❌ No commands generated")
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
        print()
    
    print("=" * 35)
    print("AI testing completed!")

def test_fallback():
    """Test fallback pattern matching"""
    print("\nTesting Fallback Pattern Matching")
    print("-" * 35)
    
    # Create AI interpreter without API key to test fallback
    ai = AIInterpreter(api_key=None)
    
    fallback_commands = [
        "create a folder called test",
        "show me the files",
        "display cpu usage",
        "list processes"
    ]
    
    for command in fallback_commands:
        print(f"Testing: '{command}'")
        result = ai.interpret(command)
        if result:
            print(f"✅ Fallback: {result}")
        else:
            print("❌ No fallback match")
        print()

if __name__ == "__main__":
    test_ai_commands()
    test_fallback()
