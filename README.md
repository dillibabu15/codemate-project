# PyTerminal - Python Command Terminal

A comprehensive Python-based command terminal with advanced features including AI natural language interpretation, system monitoring, and full file system operations.

## Features

### Core Terminal Commands
- **File System Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cat`, `touch`, `cp`, `mv`
- **System Monitoring**: `cpu`, `mem`, `ps`, `disk`
- **Terminal Features**: `help`, `history`, `clear`, `exit`

### Advanced Features
- **Command History**: Navigate through previous commands with up/down arrows
- **Auto-completion**: Tab completion for commands and file names
- **AI Natural Language Interpreter**: Convert natural language to shell commands
- **Error Handling**: Comprehensive error handling for all operations
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Quick Setup
```bash
# Clone or download the project files
python setup.py
```

### Manual Setup

1. **Download the project files**
   - Download all Python files to a directory
   - Ensure you have Python 3.7+ installed

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   - Copy `.env.template` to `.env`
   - Add your API key to `.env` file

4. **Run the terminal**
   ```bash
   python main.py
   ```

5. **Setup AI features (optional)**
   ```bash
   python setup_ai.py
   ```
   Follow the prompts to configure your LLM API key

6. **Run the web interface (optional)**
   ```bash
   pip install flask
   python web_interface.py
   ```
   Then open http://localhost:5000 in your browser

## Usage

### Basic Commands

```bash
# File system operations
ls                    # List files and directories
cd /path/to/directory # Change directory
pwd                   # Show current directory
mkdir new_folder      # Create directory
rm file.txt           # Remove file
cat file.txt          # Display file contents
touch new_file.txt    # Create empty file
cp source dest        # Copy file/directory
mv source dest        # Move/rename file/directory

# System monitoring
cpu                   # Show CPU usage
mem                   # Show memory usage
ps                    # List running processes
disk                  # Show disk usage

# Terminal features
help                  # Show help
history               # Show command history
clear                 # Clear screen
exit                  # Exit terminal
```

### AI Natural Language Commands

Use the `ai` command to interpret natural language (requires API key setup):

```bash
ai create a folder called test
ai make a file called demo.txt
ai show me the files
ai create a folder called backup and move demo.txt into it
ai show me the cpu usage
ai display memory information
ai what's my disk usage
ai list all running processes
```

**Setup AI Features:**
1. Run `python setup_ai.py` to configure your LLM API key
2. Supports OpenAI GPT models and custom API endpoints
3. Falls back to pattern matching if no API key is configured

### Command History and Auto-completion

- Use **up/down arrows** to navigate through command history
- Press **Tab** for auto-completion of commands and file names
- Type `history` to see all previous commands

## Project Structure

```
pyterminal/
├── main.py              # Main entry point
├── terminal.py          # Core terminal implementation
├── commands.py          # Command registry and implementations
├── ai_interpreter.py    # AI natural language interpreter
├── demo.py             # Demo script
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Demo

Run the demo script to see all features in action:

```bash
python demo.py
```

The demo will:
1. Demonstrate all file system commands
2. Show system monitoring capabilities
3. Test AI natural language interpretation
4. Display error handling examples

## Technical Details

### Dependencies
- **psutil**: System and process monitoring
- **readline**: Command history and auto-completion (built-in)
- **os, subprocess, shutil**: File system operations (built-in)

### Architecture
- **Modular Design**: Easy to extend with new commands
- **Command Registry**: Centralized command management
- **Error Handling**: Comprehensive error handling throughout
- **Cross-platform**: Uses standard Python libraries for compatibility

### Adding New Commands

To add a new command:

1. Add the command function to `commands.py`:
   ```python
   def _cmd_newcommand(self, args: List[str], current_dir: str) -> Tuple[bool, str]:
       # Implementation here
       return True, "Success message"
   ```

2. Register the command in the `__init__` method:
   ```python
   self.commands['newcommand'] = self._cmd_newcommand
   ```

3. Add help text in the `_show_help` method

## Error Handling

The terminal includes comprehensive error handling for:
- Invalid commands
- File/directory not found
- Permission denied errors
- Invalid arguments
- System errors

## Platform Support

- **Windows**: Full support with Windows-specific features
- **macOS**: Full support with Unix-like features
- **Linux**: Full support with native terminal features

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Future Enhancements

- Web-based interface
- Plugin system for custom commands
- Advanced AI features
- Command aliases
- Scripting support
- Remote terminal capabilities
