/**
 * Knowledge Forge - Universal knowledge ingestion library for AI systems
 *
 * Learn from ANY documentation format with multi-AI consensus validation.
 */

export { KnowledgeForge } from './core'
export { FormatDetector } from './ingest/detector'
export { ArbiterWorkerExtractor } from './extract/arbiter'
export { ChromaDBStore } from './store/chromadb'
export { EmbeddingGenerator } from './store/embeddings'

export {
  rotatingArbiter,
  singleArbiter,
  majorityVote,
  pairwiseComparison,
  weightedVoting,
  autoSelectStrategy,
} from './extract/consensus'

export type {
  KnowledgeForgeConfig,
  LearningResult,
  QueryResult,
  SearchResult,
} from './types'
