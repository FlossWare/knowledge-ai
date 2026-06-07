"""
ChromaDB backend - Default embedded vector database

Best for: Development, embedded use, simple deployments
"""

from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings

from knowledge_forge.store.base import VectorStore, ContentChunk, Fact


class ChromaDBStore(VectorStore):
    """ChromaDB backend for Knowledge Forge"""

    def __init__(self, collection: str, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB store

        Args:
            collection: Collection name
            persist_directory: Where to store data
        """
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_directory
        ))

        # Two collections: chunks and facts
        self.chunks_collection = self.client.get_or_create_collection(
            name=f"{collection}_chunks",
            metadata={"description": "Content chunks"}
        )

        self.facts_collection = self.client.get_or_create_collection(
            name=f"{collection}_facts",
            metadata={"description": "Validated facts"}
        )

        self.collection_name = collection

    def add_chunks(self, chunks: List[ContentChunk]) -> int:
        """Add chunks to ChromaDB"""
        if not chunks:
            return 0

        self.chunks_collection.add(
            ids=[c.chunk_id for c in chunks],
            embeddings=[c.embedding for c in chunks],
            documents=[c.content for c in chunks],
            metadatas=[{
                'source': c.source,
                'start_line': c.start_line,
                'end_line': c.end_line,
                'content_type': c.content_type,
                **c.metadata
            } for c in chunks]
        )

        return len(chunks)

    def add_facts(self, facts: List[Fact]) -> int:
        """Add facts to ChromaDB"""
        if not facts:
            return 0

        self.facts_collection.add(
            ids=[f.fact_id for f in facts],
            embeddings=[f.embedding for f in facts],
            documents=[f.text for f in facts],
            metadatas=[{
                'chunk_id': f.chunk_id,
                'confidence': f.confidence,
                'fact_type': f.fact_type,
                'proposed_by': ','.join(f.proposed_by),
                **f.metadata
            } for f in facts]
        )

        return len(facts)

    def search_chunks(self, query_embedding: List[float], top_k: int = 5, filter_dict: Dict = None) -> List[ContentChunk]:
        """Search chunks by vector similarity"""
        results = self.chunks_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict
        )

        chunks = []
        if results['ids'] and results['ids'][0]:
            for i, chunk_id in enumerate(results['ids'][0]):
                meta = results['metadatas'][0][i]
                chunks.append(ContentChunk(
                    chunk_id=chunk_id,
                    content=results['documents'][0][i],
                    source=meta.get('source', ''),
                    start_line=meta.get('start_line', 0),
                    end_line=meta.get('end_line', 0),
                    content_type=meta.get('content_type', 'text'),
                    metadata=meta,
                    embedding=results.get('embeddings', [[]])[0][i] if results.get('embeddings') else []
                ))

        return chunks

    def search_facts(self, query_embedding: List[float], top_k: int = 5, filter_dict: Dict = None) -> List[Fact]:
        """Search facts by vector similarity"""
        results = self.facts_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_dict
        )

        facts = []
        if results['ids'] and results['ids'][0]:
            for i, fact_id in enumerate(results['ids'][0]):
                meta = results['metadatas'][0][i]
                proposed_by = meta.get('proposed_by', '').split(',') if meta.get('proposed_by') else []
                facts.append(Fact(
                    fact_id=fact_id,
                    text=results['documents'][0][i],
                    chunk_id=meta.get('chunk_id', ''),
                    confidence=meta.get('confidence', 0.0),
                    fact_type=meta.get('fact_type', 'general'),
                    metadata=meta,
                    embedding=results.get('embeddings', [[]])[0][i] if results.get('embeddings') else [],
                    proposed_by=proposed_by
                ))

        return facts

    def get_chunk(self, chunk_id: str) -> Optional[ContentChunk]:
        """Get specific chunk by ID"""
        try:
            result = self.chunks_collection.get(ids=[chunk_id])
            if result['ids']:
                meta = result['metadatas'][0]
                return ContentChunk(
                    chunk_id=chunk_id,
                    content=result['documents'][0],
                    source=meta.get('source', ''),
                    start_line=meta.get('start_line', 0),
                    end_line=meta.get('end_line', 0),
                    content_type=meta.get('content_type', 'text'),
                    metadata=meta,
                    embedding=result.get('embeddings', [[]])[0] if result.get('embeddings') else []
                )
        except:
            return None

    def get_fact(self, fact_id: str) -> Optional[Fact]:
        """Get specific fact by ID"""
        try:
            result = self.facts_collection.get(ids=[fact_id])
            if result['ids']:
                meta = result['metadatas'][0]
                proposed_by = meta.get('proposed_by', '').split(',') if meta.get('proposed_by') else []
                return Fact(
                    fact_id=fact_id,
                    text=result['documents'][0],
                    chunk_id=meta.get('chunk_id', ''),
                    confidence=meta.get('confidence', 0.0),
                    fact_type=meta.get('fact_type', 'general'),
                    metadata=meta,
                    embedding=result.get('embeddings', [[]])[0] if result.get('embeddings') else [],
                    proposed_by=proposed_by
                )
        except:
            return None

    def list_collections(self) -> List[str]:
        """List all collections"""
        collections = self.client.list_collections()
        # Return unique base names (without _chunks/_facts suffix)
        names = set()
        for col in collections:
            name = col.name
            if name.endswith('_chunks') or name.endswith('_facts'):
                names.add(name.rsplit('_', 1)[0])
            else:
                names.add(name)
        return list(names)

    def clear_collection(self, name: str):
        """Clear a collection"""
        try:
            self.client.delete_collection(f"{name}_chunks")
        except:
            pass
        try:
            self.client.delete_collection(f"{name}_facts")
        except:
            pass

    def get_all_chunks(self) -> List[ContentChunk]:
        """Get all chunks (for export)"""
        result = self.chunks_collection.get()
        chunks = []
        if result['ids']:
            for i, chunk_id in enumerate(result['ids']):
                meta = result['metadatas'][i]
                chunks.append(ContentChunk(
                    chunk_id=chunk_id,
                    content=result['documents'][i],
                    source=meta.get('source', ''),
                    start_line=meta.get('start_line', 0),
                    end_line=meta.get('end_line', 0),
                    content_type=meta.get('content_type', 'text'),
                    metadata=meta,
                    embedding=result.get('embeddings', [])[i] if result.get('embeddings') else []
                ))
        return chunks

    def get_all_facts(self) -> List[Fact]:
        """Get all facts (for export)"""
        result = self.facts_collection.get()
        facts = []
        if result['ids']:
            for i, fact_id in enumerate(result['ids']):
                meta = result['metadatas'][i]
                proposed_by = meta.get('proposed_by', '').split(',') if meta.get('proposed_by') else []
                facts.append(Fact(
                    fact_id=fact_id,
                    text=result['documents'][i],
                    chunk_id=meta.get('chunk_id', ''),
                    confidence=meta.get('confidence', 0.0),
                    fact_type=meta.get('fact_type', 'general'),
                    metadata=meta,
                    embedding=result.get('embeddings', [])[i] if result.get('embeddings') else [],
                    proposed_by=proposed_by
                ))
        return facts
