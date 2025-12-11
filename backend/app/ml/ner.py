"""
Named Entity Recognition using spaCy.
Extracts entities like names, organizations, dates, and monetary values from documents.
"""

import spacy
from typing import List, Dict
import logging
import re

logger = logging.getLogger(__name__)


class EntityExtractor:
    """
    Extract named entities from document text using spaCy.
    """

    def __init__(self, model_name: str = "en_core_web_sm"):
        """
        Initialize the entity extractor with a spaCy model.

        Args:
            model_name: spaCy model to use. Default is the small English model.
        """
        logger.info(f"Loading spaCy model: {model_name}")
        try:
            self.nlp = spacy.load(model_name)
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning(f"Model {model_name} not found. Downloading...")
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)

    def extract(self, text: str, max_length: int = 100000) -> List[Dict]:
        """
        Extract named entities from text.

        Args:
            text: Document text to process
            max_length: Maximum text length to process

        Returns:
            List of entity dictionaries with type, value, and confidence
        """
        if not text or not text.strip():
            return []

        # Truncate if necessary (spaCy has limits)
        if len(text) > max_length:
            text = text[:max_length]

        try:
            doc = self.nlp(text)
            entities = []
            seen = set()  # Avoid duplicates

            for ent in doc.ents:
                # Create unique key to avoid duplicates
                key = (ent.label_, ent.text.strip().lower())
                if key in seen:
                    continue
                seen.add(key)

                entity = {
                    "type": self._map_entity_type(ent.label_),
                    "value": ent.text.strip(),
                    "original_type": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 0.85  # spaCy doesn't provide confidence, using default
                }
                entities.append(entity)

            # Also extract custom patterns (emails, phone numbers, etc.)
            custom_entities = self._extract_custom_patterns(text)
            entities.extend(custom_entities)

            return entities

        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return []

    def _map_entity_type(self, spacy_type: str) -> str:
        """
        Map spaCy entity types to our simplified categories.
        """
        mapping = {
            "PERSON": "PERSON",
            "ORG": "ORGANIZATION",
            "GPE": "LOCATION",  # Geopolitical entity
            "LOC": "LOCATION",
            "DATE": "DATE",
            "TIME": "TIME",
            "MONEY": "MONEY",
            "PERCENT": "PERCENTAGE",
            "CARDINAL": "NUMBER",
            "ORDINAL": "NUMBER",
            "QUANTITY": "QUANTITY",
            "EVENT": "EVENT",
            "FAC": "FACILITY",
            "PRODUCT": "PRODUCT",
            "WORK_OF_ART": "WORK",
            "LAW": "LAW",
            "LANGUAGE": "LANGUAGE",
            "NORP": "GROUP",  # Nationalities, religious/political groups
        }
        return mapping.get(spacy_type, "OTHER")

    def _extract_custom_patterns(self, text: str) -> List[Dict]:
        """
        Extract entities using regex patterns for things spaCy might miss.
        """
        entities = []

        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append({
                "type": "EMAIL",
                "value": match.group(),
                "original_type": "EMAIL",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.95
            })

        # Phone number pattern (US format)
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        for match in re.finditer(phone_pattern, text):
            entities.append({
                "type": "PHONE",
                "value": match.group(),
                "original_type": "PHONE",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.90
            })

        # Invoice/Reference number pattern
        ref_pattern = r'\b(?:INV|REF|PO|ORDER)[#\-]?\s*[A-Z0-9]{4,12}\b'
        for match in re.finditer(ref_pattern, text, re.IGNORECASE):
            entities.append({
                "type": "REFERENCE_NUMBER",
                "value": match.group(),
                "original_type": "REFERENCE",
                "start": match.start(),
                "end": match.end(),
                "confidence": 0.85
            })

        return entities

    def get_entity_summary(self, entities: List[Dict]) -> Dict:
        """
        Get a summary of extracted entities by type.
        """
        summary = {}
        for entity in entities:
            entity_type = entity["type"]
            if entity_type not in summary:
                summary[entity_type] = []
            summary[entity_type].append(entity["value"])
        return summary
