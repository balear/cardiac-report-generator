"""Utility helpers for PDF ingestion flows."""
from __future__ import annotations

import io
import logging
import string
from typing import BinaryIO, Iterable, List, Sequence, Union

try:  # Lazy optional dependency; raise friendly error if missing.
    import pdfplumber  # type: ignore
except ImportError:  # pragma: no cover - handled at runtime
    pdfplumber = None

try:  # Optional OCR dependency
    import pytesseract  # type: ignore
    from pytesseract import Output as TesseractOutput  # type: ignore[attr-defined]
except ImportError:  # pragma: no cover - handled at runtime
    pytesseract = None
    TesseractOutput = None

try:  # Pillow helpers for preprocessing
    from PIL import ImageOps
except ImportError:  # pragma: no cover - pillow should exist but guard anyway
    ImageOps = None


LOGGER = logging.getLogger(__name__)
_LAST_TEXT_CACHE: str = ""
_OCR_KEYWORDS: Sequence[str] = (
    "naam",
    "pati",
    "geboort",
    "leeftijd",
    "geslacht",
    "gewicht",
    "lengte",
    "bsa",
    "watt",
    "belasting",
    "hart",
    "bloed",
    "conclusie",
    "protocol",
    "ritme",
)
PDF_DEPENDENCY_MESSAGE = "PDF import vereist het pdfplumber pakket. Installeer het met 'pip install pdfplumber'."
PDF_NO_TEXT_MESSAGE = (
    "PDF bevat geen doorzoekbare tekst (waarschijnlijk enkel afbeeldingen). "
    "Exporteer het rapport vanuit het bronpakket als tekst-PDF of gebruik een OCR-stap alvorens te importeren."
)
OCR_DEPENDENCY_MESSAGE = (
    "OCR fallback vereist Tesseract (systeeminstallatie) en het Python-pakket 'pytesseract'. "
    "Installeer Tesseract, voeg het binaire pad toe aan PATH en voer 'pip install pytesseract' uit."
)


class PDFExtractionError(RuntimeError):
    """Raised when text cannot be extracted from the provided PDF."""


def extract_text_from_pdf(data: Union[bytes, BinaryIO]) -> str:
    """Return concatenated text from a PDF file, using OCR when necessary."""

    pdf_bytes = _ensure_pdf_bytes(data)
    text = _extract_text_via_pdfplumber(pdf_bytes)
    if text.strip():
        _set_last_text(text)
        return text
    ocr_text = _extract_text_via_ocr(pdf_bytes)
    _set_last_text(ocr_text)
    return ocr_text


def pdf_dependency_available() -> bool:
    """Return True when pdfplumber can be imported in this environment."""

    return pdfplumber is not None


def ocr_dependency_available() -> bool:
    """Return True when pytesseract is importable."""

    return pytesseract is not None


def get_last_extracted_text() -> str:
    """Return the raw text content from the most recent PDF extraction."""

    return _LAST_TEXT_CACHE


def _set_last_text(value: str) -> None:
    global _LAST_TEXT_CACHE
    _LAST_TEXT_CACHE = value


def normalize_whitespace(text: str) -> str:
    """Collapse consecutive whitespace to single spaces for easier regex parsing."""

    lines = [" ".join(line.split()) for line in text.splitlines()]
    filtered = [line for line in lines if line]
    return "\n".join(filtered)


def _ensure_pdf_bytes(data: Union[bytes, BinaryIO]) -> bytes:
    if isinstance(data, (bytes, bytearray)):
        return bytes(data)
    try:
        raw = data.read()
    except Exception as exc:  # pragma: no cover - invalid stream
        raise PDFExtractionError("Kon PDF-inhoud niet lezen") from exc
    if isinstance(raw, str):  # pragma: no cover - unexpected but safe
        raw = raw.encode("utf-8")
    return bytes(raw)


def _extract_text_via_pdfplumber(pdf_bytes: bytes) -> str:
    if pdfplumber is None:  # pragma: no cover - environment specific
        raise PDFExtractionError(PDF_DEPENDENCY_MESSAGE)

    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:  # pragma: no cover - depends on pdfplumber
        raise PDFExtractionError("Failed to read PDF") from exc

    joined = "\n".join(pages)
    return normalize_whitespace(joined)


def _extract_text_via_ocr(pdf_bytes: bytes, dpi: int = 300) -> str:
    if pytesseract is None:  # pragma: no cover - optional dependency missing
        raise PDFExtractionError(OCR_DEPENDENCY_MESSAGE)
    if pdfplumber is None:  # pragma: no cover - should already be checked
        raise PDFExtractionError(PDF_DEPENDENCY_MESSAGE)

    page_texts: List[str] = []
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                for segment in _iter_page_segments(page):
                    try:
                        pil_image = segment.to_image(resolution=dpi).original
                        pil_image = _prepare_image_for_ocr(pil_image)
                    except Exception as exc:
                        raise PDFExtractionError("Kon PDF niet naar afbeelding renderen voor OCR") from exc
                    ocr_text = _best_ocr_text(pil_image)
                    if ocr_text:
                        page_texts.append(ocr_text)
    except PDFExtractionError:
        raise
    except Exception as exc:  # pragma: no cover - unexpected OCR failure
        raise PDFExtractionError("OCR kon PDF niet openen") from exc

    joined = "\n".join(page_texts).strip()
    if not joined:
        raise PDFExtractionError(PDF_NO_TEXT_MESSAGE)
    return normalize_whitespace(joined)


def _best_ocr_text(image, angles: Sequence[int] = (0, 90, 180, 270)) -> str:
    """Run OCR across multiple rotations and return the text with the highest score."""

    ordered_angles = _ordered_angles(image, angles)
    best_text = ""
    best_score = 0
    for angle in ordered_angles:
        rotated = image if angle == 0 else image.rotate(angle, expand=True)
        text = pytesseract.image_to_string(rotated, config="--psm 6 -c preserve_interword_spaces=1")
        score = _ocr_text_score(text)
        if score > best_score:
            best_score = score
            best_text = text
    return best_text


def _ocr_text_score(text: str) -> int:
    letters = sum(1 for char in text if char in string.ascii_letters)
    digits = sum(1 for char in text if char in string.digits)
    normalized = text.lower()
    keyword_hits = sum(normalized.count(keyword) for keyword in _OCR_KEYWORDS)
    ascii_ratio = letters / max(len(text), 1)
    return int(letters * 4 + digits * 2 + ascii_ratio * 1000 + keyword_hits * 300)


def _ordered_angles(image, base_angles: Sequence[int]) -> List[int]:
    if pytesseract is None or TesseractOutput is None:
        return list(base_angles)
    try:
        osd = pytesseract.image_to_osd(image, output_type=TesseractOutput.DICT)
        rotate = int(osd.get("rotate", 0)) % 360
        if rotate in base_angles:
            return [rotate] + [angle for angle in base_angles if angle != rotate]
    except Exception:
        pass
    return list(base_angles)


def _prepare_image_for_ocr(image):
    if ImageOps is None:
        return image.convert("L")
    gray = image.convert("L")
    enhanced = ImageOps.autocontrast(gray)
    return enhanced


def _iter_page_segments(page) -> Iterable["pdfplumber.page.Page"]:  # type: ignore[name-defined]
    width = getattr(page, "width", 0) or 0
    height = getattr(page, "height", 0) or 0
    boxes = [(0, 0, width, height)]
    if width and height:
        boxes.append((0, 0, width * 0.7, height))
        boxes.append((width * 0.2, 0, width, height))
        boxes.append((0, height * 0.2, width * 0.7, height))
    seen = set()
    for box in boxes:
        key = tuple(round(v, 2) for v in box)
        if key in seen:
            continue
        seen.add(key)
        yield page.within_bbox(box)
