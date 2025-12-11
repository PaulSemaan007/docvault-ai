"""
Document Management API endpoints.
Handles upload, retrieval, and processing of documents.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from app.security.jwt import get_current_user
from app.security.audit import log_action
from app.services.document_service import DocumentService
from app.services.storage_service import StorageService
from app.ml.pipeline import process_document

router = APIRouter()


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    mime_type: str
    classification: Optional[str]
    confidence_score: Optional[float]
    status: str
    tags: List[str]
    created_at: str
    entities: Optional[List[dict]]


class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int
    page: int
    page_size: int


class UpdateDocumentRequest(BaseModel):
    tags: Optional[List[str]] = None


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload and process a new document.

    Processing pipeline:
    1. Validate file type and size
    2. Store file in Supabase Storage
    3. Extract text (OCR if image/scanned PDF)
    4. Classify document type using ML
    5. Extract named entities (dates, names, amounts)
    6. Store metadata in database
    7. Evaluate workflow rules
    """
    document_service = DocumentService()
    storage_service = StorageService()

    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Check file extension
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".txt"]
    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(allowed_extensions)}"
        )

    try:
        # Read file content
        content = await file.read()
        file_size = len(content)

        # Check file size (10MB limit)
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

        # Generate unique file path
        file_id = str(uuid.uuid4())
        file_path = f"{current_user['id']}/{file_id}{file_ext}"

        # Upload to storage
        await storage_service.upload(file_path, content, file.content_type)

        # Create document record
        document = await document_service.create(
            user_id=current_user["id"],
            filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type
        )

        # Process document asynchronously (classification, OCR, NER)
        classifier = request.app.state.classifier
        entity_extractor = request.app.state.entity_extractor

        processed = await process_document(
            document_id=document["id"],
            file_path=file_path,
            content=content,
            mime_type=file.content_type,
            classifier=classifier,
            entity_extractor=entity_extractor
        )

        # Update document with processing results
        document = await document_service.update(
            document_id=document["id"],
            classification=processed["classification"],
            confidence_score=processed["confidence"],
            extracted_text=processed["text"],
            entities=processed["entities"],
            status="processed"
        )

        # Log action
        await log_action(
            user_id=current_user["id"],
            action="DOCUMENT_UPLOADED",
            resource_type="document",
            resource_id=document["id"],
            details={"filename": file.filename, "classification": processed["classification"]}
        )

        return DocumentResponse(**document)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DemoUploadResponse(BaseModel):
    """Response model for demo upload endpoint."""
    id: str
    filename: str
    file_size: int
    mime_type: str
    classification: str
    confidence_score: float
    entities: List[dict]
    status: str


@router.post("/demo-upload", response_model=DemoUploadResponse)
async def demo_upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    """
    Demo upload endpoint - no authentication required.
    Processes document with real AI but doesn't persist to database.
    Perfect for showcasing the ML pipeline capabilities.
    """
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    # Check file extension
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx", ".txt"]
    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(allowed_extensions)}"
        )

    try:
        # Read file content
        content = await file.read()
        file_size = len(content)

        # Check file size (10MB limit)
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB")

        # Generate a temporary ID for demo
        file_id = str(uuid.uuid4())

        # Process document with real AI (classification, OCR, NER)
        classifier = request.app.state.classifier
        entity_extractor = request.app.state.entity_extractor

        processed = await process_document(
            document_id=file_id,
            file_path=f"demo/{file_id}{file_ext}",
            content=content,
            mime_type=file.content_type or "application/octet-stream",
            classifier=classifier,
            entity_extractor=entity_extractor
        )

        return DemoUploadResponse(
            id=file_id,
            filename=file.filename,
            file_size=file_size,
            mime_type=file.content_type or "application/octet-stream",
            classification=processed["classification"],
            confidence_score=processed["confidence"],
            entities=processed["entities"],
            status="processed"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    page: int = 1,
    page_size: int = 20,
    classification: Optional[str] = None,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    List documents for the current user with optional filtering.
    """
    document_service = DocumentService()

    documents, total = await document_service.list(
        user_id=current_user["id"],
        page=page,
        page_size=page_size,
        classification=classification,
        status=status
    )

    return DocumentListResponse(
        documents=[DocumentResponse(**doc) for doc in documents],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific document by ID.
    """
    document_service = DocumentService()

    document = await document_service.get(document_id, current_user["id"])

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse(**document)


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    request: UpdateDocumentRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update document metadata (tags, etc).
    """
    document_service = DocumentService()

    document = await document_service.get(document_id, current_user["id"])

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    updated = await document_service.update(
        document_id=document_id,
        tags=request.tags
    )

    await log_action(
        user_id=current_user["id"],
        action="DOCUMENT_UPDATED",
        resource_type="document",
        resource_id=document_id
    )

    return DocumentResponse(**updated)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a document and its associated file.
    """
    document_service = DocumentService()
    storage_service = StorageService()

    document = await document_service.get(document_id, current_user["id"])

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Delete file from storage
    await storage_service.delete(document["file_path"])

    # Delete database record
    await document_service.delete(document_id)

    await log_action(
        user_id=current_user["id"],
        action="DOCUMENT_DELETED",
        resource_type="document",
        resource_id=document_id,
        details={"filename": document["filename"]}
    )

    return {"message": "Document deleted successfully"}


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a signed URL to download the original document.
    """
    document_service = DocumentService()
    storage_service = StorageService()

    document = await document_service.get(document_id, current_user["id"])

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Generate signed URL (valid for 1 hour)
    download_url = await storage_service.get_signed_url(document["file_path"])

    await log_action(
        user_id=current_user["id"],
        action="DOCUMENT_DOWNLOADED",
        resource_type="document",
        resource_id=document_id
    )

    return {"download_url": download_url, "filename": document["filename"]}
