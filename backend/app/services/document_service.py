"""
Document Service.
Handles document CRUD operations and metadata management.
"""

from typing import Optional, List, Tuple
from datetime import datetime
import uuid

# In-memory document store (replace with Supabase in production)
_documents = {}
_entities = {}


class DocumentService:
    """
    Service for document management operations.
    """

    async def create(
        self,
        user_id: str,
        filename: str,
        file_path: str,
        file_size: int,
        mime_type: str
    ) -> dict:
        """
        Create a new document record.
        """
        doc_id = str(uuid.uuid4())

        document = {
            "id": doc_id,
            "user_id": user_id,
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "mime_type": mime_type,
            "classification": None,
            "confidence_score": None,
            "extracted_text": None,
            "tags": [],
            "status": "processing",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }

        _documents[doc_id] = document
        _entities[doc_id] = []

        return document

    async def get(self, document_id: str, user_id: str) -> Optional[dict]:
        """
        Get a document by ID (only if owned by user).
        """
        doc = _documents.get(document_id)

        if not doc or doc["user_id"] != user_id:
            return None

        doc["entities"] = _entities.get(document_id, [])
        return doc

    async def list(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 20,
        classification: Optional[str] = None,
        status: Optional[str] = None
    ) -> Tuple[List[dict], int]:
        """
        List documents for a user with optional filtering.
        """
        # Filter documents
        user_docs = [
            d for d in _documents.values()
            if d["user_id"] == user_id
        ]

        if classification:
            user_docs = [d for d in user_docs if d["classification"] == classification]

        if status:
            user_docs = [d for d in user_docs if d["status"] == status]

        # Sort by date descending
        user_docs.sort(key=lambda x: x["created_at"], reverse=True)

        # Paginate
        total = len(user_docs)
        start = (page - 1) * page_size
        end = start + page_size
        paginated = user_docs[start:end]

        # Add entities to each document
        for doc in paginated:
            doc["entities"] = _entities.get(doc["id"], [])

        return paginated, total

    async def update(
        self,
        document_id: str,
        classification: Optional[str] = None,
        confidence_score: Optional[float] = None,
        extracted_text: Optional[str] = None,
        entities: Optional[List[dict]] = None,
        tags: Optional[List[str]] = None,
        status: Optional[str] = None
    ) -> dict:
        """
        Update document metadata and processing results.
        """
        doc = _documents.get(document_id)
        if not doc:
            raise Exception("Document not found")

        if classification is not None:
            doc["classification"] = classification

        if confidence_score is not None:
            doc["confidence_score"] = confidence_score

        if extracted_text is not None:
            doc["extracted_text"] = extracted_text

        if tags is not None:
            doc["tags"] = tags

        if status is not None:
            doc["status"] = status

        if entities is not None:
            _entities[document_id] = entities

        doc["updated_at"] = datetime.utcnow().isoformat()
        doc["entities"] = _entities.get(document_id, [])

        return doc

    async def delete(self, document_id: str) -> bool:
        """
        Delete a document record.
        """
        if document_id in _documents:
            del _documents[document_id]
            if document_id in _entities:
                del _entities[document_id]
            return True
        return False

    async def get_classification_stats(self, user_id: str) -> dict:
        """
        Get document classification statistics for a user.
        """
        user_docs = [
            d for d in _documents.values()
            if d["user_id"] == user_id
        ]

        stats = {}
        for doc in user_docs:
            classification = doc.get("classification") or "unclassified"
            stats[classification] = stats.get(classification, 0) + 1

        return stats
