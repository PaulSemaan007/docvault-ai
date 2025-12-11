"""
Search Service.
Full-text search across documents.
"""

from typing import Optional, List, Tuple
from app.services.document_service import _documents, _entities


class SearchService:
    """
    Service for document search operations.
    """

    async def search(
        self,
        user_id: str,
        query: str,
        classification: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_value: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Tuple[List[dict], int]:
        """
        Search documents with full-text and filters.

        In production, this would use PostgreSQL full-text search.
        """
        query_lower = query.lower()
        results = []

        for doc_id, doc in _documents.items():
            # Only search user's documents
            if doc["user_id"] != user_id:
                continue

            # Apply filters
            if classification and doc.get("classification") != classification:
                continue

            if date_from and doc["created_at"] < date_from:
                continue

            if date_to and doc["created_at"] > date_to:
                continue

            # Calculate relevance score
            score = 0.0
            snippet = ""

            # Search in filename
            if query_lower in doc["filename"].lower():
                score += 2.0
                snippet = doc["filename"]

            # Search in extracted text
            text = doc.get("extracted_text") or ""
            if query_lower in text.lower():
                score += 1.0
                # Extract snippet around the match
                idx = text.lower().find(query_lower)
                start = max(0, idx - 50)
                end = min(len(text), idx + len(query) + 50)
                snippet = "..." + text[start:end] + "..."

            # Search in entities
            doc_entities = _entities.get(doc_id, [])
            for entity in doc_entities:
                if query_lower in entity["value"].lower():
                    score += 1.5

                # Filter by entity type/value
                if entity_type and entity["type"] == entity_type:
                    if entity_value and entity_value.lower() in entity["value"].lower():
                        score += 0.5

            # Add to results if matched
            if score > 0:
                results.append({
                    "id": doc_id,
                    "filename": doc["filename"],
                    "classification": doc.get("classification"),
                    "snippet": snippet or doc["filename"],
                    "score": score,
                    "created_at": doc["created_at"]
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        # Paginate
        total = len(results)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = results[start:end]

        return paginated, total

    async def get_filter_options(self, user_id: str) -> dict:
        """
        Get available filter options for the user's documents.
        """
        user_docs = [
            d for d in _documents.values()
            if d["user_id"] == user_id
        ]

        # Get unique classifications
        classifications = list(set(
            d["classification"] for d in user_docs
            if d.get("classification")
        ))

        # Get unique entity types
        entity_types = set()
        for doc_id in [d["id"] for d in user_docs]:
            for entity in _entities.get(doc_id, []):
                entity_types.add(entity["type"])

        # Get date range
        dates = [d["created_at"] for d in user_docs]
        date_range = {
            "min": min(dates) if dates else None,
            "max": max(dates) if dates else None
        }

        return {
            "classifications": sorted(classifications),
            "entity_types": sorted(entity_types),
            "date_range": date_range
        }

    async def suggest(
        self,
        user_id: str,
        partial_query: str,
        limit: int = 10
    ) -> List[str]:
        """
        Get search suggestions based on partial query.
        """
        suggestions = set()
        query_lower = partial_query.lower()

        user_docs = [
            d for d in _documents.values()
            if d["user_id"] == user_id
        ]

        # Suggest from filenames
        for doc in user_docs:
            if query_lower in doc["filename"].lower():
                suggestions.add(doc["filename"])

        # Suggest from entity values
        for doc in user_docs:
            for entity in _entities.get(doc["id"], []):
                if query_lower in entity["value"].lower():
                    suggestions.add(entity["value"])

        return sorted(suggestions)[:limit]
