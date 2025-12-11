"""
Document Processing Pipeline.
Orchestrates OCR, classification, and entity extraction.
"""

from typing import Dict, List, Any
import logging

from app.ml.ocr import OCRProcessor
from app.ml.classifier import DocumentClassifier, KeywordClassifier
from app.ml.ner import EntityExtractor

logger = logging.getLogger(__name__)


async def process_document(
    document_id: str,
    file_path: str,
    content: bytes,
    mime_type: str,
    classifier: DocumentClassifier,
    entity_extractor: EntityExtractor
) -> Dict[str, Any]:
    """
    Full document processing pipeline.

    Steps:
    1. Extract text (OCR if needed)
    2. Classify document type
    3. Extract named entities
    4. Return processed data

    Args:
        document_id: Unique document identifier
        file_path: Storage path of the document
        content: Raw file bytes
        mime_type: File MIME type
        classifier: DocumentClassifier instance
        entity_extractor: EntityExtractor instance

    Returns:
        Processed document data including text, classification, and entities
    """
    logger.info(f"Processing document {document_id} ({mime_type})")

    # Step 1: Extract text
    ocr = OCRProcessor()
    text = ocr.extract_text(content, mime_type)

    if not text.strip():
        logger.warning(f"No text extracted from document {document_id}")
        return {
            "text": "",
            "classification": "other",
            "confidence": 0.0,
            "entities": [],
            "status": "no_text"
        }

    logger.info(f"Extracted {len(text)} characters from document")

    # Step 2: Classify document
    try:
        classification_result = classifier.classify(text)
    except Exception as e:
        logger.error(f"Classification failed, using keyword fallback: {e}")
        fallback = KeywordClassifier()
        classification_result = fallback.classify(text)

    logger.info(f"Classified as: {classification_result['label']} "
                f"(confidence: {classification_result['confidence']})")

    # Step 3: Extract entities
    entities = entity_extractor.extract(text)
    logger.info(f"Extracted {len(entities)} entities")

    # Step 4: Return processed data
    return {
        "text": text,
        "classification": classification_result["label"],
        "confidence": classification_result["confidence"],
        "all_classifications": classification_result.get("all_scores", {}),
        "entities": entities,
        "entity_summary": entity_extractor.get_entity_summary(entities),
        "status": "processed"
    }


async def reprocess_document(
    document_id: str,
    text: str,
    classifier: DocumentClassifier,
    entity_extractor: EntityExtractor
) -> Dict[str, Any]:
    """
    Reprocess an existing document (when models are updated).
    Skips OCR since text is already extracted.
    """
    classification_result = classifier.classify(text)
    entities = entity_extractor.extract(text)

    return {
        "classification": classification_result["label"],
        "confidence": classification_result["confidence"],
        "entities": entities,
        "entity_summary": entity_extractor.get_entity_summary(entities)
    }


def validate_processing_result(result: Dict) -> bool:
    """
    Validate that processing result has required fields.
    """
    required_fields = ["text", "classification", "confidence", "entities"]
    return all(field in result for field in required_fields)
