# GitHub Issue for knowledge-ai

**Repository:** https://github.com/FlossWare/knowledge-ai  
**Title:** feat: Add optional multi-AI consensus for model quality testing and training data assessment

---

## Issue Body

### Summary

Multi-AI arbiter/worker pattern analysis (using 12 AI workers + 4 arbiters) recommends adding **OPTIONAL** multi-AI consensus to knowledge-ai for 2 specific high-value operations.

**Consensus:** Unanimous (3/3 models: Opus, Sonnet, Haiku)  
**Priority:** Medium  
**Confidence:** 87%

---

### Analysis Findings

#### Why Optional, Not Default?

- System is currently **rule-based**, not AI-based
- Pattern extraction uses regex/keywords, not LLM calls
- Multi-AI would require fundamental architecture redesign for hot path
- Runs continuously (every 24h) - multi-AI = 3-4x recurring cost
- Current rule-based approach is fast, predictable, free, and offline-capable

#### Where Multi-AI Adds Value

✅ **Infrequent, high-value operations** - Perfect for multi-AI  
❌ **Continuous hot path** - Keep rule-based for cost/performance

---

### Recommended Implementations

#### 1. Model Quality Testing (HIGHEST PRIORITY)

**Current State:**
```python
# continuous_tuning.py:422
def _test_model_quality(self):
    return 0.1  # PLACEHOLDER - currently useless
```

**Multi-AI Implementation:**
```python
def _test_model_quality(self, use_consensus=False):
    """Evaluate tuned vs base model quality.
    
    Args:
        use_consensus: If True, use multi-model evaluation (4 workers + arbiter)
                      If False, use simple evaluation or placeholder
    
    Returns:
        float: Quality score 0.0-1.0
    """
    if not use_consensus:
        return self._simple_quality_test()  # Fast, single-model
    
    # Multi-model consensus evaluation
    from consensus_ai import ConsensusOrchestrator
    
    orch = ConsensusOrchestrator(
        workers=['claude-opus-4-7', 'claude-sonnet-4-6', 'gpt-4o', 'gemini-1.5-pro'],
        arbiter='claude-opus-4-7',
        graceful_fallback=True,
        min_workers=2
    )
    
    # Test same inputs on tuned vs base model
    test_inputs = self._get_test_inputs()
    
    result = orch.review(
        content=f"Tuned model outputs: {tuned_outputs}\nBase model outputs: {base_outputs}",
        prompt="Evaluate if tuned model outputs are higher quality than base model. Return quality score 0.0-1.0."
    )
    
    return result.quality_score
```

**Why This Matters:**
- Currently returns hardcoded 0.1 (meaningless)
- Runs **monthly** (very low frequency)
- **Perfect candidate** for multi-AI evaluation
- High value, low cost

---

#### 2. Training Data Quality Assessment (MEDIUM PRIORITY)

**Current State:**
```python
# quality_filter.py:309
def apply_all_filters(self, examples):
    # Uses only numeric thresholds
    # Misses semantically poor examples that pass numeric filters
```

**Multi-AI Implementation:**
```python
def apply_all_filters(self, examples, use_consensus=False):
    """Filter training examples by quality.
    
    Args:
        examples: Training examples to filter
        use_consensus: If True, use multi-AI for borderline cases
    
    Returns:
        Filtered examples
    """
    # First pass: numeric thresholds (fast, deterministic)
    high_quality = [e for e in examples if e.quality_score >= 0.85]
    low_quality = [e for e in examples if e.quality_score < 0.70]
    borderline = [e for e in examples if 0.70 <= e.quality_score < 0.85]
    
    if not use_consensus or not borderline:
        # No consensus or no borderline cases
        return high_quality
    
    # Second pass: multi-AI for borderline cases only
    from consensus_ai import ConsensusOrchestrator
    
    orch = ConsensusOrchestrator(
        workers=['claude-opus-4-7', 'claude-sonnet-4-6', 'gpt-4o', 'gemini-1.5-pro'],
        arbiter='claude-opus-4-7',
        graceful_fallback=True,
        min_workers=2
    )
    
    # Evaluate semantic quality of borderline examples
    validated = []
    for example in borderline:
        result = orch.review(
            content=example.content,
            prompt="Evaluate semantic quality of this InstructLab training example. Is it clear, correct, and useful?"
        )
        
        if result.is_high_quality:
            validated.append(example)
    
    return high_quality + validated
```

**Why This Matters:**
- Catches semantically poor examples that pass numeric filters
- **Batch operation** (bounded cost)
- Only evaluates borderline cases (0.70-0.85 confidence)
- Prevents bad examples from entering fine-tuning pipeline

---

### Configuration

Add to `KnowledgeConfig`:

```python
@dataclass
class KnowledgeConfig:
    # ... existing fields ...
    
    # Multi-AI consensus settings
    consensus_enabled: bool = False  # Default: OFF (fast, free, offline)
    consensus_min_workers: int = 2   # Require at least 2 workers
    consensus_workers: List[str] = field(default_factory=lambda: [
        'claude-opus-4-7',
        'claude-sonnet-4-6', 
        'gpt-4o',
        'gemini-1.5-pro'
    ])
    consensus_arbiter: str = 'claude-opus-4-7'
```

**Environment Variable:**
```bash
# Enable multi-AI consensus
export KNOWLEDGE_AI_CONSENSUS_ENABLED=true
```

---

### What NOT to Change

❌ **DO NOT add multi-AI to:**
- Pattern extraction (continuous hot path)
- Anti-pattern detection (high frequency)
- Learning engine background thread
- RAG enhancement
- Vector search/embeddings

**Keep these operations:**
- Rule-based (regex/keywords)
- Fast (milliseconds)
- Free (no API costs)
- Offline-capable (no cloud dependencies)
- Deterministic (debuggable)

---

### Expected Impact

**Quality Improvement:**
- Model quality testing: **0% → functional** (currently placeholder)
- Training data assessment: **+15-25%** accuracy on borderline examples
- Overall downstream impact: **+5-10%** in role execution quality (attenuated through RAG chain)

**Cost Impact:**
- Model quality testing: **Low** (monthly operation, ~$0.10-0.50/month)
- Training data assessment: **Medium** (batch operation, ~$1-5 per batch)
- Total: **$2-10/month** when enabled (vs $0 when disabled)

**Performance Impact:**
- Hot path: **No change** (multi-AI only for opt-in operations)
- Model quality testing: **+2-5 seconds** when consensus enabled
- Training data assessment: **+0.5-1 second per borderline example**

---

### Implementation Estimate

**Code Changes:**
- ~200-300 lines of code
- 2 integration points (ContinuousTuning, TrainingDataFilter)
- Config additions
- Tests for consensus path

**Dependencies:**
- consensus-ai library (already exists in FlossWare ecosystem)
- graceful_fallback for model failures
- min_workers enforcement

**Backward Compatibility:**
- ✅ Fully backward compatible (default: consensus_enabled=False)
- ✅ No breaking changes
- ✅ Existing behavior unchanged when disabled

---

### Testing

```python
# Test model quality testing with consensus
def test_model_quality_with_consensus():
    config = KnowledgeConfig(consensus_enabled=True)
    tuner = ContinuousTuning(config)
    
    score = tuner._test_model_quality(use_consensus=True)
    assert 0.0 <= score <= 1.0
    assert score != 0.1  # Not the placeholder!

# Test training data filtering with consensus
def test_training_data_consensus():
    config = KnowledgeConfig(consensus_enabled=True)
    filter = TrainingDataFilter(config)
    
    borderline_examples = [...]  # Examples with 0.70-0.85 quality
    filtered = filter.apply_all_filters(borderline_examples, use_consensus=True)
    
    # Should filter out some borderline examples
    assert len(filtered) < len(borderline_examples)
```

---

### References

- **Analysis Source:** autodev-ai multi-AI analysis (GitLab internal)
- **consensus-ai Library:** https://github.com/FlossWare/consensus-ai
- **Multi-AI Pattern:** Arbiter/worker with graceful fallback
- **Related Issues:** None

---

### Next Steps

1. Review and approve this approach
2. Implement multi-AI for `_test_model_quality` first (highest value)
3. Add config options
4. Test with consensus enabled/disabled
5. Implement training data quality assessment
6. Document cost/benefit tradeoffs in README
7. Add examples showing when to enable consensus

---

### Questions

- Should consensus be opt-in per operation, or global config only?
- Should we log multi-AI decisions for debugging?
- Should we track consensus costs in telemetry?
- Should we add a "consensus quality score" to Facts for transparency?
