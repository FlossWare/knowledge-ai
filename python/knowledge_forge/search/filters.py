"""
Advanced Filtering - MongoDB-style query operators

Supports:
- Comparison: $eq, $ne, $gt, $gte, $lt, $lte
- Logical: $and, $or, $not
- Array: $in, $nin
- String: $regex, $glob
- Existence: $exists
"""

from typing import Dict, Any, List
import re
from fnmatch import fnmatch
from datetime import datetime


class AdvancedFilter:
    """
    Advanced filtering with MongoDB-style operators

    Examples:
        # Comparison
        {'confidence': {'$gte': 0.8}}
        {'start_line': {'$lt': 100}}

        # String matching
        {'source': {'$regex': r'.*\.pdf$'}}
        {'source': {'$glob': 'docs/*.md'}}

        # Logical operators
        {'$and': [
            {'confidence': {'$gte': 0.8}},
            {'content_type': 'documentation'}
        ]}

        # Array operators
        {'content_type': {'$in': ['code', 'documentation']}}

        # Date ranges
        {'date': {'$gte': '2024-01-01', '$lt': '2024-12-31'}}
    """

    @staticmethod
    def matches(document: Any, filter_dict: Dict) -> bool:
        """
        Check if document matches filter

        Args:
            document: Document to check (ContentChunk or Fact)
            filter_dict: Filter specification

        Returns:
            True if document matches filter
        """
        if not filter_dict:
            return True

        # Handle logical operators
        if '$and' in filter_dict:
            return all(
                AdvancedFilter.matches(document, sub_filter)
                for sub_filter in filter_dict['$and']
            )

        if '$or' in filter_dict:
            return any(
                AdvancedFilter.matches(document, sub_filter)
                for sub_filter in filter_dict['$or']
            )

        if '$not' in filter_dict:
            return not AdvancedFilter.matches(document, filter_dict['$not'])

        # Handle field filters
        for field, condition in filter_dict.items():
            if field.startswith('$'):
                continue  # Skip operators at root level

            # Get field value from document
            if hasattr(document, field):
                value = getattr(document, field)
            elif hasattr(document, 'metadata') and field in document.metadata:
                value = document.metadata[field]
            else:
                # Field doesn't exist
                if isinstance(condition, dict) and '$exists' in condition:
                    if not condition['$exists']:
                        continue  # Field should not exist - OK
                return False  # Field missing

            # Check condition
            if not AdvancedFilter._check_condition(value, condition):
                return False

        return True

    @staticmethod
    def _check_condition(value: Any, condition: Any) -> bool:
        """Check if value satisfies condition"""

        # Simple equality
        if not isinstance(condition, dict):
            return value == condition

        # Operator-based conditions
        for operator, operand in condition.items():
            if operator == '$eq':
                if value != operand:
                    return False

            elif operator == '$ne':
                if value == operand:
                    return False

            elif operator == '$gt':
                if not (value > operand):
                    return False

            elif operator == '$gte':
                if not (value >= operand):
                    return False

            elif operator == '$lt':
                if not (value < operand):
                    return False

            elif operator == '$lte':
                if not (value <= operand):
                    return False

            elif operator == '$in':
                if value not in operand:
                    return False

            elif operator == '$nin':
                if value in operand:
                    return False

            elif operator == '$regex':
                if not isinstance(value, str):
                    return False
                pattern = re.compile(operand)
                if not pattern.search(value):
                    return False

            elif operator == '$glob':
                if not isinstance(value, str):
                    return False
                if not fnmatch(value, operand):
                    return False

            elif operator == '$exists':
                # Handled earlier
                pass

            else:
                raise ValueError(f"Unknown operator: {operator}")

        return True

    @staticmethod
    def filter_results(documents: List, filter_dict: Dict) -> List:
        """
        Filter list of documents

        Args:
            documents: List of documents
            filter_dict: Filter specification

        Returns:
            Filtered list
        """
        if not filter_dict:
            return documents

        return [
            doc for doc in documents
            if AdvancedFilter.matches(doc, filter_dict)
        ]


# Convenience function
def apply_filter(documents: List, filter_dict: Dict) -> List:
    """
    Apply advanced filter to documents

    Args:
        documents: List of documents
        filter_dict: MongoDB-style filter

    Returns:
        Filtered documents

    Example:
        >>> filtered = apply_filter(results, {
        ...     '$and': [
        ...         {'confidence': {'$gte': 0.8}},
        ...         {'source': {'$glob': '*.pdf'}}
        ...     ]
        ... })
    """
    return AdvancedFilter.filter_results(documents, filter_dict)
