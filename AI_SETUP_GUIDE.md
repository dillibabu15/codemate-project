# AI Setup Guide for PyTerminal

## 🚀 Quick Setup

### Option 1: Interactive Setup (Recommended)
```bash
python setup_ai.py
```
Follow the prompts to configure your LLM API key.

### Option 2: Environment Variable
```bash
# For OpenAI
export OPENAI_API_KEY="your-api-key-here"

# Or for custom LLM
export LLM_API_KEY="your-api-key-here"
```

### Option 3: Manual Configuration
Create a file `~/.pyterminal_config`:
```
API_KEY=your-api-key-here
MODEL=gpt-3.5-turbo
API_URL=https://api.openai.com/v1/chat/completions
```

## 🔧 Supported LLM Providers

### OpenAI (Default)
- **Models**: GPT-3.5-turbo, GPT-4, GPT-4-turbo
- **API URL**: https://api.openai.com/v1/chat/completions
- **Setup**: Get API key from https://platform.openai.com/api-keys

### Custom API Endpoints
- **Compatible**: Any OpenAI-compatible API
- **Examples**: Local LLM servers, other providers
- **Setup**: Provide custom API URL and model name

## 🧪 Testing Your Setup

### Test AI Commands
```bash
python test_ai.py
```

### Test in Terminal
```bash
python main.py
# Then try:
ai create a folder called test
ai show me the cpu usage
ai display memory information
```

## 📋 Example Commands

Once configured, you can use natural language:

```bash
# File operations
ai create a folder called backup
ai make a file called notes.txt
ai show me all the files
ai delete the file temp.txt
ai copy file1.txt to file2.txt
ai move old_file.txt to backup/

# System monitoring
ai what's my CPU usage
ai show memory information
ai list running processes
ai display disk usage

# Complex operations
ai create a folder called project and move all .py files into it
ai backup my documents folder to a new location
```

## ⚙️ Configuration Options

### Environment Variables
- `OPENAI_API_KEY` or `LLM_API_KEY`: Your API key
- `PYTERMINAL_MODEL`: Model name (default: gpt-3.5-turbo)
- `PYTERMINAL_API_URL`: API endpoint (default: OpenAI)
- `PYTERMINAL_MAX_TOKENS`: Max tokens per request (default: 500)
- `PYTERMINAL_TEMPERATURE`: Response randomness (default: 0.1)

### Configuration File
The setup script creates `~/.pyterminal_config` with your settings.

## 🔄 Fallback Mode

If no API key is configured, PyTerminal automatically falls back to pattern matching:
- Basic commands still work
- Limited natural language understanding
- No internet connection required

## 🐛 Troubleshooting

### Common Issues

1. **"No API key configured"**
   - Run `python setup_ai.py` to configure
   - Or set `OPENAI_API_KEY` environment variable

2. **"LLM interpretation failed"**
   - Check your internet connection
   - Verify API key is correct
   - Check API endpoint URL

3. **"No commands generated"**
   - Try simpler commands
   - Check if the request is clear
   - Fallback pattern matching will activate

### Testing Commands
```bash
# Test configuration
python -c "from config import PyTerminalConfig; print(PyTerminalConfig().is_configured())"

# Test AI interpreter
python -c "from ai_interpreter import AIInterpreter; ai = AIInterpreter(); print(ai.interpret('show files'))"
```

## 💡 Tips

1. **Start Simple**: Begin with basic commands like "show files" or "cpu usage"
2. **Be Specific**: "create a folder called backup" works better than "make a backup"
3. **Check Fallback**: If AI fails, fallback pattern matching will still work
4. **Monitor Usage**: Keep track of API usage to avoid overages

## 🎯 Success Indicators

You'll know the AI is working when:
- ✅ `python test_ai.py` shows "✅ AI test successful!"
- ✅ `ai show files` generates `ls` command
- ✅ Complex commands like "create folder and move file" work
- ✅ No "LLM interpretation failed" errors

Happy terminal-ing! 🚀
