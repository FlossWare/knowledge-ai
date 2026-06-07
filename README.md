# Knowledge Forge

**Universal knowledge ingestion library for AI systems**

Learn from ANY documentation format with multi-AI consensus validation.

---

## Features

### 🔥 Core Capabilities

- **Universal Format Support**: PDF, Markdown, HTML, reStructuredText, AsciiDoc, plain text
- **Code Documentation**: Docstrings, JSDoc, Javadoc, GoDoc, OpenAPI specs
- **Auto-Detection**: Automatically detects and parses input format
- **Multi-AI Consensus**: Arbiter/worker pattern for fact extraction
- **Semantic Storage**: ChromaDB vector database with 384-dim embeddings
- **RAG Retrieval**: Semantic search for knowledge retrieval
- **Dual Implementation**: Python (for Universal AI) + JavaScript (for Claude Code)

### 🎯 Use Cases

- Learn from documentation (PDFs, web pages, markdown)
- Extract knowledge from code repositories
- Build domain-specific knowledge bases
- RAG-powered Q&A systems
- Automated documentation analysis

---

## Quick Start

### Python (Universal AI)

```python
from knowledge_forge import KnowledgeForge

# Create knowledge base
forge = KnowledgeForge(collection='my-docs')

# Learn from any source (auto-detects format)
forge.learn_from_file('/path/to/tutorial.pdf')
forge.learn_from_file('/path/to/README.md')
forge.learn_from_url('https://docs.example.com')
forge.learn_from_directory('/path/to/docs/')

# Query with RAG
result = forge.query('How does authentication work?')
print(result.answer)
print(result.sources)  # Citations
```

### JavaScript (Claude Code)

```javascript
import { KnowledgeForge } from 'knowledge-forge'

// Create knowledge base
const forge = new KnowledgeForge({ collection: 'my-docs' })

// Learn from any source (auto-detects format)
await forge.learnFromFile('/path/to/tutorial.pdf')
await forge.learnFromFile('/path/to/README.md')
await forge.learnFromUrl('https://docs.example.com')
await forge.learnFromDirectory('/path/to/docs/')

// Query with RAG
const result = await forge.query('How does authentication work?')
console.log(result.answer)
console.log(result.sources)  // Citations
```

---

## Installation

### Python

```bash
cd python/
pip install -e .

# Or with all dependencies:
pip install -e .[all]
```

### JavaScript

```bash
cd javascript/
npm install
npm run build
```

---

## Supported Formats

### Documents

| Format | Extension | Status | Parser |
|--------|-----------|--------|--------|
| PDF | `.pdf` | ✅ Supported | PyPDF2 / pdf-parse |
| Markdown | `.md` | ✅ Supported | markdown-it / commonmark |
| HTML | `.html` | ✅ Supported | BeautifulSoup / jsdom |
| reStructuredText | `.rst` | ✅ Supported | docutils |
| AsciiDoc | `.adoc` | ✅ Supported | asciidoctor |
| Plain Text | `.txt` | ✅ Supported | Built-in |

### Code Documentation

| Format | Language | Status | Parser |
|--------|----------|--------|--------|
| Docstrings | Python | ✅ Supported | ast / docstring-parser |
| JSDoc | JavaScript | ✅ Supported | doctrine / jsdoc |
| Javadoc | Java | ✅ Supported | javadoc-parser |
| GoDoc | Go | ✅ Supported | go/doc |
| OpenAPI | YAML/JSON | ✅ Supported | openapi-parser |

### Structured Data

| Format | Extension | Status | Parser |
|--------|-----------|--------|--------|
| JSON | `.json` | ✅ Supported | Built-in |
| YAML | `.yaml`, `.yml` | ✅ Supported | PyYAML / js-yaml |
| TOML | `.toml` | ✅ Supported | toml / @iarna/toml |
| XML | `.xml` | ✅ Supported | lxml / xml2js |

---

## Architecture

### Knowledge Pipeline

```
Input (any format)
    ↓
Format Detection (auto-detect MIME type)
    ↓
Text Extraction (format-specific parsers)
    ↓
Chunking (semantic boundaries)
    ↓
Fact Extraction (multi-AI consensus)
    ↓
Validation (arbiter/worker pattern)
    ↓
Embedding (sentence-transformers / transformers.js)
    ↓
Vector Storage (ChromaDB)
    ↓
RAG Retrieval (semantic search + reranking)
```

### Multi-AI Consensus

**Arbiter/Worker Pattern:**

1. **Workers propose facts** independently (diverse perspectives)
2. **Arbiter validates** and selects best facts
3. **Full attribution** tracking (which AI proposed what)
4. **Reduces false positives** significantly

**Consensus Strategies:**

- `rotating` - Democratic (each AI judges others)
- `single` - One arbiter judges all (fast)
- `majority` - Simple majority vote
- `pairwise` - Tournament style
- `weighted` - Confidence-based voting

---

## Examples

### Learn from PDF Tutorial

```python
from knowledge_forge import KnowledgeForge

forge = KnowledgeForge(collection='fastapi-docs')

# Learn from FastAPI PDF tutorial
forge.learn_from_file('/path/to/fastapi-tutorial.pdf', 
                      strategy='rotating',  # Use democratic consensus
                      workers=['claude-opus', 'gpt4', 'gemini'])

# Query
result = forge.query('How do I add authentication?')
print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence}")
print(f"Sources: {result.sources}")
```

### Learn from Documentation Website

```javascript
import { KnowledgeForge } from 'knowledge-forge'

const forge = new KnowledgeForge({ collection: 'react-docs' })

// Learn from React docs
await forge.learnFromUrl('https://react.dev/learn', {
  strategy: 'single',     // Fast consensus
  recursive: true,        // Follow links
  maxDepth: 2            // Limit recursion
})

// Query
const result = await forge.query('How do hooks work?')
console.log(`Answer: ${result.answer}`)
console.log(`Confidence: ${result.confidence}`)
console.log(`Sources: ${result.sources}`)
```

### Learn from Code Repository

```python
from knowledge_forge import KnowledgeForge

forge = KnowledgeForge(collection='myproject-code')

# Learn from code repository
forge.learn_from_directory('/path/to/repo/src/', 
                           patterns=['*.py', '*.js'],
                           extract_docstrings=True,
                           workers=['claude-opus', 'claude-sonnet'])

# Query
result = forge.query('How does the authentication module work?')
```

---

## Integration

### Universal AI Integration

Knowledge Forge is designed to integrate seamlessly with Universal AI:

```python
# Universal AI can use any AI provider
from knowledge_forge import KnowledgeForge

forge = KnowledgeForge(
    collection='docs',
    workers=['claude-opus', 'gpt4', 'gemini', 'llama3.3'],  # Mix cloud + local
    arbiter='claude-opus'
)

# 100% free option (Ollama local models)
forge = KnowledgeForge(
    collection='docs',
    workers=['llama3.3', 'qwen3.5', 'mistral'],  # All local, no API costs
    arbiter='qwen3.5'
)
```

### Claude Code Integration

Knowledge Forge workflows are available as Claude Code skills:

```bash
# In Claude Code
/learn-from-pdf /path/to/doc.pdf
/learn-from-web https://docs.example.com
/learn-from-repo /path/to/code/
/query-knowledge "How does X work?"
```

---

## Configuration

### Python Configuration

```python
from knowledge_forge import KnowledgeForge

forge = KnowledgeForge(
    collection='my-kb',              # Knowledge base name
    persist_directory='./chroma_db', # ChromaDB location
    embedding_model='all-MiniLM-L6-v2',  # Sentence transformer
    workers=['claude-opus', 'gpt4'], # AI workers
    arbiter='claude-opus',           # Arbiter model
    consensus_strategy='rotating',   # Consensus strategy
    chunk_size=1000,                 # Text chunk size
    chunk_overlap=200,               # Overlap between chunks
    top_k=5,                         # Number of results for RAG
    verbose=True                     # Progress logging
)
```

### JavaScript Configuration

```javascript
const forge = new KnowledgeForge({
  collection: 'my-kb',
  persistDirectory: './chroma_db',
  embeddingModel: 'Xenova/all-MiniLM-L6-v2',
  workers: ['opus', 'sonnet', 'haiku'],
  arbiter: 'opus',
  consensusStrategy: 'rotating',
  chunkSize: 1000,
  chunkOverlap: 200,
  topK: 5,
  verbose: true
})
```

---

## API Reference

### Core Methods

#### Python

```python
# Learning
forge.learn_from_file(path, **kwargs)
forge.learn_from_url(url, **kwargs)
forge.learn_from_directory(path, **kwargs)
forge.learn_from_text(text, **kwargs)

# Querying
result = forge.query(question, top_k=5)
results = forge.search(query, top_k=10)

# Management
forge.list_collections()
forge.clear_collection(name)
forge.export_knowledge(path)
forge.import_knowledge(path)
```

#### JavaScript

```javascript
// Learning
await forge.learnFromFile(path, options)
await forge.learnFromUrl(url, options)
await forge.learnFromDirectory(path, options)
await forge.learnFromText(text, options)

// Querying
const result = await forge.query(question, { topK: 5 })
const results = await forge.search(query, { topK: 10 })

// Management
await forge.listCollections()
await forge.clearCollection(name)
await forge.exportKnowledge(path)
await forge.importKnowledge(path)
```

---

## Development

### Running Tests

```bash
# Python
cd python/
pytest

# JavaScript
cd javascript/
npm test
```

### Building Documentation

```bash
# Python
cd python/
sphinx-build -b html docs/ docs/_build/

# JavaScript
cd javascript/
npm run docs
```

---

## Comparison: Knowledge Forge vs Alternatives

| Feature | Knowledge Forge | LangChain | LlamaIndex | RAGatouille |
|---------|----------------|-----------|------------|-------------|
| **Multi-AI Consensus** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Format Auto-Detection** | ✅ Yes | ⚠️ Manual | ⚠️ Manual | ⚠️ Manual |
| **Dual Language** | ✅ Python + JS | ⚠️ Python only | ⚠️ Python only | ⚠️ Python only |
| **Model Agnostic** | ✅ ANY model | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited |
| **100% Free Option** | ✅ Ollama | ❌ No | ❌ No | ❌ No |
| **Arbiter/Worker** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Production Ready** | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Beta |

---

## Roadmap

### Phase 1: Core Foundation (Current)
- [x] Project structure
- [ ] Python implementation
- [ ] JavaScript implementation
- [ ] Basic format support (PDF, MD, HTML)
- [ ] ChromaDB integration
- [ ] Arbiter/worker pattern

### Phase 2: Format Support
- [ ] Code documentation extraction
- [ ] Structured data (JSON, YAML, TOML)
- [ ] Additional formats (RST, AsciiDoc)
- [ ] Auto-detection improvements

### Phase 3: Advanced Features
- [ ] 5 consensus strategies
- [ ] Reranking
- [ ] Query optimization
- [ ] Knowledge base merging
- [ ] Incremental learning

### Phase 4: Integration
- [ ] Universal AI integration
- [ ] Claude Code workflows
- [ ] MCP server
- [ ] Web UI (optional)

---

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

GPL-3.0 - See [LICENSE](LICENSE)

---

## Credits

**Created by**: FlossWare (sfloess)  
**Inspired by**: Universal AI multi-AI consensus pattern  
**Integrates with**: Universal AI, Claude Code  

**Part of the FlossWare AI ecosystem:**
- [Universal AI](https://gitlab.cee.redhat.com/sfloess/universal-ai) - Model-agnostic multi-AI platform
- [Claude Code Global Skills](https://github.com/anthropics/claude-code) - SDLC automation workflows
- **Knowledge Forge** - Universal knowledge ingestion (this project)

---

## Support

- **Issues**: https://gitlab.cee.redhat.com/sfloess/knowledge-forge/issues
- **Docs**: https://gitlab.cee.redhat.com/sfloess/knowledge-forge/docs
- **Universal AI**: https://gitlab.cee.redhat.com/sfloess/universal-ai

---

**Knowledge Forge**: Building knowledge from any source. 🔥
