"""Parse ECG PDF reports into structured measurements."""
from __future__ import annotations

import re
from typing import Iterable, List, Optional, Tuple

from cardiac_report.models import ECGMeasurements, PatientContext

from .patient_extraction import extract_patient_fields
from .utils import PDFExtractionError, extract_text_from_pdf


def _search(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


def _num(pattern: str, text: str) -> Optional[float]:
    raw = _search(pattern, text)
    if raw is None:
        return None
    try:
        norm = raw.replace(",", ".")
        match = re.search(r"[-+]?\d+(?:\.\d+)?", norm)
        if not match:
            return None
        return float(match.group())
    except Exception:
        return None


def _num_from_patterns(patterns: Iterable[str], text: str) -> Optional[float]:
    for pattern in patterns:
        value = _num(pattern, text)
        if value is not None:
            return value
    return None


def _line_after_label(text: str, label: str) -> Optional[str]:
    pattern = re.compile(rf"{label}\s*[:\-]?\s*([^\n]+)", flags=re.IGNORECASE)
    match = pattern.search(text)
    if match:
        candidate = match.group(1).strip()
        if candidate:
            return candidate
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if label.lower() in line.lower() and idx + 1 < len(lines):
            candidate = lines[idx + 1].strip()
            if candidate:
                return candidate
    return None


def parse_ecg_pdf(pdf_bytes: bytes) -> Tuple[Optional[PatientContext], Optional[ECGMeasurements], List[str]]:
    warnings: List[str] = []
    try:
        text = extract_text_from_pdf(pdf_bytes)
    except PDFExtractionError as exc:
        warnings.append(str(exc))
        return None, None, warnings

    patient_fields = extract_patient_fields(text)
    patient_id = patient_fields.patient_id or _search(r"pati[eë]nt(?:\s*id)?[:\-]\s*(.+?)\s", text)
    name = patient_fields.full_name or _search(r"naam[:\-]\s*(.+?)\s+(?:geboorte|geslacht)", text)
    dob = patient_fields.date_of_birth or _search(r"geboorte(?:datum)?[:\-]\s*(\d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4})", text)

    patient = PatientContext(
        sex=patient_fields.sex,
        patient_id=patient_id,
        full_name=name,
        date_of_birth=dob,
        leeftijd=patient_fields.leeftijd,
        bsa=patient_fields.bsa,
        weight=patient_fields.weight,
        length=patient_fields.length,
    )

    recorded_at = _search(r"datum[:\-]\s*(\d{1,2}[-/ ]\d{1,2}[-/ ]\d{2,4})", text)
    if recorded_at is None:
        timestamp_match = re.search(r"(\d{2}[./-]\d{2}[./-]\d{4}\s+\d{2}:\d{2}:\d{2})", text)
        if timestamp_match:
            recorded_at = timestamp_match.group(1)

    rhythm_summary = _search(r"ritme[:\-]\s*(.+?)\s{2,}", text)
    if rhythm_summary is None:
        rhythm_summary = _search(r"(sinusritme[^\n]*)", text)

    auto_report_text = (
        _line_after_label(text, "Opmerking")
        or _line_after_label(text, "Conclusie")
        or _line_after_label(text, "Protocol")
    )

    acquisition_device = _search(r"toestel[:\-]\s*(.+?)\s{2,}", text)
    if acquisition_device is None:
        acquisition_device = _line_after_label(text, "Apparaat-ID")
    if acquisition_device:
        acquisition_device = acquisition_device.split()[0]

    measurements = ECGMeasurements(
        patient=patient,
        recorded_at=recorded_at,
        vent_rate=_num_from_patterns(
            [
                r"vent(?:riculaire)?\s+frequentie\s*(?:[:=\-]|is)?\s*([^\s]+)",
                r"hf\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        pr_interval_ms=_num_from_patterns(
            [
                r"pr(?:\s*interval)?\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        qrs_duration_ms=_num_from_patterns(
            [
                r"qrs(?:\s*duur)?\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        qt_interval_ms=_num_from_patterns(
            [
                r"qt(?!c)\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        qtc_interval_ms=_num_from_patterns(
            [
                r"qtc[a-z]*\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        p_axis_deg=_num_from_patterns(
            [
                r"p[-\s]?(?:axis|as)\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        qrs_axis_deg=_num_from_patterns(
            [
                r"qrs[-\s]?(?:axis|as)\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        p_duration_ms=_num_from_patterns(
            [
                r"p\s*[-]?\s*duur\s*(?:[:=\-]|is)?\s*([^\s]+)",
                r"p-?wave(?:\s*duration)?\s*(?:[:=\-]|is)?\s*([^\s]+)",
                r"p[-\s]?wave[-\s]?duration\s*(?:[:=\-]|is)?\s*([^\s]+)",
                r"p[-\s]?duur(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        t_axis_deg=_num_from_patterns(
            [
                r"t[-\s]?(?:axis|as)\s*(?:[:=\-]|is)?\s*([^\s]+)",
            ],
            text,
        ),
        rhythm_summary=rhythm_summary,
        auto_report_text=auto_report_text,
        acquisition_device=acquisition_device,
    )

    missing: List[str] = []
    if measurements.pr_interval_ms is None:
        missing.append("PR")
    if measurements.qrs_duration_ms is None:
        missing.append("QRS")
    if measurements.qt_interval_ms is None:
        missing.append("QT")
    if missing:
        warnings.append("Kon niet alle intervalwaarden uitlezen: " + ", ".join(missing))

    return patient, measurements, warnings
