"""Parse fietsproef PDF reports into structured measurements."""
from __future__ import annotations

import re
from typing import Callable, List, Optional, Tuple

from cardiac_report.models import FietstestMeasurements, PatientContext

from .utils import PDFExtractionError, extract_text_from_pdf
from .patient_extraction import extract_patient_fields

_FLAGS = re.IGNORECASE | re.MULTILINE
_NUMERIC = re.compile(r"[-+]?\d+(?:[\.,]\d+)?")
_TIME_TOKEN = re.compile(r"(\d{1,2})[:.](\d{2})")

_MEASURE_PATTERNS = {
    "Start watt": [
        r"start(?:\s*belasting)?(?:\s*watt)?(?:\s*\(w(?:att)?\))?\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"start\s*load\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
    ],
    "Opdrijven": [
        r"opdrij(?:ving|fing|ven)\s*(?:[(][^)]*\))?\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"stapgrootte\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
    ],
    "Max watt": [
        r"max(?:imale)?\s*(?:belasting|vermogen|watt)\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"piek\s*watt\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"max[.\s]*belasting[^0-9]*([0-9][0-9\.,]*)\s*w",
    ],
    "Duur": [
        r"duur(?:\s*(?:bij|op))?\s*(?:max(?:imale)?\s*)?(?:belasting|vermogen)?\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"tijd\s*aan\s*top\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"inspanning\s*([0-9]{1,2}[:.][0-9]{2})",
    ],
    "Max HR": [
        r"max(?:imale)?\s*(?:hartslag|hr|hartfrequentie)\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"piek\s*hr\s*(?:[:=\-]\s*)?([0-9][0-9\.,]*)",
        r"max[.\s]*hf[^0-9]*([0-9][0-9\.,]*)",
    ],
}


def _search(pattern: str, text: str) -> Optional[str]:
    match = re.search(pattern, text, flags=_FLAGS)
    if match:
        return match.group(1).strip()
    return None


def _to_float(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    try:
        norm = raw.replace(",", ".")
        return float(_NUMERIC.search(norm).group()) if _NUMERIC.search(norm) else None
    except Exception:
        return None


def _to_seconds(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    match = _TIME_TOKEN.search(raw)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        return float(minutes * 60 + seconds)
    return _to_float(raw)


def _extract_workloads(text: str) -> List[Tuple[str, float]]:
    series: List[Tuple[str, float]] = []
    seen = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        lower = line.lower()
        if not (lower.startswith("opwarmen") or lower.startswith("werken")):
            continue
        watt = _line_watt_value(line)
        if watt is None:
            continue
        label = "opwarmen" if lower.startswith("opwarmen") else "werken"
        key = (label, watt)
        if key in seen:
            continue
        seen.add(key)
        series.append((label, watt))
    return series


def _line_watt_value(line: str) -> Optional[float]:
    sanitized = line.replace("-", " ")
    tokens = sanitized.split()
    seen_time = False
    for token in tokens:
        stripped = token.strip("()")
        if _TIME_TOKEN.fullmatch(stripped):
            seen_time = True
            continue
        if not seen_time:
            continue
        cleaned = re.sub(r"[^0-9\.,]", "", stripped)
        value = _to_float(cleaned)
        if value is not None:
            return value
        break
    return None


def _first_watt(workloads: List[Tuple[str, float]], prefer: str) -> Optional[float]:
    for label, value in workloads:
        if label == prefer:
            return value
    return None


def _estimate_increment(workloads: List[Tuple[str, float]]) -> Optional[float]:
    work_values = [value for label, value in workloads if label == "werken"]
    if len(work_values) < 2:
        return None
    for idx in range(len(work_values) - 1):
        diff = work_values[idx + 1] - work_values[idx]
        if diff > 0:
            return diff
    return None


def parse_fietstest_pdf(pdf_bytes: bytes) -> Tuple[Optional[PatientContext], Optional[FietstestMeasurements], List[str]]:
    """Return patient + fiets measurements parsed from PDF contents."""

    warnings: List[str] = []
    try:
        text = extract_text_from_pdf(pdf_bytes)
    except PDFExtractionError as exc:
        warnings.append(str(exc))
        return None, None, warnings

    patient_fields = extract_patient_fields(text)

    patient = PatientContext(
        sex=patient_fields.sex,
        patient_id=patient_fields.patient_id,
        full_name=patient_fields.full_name,
        date_of_birth=patient_fields.date_of_birth,
        leeftijd=patient_fields.leeftijd,
        bsa=patient_fields.bsa,
        weight=patient_fields.weight,
        length=patient_fields.length,
    )

    def _find_measure(
        key: str,
        patterns: List[str],
        parser: Callable[[Optional[str]], Optional[float]] = None,
        warn: bool = True,
    ) -> Optional[float]:
        parser = parser or _to_float
        for pattern in patterns:
            value = _search(pattern, text)
            if value is None:
                continue
            parsed = parser(value)
            if parsed is not None:
                return parsed
        if warn:
            warnings.append(f"{key} niet gevonden in PDF")
        return None

    workloads = _extract_workloads(text)

    start_watt = _find_measure("Start watt", _MEASURE_PATTERNS["Start watt"], warn=False)
    if start_watt is None:
        start_watt = _first_watt(workloads, prefer="opwarmen") or _first_watt(workloads, prefer="werken")
    if start_watt is None:
        warnings.append("Start watt niet gevonden in PDF")

    increment_watt = _find_measure("Opdrijven", _MEASURE_PATTERNS["Opdrijven"], warn=False)
    if increment_watt is None:
        increment_watt = _estimate_increment(workloads)
    if increment_watt is None:
        warnings.append("Opdrijven niet gevonden in PDF")

    max_watt = _find_measure("Max watt", _MEASURE_PATTERNS["Max watt"])
    if max_watt is None and workloads:
        max_watt = max(value for _, value in workloads)

    duration_at_max = _find_measure("Duur", _MEASURE_PATTERNS["Duur"], parser=_to_seconds)
    max_hr = _find_measure("Max HR", _MEASURE_PATTERNS["Max HR"])

    bp_evolutie = _search(r"bloeddruk(?:evolutie)?[:\-]\s*([^\n]+)", text)
    ritme = _search(r"ritme[:\-]\s*([^\n]+)", text)
    effort_type = _search(r"inspanning[:\-]\s*([^\n]+)", text)
    stop_criterium = _search(r"criterium[:\-]\s*([^\n]+)", text)
    ecg_changes = _search(r"ecg(?:\s+verloop)?[:\-]\s*([^\n]+)", text)
    conclusion = _search(r"conclusie[:\-]\s*([^\n]+)", text)

    measurements = FietstestMeasurements(
        patient=patient,
        start_watt=start_watt,
        increment_watt=increment_watt,
        max_watt=max_watt,
        duration_at_max=duration_at_max,
        max_hr=max_hr,
        bp_evolutie=bp_evolutie,
        ritme=ritme,
        effort_type=effort_type,
        stop_criterium=stop_criterium,
        ecg_changes=ecg_changes,
        conclusion=conclusion,
    )

    return patient, measurements, warnings
