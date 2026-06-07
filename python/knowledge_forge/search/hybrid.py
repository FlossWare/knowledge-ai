"""
Hybrid Search - Combine semantic and keyword search

Best of both worlds: semantic similarity + exact keyword matching.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
import re


@dataclass
class SearchResult:
    """Unified search result"""
    chunk_id: str
    content: str
    semantic_score: float = 0.0
    keyword_score: float = 0.0
    combined_score: float = 0.0
    source: str = ""
    metadata: Dict = None


class HybridSearch:
    """
    Hybrid search combining semantic and keyword matching

    Uses:
    - Semantic: Vector similarity (cosine) for meaning
    - Keyword: BM25 algorithm for exact terms
    - Fusion: Reciprocal Rank Fusion (RRF) to combine
    """

    def __init__(
        self,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3
    ):
        """
        Initialize hybrid search

        Args:
            semantic_weight: Weight for semantic results (0-1)
            keyword_weight: Weight for keyword results (0-1)
        """
        # Normalize weights
        total = semantic_weight + keyword_weight
        self.semantic_weight = semantic_weight / total
        self.keyword_weight = keyword_weight / total

    def merge_results(
        self,
        semantic_results: List,
        keyword_results: List,
        top_k: int = 10
    ) -> List[SearchResult]:
        """
        Merge semantic and keyword results using Reciprocal Rank Fusion

        RRF formula: score = sum(1 / (k + rank_i))
        where k=60 (standard constant), rank_i is position in each list

        Args:
            semantic_results: Results from vector search
            keyword_results: Results from keyword search
            top_k: Number of results to return

        Returns:
            Merged and ranked results
        """
        k = 60  # RRF constant

        # Build score maps
        semantic_scores = {}
        keyword_scores = {}
        all_chunks = {}

        # Process semantic results
        for rank, result in enumerate(semantic_results, start=1):
            chunk_id = result.chunk_id if hasattr(result, 'chunk_id') else str(result)
            semantic_scores[chunk_id] = 1.0 / (k + rank)
            all_chunks[chunk_id] = result

        # Process keyword results
        for rank, result in enumerate(keyword_results, start=1):
            chunk_id = result.chunk_id if hasattr(result, 'chunk_id') else str(result)
            keyword_scores[chunk_id] = 1.0 / (k + rank)
            if chunk_id not in all_chunks:
                all_chunks[chunk_id] = result

        # Combine scores
        results = []
        for chunk_id, chunk in all_chunks.items():
            sem_score = semantic_scores.get(chunk_id, 0.0)
            kw_score = keyword_scores.get(chunk_id, 0.0)

            # Weighted combination
            combined = (
                self.semantic_weight * sem_score +
                self.keyword_weight * kw_score
            )

            results.append(SearchResult(
                chunk_id=chunk_id,
                content=chunk.content if hasattr(chunk, 'content') else str(chunk),
                semantic_score=sem_score,
                keyword_score=kw_score,
                combined_score=combined,
                source=chunk.source if hasattr(chunk, 'source') else '',
                metadata=chunk.metadata if hasattr(chunk, 'metadata') else {}
            ))

        # Sort by combined score
        results.sort(key=lambda x: x.combined_score, reverse=True)

        return results[:top_k]

    def keyword_search_simple(
        self,
        query: str,
        documents: List,
        top_k: int = 10
    ) -> List:
        """
        Simple keyword search using term frequency

        This is a lightweight BM25-like scoring.
        For production, consider using Elasticsearch or Solr for keyword search.

        Args:
            query: Search query
            documents: List of documents (ContentChunk objects)
            top_k: Number of results

        Returns:
            Ranked documents by keyword relevance
        """
        query_terms = set(query.lower().split())

        scores = []
        for doc in documents:
            content = doc.content.lower() if hasattr(doc, 'content') else str(doc).lower()

            # Simple term frequency scoring
            score = 0.0
            for term in query_terms:
                # Count occurrences
                count = content.count(term)
                if count > 0:
                    # TF component (with diminishing returns)
                    score += 1 + (count / (count + 1))

                # Boost for exact phrase match
                if query.lower() in content:
                    score += 5.0

            scores.append((doc, score))

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, score in scores[:top_k]]


# Singleton for reuse
_hybrid_search = None


def get_hybrid_search(semantic_weight: float = 0.7, keyword_weight: float = 0.3) -> HybridSearch:
    """Get or create hybrid search instance"""
    global _hybrid_search

    if _hybrid_search is None:
        _hybrid_search = HybridSearch(semantic_weight, keyword_weight)

    return _hybrid_search
