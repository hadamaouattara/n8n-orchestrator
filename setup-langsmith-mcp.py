#!/usr/bin/env python3
"""
Setup script for LangSmith MCP Server
Installs dependencies and configures the server for SAPience integration
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def install_dependencies():
    """Install Python dependencies for LangSmith MCP."""
    print("🔧 Installing LangSmith MCP dependencies...")
    
    requirements = [
        "langsmith>=0.1.0",
        "mcp>=1.0.0", 
        "pydantic>=2.0.0",
        "httpx>=0.27.0",
        "asyncio-throttle>=1.0.0"
    ]
    
    for req in requirements:
        run_command([sys.executable, "-m", "pip", "install", req])
    
    print("✅ Dependencies installed successfully!")

def setup_server_directory():
    """Create the LangSmith MCP server directory."""
    server_dir = Path.home() / "langsmith-mcp-server"
    server_dir.mkdir(exist_ok=True)
    
    # Copy server files
    current_dir = Path(__file__).parent
    server_files = [
        "server.py",
        "package.json", 
        "README.md"
    ]
    
    for file in server_files:
        src = current_dir / "mcp-servers" / "langsmith-mcp" / file
        dst = server_dir / file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"📁 Copied {file} to {server_dir}")
    
    return server_dir

def create_claude_config():
    """Create Claude Desktop configuration with LangSmith MCP."""
    config_dir = Path.home() / ".claude"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "claude_desktop_config.json"
    server_dir = Path.home() / "langsmith-mcp-server"
    
    # Your existing configuration with LangSmith added
    config = {
        "mcpServers": {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", ""),
                    "GITHUB_DEFAULT_OWNER": "hadamaouattara",
                    "NODE_OPTIONS": "--max-old-space-size=4096",
                    "MCP_TIMEOUT": "60000",
                    "MCP_RETRY_COUNT": "5",
                    "GITHUB_API_VERSION": "2022-11-28"
                },
                "disabled": False
            },
            "qiskit-mcp": {
                "command": str(Path.home() / "qiskit-mcp-server" / ".venv" / "Scripts" / "python.exe"),
                "args": [str(Path.home() / "qiskit-mcp-server" / "main.py")],
                "env": {
                    "PYTHONPATH": str(Path.home() / "qiskit-mcp-server"),
                    "MCP_TIMEOUT": "60000",
                    "QISKIT_SUPPRESS_PACKAGING_WARNINGS": "Y",
                    "PYTHONUNBUFFERED": "1"
                },
                "disabled": False
            },
            "n8n-mcp": {
                "command": "docker",
                "args": [
                    "run", "-i", "--rm", "--init", "--network=host",
                    "-e", "MCP_MODE=stdio",
                    "-e", "LOG_LEVEL=info", 
                    "-e", "DISABLE_CONSOLE_OUTPUT=false",
                    "-e", f"N8N_API_URL={os.getenv('N8N_API_URL', 'https://exonov-u39090.vm.elestio.app')}",
                    "-e", f"N8N_API_KEY={os.getenv('N8N_API_KEY', '')}",
                    "-e", "N8N_API_TIMEOUT=60000",
                    "-e", "N8N_VERIFY_SSL=false",
                    "-e", "N8N_REQUEST_TIMEOUT=30000",
                    "ghcr.io/czlonkowski/n8n-mcp:latest"
                ],
                "disabled": False
            },
            "langsmith-mcp": {
                "command": sys.executable,
                "args": [str(server_dir / "server.py")],
                "env": {
                    "LANGSMITH_API_KEY": "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",
                    "LANGSMITH_PROJECT": "sapience",
                    "LANGSMITH_ENDPOINT": "https://api.smith.langchain.com",
                    "SAP_COMPANY_CODES": "1000,2000,3000",
                    "SAPIENCE_API_URL": os.getenv('SAPIENCE_API_URL', 'https://exonov-u39090.vm.elestio.app/api'),
                    "N8N_WEBHOOK_URL": os.getenv('N8N_WEBHOOK_URL', 'https://exonov-u39090.vm.elestio.app/webhook'),
                    "PYTHONPATH": str(server_dir),
                    "PYTHONUNBUFFERED": "1",
                    "MCP_TIMEOUT": "60000",
                    "LOG_LEVEL": "info"
                },
                "disabled": False
            },
            "postgres": {
                "command": "docker",
                "args": [
                    "run", "-i", "--rm", "--init", "--network=host",
                    "-e", f"POSTGRES_CONNECTION_STRING={os.getenv('POSTGRES_CONNECTION_STRING', '')}",
                    "-e", "PGCONNECT_TIMEOUT=30",
                    "-e", "PGCOMMAND_TIMEOUT=60000"
                ],
                "image": "mcp/postgres",
                "disabled": False
            }
        },
        "globalSettings": {
            "logging": {
                "level": "info",
                "enabled": True,
                "maxFileSize": "10MB",
                "maxFiles": 5
            },
            "timeout": 60000,
            "retryPolicy": {
                "enabled": True,
                "maxRetries": 5,
                "retryDelay": 3000,
                "exponentialBackoff": True
            },
            "performance": {
                "concurrentConnections": 10,
                "requestPooling": True
            }
        }
    }
    
    # Write configuration
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Claude Desktop config created: {config_file}")
    return config_file

def test_langsmith_connection():
    """Test LangSmith API connection."""
    print("🧪 Testing LangSmith connection...")
    
    try:
        import langsmith
        client = langsmith.Client(
            api_key="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"
        )
        
        # Test API connection
        projects = list(client.list_projects(limit=1))
        print("✅ LangSmith connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ LangSmith connection failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up LangSmith MCP Server for SAPience...")
    
    # Install dependencies
    install_dependencies()
    
    # Setup server directory
    server_dir = setup_server_directory()
    print(f"📁 Server directory: {server_dir}")
    
    # Create Claude configuration
    config_file = create_claude_config()
    
    # Test connection
    test_langsmith_connection()
    
    print(f"""
🎉 LangSmith MCP Server setup complete!

📋 Next steps:
1. Restart Claude Desktop to load new configuration
2. Test the integration with: "Claude, trace a sapience workflow"
3. View traces at: https://smith.langchain.com/projects/sapience

🔧 Configuration:
- Server: {server_dir}
- Config: {config_file}
- Project: sapience

🚀 Ready to trace your SAPience ML workflows!
""")

if __name__ == "__main__":
    main()