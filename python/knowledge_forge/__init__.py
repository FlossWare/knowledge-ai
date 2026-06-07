"""
Knowledge Forge - Universal knowledge ingestion library for AI systems

Learn from ANY documentation format with multi-AI consensus validation.
"""

__version__ = "0.1"
__author__ = "FlossWare (sfloess)"
__license__ = "GPL-3.0"

from knowledge_forge.core import KnowledgeForge
from knowledge_forge.store.base import ContentChunk, Fact, VectorStore
from knowledge_forge.store.embeddings import EmbeddingGenerator, embed
from knowledge_forge.store.factory import VectorStoreFactory

__all__ = [
    "KnowledgeForge",
    "ContentChunk",
    "Fact",
    "VectorStore",
    "EmbeddingGenerator",
    "embed",
    "VectorStoreFactory",
]
