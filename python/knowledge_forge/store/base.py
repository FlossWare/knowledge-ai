"""
Base class for vector store backends

Abstract interface that all vector databases must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import json


@dataclass
class ContentChunk:
    """
    Universal chunk format - portable across all backends

    This format can be serialized to JSON for portability.
    """
    chunk_id: str
    content: str
    source: str
    start_line: int = 0
    end_line: int = 0
    content_type: str = 'text'
    metadata: Dict = None
    embedding: List[float] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.embedding is None:
            self.embedding = []

    def to_dict(self) -> Dict:
        """Serialize to portable format"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        """Deserialize from portable format"""
        return cls(**data)


@dataclass
class Fact:
    """
    Structured fact extracted from chunks

    Facts are validated by multi-AI consensus.
    """
    fact_id: str
    text: str
    chunk_id: str  # Link to source chunk
    confidence: float
    fact_type: str = 'general'
    metadata: Dict = None
    embedding: List[float] = None
    proposed_by: List[str] = None  # Which AI workers proposed this

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.embedding is None:
            self.embedding = []
        if self.proposed_by is None:
            self.proposed_by = []

    def to_dict(self) -> Dict:
        """Serialize to portable format"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict):
        """Deserialize from portable format"""
        return cls(**data)


class VectorStore(ABC):
    """
    Abstract interface for vector database backends

    All vector databases must implement this interface.
    """

    @abstractmethod
    def add_chunks(self, chunks: List[ContentChunk]) -> int:
        """
        Add chunks to vector store

        Args:
            chunks: List of content chunks with embeddings

        Returns:
            Number of chunks added
        """
        pass

    @abstractmethod
    def add_facts(self, facts: List[Fact]) -> int:
        """
        Add facts to vector store

        Args:
            facts: List of validated facts with embeddings

        Returns:
            Number of facts added
        """
        pass

    @abstractmethod
    def search_chunks(self, query_embedding: List[float], top_k: int = 5, filter_dict: Dict = None) -> List[ContentChunk]:
        """
        Search chunks by vector similarity

        Args:
            query_embedding: Query vector (384-dim)
            top_k: Number of results
            filter_dict: Optional metadata filters

        Returns:
            List of matching chunks
        """
        pass

    @abstractmethod
    def search_facts(self, query_embedding: List[float], top_k: int = 5, filter_dict: Dict = None) -> List[Fact]:
        """
        Search facts by vector similarity

        Args:
            query_embedding: Query vector (384-dim)
            top_k: Number of results
            filter_dict: Optional metadata filters

        Returns:
            List of matching facts
        """
        pass

    @abstractmethod
    def get_chunk(self, chunk_id: str) -> Optional[ContentChunk]:
        """Get specific chunk by ID"""
        pass

    @abstractmethod
    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """Get specific fact by ID"""
        pass

    @abstractmethod
    def list_collections(self) -> List[str]:
        """List all collections"""
        pass

    @abstractmethod
    def clear_collection(self, name: str):
        """Clear a collection"""
        pass

    def export(self, path: str, format: str = 'json'):
        """
        Export to portable format

        Default implementation (can override for efficiency)
        """
        data = {
            'version': '1.0',
            'embedding_model': 'all-MiniLM-L6-v2',
            'embedding_dim': 384,
            'backend': self.__class__.__name__,
            'chunks': [c.to_dict() for c in self.get_all_chunks()],
            'facts': [f.to_dict() for f in self.get_all_facts()]
        }

        if format == 'json':
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def import_from(self, path: str, format: str = 'json'):
        """
        Import from portable format

        Default implementation (can override for efficiency)
        """
        if format == 'json':
            with open(path) as f:
                data = json.load(f)
        else:
            raise ValueError(f"Unsupported format: {format}")

        chunks = [ContentChunk.from_dict(c) for c in data.get('chunks', [])]
        facts = [Fact.from_dict(f) for f in data.get('facts', [])]

        if chunks:
            self.add_chunks(chunks)
        if facts:
            self.add_facts(facts)

    @abstractmethod
    def get_all_chunks(self) -> List[ContentChunk]:
        """Get all chunks (for export)"""
        pass

    @abstractmethod
    def get_all_facts(self) -> List[Fact]:
        """Get all facts (for export)"""
        pass
