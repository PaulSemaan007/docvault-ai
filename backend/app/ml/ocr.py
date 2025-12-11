"""
OCR (Optical Character Recognition) using Tesseract.
Extracts text from images and scanned PDFs.
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader
import io
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class OCRProcessor:
    """
    Extract text from images and PDFs using Tesseract OCR.
    """

    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize OCR processor.

        Args:
            tesseract_cmd: Path to Tesseract executable (if not in PATH)
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_from_image(self, image_bytes: bytes) -> str:
        """
        Extract text from an image file.

        Args:
            image_bytes: Raw image bytes

        Returns:
            Extracted text string
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))

            # Preprocess image for better OCR
            image = self._preprocess_image(image)

            # Run OCR
            text = pytesseract.image_to_string(image, lang='eng')

            return text.strip()

        except Exception as e:
            logger.error(f"Image OCR error: {e}")
            return ""

    def extract_from_pdf(self, pdf_bytes: bytes) -> str:
        """
        Extract text from a PDF file.
        First tries direct text extraction, falls back to OCR if needed.

        Args:
            pdf_bytes: Raw PDF bytes

        Returns:
            Extracted text string
        """
        try:
            # First try direct text extraction (for text-based PDFs)
            text = self._extract_pdf_text(pdf_bytes)

            # If no text found, use OCR
            if not text.strip():
                logger.info("PDF has no text layer, using OCR...")
                text = self._ocr_pdf(pdf_bytes)

            return text.strip()

        except Exception as e:
            logger.error(f"PDF extraction error: {e}")
            return ""

    def _extract_pdf_text(self, pdf_bytes: bytes) -> str:
        """
        Extract text directly from PDF (for text-based PDFs).
        """
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text_parts = []

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

            return "\n".join(text_parts)

        except Exception as e:
            logger.error(f"PDF text extraction error: {e}")
            return ""

    def _ocr_pdf(self, pdf_bytes: bytes) -> str:
        """
        Convert PDF pages to images and run OCR.
        """
        try:
            # Convert PDF to images
            images = convert_from_bytes(pdf_bytes, dpi=200)
            text_parts = []

            for i, image in enumerate(images):
                logger.info(f"OCR processing page {i + 1}/{len(images)}")
                image = self._preprocess_image(image)
                page_text = pytesseract.image_to_string(image, lang='eng')
                text_parts.append(page_text)

            return "\n".join(text_parts)

        except Exception as e:
            logger.error(f"PDF OCR error: {e}")
            return ""

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy.
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')

        # Resize if too small (OCR works better with larger images)
        min_width = 1000
        if image.width < min_width:
            ratio = min_width / image.width
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        return image

    def extract_text(self, file_bytes: bytes, mime_type: str) -> str:
        """
        Extract text from file based on MIME type.

        Args:
            file_bytes: Raw file bytes
            mime_type: File MIME type

        Returns:
            Extracted text
        """
        if mime_type == "application/pdf":
            return self.extract_from_pdf(file_bytes)
        elif mime_type.startswith("image/"):
            return self.extract_from_image(file_bytes)
        elif mime_type in ["text/plain", "text/html", "text/csv"]:
            return file_bytes.decode("utf-8", errors="ignore")
        else:
            logger.warning(f"Unsupported MIME type for text extraction: {mime_type}")
            return ""
