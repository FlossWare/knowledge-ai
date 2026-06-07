"""
Reranker - Improve result quality with cross-encoder

Two-stage retrieval:
1. Bi-encoder (fast): Get 100 candidates
2. Cross-encoder (accurate): Rerank top candidates
"""

from typing import List, Tuple
import numpy as np


class Reranker:
    """
    Rerank search results using cross-encoder

    Bi-encoder (sentence-transformers):
    - Encodes query and docs separately
    - Fast similarity search
    - Less accurate (no query-doc interaction)

    Cross-encoder (reranking):
    - Encodes query+doc together
    - Slow (must process each pair)
    - More accurate (understands relevance)
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize reranker

        Args:
            model_name: Cross-encoder model name
        """
        from sentence_transformers import CrossEncoder

        self.model = CrossEncoder(model_name)
        self.model_name = model_name

    def rerank(
        self,
        query: str,
        documents: List,
        top_k: int = 5
    ) -> List[Tuple[any, float]]:
        """
        Rerank documents using cross-encoder

        Args:
            query: Search query
            documents: List of documents (ContentChunk objects)
            top_k: Number of results to return

        Returns:
            List of (document, score) tuples, sorted by relevance
        """
        if not documents:
            return []

        # Prepare query-document pairs
        pairs = []
        for doc in documents:
            content = doc.content if hasattr(doc, 'content') else str(doc)
            pairs.append([query, content])

        # Score all pairs
        scores = self.model.predict(pairs)

        # Combine documents with scores
        doc_scores = list(zip(documents, scores))

        # Sort by score (descending)
        doc_scores.sort(key=lambda x: x[1], reverse=True)

        return doc_scores[:top_k]

    def rerank_with_scores(
        self,
        query: str,
        documents: List,
        top_k: int = 5
    ) -> List:
        """
        Rerank and add scores to documents

        Args:
            query: Search query
            documents: List of documents
            top_k: Number of results

        Returns:
            List of documents with rerank_score added
        """
        reranked = self.rerank(query, documents, top_k)

        results = []
        for doc, score in reranked:
            # Add rerank score to document
            if hasattr(doc, 'metadata'):
                doc.metadata['rerank_score'] = float(score)
            results.append(doc)

        return results


# Singleton for reuse (model is large)
_reranker = None


def get_reranker(model_name: str = None) -> Reranker:
    """
    Get or create reranker instance

    Caches the model to avoid reloading.
    """
    global _reranker

    if _reranker is None or (model_name and model_name != _reranker.model_name):
        _reranker = Reranker(model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2")

    return _reranker


def rerank(query: str, documents: List, top_k: int = 5) -> List:
    """
    Convenience function for reranking

    Args:
        query: Search query
        documents: List of documents
        top_k: Number of results

    Returns:
        Reranked documents

    Example:
        >>> results = forge.search("query", top_k=100)  # Get many candidates
        >>> reranked = rerank("query", results, top_k=5)  # Rerank to top 5
    """
    ranker = get_reranker()
    return ranker.rerank_with_scores(query, documents, top_k)
