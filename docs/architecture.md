# Knowledge Forge Architecture

**Multi-layered knowledge ingestion system with AI consensus validation**

---

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Input Layer                           │
│  (PDF, MD, HTML, RST, Code, JSON, YAML, Web, ...)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Format Detection                          │
│  (Auto-detect MIME type, extension, content analysis)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Text Extraction                           │
│  (Format-specific parsers: PDF, HTML, Markdown, etc.)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Text Chunking                           │
│  (Semantic boundaries, configurable overlap)                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Fact Extraction                            │
│  (Multi-AI workers propose facts independently)             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Validation                               │
│  (Arbiter validates facts, resolves conflicts)              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Embedding                                │
│  (Sentence transformers: 384-dim semantic vectors)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Vector Storage                             │
│  (ChromaDB with cosine similarity search)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    RAG Retrieval                             │
│  (Semantic search + reranking + answer synthesis)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Ingestion Layer

**Purpose**: Convert any format to plain text

**Components**:
- `FormatDetector` - Auto-detect input format
- Format-specific parsers:
  - `PDFParser` - Extract text from PDFs
  - `MarkdownParser` - Parse Markdown
  - `HTMLParser` - Extract from web pages
  - `CodeParser` - Extract docstrings
  - `StructuredParser` - Parse JSON/YAML/TOML

**Key Features**:
- MIME type detection
- Extension-based fallback
- Content analysis for ambiguous files
- Configurable parser options

### 2. Extraction Layer

**Purpose**: Extract structured facts with multi-AI consensus

**Components**:
- `ArbiterWorkerExtractor` - Orchestrates multi-AI extraction
- `ConsensusStrategies` - 5 consensus algorithms
- `FactSchemas` - Structured output validation

**Arbiter/Worker Pattern**:

```python
# Workers propose facts independently
workers = [
    {'model': 'claude-opus', 'name': 'opus-worker'},
    {'model': 'gpt4', 'name': 'gpt4-worker'},
    {'model': 'gemini', 'name': 'gemini-worker'}
]

# Each worker extracts facts
proposals = parallel_extract(workers, text, schema)

# Arbiter validates and selects best facts
validated = arbiter_validate(proposals, arbiter='claude-opus')

# Full attribution tracking
facts = [
    {
        'text': 'FastAPI uses async/await',
        'proposed_by': ['opus-worker', 'gpt4-worker'],
        'rejected_by': [],
        'confidence': 0.95
    }
]
```

**Consensus Strategies**:

1. **Rotating** - Democratic (each AI judges others)
   - Most thorough
   - Catches most errors
   - Slowest

2. **Single** - One arbiter judges all
   - Fast
   - Simple
   - Less democratic

3. **Majority** - Simple majority vote
   - Fastest
   - No arbiter overhead
   - Works when solutions are similar

4. **Pairwise** - Tournament style
   - Balanced
   - Good for diverse solutions
   - Medium speed

5. **Weighted** - Confidence-based voting
   - Quality-aware
   - Prioritizes high-confidence
   - Best when confidence varies

### 3. Storage Layer

**Purpose**: Persistent vector storage with semantic search

**Components**:
- `ChromaDBStore` - Vector database interface
- `EmbeddingGenerator` - Semantic embedding creation
- `Retrieval` - RAG retrieval with reranking

**Vector Storage**:

```python
# Generate embeddings (384-dim)
embeddings = sentence_transformer.encode(facts)

# Store in ChromaDB
collection.add(
    ids=[f'fact_{i}' for i in range(len(facts))],
    embeddings=embeddings,
    documents=facts,
    metadatas=[
        {
            'source': 'fastapi-tutorial.pdf',
            'page': 5,
            'proposed_by': ['opus', 'gpt4'],
            'confidence': 0.95
        }
    ]
)
```

**Retrieval**:

```python
# Query with semantic search
query_embedding = sentence_transformer.encode(question)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,
    where={'confidence': {'$gte': 0.8}}  # Filter low-confidence
)

# Rerank by relevance
reranked = reranker.rank(query, results)

# Synthesize answer
answer = arbiter.synthesize(query, reranked)
```

---

## Data Flow

### Learning Flow

```
User: forge.learn_from_file('tutorial.pdf')
    ↓
1. Format Detection
    - Detect: PDF
    - Select parser: PDFParser
    ↓
2. Text Extraction
    - Extract text from PDF
    - Preserve structure (headings, paragraphs)
    ↓
3. Chunking
    - Split into 1000-char chunks
    - 200-char overlap
    - Break at sentence boundaries
    ↓
4. Multi-AI Extraction (per chunk)
    - Opus worker: extract facts
    - Sonnet worker: extract facts
    - Haiku worker: extract facts
    ↓
5. Arbiter Validation
    - Cross-check facts
    - Resolve conflicts
    - Track attribution
    ↓
6. Embedding
    - Generate 384-dim vectors
    - Use sentence-transformers
    ↓
7. Storage
    - Store in ChromaDB
    - Index by embedding
    - Persist to disk
    ↓
Result: {'source': 'tutorial.pdf', 'chunks': 15, 'facts': 42, 'stored': 42}
```

### Query Flow

```
User: forge.query('How does authentication work?')
    ↓
1. Query Embedding
    - Convert question to 384-dim vector
    ↓
2. Semantic Search
    - Find top-k similar facts (cosine similarity)
    - Filter by confidence threshold
    ↓
3. Reranking
    - Score by relevance
    - Diversify sources
    ↓
4. Answer Synthesis
    - Arbiter synthesizes answer from facts
    - Includes citations
    - Calculates confidence
    ↓
Result: {
    'answer': 'FastAPI uses OAuth2 with JWT tokens...',
    'sources': [fact1, fact2, fact3],
    'confidence': 0.92
}
```

---

## Scalability

### Horizontal Scaling

**Multi-worker extraction**:
- N workers can process chunks in parallel
- No barriers - pipeline execution
- Each worker independent

**Distributed storage**:
- ChromaDB can run on separate server
- Embeddings can be cached
- Collections can be sharded

### Performance Optimization

**Caching**:
```python
# Cache embeddings for common queries
@lru_cache(maxsize=1000)
def get_query_embedding(query: str):
    return embedding_model.encode(query)

# Cache parsed documents
@lru_cache(maxsize=100)
def get_parsed_doc(path: str):
    return parser.parse(path)
```

**Batching**:
```python
# Batch embedding generation
embeddings = embedding_model.encode(
    facts,
    batch_size=32,  # Process 32 at once
    show_progress_bar=True
)

# Batch storage
collection.add(
    ids=batch_ids,
    embeddings=batch_embeddings,
    documents=batch_docs
)
```

---

## Error Handling

### Graceful Degradation

**No workers specified**:
- Disable fact extraction
- Store raw chunks
- Still functional for basic RAG

**Worker failure**:
- Continue with remaining workers
- Log failure
- Arbiter uses partial results

**Format detection failure**:
- Fall back to plain text
- User can override detection

### Validation

**Input validation**:
```python
if not path.exists():
    raise FileNotFoundError(f"File not found: {path}")

if not workers:
    logger.warning("No workers - extraction disabled")

if chunk_size < 100:
    raise ValueError("chunk_size too small")
```

**Output validation**:
```python
# Validate extracted facts
for fact in facts:
    if not isinstance(fact, dict):
        logger.error(f"Invalid fact: {fact}")
        continue

    if 'text' not in fact:
        logger.error(f"Missing text in fact: {fact}")
        continue
```

---

## Integration Points

### Universal AI Integration

```python
# Universal AI provides the workers
from universal_ai import get_available_models

workers = get_available_models(
    local=True,   # Include Ollama models
    cloud=True    # Include API models
)

forge = KnowledgeForge(
    collection='docs',
    workers=[w.id for w in workers[:3]],  # Use top 3
    arbiter=workers[0].id                 # Best as arbiter
)
```

### Claude Code Integration

```javascript
// Claude Code workflow
export const meta = {
  name: 'learn-from-docs',
  description: 'Learn from documentation sources',
  phases: [
    { title: 'Ingest', detail: 'Parse and extract text' },
    { title: 'Extract', detail: 'Multi-AI fact extraction' },
    { title: 'Store', detail: 'Store in vector DB' }
  ]
}

import { KnowledgeForge } from 'knowledge-forge'

phase('Ingest')
const forge = new KnowledgeForge({ collection: args.collection })

phase('Extract')
await forge.learnFromFile(args.file, {
  workers: ['opus', 'sonnet', 'haiku'],
  strategy: 'rotating'
})

phase('Store')
log('Knowledge base updated!')
```

---

## Security Considerations

### Input Sanitization

- Validate file paths (no directory traversal)
- Limit file size (prevent DoS)
- Validate URLs (no SSRF)
- Sanitize HTML (prevent XSS)

### Data Privacy

- No data sent to external services (unless using cloud AI)
- ChromaDB data stored locally
- Optional encryption at rest
- Configurable data retention

### Model Safety

- Validate AI responses (structured schemas)
- Track attribution (which AI said what)
- Confidence thresholds (filter low-quality)
- Human-in-the-loop option (review before storing)

---

## Future Enhancements

### Phase 2
- Incremental learning (update existing facts)
- Knowledge base merging
- Cross-collection queries
- Advanced reranking

### Phase 3
- Graph knowledge representation
- Temporal knowledge (time-aware facts)
- Relationship extraction
- Entity recognition

### Phase 4
- Web UI
- REST API
- MCP server
- Cloud deployment

---

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Universal AI](https://gitlab.cee.redhat.com/sfloess/universal-ai)
- [Claude Code Workflows](https://github.com/anthropics/claude-code)
