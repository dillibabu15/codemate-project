#!/usr/bin/env python3
"""
Demo script for PyTerminal
Demonstrates all the core features and commands
"""

import os
import sys
import time
from terminal import PyTerminal

def run_demo():
    """Run a comprehensive demo of PyTerminal features"""
    print("=" * 60)
    print("PyTerminal Demo - Comprehensive Feature Demonstration")
    print("=" * 60)
    print()
    
    # Create demo directory
    demo_dir = "pyterminal_demo"
    if not os.path.exists(demo_dir):
        os.makedirs(demo_dir)
    
    # Change to demo directory
    os.chdir(demo_dir)
    
    print("1. File System Commands Demo")
    print("-" * 30)
    
    # Initialize terminal for demo
    terminal = PyTerminal()
    
    # Demo commands
    demo_commands = [
        "pwd",
        "mkdir test_folder",
        "touch demo_file.txt",
        "ls",
        "echo 'Hello PyTerminal!' > demo_file.txt",
        "cat demo_file.txt",
        "cp demo_file.txt test_folder/",
        "ls test_folder",
        "mv demo_file.txt test_folder/renamed_file.txt",
        "ls test_folder",
        "rm test_folder/renamed_file.txt",
        "ls test_folder",
        "rmdir test_folder",
        "ls"
    ]
    
    for cmd in demo_commands:
        print(f"$ {cmd}")
        success, output = terminal._process_command(cmd)
        if output:
            print(output)
        print()
    
    print("2. System Monitoring Commands Demo")
    print("-" * 40)
    
    monitoring_commands = [
        "cpu",
        "mem",
        "ps",
        "disk"
    ]
    
    for cmd in monitoring_commands:
        print(f"$ {cmd}")
        success, output = terminal._process_command(cmd)
        if output:
            print(output)
        print()
    
    print("3. AI Natural Language Interpreter Demo")
    print("-" * 45)
    
    ai_commands = [
        "ai create a folder called ai_test",
        "ai make a file called ai_demo.txt",
        "ai show me the files",
        "ai create a folder called complex and move ai_demo.txt into it",
        "ai show me the cpu usage",
        "ai display memory information"
    ]
    
    for cmd in ai_commands:
        print(f"$ {cmd}")
        success, output = terminal._process_command(cmd)
        if output:
            print(output)
        print()
    
    print("4. Command History and Auto-completion Demo")
    print("-" * 50)
    print("Note: These features work interactively in the terminal")
    print("Try typing 'ls' and pressing Tab for auto-completion")
    print("Use up/down arrows to navigate command history")
    print()
    
    print("5. Error Handling Demo")
    print("-" * 25)
    
    error_commands = [
        "cd nonexistent_directory",
        "cat nonexistent_file.txt",
        "rm nonexistent_file.txt",
        "invalid_command"
    ]
    
    for cmd in error_commands:
        print(f"$ {cmd}")
        success, output = terminal._process_command(cmd)
        if output:
            print(output)
        print()
    
    # Clean up demo directory
    os.chdir("..")
    import shutil
    shutil.rmtree(demo_dir, ignore_errors=True)
    
    print("=" * 60)
    print("Demo completed! All features demonstrated successfully.")
    print("Run 'python main.py' to start the interactive terminal.")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()
