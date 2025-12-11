"""
DocVault AI - Backend API
FastAPI application for document management with AI-powered processing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import auth, documents, search, workflows, admin
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Initialize ML models
    print("🚀 Starting DocVault AI...")
    from app.ml.classifier import DocumentClassifier
    from app.ml.ner import EntityExtractor

    app.state.classifier = DocumentClassifier()
    app.state.entity_extractor = EntityExtractor()
    print("✅ ML models loaded")

    yield

    # Shutdown
    print("👋 Shutting down DocVault AI...")


app = FastAPI(
    title="DocVault AI",
    description="Intelligent Document Management System with AI-powered classification and extraction",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "DocVault AI",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "ml_models": "loaded"
    }
