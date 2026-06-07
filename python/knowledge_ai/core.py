"""
Core KnowledgeAI class - main entry point for the library
"""

from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import logging

from knowledge_ai.ingest.detector import FormatDetector
from knowledge_ai.extract.arbiter import ArbiterWorkerExtractor
from vectordb_ai import VectorStoreFactory, EmbeddingGenerator

logger = logging.getLogger(__name__)


class KnowledgeAI:
    """
    Universal knowledge ingestion library

    Learn from ANY documentation format with multi-AI consensus validation.

    Example:
        >>> ai = KnowledgeAI(collection='my-docs')
        >>> ai.learn_from_file('/path/to/tutorial.pdf')
        >>> result = ai.query('How does authentication work?')
        >>> print(result.answer)
    """

    def __init__(
        self,
        collection: str,
        persist_directory: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        workers: Optional[List[str]] = None,
        arbiter: Optional[str] = None,
        consensus_strategy: str = "rotating",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        top_k: int = 5,
        verbose: bool = False,
    ):
        """
        Initialize Knowledge AI

        Args:
            collection: Name of the knowledge base collection
            persist_directory: Where to store vector database data
            embedding_model: Sentence transformer model name
            workers: List of AI models for extraction (e.g., ['claude-opus', 'gpt4'])
            arbiter: Arbiter model for validation (default: first worker)
            consensus_strategy: Strategy for multi-AI consensus
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
            top_k: Number of results for RAG retrieval
            verbose: Enable verbose logging
        """
        self.collection_name = collection
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.verbose = verbose

        # Setup logging
        if verbose:
            logging.basicConfig(level=logging.INFO)

        # Initialize components
        # Note: detector, extractor are placeholders (not yet implemented)
        # self.detector = FormatDetector()

        from knowledge_forge.store.embeddings import EmbeddingGenerator
        from knowledge_forge.store.factory import VectorStoreFactory

        self.embedding_generator = EmbeddingGenerator(model_name=embedding_model)

        # Create vector store backend
        self.store = VectorStoreFactory.create(
            backend='chromadb',  # Default backend
            collection=collection,
            persist_directory=persist_directory
        )

        # Store embedding generator for later use
        self.store.embedding_generator = self.embedding_generator

        # Initialize extractor (if workers provided)
        if workers:
            # Note: ArbiterWorkerExtractor not yet implemented
            # Will use consensus-ai library when ready
            # self.extractor = ArbiterWorkerExtractor(...)
            self.extractor = None
            logger.info("Workers specified but extractor not yet implemented")
        else:
            self.extractor = None
            if verbose:
                logger.info("No workers specified - will store raw chunks without extraction")

    def learn_from_file(
        self,
        path: Union[str, Path],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Learn from a file (auto-detects format)

        Args:
            path: Path to file
            **kwargs: Additional options (strategy, workers, etc.)

        Returns:
            Dict with learning results
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        logger.info(f"Learning from file: {path}")

        # Detect format
        file_format = self.detector.detect_file(path)
        logger.info(f"Detected format: {file_format}")

        # Extract text
        parser = self.detector.get_parser(file_format)
        text = parser.parse_file(path)

        # Learn from text
        return self.learn_from_text(text, source=str(path), **kwargs)

    def learn_from_url(
        self,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Learn from a URL (web page)

        Args:
            url: URL to learn from
            **kwargs: Additional options

        Returns:
            Dict with learning results
        """
        logger.info(f"Learning from URL: {url}")

        # Import web parser
        from knowledge_forge.ingest.web import WebParser

        parser = WebParser()
        text = parser.parse_url(url)

        return self.learn_from_text(text, source=url, **kwargs)

    def learn_from_directory(
        self,
        path: Union[str, Path],
        patterns: Optional[List[str]] = None,
        recursive: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Learn from all files in a directory

        Args:
            path: Directory path
            patterns: File patterns to match (e.g., ['*.py', '*.md'])
            recursive: Search subdirectories
            **kwargs: Additional options

        Returns:
            Dict with learning results
        """
        path = Path(path)

        if not path.is_dir():
            raise NotADirectoryError(f"Not a directory: {path}")

        logger.info(f"Learning from directory: {path}")

        # Find files
        files = []
        if patterns:
            for pattern in patterns:
                if recursive:
                    files.extend(path.rglob(pattern))
                else:
                    files.extend(path.glob(pattern))
        else:
            if recursive:
                files = list(path.rglob('*'))
            else:
                files = list(path.glob('*'))

        # Filter out directories
        files = [f for f in files if f.is_file()]

        logger.info(f"Found {len(files)} files to process")

        # Learn from each file
        results = []
        for file_path in files:
            try:
                result = self.learn_from_file(file_path, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")

        return {
            'total_files': len(files),
            'processed': len(results),
            'results': results
        }

    def learn_from_text(
        self,
        text: str,
        source: str = "unknown",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Learn from raw text

        Args:
            text: Text content
            source: Source identifier
            **kwargs: Additional options

        Returns:
            Dict with learning results
        """
        logger.info(f"Learning from text (source: {source})")

        # Chunk text
        chunks = self._chunk_text(text)
        logger.info(f"Created {len(chunks)} chunks")

        # Extract facts (if extractor available)
        if self.extractor:
            facts = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Extracting facts from chunk {i+1}/{len(chunks)}")
                chunk_facts = self.extractor.extract(chunk, **kwargs)
                facts.extend(chunk_facts)
        else:
            # No extraction - just store chunks as-is
            facts = [{'text': chunk, 'type': 'raw'} for chunk in chunks]

        logger.info(f"Extracted {len(facts)} facts")

        # Generate embeddings for chunks (if not already embedded)
        if facts and not facts[0].get('embedding'):
            if self.verbose:
                logger.info(f"Generating embeddings for {len(facts)} facts")
            texts = [f.get('text', f.get('content', '')) for f in facts]
            embeddings = self.embedding_generator.encode(texts, show_progress=self.verbose)

            # Add embeddings to facts
            for i, fact in enumerate(facts):
                fact['embedding'] = embeddings[i]

        # Convert dict facts to Fact objects if needed
        from knowledge_forge.store.base import ContentChunk
        chunk_objects = []
        for i, fact in enumerate(facts):
            chunk_objects.append(ContentChunk(
                chunk_id=f"{source}:chunk_{i}",
                content=fact.get('text', fact.get('content', '')),
                source=source,
                start_line=0,
                end_line=0,
                content_type=fact.get('type', 'raw'),
                metadata=fact,
                embedding=fact.get('embedding', [])
            ))

        # Store in vector DB
        stored = self.store.add_chunks(chunk_objects)

        return {
            'source': source,
            'chunks': len(chunks),
            'facts': len(facts),
            'stored': stored
        }

    def query(
        self,
        question: str,
        top_k: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Query the knowledge base with semantic search

        Args:
            question: Question to answer
            top_k: Number of results to retrieve
            **kwargs: Additional options

        Returns:
            Dict with answer and sources
        """
        top_k = top_k or self.top_k

        if self.verbose:
            logger.info(f"Querying: {question}")

        # Generate embedding for query
        query_embedding = self.embedding_generator.encode(question)

        # Retrieve relevant chunks
        chunks = self.store.search_chunks(query_embedding, top_k=top_k)

        # Generate answer (if extractor available)
        if self.extractor:
            answer = self.extractor.synthesize(question, chunks, **kwargs)
        else:
            # No extractor - just concatenate chunks
            answer = "\n\n".join([c.content for c in chunks])

        return {
            'question': question,
            'answer': answer,
            'chunks': chunks,
            'confidence': self._calculate_confidence(chunks)
        }

    def search(
        self,
        query: str,
        top_k: Optional[int] = None,
        search_type: str = 'chunks',  # 'chunks' or 'facts'
        **kwargs
    ) -> List:
        """
        Semantic search (without answer synthesis)

        Args:
            query: Search query
            top_k: Number of results
            search_type: Search 'chunks' (full context) or 'facts' (validated)
            **kwargs: Additional options

        Returns:
            List of matching chunks or facts
        """
        top_k = top_k or self.top_k

        # Generate embedding for query
        query_embedding = self.embedding_generator.encode(query)

        if search_type == 'facts':
            return self.store.search_facts(query_embedding, top_k=top_k)
        else:
            return self.store.search_chunks(query_embedding, top_k=top_k)

    def list_collections(self) -> List[str]:
        """List all collections"""
        return self.store.list_collections()

    def clear_collection(self, name: str):
        """Clear a collection"""
        return self.store.clear_collection(name)

    def export_knowledge(self, path: Union[str, Path]):
        """Export knowledge base to file"""
        return self.store.export(path)

    def import_knowledge(self, path: Union[str, Path]):
        """Import knowledge base from file"""
        return self.store.import_from(path)

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        # Simple chunking for now - can be enhanced later
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending
                for marker in ['. ', '.\n', '! ', '?\n']:
                    pos = text.rfind(marker, start, end)
                    if pos != -1:
                        end = pos + 1
                        break

            chunks.append(text[start:end].strip())
            start = end - self.chunk_overlap

        return chunks

    def _calculate_confidence(self, results: List) -> float:
        """Calculate confidence score from results"""
        if not results:
            return 0.0

        # For now, return a simple score
        # TODO: Calculate actual similarity scores
        return 0.85
