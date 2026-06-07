"""
Embedding Generator - Convert text to semantic vectors

Standardized on all-MiniLM-L6-v2 (384-dim) for portability.
"""

from typing import List, Union
import numpy as np


class EmbeddingGenerator:
    """
    Generate semantic embeddings from text

    Uses sentence-transformers (all-MiniLM-L6-v2) for 384-dim vectors.
    This model is standardized across all Knowledge Forge backends.
    """

    # Standardized embedding model
    MODEL_NAME = "all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384

    def __init__(self, model_name: str = None, device: str = None):
        """
        Initialize embedding generator

        Args:
            model_name: Model name (default: all-MiniLM-L6-v2)
            device: Device to use ('cpu', 'cuda', 'mps')
        """
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name or self.MODEL_NAME
        self.device = device

        # Load model
        self.model = SentenceTransformer(self.model_name, device=device)

        # Verify dimension
        test_embedding = self.model.encode("test", show_progress_bar=False)
        actual_dim = len(test_embedding)

        if self.model_name == self.MODEL_NAME and actual_dim != self.EMBEDDING_DIM:
            raise ValueError(
                f"Expected {self.EMBEDDING_DIM}-dim embeddings, "
                f"got {actual_dim}-dim. Model mismatch?"
            )

        self.embedding_dim = actual_dim

    def encode(self, text: Union[str, List[str]], batch_size: int = 32, show_progress: bool = False) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings from text

        Args:
            text: Single text or list of texts
            batch_size: Batch size for encoding
            show_progress: Show progress bar

        Returns:
            Single embedding or list of embeddings
        """
        is_single = isinstance(text, str)

        if is_single:
            text = [text]

        # Generate embeddings
        embeddings = self.model.encode(
            text,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )

        # Convert to list of lists
        embeddings = embeddings.tolist()

        return embeddings[0] if is_single else embeddings

    def encode_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Encode batch of texts (alias for encode)

        Args:
            texts: List of texts
            batch_size: Batch size

        Returns:
            List of embeddings
        """
        return self.encode(texts, batch_size=batch_size, show_progress=True)

    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.embedding_dim

    def get_model_name(self) -> str:
        """Get model name"""
        return self.model_name


# Singleton instance for reuse
_default_generator = None


def get_embedding_generator(model_name: str = None) -> EmbeddingGenerator:
    """
    Get or create default embedding generator

    This is cached to avoid reloading the model.
    """
    global _default_generator

    if _default_generator is None or (model_name and model_name != _default_generator.model_name):
        _default_generator = EmbeddingGenerator(model_name)

    return _default_generator


# Convenience function
def embed(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    """
    Quick embedding generation

    Uses default model (all-MiniLM-L6-v2).

    Args:
        text: Text or list of texts

    Returns:
        Embedding(s)

    Example:
        >>> embedding = embed("Hello world")
        >>> len(embedding)
        384

        >>> embeddings = embed(["Hello", "World"])
        >>> len(embeddings)
        2
        >>> len(embeddings[0])
        384
    """
    generator = get_embedding_generator()
    return generator.encode(text)
