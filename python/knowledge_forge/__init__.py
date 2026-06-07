"""
Knowledge Forge - Universal knowledge ingestion library for AI systems

Learn from ANY documentation format with multi-AI consensus validation.
"""

__version__ = "0.1.0"
__author__ = "FlossWare (sfloess)"
__license__ = "GPL-3.0"

from knowledge_forge.core import KnowledgeForge
from knowledge_forge.extract.schemas import FactSchema, ValidationSchema, DecisionSchema
from knowledge_forge.extract.consensus import (
    rotating_arbiter,
    single_arbiter,
    majority_vote,
    pairwise_comparison,
    weighted_voting,
    auto_select_strategy,
)

__all__ = [
    "KnowledgeForge",
    "FactSchema",
    "ValidationSchema",
    "DecisionSchema",
    "rotating_arbiter",
    "single_arbiter",
    "majority_vote",
    "pairwise_comparison",
    "weighted_voting",
    "auto_select_strategy",
]
