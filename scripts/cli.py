#!/usr/bin/env python3
"""
Jade Box CLI
Command-line interface for managing and using Jade Box.
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import Jade components
try:
    from rag.logic.embed import embed_all_tools, search_similar_tools
    from rag.embed import EmbeddingModel
    from unified_api.logic.executor import execute_tool_by_name
except ImportError:
    print("⚠️  Can't find Jade Box modules. Are you in the right directory?")
    sys.exit(1)

class JadeCLI:
    def __init__(self):
        self.tools_dir = Path("db/mcp_tools")
        self.embedding_model = None
    
    def setup_embedding_model(self, model_type: str = "minilm") -> None:
        """Initialize the embedding model."""
        try:
            self.embedding_model = EmbeddingModel(model_type)
            print(f"✅ Initialized {model_type} embedding model")
        except Exception as e:
            print(f"❌ Failed to initialize embedding model: {e}")
            sys.exit(1)
    
    def reindex(self, tools_dir: Optional[str] = None) -> None:
        """Rebuild the vector index for all tools."""
        if tools_dir:
            self.tools_dir = Path(tools_dir)
        
        print(f"🔄 Reindexing tools from {self.tools_dir}...")
        try:
            embed_all_tools(str(self.tools_dir))
            print("✅ Reindex complete!")
        except Exception as e:
            print(f"❌ Reindex failed: {e}")
            sys.exit(1)
    
    def search(self, query: str, limit: int = 3) -> None:
        """Search the knowledge base."""
        print(f"🔍 Searching: {query}")
        try:
            results = search_similar_tools(query, top_k=limit)
            
            if not results:
                print("❌ No matching tools or documents found")
                return
            
            for i, result in enumerate(results, 1):
                print(f"\n📌 Match {i} (Score: {result['score']:.1%})")
                print(f"Tool: {result['tool_name']}")
                print(f"Source: {result['source']}")
                print("Context:")
                print(result['text'])
                
        except Exception as e:
            print(f"❌ Search failed: {e}")
            sys.exit(1)
    
    def execute(self, tool_name: str) -> None:
        """Execute a specific tool."""
        print(f"⚡ Executing tool: {tool_name}")
        try:
            result = execute_tool_by_name(tool_name)
            
            if result["returncode"] == 0:
                print("✅ Tool execution successful:")
                if result["stdout"]:
                    print(result["stdout"])
            else:
                print("❌ Tool execution failed:")
                if result["stderr"]:
                    print(result["stderr"])
                sys.exit(1)
                
        except FileNotFoundError:
            print(f"❌ Tool '{tool_name}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Execution failed: {e}")
            sys.exit(1)
    
    def create_tool(self, name: str, command: str, description: str) -> None:
        """Create a new tool definition."""
        tool_file = self.tools_dir / f"{name}.json"
        
        if tool_file.exists():
            print(f"❌ Tool '{name}' already exists")
            sys.exit(1)
        
        tool_data = {
            "tool_name": name,
            "description": description,
            "command": command,
            "created_at": datetime.now().isoformat(),
            "tags": [],
            "examples": []
        }
        
        try:
            self.tools_dir.mkdir(parents=True, exist_ok=True)
            with open(tool_file, 'w') as f:
                json.dump(tool_data, f, indent=2)
            
            print(f"✅ Created tool: {name}")
            print("🔄 Reindexing tools...")
            self.reindex()
            
        except Exception as e:
            print(f"❌ Failed to create tool: {e}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Jade Box CLI - Manage and use Jade Box from the command line"
    )
    
    # Main commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Reindex command
    reindex_parser = subparsers.add_parser("reindex", help="Rebuild the vector index")
    reindex_parser.add_argument(
        "--dir",
        help="Tools directory to index (default: db/mcp_tools)"
    )
    reindex_parser.add_argument(
        "--model",
        choices=["minilm", "instructor"],
        default="minilm",
        help="Embedding model to use"
    )
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search the knowledge base")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--limit",
        type=int,
        default=3,
        help="Maximum number of results"
    )
    
    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute a tool")
    execute_parser.add_argument("tool", help="Name of tool to execute")
    
    # Create tool command
    create_parser = subparsers.add_parser("create", help="Create a new tool")
    create_parser.add_argument("name", help="Tool name")
    create_parser.add_argument("command", help="Command to execute")
    create_parser.add_argument(
        "--description",
        default="",
        help="Tool description"
    )
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = JadeCLI()
    
    # Handle commands
    if args.command == "reindex":
        cli.setup_embedding_model(args.model)
        cli.reindex(args.dir)
        
    elif args.command == "search":
        cli.search(args.query, args.limit)
        
    elif args.command == "execute":
        cli.execute(args.tool)
        
    elif args.command == "create":
        cli.create_tool(args.name, args.command, args.description)
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 