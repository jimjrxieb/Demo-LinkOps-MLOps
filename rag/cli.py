#!/usr/bin/env python3
"""
RAG CLI Tool
Manage embeddings and test the RAG system.
"""

import argparse
import time
from pathlib import Path

from .logic.embed import embed_all_tools, search_similar_tools
from .embed import EmbeddingModel

def main():
    parser = argparse.ArgumentParser(description="RAG System Management CLI")
    
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Re-embed all tools in the tools directory"
    )
    
    parser.add_argument(
        "--model",
        choices=["minilm", "instructor"],
        default="minilm",
        help="Choose embedding model (default: minilm)"
    )
    
    parser.add_argument(
        "--search",
        type=str,
        help="Test search with a query"
    )
    
    parser.add_argument(
        "--tools-dir",
        type=str,
        default="db/mcp_tools",
        help="Directory containing tool JSON files"
    )
    
    args = parser.parse_args()
    
    # Initialize embedding model
    if args.model == "instructor":
        print("🧠 Using Instructor model")
    else:
        print("🧠 Using MiniLM model")
    
    # Handle reindexing
    if args.reindex:
        print(f"\n📥 Indexing tools from {args.tools_dir}")
        start_time = time.time()
        embed_all_tools(args.tools_dir)
        duration = time.time() - start_time
        print(f"✅ Indexing complete in {duration:.1f}s")
    
    # Handle search test
    if args.search:
        print(f"\n🔍 Searching for: {args.search}")
        results = search_similar_tools(args.search)
        
        if not results:
            print("❌ No matching tools found")
        else:
            for r in results:
                print(f"\n📌 {r['tool_name']}")
                print(f"Score: {r['score']:.1%}")
                print(f"Source: {r['source']}")
                print("Text:")
                print(r['text'])

if __name__ == "__main__":
    main() 