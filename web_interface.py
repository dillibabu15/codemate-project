#!/usr/bin/env python3
"""
Web-based interface for PyTerminal
Optional web interface using Flask
"""

from flask import Flask, render_template, request, jsonify
import os
import sys
from terminal import PyTerminal
import threading
import queue

app = Flask(__name__)

# Global terminal instance
terminal = PyTerminal()
command_queue = queue.Queue()
output_queue = queue.Queue()

def terminal_worker():
    """Background worker to process commands"""
    while True:
        try:
            command = command_queue.get(timeout=1)
            if command == "EXIT":
                break
            
            success, output = terminal._process_command(command)
            output_queue.put({
                'success': success,
                'output': output,
                'command': command
            })
        except queue.Empty:
            continue
        except Exception as e:
            output_queue.put({
                'success': False,
                'output': f"Error: {str(e)}",
                'command': command
            })

# Start background worker
worker_thread = threading.Thread(target=terminal_worker, daemon=True)
worker_thread.start()

@app.route('/')
def index():
    """Main web interface"""
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    """Execute a command and return output"""
    data = request.get_json()
    command = data.get('command', '')
    
    if not command.strip():
        return jsonify({'success': False, 'output': 'No command provided'})
    
    # Add command to queue
    command_queue.put(command)
    
    # Wait for output
    try:
        result = output_queue.get(timeout=5)
        return jsonify(result)
    except queue.Empty:
        return jsonify({'success': False, 'output': 'Command timeout'})

@app.route('/status')
def status():
    """Get current terminal status"""
    return jsonify({
        'current_dir': terminal.current_dir,
        'prompt': terminal._get_prompt()
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PyTerminal Web Interface</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background-color: #1e1e1e;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        .terminal {
            background-color: #000000;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 20px;
            min-height: 400px;
            overflow-y: auto;
        }
        .output {
            white-space: pre-wrap;
            margin-bottom: 10px;
        }
        .input-container {
            display: flex;
            align-items: center;
        }
        .prompt {
            color: #00ff00;
            margin-right: 10px;
        }
        .command-input {
            background: transparent;
            border: none;
            color: #ffffff;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            outline: none;
            flex: 1;
        }
        .error {
            color: #ff4444;
        }
        .success {
            color: #44ff44;
        }
        .help {
            color: #4444ff;
        }
    </style>
</script>
</head>
<body>
    <h1>PyTerminal Web Interface</h1>
    <div class="terminal" id="terminal">
        <div class="output">Welcome to PyTerminal Web Interface!</div>
        <div class="output">Type 'help' for available commands or 'exit' to quit</div>
        <div class="output">----------------------------------------</div>
    </div>
    
    <div class="input-container">
        <span class="prompt" id="prompt">user@pyterminal:~$</span>
        <input type="text" class="command-input" id="commandInput" autofocus>
    </div>

    <script>
        const terminal = document.getElementById('terminal');
        const commandInput = document.getElementById('commandInput');
        const prompt = document.getElementById('prompt');
        
        let commandHistory = [];
        let historyIndex = -1;
        
        // Load initial status
        loadStatus();
        
        function loadStatus() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    prompt.textContent = data.prompt;
                });
        }
        
        function addOutput(text, className = '') {
            const output = document.createElement('div');
            output.className = `output ${className}`;
            output.textContent = text;
            terminal.appendChild(output);
            terminal.scrollTop = terminal.scrollHeight;
        }
        
        function executeCommand(command) {
            if (!command.trim()) return;
            
            // Add to history
            commandHistory.unshift(command);
            if (commandHistory.length > 100) {
                commandHistory.pop();
            }
            historyIndex = -1;
            
            // Show command
            addOutput(`$ ${command}`);
            
            // Execute command
            fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                if (data.output) {
                    const className = data.success ? 'success' : 'error';
                    addOutput(data.output, className);
                }
                
                // Update prompt
                loadStatus();
            })
            .catch(error => {
                addOutput(`Error: ${error.message}`, 'error');
            });
        }
        
        commandInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                const command = commandInput.value.trim();
                if (command) {
                    executeCommand(command);
                    commandInput.value = '';
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (historyIndex < commandHistory.length - 1) {
                    historyIndex++;
                    commandInput.value = commandHistory[historyIndex];
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex > 0) {
                    historyIndex--;
                    commandInput.value = commandHistory[historyIndex];
                } else if (historyIndex === 0) {
                    historyIndex = -1;
                    commandInput.value = '';
                }
            }
        });
        
        // Auto-focus input
        commandInput.focus();
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    
    print("Starting PyTerminal Web Interface...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
