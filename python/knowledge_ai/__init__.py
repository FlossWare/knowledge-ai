"""
Knowledge AI - Universal knowledge ingestion library for AI systems

Learn from ANY documentation format with multi-AI consensus validation.

Uses:
- vectordb-ai: Vector storage layer
- semantic-search-ai: Search enhancements
- consensus-ai: Multi-AI validation
"""

__version__ = "0.4"
__author__ = "FlossWare (sfloess)"
__license__ = "GPL-3.0"

from knowledge_ai.core import KnowledgeAI

# Re-export from dependencies for convenience
from vectordb_ai import ContentChunk, Fact, VectorStore, VectorStoreFactory, embed
from semantic_search_ai import HybridSearch, Reranker, AdvancedFilter

__all__ = [
    "KnowledgeAI",
    # From vectordb-ai
    "ContentChunk",
    "Fact",
    "VectorStore",
    "VectorStoreFactory",
    "embed",
    # From semantic-search-ai
    "HybridSearch",
    "Reranker",
    "AdvancedFilter",
]
