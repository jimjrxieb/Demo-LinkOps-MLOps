"""
RAG Logic Package
================

Core logic for RAG functionality.
"""

from .embed import DocumentEmbedder, embed_file
from .search import RAGSearchEngine, search_query

__all__ = ["RAGSearchEngine", "search_query", "DocumentEmbedder", "embed_file"]
