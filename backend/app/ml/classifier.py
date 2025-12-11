"""
Document Classification using Hugging Face Transformers.
Classifies documents into categories: invoice, contract, report, letter, form, other.
"""

from transformers import pipeline
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# Document categories we classify into
DOCUMENT_CATEGORIES = [
    "invoice",
    "contract",
    "report",
    "letter",
    "form",
    "receipt",
    "memo",
    "other"
]


class DocumentClassifier:
    """
    ML-based document classifier using zero-shot classification.
    Uses a pre-trained model that can classify text without task-specific training.
    """

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Initialize the classifier with a zero-shot classification model.

        Args:
            model_name: Hugging Face model for zero-shot classification.
                        Default uses BART-large fine-tuned on MNLI.
        """
        logger.info(f"Loading document classifier: {model_name}")
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model=model_name,
                device=-1  # CPU, set to 0 for GPU
            )
            self.categories = DOCUMENT_CATEGORIES
            logger.info("Document classifier loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load classifier: {e}")
            self.classifier = None

    def classify(self, text: str, max_length: int = 1024) -> Dict[str, any]:
        """
        Classify a document based on its text content.

        Args:
            text: The document text to classify
            max_length: Maximum characters to use for classification

        Returns:
            Dict with classification label and confidence score
        """
        if not self.classifier:
            return {"label": "other", "confidence": 0.0, "all_scores": {}}

        # Truncate text if too long (model has token limits)
        truncated_text = text[:max_length] if len(text) > max_length else text

        if not truncated_text.strip():
            return {"label": "other", "confidence": 0.0, "all_scores": {}}

        try:
            # Run zero-shot classification
            result = self.classifier(
                truncated_text,
                candidate_labels=self.categories,
                hypothesis_template="This document is a {}."
            )

            # Extract results
            label = result["labels"][0]
            confidence = result["scores"][0]
            all_scores = dict(zip(result["labels"], result["scores"]))

            return {
                "label": label,
                "confidence": round(confidence, 4),
                "all_scores": {k: round(v, 4) for k, v in all_scores.items()}
            }

        except Exception as e:
            logger.error(f"Classification error: {e}")
            return {"label": "other", "confidence": 0.0, "all_scores": {}}

    def batch_classify(self, texts: list) -> list:
        """
        Classify multiple documents in batch.

        Args:
            texts: List of document texts

        Returns:
            List of classification results
        """
        return [self.classify(text) for text in texts]


# Fallback classifier using keyword matching (no ML dependency)
class KeywordClassifier:
    """
    Simple keyword-based classifier as fallback when ML models unavailable.
    """

    KEYWORDS = {
        "invoice": ["invoice", "bill", "payment due", "amount due", "total due", "subtotal"],
        "contract": ["agreement", "contract", "terms and conditions", "hereby agree", "party", "whereas"],
        "report": ["report", "summary", "findings", "analysis", "conclusion", "executive summary"],
        "letter": ["dear", "sincerely", "regards", "to whom it may concern"],
        "form": ["form", "please fill", "application", "checkbox", "signature required"],
        "receipt": ["receipt", "transaction", "paid", "thank you for your purchase"],
        "memo": ["memo", "memorandum", "to:", "from:", "subject:", "re:"],
    }

    def classify(self, text: str) -> Dict[str, any]:
        """
        Classify document using keyword matching.
        """
        text_lower = text.lower()
        scores = {}

        for category, keywords in self.KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[category] = score

        if max(scores.values()) == 0:
            return {"label": "other", "confidence": 0.5, "all_scores": scores}

        best_category = max(scores, key=scores.get)
        confidence = min(scores[best_category] / 3, 1.0)  # Normalize

        return {
            "label": best_category,
            "confidence": round(confidence, 4),
            "all_scores": scores
        }
