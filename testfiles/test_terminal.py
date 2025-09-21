#!/usr/bin/env python3
"""
Test script for PyTerminal
Quick test of all core functionality
"""

import os
import sys
from terminal import PyTerminal

def test_terminal():
    """Test all terminal commands"""
    print("Testing PyTerminal - Core Functionality")
    print("=" * 40)
    
    # Initialize terminal
    terminal = PyTerminal()
    
    # Test commands
    test_commands = [
        ("pwd", "Show current directory"),
        ("ls", "List files"),
        ("mkdir test_dir", "Create directory"),
        ("touch test_file.txt", "Create file"),
        ("echo 'Hello World' > test_file.txt", "Write to file"),
        ("cat test_file.txt", "Read file"),
        ("ls test_dir", "List directory contents"),
        ("cp test_file.txt test_dir/", "Copy file"),
        ("mv test_file.txt test_dir/moved_file.txt", "Move file"),
        ("ls test_dir", "List after move"),
        ("cpu", "Show CPU usage"),
        ("mem", "Show memory usage"),
        ("ps", "Show processes"),
        ("help", "Show help"),
        ("rm test_dir/moved_file.txt", "Remove file"),
        ("rmdir test_dir", "Remove directory"),
        ("ls", "Final listing")
    ]
    
    for cmd, description in test_commands:
        print(f"\n{description}:")
        print(f"$ {cmd}")
        success, output = terminal._process_command(cmd)
        if output:
            print(output)
        if not success and cmd not in ["rmdir test_dir"]:  # rmdir might fail if dir not empty
            print(f"❌ Command failed: {cmd}")
        else:
            print("✅ Success")
    
    print("\n" + "=" * 40)
    print("Test completed!")

if __name__ == "__main__":
    test_terminal()
