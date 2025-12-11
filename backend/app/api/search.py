"""
Search API endpoints.
Full-text search across documents with filters.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import List, Optional

from app.security.jwt import get_current_user
from app.services.search_service import SearchService

router = APIRouter()


class SearchResult(BaseModel):
    id: str
    filename: str
    classification: Optional[str]
    snippet: str  # Highlighted text excerpt
    score: float
    created_at: str


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    query: str
    filters_applied: dict


class FilterOptions(BaseModel):
    classifications: List[str]
    entity_types: List[str]
    date_range: dict


@router.get("", response_model=SearchResponse)
async def search_documents(
    q: str = Query(..., min_length=1, description="Search query"),
    classification: Optional[str] = None,
    entity_type: Optional[str] = None,
    entity_value: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Full-text search across all user documents.

    Features:
    - Searches document content, filenames, and extracted entities
    - Supports filtering by classification, entity type, date range
    - Returns highlighted snippets showing match context
    - Results ranked by relevance score
    """
    search_service = SearchService()

    results, total = await search_service.search(
        user_id=current_user["id"],
        query=q,
        classification=classification,
        entity_type=entity_type,
        entity_value=entity_value,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size
    )

    filters_applied = {
        "classification": classification,
        "entity_type": entity_type,
        "entity_value": entity_value,
        "date_from": date_from,
        "date_to": date_to
    }

    return SearchResponse(
        results=[SearchResult(**r) for r in results],
        total=total,
        query=q,
        filters_applied={k: v for k, v in filters_applied.items() if v}
    )


@router.get("/filters", response_model=FilterOptions)
async def get_filter_options(current_user: dict = Depends(get_current_user)):
    """
    Get available filter options for the current user's documents.

    Returns:
    - List of classifications present in user's documents
    - List of entity types extracted
    - Date range of documents
    """
    search_service = SearchService()

    options = await search_service.get_filter_options(current_user["id"])

    return FilterOptions(**options)


@router.get("/suggest")
async def suggest_queries(
    q: str = Query(..., min_length=2),
    current_user: dict = Depends(get_current_user)
):
    """
    Get search query suggestions based on partial input.
    Suggests based on document titles, entity values, and tags.
    """
    search_service = SearchService()

    suggestions = await search_service.suggest(
        user_id=current_user["id"],
        partial_query=q
    )

    return {"suggestions": suggestions}
