"""
In-memory document store for demo purposes.
Stores processed documents without requiring a database.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

# In-memory storage for demo documents
_demo_documents: List[Dict[str, Any]] = []


def add_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Add a processed document to the store."""
    doc["created_at"] = datetime.now().isoformat()
    _demo_documents.append(doc)
    return doc


def get_all_documents() -> List[Dict[str, Any]]:
    """Get all stored documents."""
    return list(reversed(_demo_documents))  # Newest first


def get_document_by_id(doc_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific document by ID."""
    for doc in _demo_documents:
        if doc.get("id") == doc_id:
            return doc
    return None


def search_documents(query: str) -> List[Dict[str, Any]]:
    """
    Search documents by text content, filename, or classification.
    Simple case-insensitive substring matching.
    """
    if not query:
        return get_all_documents()

    query_lower = query.lower()
    results = []

    for doc in _demo_documents:
        # Search in extracted text
        text = doc.get("extracted_text", "").lower()
        filename = doc.get("filename", "").lower()
        classification = doc.get("classification", "").lower()

        # Check entities too
        entities_text = " ".join(
            e.get("value", "") for e in doc.get("entities", [])
        ).lower()

        if (query_lower in text or
            query_lower in filename or
            query_lower in classification or
            query_lower in entities_text):
            results.append(doc)

    return list(reversed(results))  # Newest first


def get_stats() -> Dict[str, Any]:
    """Get statistics about stored documents."""
    total = len(_demo_documents)

    # Count by classification
    classifications = {}
    for doc in _demo_documents:
        cls = doc.get("classification", "unknown")
        classifications[cls] = classifications.get(cls, 0) + 1

    return {
        "total_documents": total,
        "classifications": classifications,
        "recent_count": min(total, 5)
    }


def clear_store() -> None:
    """Clear all documents (useful for testing)."""
    _demo_documents.clear()
