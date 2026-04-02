# Agentic MCP AI

A custom ReAct agent using Model Context Protocol (MCP) with file and terminal tools.

## Features

- ReAct pattern agent with thinking steps
- File reading capabilities
- Terminal command execution
- Configurable LLM integration (OpenRouter/OpenAI compatible)
- Simple CLI interface

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/agentic-mcp.git
cd agentic-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API credentials
```

## Configuration

Set the following environment variables in `.env`:

```env
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://openrouter.ai/api/v1
```

## Usage

```bash
python main.py
```

Example commands:
```
>> list files in current directory
>> read file README.md
>> execute: ls -la
```

## Project Structure

```
agentic-mcp/
├── app/
│   ├── agent.py          # ReAct agent implementation
│   ├── llm.py            # LLM configuration
│   ├── mcp.py            # MCP manager
│   └── tools/
│       ├── base.py       # Base tool interface
│       ├── file_tool.py  # File operations
│       └── terminal_tool.py  # Terminal commands
├── main.py               # CLI entry point
├── tests/                # Test files
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Tools

- **FileReader**: Read content from files on disk
- **Terminal**: Execute shell commands

## License

MIT
