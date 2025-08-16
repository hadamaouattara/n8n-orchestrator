#!/usr/bin/env python3
"""
Simple LangSmith MCP Server for SAPience
Minimal dependencies version
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List
from datetime import datetime

try:
    from langsmith import Client
    LANGSMITH_AVAILABLE = True
except ImportError:
    LANGSMITH_AVAILABLE = False
    print("Warning: LangSmith not available. Install with: python -m pip install langsmith")

class SimpleLangSmithMCP:
    def __init__(self):
        self.api_key = os.getenv("LANGSMITH_API_KEY")
        self.project = os.getenv("LANGSMITH_PROJECT", "sapience")
        self.client = None
        
        if LANGSMITH_AVAILABLE and self.api_key:
            try:
                self.client = Client(api_key=self.api_key)
                print(f"✅ LangSmith connected to project: {self.project}")
            except Exception as e:
                print(f"❌ LangSmith connection failed: {e}")
    
    async def trace_workflow(self, workflow_name: str, metadata: Dict = None):
        """Trace a SAPience workflow."""
        if not self.client:
            return {"error": "LangSmith not available"}
        
        try:
            session_id = f"sapience_{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create trace
            run = self.client.create_run(
                name=workflow_name,
                session_id=session_id,
                project_name=self.project,
                inputs={"metadata": metadata or {}},
                run_type="chain"
            )
            
            return {
                "success": True,
                "session_id": session_id,
                "run_id": str(run.id),
                "trace_url": f"https://smith.langchain.com/projects/{self.project}/runs/{run.id}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def log_prediction(self, model_name: str, prediction: Any, metadata: Dict = None):
        """Log ML prediction results."""
        if not self.client:
            return {"error": "LangSmith not available"}
        
        try:
            run = self.client.create_run(
                name=f"ml_prediction_{model_name}",
                project_name=self.project,
                inputs={"model": model_name, "metadata": metadata or {}},
                outputs={"prediction": prediction},
                run_type="llm"
            )
            
            return {
                "success": True,
                "run_id": str(run.id),
                "logged_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

# Simple MCP protocol handler
async def handle_mcp_message(message: Dict) -> Dict:
    """Handle MCP protocol messages."""
    mcp = SimpleLangSmithMCP()
    
    method = message.get("method")
    params = message.get("params", {})
    
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "trace_sapience_workflow",
                        "description": "Trace a SAPience ML workflow",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "workflow_name": {"type": "string"},
                                "metadata": {"type": "object"}
                            },
                            "required": ["workflow_name"]
                        }
                    },
                    {
                        "name": "log_ml_prediction",
                        "description": "Log ML prediction results",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "prediction": {"type": "object"},
                                "metadata": {"type": "object"}
                            },
                            "required": ["model_name", "prediction"]
                        }
                    }
                ]
            }
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "trace_sapience_workflow":
            result = await mcp.trace_workflow(
                arguments.get("workflow_name"),
                arguments.get("metadata")
            )
        elif tool_name == "log_ml_prediction":
            result = await mcp.log_prediction(
                arguments.get("model_name"),
                arguments.get("prediction"),
                arguments.get("metadata")
            )
        else:
            result = {"error": f"Unknown tool: {tool_name}"}
        
        return {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
        }
    
    return {
        "jsonrpc": "2.0",
        "id": message.get("id"),
        "error": {"code": -32601, "message": f"Unknown method: {method}"}
    }

async def main():
    """Main MCP server loop."""
    print("🚀 Starting Simple LangSmith MCP Server...")
    
    # Test LangSmith connection
    mcp = SimpleLangSmithMCP()
    if mcp.client:
        print("✅ LangSmith connection successful!")
    else:
        print("⚠️  LangSmith not connected - check LANGSMITH_API_KEY")
    
    # Simple stdin/stdout MCP protocol
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            try:
                message = json.loads(line.strip())
                response = await handle_mcp_message(message)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                continue
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())