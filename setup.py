#!/usr/bin/env python3
"""
Setup script for PyTerminal
Handles initial project setup and environment configuration
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_template():
    """Create .env template file"""
    env_template = """# PyTerminal Environment Configuration
# Copy this file to .env and add your actual API key

# For Google AI (Gemini)
api_key=your_google_ai_api_key_here

# For OpenAI (alternative)
# OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom model and endpoint
# PYTERMINAL_MODEL=gemini-1.5-flash
# PYTERMINAL_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent
"""
    
    if not os.path.exists('.env'):
        with open('.env.template', 'w') as f:
            f.write(env_template)
        print("✅ Created .env.template file")
        print("📝 Copy .env.template to .env and add your API key")
    else:
        print("✅ .env file already exists")

def show_next_steps():
    """Show next steps to the user"""
    print("\n" + "="*50)
    print("🎉 PyTerminal Setup Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Add your API key to .env file:")
    print("   - Copy .env.template to .env")
    print("   - Add your Google AI API key")
    print("\n2. Test the installation:")
    print("   python test_ai.py")
    print("\n3. Run PyTerminal:")
    print("   python main.py")
    print("\n4. Try AI commands:")
    print("   ai create a folder called test")
    print("   ai show me the cpu usage")
    print("\n5. Optional - Run web interface:")
    print("   python web_interface.py")
    print("\nFor more help, see README.md or AI_SETUP_GUIDE.md")

def main():
    """Main setup function"""
    print("🚀 PyTerminal Setup")
    print("="*20)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create environment template
    create_env_template()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
