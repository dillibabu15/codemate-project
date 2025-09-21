#!/usr/bin/env python3
"""
Setup script for PyTerminal AI features
Helps users configure their LLM API key
"""

import os
import sys
from config import PyTerminalConfig

def setup_api_key():
    """Interactive setup for API key"""
    print("PyTerminal AI Setup")
    print("=" * 20)
    print()
    
    config = PyTerminalConfig()
    
    if config.is_configured():
        print(f"✅ API key is already configured")
        print(f"Model: {config.model}")
        print(f"API URL: {config.api_url}")
        
        response = input("\nDo you want to update the configuration? (y/N): ").strip().lower()
        if response != 'y':
            return True
    
    print("\nChoose your LLM provider:")
    print("1. OpenAI (GPT-3.5-turbo, GPT-4)")
    print("2. Custom API endpoint")
    print("3. Skip setup (use fallback pattern matching)")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '3':
        print("\nSkipping AI setup. You can use basic pattern matching.")
        return False
    
    if choice == '1':
        api_key = input("\nEnter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ No API key provided")
            return False
        
        config.api_key = api_key
        config.model = "gpt-3.5-turbo"
        config.api_url = "https://api.openai.com/v1/chat/completions"
    
    elif choice == '2':
        api_key = input("\nEnter your API key: ").strip()
        if not api_key:
            print("❌ No API key provided")
            return False
        
        api_url = input("Enter API endpoint URL: ").strip()
        if not api_url:
            print("❌ No API URL provided")
            return False
        
        model = input("Enter model name (default: gpt-3.5-turbo): ").strip()
        if not model:
            model = "gpt-3.5-turbo"
        
        config.api_key = api_key
        config.model = model
        config.api_url = api_url
    
    else:
        print("❌ Invalid choice")
        return False
    
    # Save configuration
    if config.save_api_key(config.api_key):
        print("\n✅ Configuration saved successfully!")
        print(f"API key: {config.api_key[:10]}...")
        print(f"Model: {config.model}")
        print(f"API URL: {config.api_url}")
        return True
    else:
        print("\n❌ Failed to save configuration")
        return False

def test_ai_setup():
    """Test the AI configuration"""
    print("\nTesting AI configuration...")
    
    try:
        from ai_interpreter import AIInterpreter
        ai = AIInterpreter()
        
        if not ai.api_key:
            print("❌ No API key configured")
            return False
        
        # Test with a simple command
        result = ai.interpret("show me the files")
        if result:
            print(f"✅ AI test successful! Generated command: {result}")
            return True
        else:
            print("❌ AI test failed - no commands generated")
            return False
    
    except Exception as e:
        print(f"❌ AI test failed with error: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("Welcome to PyTerminal AI Setup!")
    print()
    
    # Setup API key
    if setup_api_key():
        # Test the setup
        if test_ai_setup():
            print("\n🎉 AI setup completed successfully!")
            print("You can now use natural language commands with 'ai <command>'")
        else:
            print("\n⚠️  Setup completed but AI test failed.")
            print("Check your API key and internet connection.")
    else:
        print("\n⚠️  AI setup skipped or failed.")
        print("You can still use PyTerminal with regular commands.")
    
    print("\nTo start PyTerminal, run: python main.py")

if __name__ == "__main__":
    main()
