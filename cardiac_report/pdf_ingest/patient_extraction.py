"""Patient metadata extraction helpers shared across PDF parsers."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .utils import normalize_whitespace

_NUMERIC = re.compile(r"[-+]?\d+(?:[\.,]\d+)?")
_DATE = re.compile(r"(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}[./-]\d{2}[./-]\d{2})")
_OCR_DIGIT_FIXUPS = str.maketrans({
    "O": "0",
    "o": "0",
    "D": "0",
    "I": "1",
    "l": "1",
    "|": "1",
    "S": "5",
    "s": "5",
    "B": "8",
    "T": "7",
})


@dataclass
class PatientFields:
    """Loose container for patient details discovered inside a PDF."""

    sex: str = "Man"
    patient_id: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    leeftijd: Optional[float] = None
    bsa: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None


def extract_patient_fields(raw_text: str) -> PatientFields:
    """Return best-effort patient fields parsed from raw PDF text."""

    text = normalize_whitespace(raw_text)

    full_name = _clean_name(_match(_label_pattern("naam"), text))
    patient_id_primary = _match(
        r"(?:pati[éeë]?nt[-\s]*(?:id|nr)|patient\s*id|mrn)(?:[:=\-]\s*|\s+)([^\n]+)",
        text,
    )
    patient_id_secondary = _match(r"(?:order[-\s]*id|bezoek[-\s]*id)(?:[:=\-]\s*|\s+)([^\n]+)", text)
    date_of_birth = _extract_date(
        _match(r"(?:geboorte(?:datum|dat)|dob|date\s*of\s*birth)(?:[:=\-]\s*|[.\s]+)([^\n]+)", text)
    )
    leeftijd = _extract_numeric(_match(_label_pattern("leeftijd"), text))
    bsa = _extract_numeric(_match(_label_pattern(r"\bBSA\b"), text))
    weight = _extract_numeric(_match(_label_pattern("(?:gewicht|weight)"), text))
    length = _normalize_length(_match(_label_pattern("(?:lengte|length|height)"), text))
    sex = _normalize_sex(_match(_label_pattern("(?:geslacht|sex|gender)"), text))

    return PatientFields(
        sex=sex or "Man",
        patient_id=_first_token(patient_id_primary) or _first_token(patient_id_secondary),
        full_name=full_name,
        date_of_birth=date_of_birth,
        leeftijd=leeftijd,
        bsa=bsa,
        weight=weight,
        length=length,
    )


def _match(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _extract_numeric(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    cleaned = raw.translate(_OCR_DIGIT_FIXUPS)
    cleaned = cleaned.replace(",", ".")
    match = _NUMERIC.search(cleaned)
    if not match:
        return None
    try:
        return float(match.group().replace(",", "."))
    except ValueError:
        return None


def _normalize_length(raw: Optional[str]) -> Optional[float]:
    value = _extract_numeric(raw)
    if value is None:
        return None
    lowered = raw.lower() if raw else ""
    if "m" in lowered and value < 3:
        return value * 100  # convert meters to centimeters
    return value


def _extract_date(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    match = _DATE.search(raw)
    if match:
        return match.group()
    return None


def _normalize_sex(raw: Optional[str]) -> str:
    if not raw:
        return "Man"
    token = raw.strip().lower()
    if token.startswith(("v", "f")):
        return "Vrouw"
    if token.startswith("man") or token.startswith("m"):
        return "Man"
    if token.startswith("female"):
        return "Vrouw"
    if token.startswith("male"):
        return "Man"
    return "Man"


def _clean_value(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    return raw.strip() or None


def _clean_name(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    tokens = []
    for token in raw.split():
        if any(ch.isdigit() for ch in token):
            break
        tokens.append(token)
    if not tokens:
        return raw.strip() or None
    return " ".join(tokens)


def _first_token(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    for token in raw.split():
        token = token.strip()
        if token:
            return token
    return None


def _label_pattern(label: str) -> str:
    return rf"{label}(?:[:=\-]\s*|[.\s]+)([^\n]+)"
