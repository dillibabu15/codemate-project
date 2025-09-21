#!/usr/bin/env python3
"""
PyTerminal - Core terminal implementation
Handles command processing, execution, and user interface
"""

import os
import sys
import subprocess
import shutil
import psutil
import glob
from pathlib import Path
from typing import List, Optional, Tuple
from commands import CommandRegistry
from ai_interpreter import AIInterpreter

# Try to import readline, fallback for Windows
try:
    import readline
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

class PyTerminal:
    """Main terminal class that handles command processing and execution"""
    
    def __init__(self, ai_api_key: str = None):
        self.current_dir = os.getcwd()
        self.command_registry = CommandRegistry()
        self.ai_interpreter = AIInterpreter(api_key=ai_api_key)
        self.history_file = os.path.expanduser("~/.pyterminal_history")
        self._setup_readline()
        
    def _setup_readline(self):
        """Setup readline for command history and auto-completion"""
        if not HAS_READLINE:
            return
            
        # Load history
        if os.path.exists(self.history_file):
            readline.read_history_file(self.history_file)
        
        # Set up auto-completion
        readline.set_completer(self._completer)
        readline.parse_and_bind("tab: complete")
        
        # Set history length
        readline.set_history_length(1000)
    
    def _completer(self, text: str, state: int) -> Optional[str]:
        """Auto-completion function for readline"""
        if not HAS_READLINE:
            return None
            
        options = []
        
        # Get available commands
        commands = list(self.command_registry.commands.keys())
        options.extend([cmd for cmd in commands if cmd.startswith(text)])
        
        # Get files/directories in current directory
        try:
            files = os.listdir(self.current_dir)
            options.extend([f for f in files if f.startswith(text)])
        except OSError:
            pass
        
        # Return the option at the given state
        if state < len(options):
            return options[state]
        return None
    
    def _get_prompt(self) -> str:
        """Generate the terminal prompt"""
        username = os.getenv('USERNAME', 'user')
        hostname = os.getenv('COMPUTERNAME', 'pyterminal')
        current_dir_name = os.path.basename(self.current_dir) or '~'
        return f"{username}@{hostname}:{current_dir_name}$ "
    
    def _save_history(self):
        """Save command history to file"""
        if not HAS_READLINE:
            return
            
        try:
            readline.write_history_file(self.history_file)
        except OSError:
            pass
    
    def _process_command(self, command_line: str) -> Tuple[bool, str]:
        """
        Process a command line and return (success, output)
        """
        if not command_line.strip():
            return True, ""
        
        # Check for AI interpretation first
        if command_line.strip().startswith('ai '):
            ai_command = command_line[3:].strip()
            try:
                interpreted_commands = self.ai_interpreter.interpret(ai_command)
                if interpreted_commands:
                    output = []
                    for cmd in interpreted_commands:
                        success, cmd_output = self._process_command(cmd)
                        output.append(f"$ {cmd}")
                        output.append(cmd_output)
                    return True, "\n".join(output)
                else:
                    return False, "Could not interpret the command"
            except Exception as e:
                return False, f"AI interpretation error: {str(e)}"
        
        # Split command and arguments
        parts = command_line.strip().split()
        if not parts:
            return True, ""
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Handle built-in commands
        if command == "exit":
            return "exit", ""
        elif command == "help":
            return self._show_help()
        elif command == "history":
            return self._show_history()
        elif command == "clear":
            return True, "\033[2J\033[H"  # Clear screen
        else:
            # Execute command through registry
            return self.command_registry.execute(command, args, self.current_dir)
    
    def _show_help(self) -> Tuple[bool, str]:
        """Show help information"""
        help_text = """
PyTerminal - Available Commands:

File System Commands:
  ls [path]              - List files and directories
  cd <path>              - Change directory
  pwd                    - Print current directory
  mkdir <name>           - Create directory
  rm <file/folder>       - Remove file or directory
  cat <file>             - Display file contents
  touch <file>           - Create empty file
  cp <src> <dest>        - Copy file or directory
  mv <src> <dest>        - Move/rename file or directory
  rmdir <dir>            - Remove empty directory
  echo <text>            - Display text or write to file

System Monitoring:
  cpu                    - Show CPU usage
  mem                    - Show memory usage
  ps                     - List running processes
  disk                   - Show disk usage

Terminal Features:
  help                   - Show this help
  history                - Show command history
  clear                  - Clear screen
  exit                   - Exit terminal
  ai <command>           - AI natural language command interpreter

Examples:
  ai create a folder called test and move file1.txt into it
  ls -la
  cd /home/user
  cpu
        """
        return True, help_text.strip()
    
    def _show_history(self) -> Tuple[bool, str]:
        """Show command history"""
        if not HAS_READLINE:
            return False, "Command history not available on this platform"
            
        try:
            history = []
            for i in range(readline.get_current_history_length()):
                history.append(f"{i+1:4d}  {readline.get_history_item(i+1)}")
            return True, "\n".join(history) if history else "No history available"
        except Exception:
            return False, "Error retrieving history"
    
    def run(self):
        """Main terminal loop"""
        try:
            while True:
                try:
                    # Get user input
                    command_line = input(self._get_prompt())
                    
                    # Process command
                    result, output = self._process_command(command_line)
                    
                    # Handle special results
                    if result == "exit":
                        break
                    
                    # Display output
                    if output:
                        print(output)
                        
                except KeyboardInterrupt:
                    print("\nUse 'exit' to quit the terminal")
                    continue
                except EOFError:
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
        
        finally:
            # Save history before exiting
            self._save_history()
            print("\nGoodbye!")

if __name__ == "__main__":
    terminal = PyTerminal()
    terminal.run()
