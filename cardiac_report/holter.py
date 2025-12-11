"""Holter monitoring domain helpers and report generation."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from cardiac_report.models import PatientContext


@dataclass
class HolterMeasurements:
    """Structured input for Holter monitoring interpretation."""

    patient: PatientContext
    recording_date: Optional[str] = None
    recording_duration_hours: Optional[int] = None
    avg_hr: Optional[int] = None
    min_hr: Optional[int] = None
    max_hr: Optional[int] = None
    afib_percentage: Optional[float] = None
    pauses_count: Optional[int] = None
    longest_pause_ms: Optional[int] = None
    ves_count: Optional[int] = None
    sves_count: Optional[int] = None
    av_block_type: Optional[str] = None
    other_findings: Optional[str] = None

    @property
    def sex(self) -> str:
        return self.patient.sex

    @property
    def leeftijd(self) -> Optional[float]:
        return self.patient.leeftijd

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        result["patient"] = asdict(self.patient)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HolterMeasurements:
        """Create instance from dictionary."""
        patient_data = data.pop("patient", {})
        patient = PatientContext(**patient_data)
        return cls(patient=patient, **data)


@dataclass
class HolterMetrics:
    """Derived metrics and summary for Holter monitoring."""

    brady_flag: bool = False
    tachy_flag: bool = False
    afib_detected: bool = False
    significant_pauses: bool = False
    frequent_ves: bool = False
    frequent_sves: bool = False
    av_block_detected: bool = False
    summary_lines: List[str] = None

    def __post_init__(self):
        if self.summary_lines is None:
            self.summary_lines = []


def compute_holter_metrics(measurements: HolterMeasurements) -> HolterMetrics:
    """Derive convenience metrics for the Holter UI."""

    summary: List[str] = []
    brady_flag = False
    tachy_flag = False
    afib_detected = False
    significant_pauses = False
    frequent_ves = False
    frequent_sves = False
    av_block_detected = False

    # Recording duration
    if measurements.recording_duration_hours:
        summary.append(f"Registratieduur: {measurements.recording_duration_hours} uur")

    # Heart rate analysis
    if measurements.avg_hr is not None:
        summary.append(f"Gemiddelde hartfrequentie: {measurements.avg_hr} bpm")
    
    if measurements.min_hr is not None:
        brady_flag = measurements.min_hr < 40
        min_hr_text = f"Minimale hartfrequentie: {measurements.min_hr} bpm"
        if brady_flag:
            min_hr_text += " (bradycardie)"
        summary.append(min_hr_text)
    
    if measurements.max_hr is not None:
        tachy_flag = measurements.max_hr > 120
        max_hr_text = f"Maximale hartfrequentie: {measurements.max_hr} bpm"
        if tachy_flag:
            max_hr_text += " (tachycardie)"
        summary.append(max_hr_text)

    # Atrial fibrillation
    if measurements.afib_percentage is not None and measurements.afib_percentage > 0:
        afib_detected = True
        summary.append(f"Atriumfibrilleren: {measurements.afib_percentage}% van de tijd")

    # Pauses
    if measurements.pauses_count is not None and measurements.pauses_count > 0:
        significant_pauses = measurements.longest_pause_ms and measurements.longest_pause_ms > 2000
        pause_text = f"Pauzes: {measurements.pauses_count}"
        if measurements.longest_pause_ms:
            pause_text += f" (langste: {measurements.longest_pause_ms} ms)"
        if significant_pauses:
            pause_text += " - significant"
        summary.append(pause_text)

    # Ventricular ectopy
    if measurements.ves_count is not None:
        frequent_ves = measurements.ves_count > 1000
        ves_text = f"VES: {measurements.ves_count}"
        if frequent_ves:
            ves_text += " (frequent)"
        summary.append(ves_text)

    # Supraventricular ectopy
    if measurements.sves_count is not None:
        frequent_sves = measurements.sves_count > 1000
        sves_text = f"SVES: {measurements.sves_count}"
        if frequent_sves:
            sves_text += " (frequent)"
        summary.append(sves_text)

    # AV block
    if measurements.av_block_type:
        av_block_detected = True
        summary.append(f"AV-blok: {measurements.av_block_type}")

    return HolterMetrics(
        brady_flag=brady_flag,
        tachy_flag=tachy_flag,
        afib_detected=afib_detected,
        significant_pauses=significant_pauses,
        frequent_ves=frequent_ves,
        frequent_sves=frequent_sves,
        av_block_detected=av_block_detected,
        summary_lines=summary,
    )


def generate_holter_report(measurements: HolterMeasurements, metrics: HolterMetrics) -> str:
    """Generate a textual Holter monitoring report based on captured measurements."""

    lines: List[str] = []

    # Header
    if measurements.recording_date:
        lines.append(f"Holter-monitoring geregistreerd op {measurements.recording_date}.")
    else:
        lines.append("Holter-monitoring registratie.")

    if measurements.recording_duration_hours:
        lines.append(f"Registratieduur: {measurements.recording_duration_hours} uur.")

    # Heart rate
    hr_parts: List[str] = []
    if measurements.avg_hr is not None:
        hr_parts.append(f"gemiddelde hartfrequentie {measurements.avg_hr} bpm")
    if measurements.min_hr is not None:
        hr_parts.append(f"minimum {measurements.min_hr} bpm")
    if measurements.max_hr is not None:
        hr_parts.append(f"maximum {measurements.max_hr} bpm")
    
    if hr_parts:
        lines.append("Hartfrequentie: " + ", ".join(hr_parts) + ".")

    # Bradycardie/tachycardie interpretation
    if metrics.brady_flag:
        lines.append("Er werd bradycardie vastgesteld.")
    if metrics.tachy_flag:
        lines.append("Er werden episoden van tachycardie waargenomen.")

    # Rhythm analysis
    rhythm_findings: List[str] = []

    # Atrial fibrillation
    if metrics.afib_detected and measurements.afib_percentage is not None:
        if measurements.afib_percentage >= 50:
            rhythm_findings.append(
                f"Er werd permanent atriumfibrilleren vastgesteld ({measurements.afib_percentage}% van de tijd)."
            )
        elif measurements.afib_percentage >= 10:
            rhythm_findings.append(
                f"Er werden frequente episoden van atriumfibrilleren waargenomen ({measurements.afib_percentage}% van de tijd)."
            )
        else:
            rhythm_findings.append(
                f"Er werden incidentele episoden van atriumfibrilleren waargenomen ({measurements.afib_percentage}% van de tijd)."
            )

    # Pauses
    if measurements.pauses_count is not None and measurements.pauses_count > 0:
        pause_text = f"{measurements.pauses_count} pauze(s)"
        if measurements.longest_pause_ms:
            pause_text += f" met een maximale duur van {measurements.longest_pause_ms} ms"
        if metrics.significant_pauses:
            rhythm_findings.append(f"Er werden significante pauzes geregistreerd: {pause_text}.")
        else:
            rhythm_findings.append(f"Er werden {pause_text} geregistreerd.")

    # Ectopy
    ectopy_parts: List[str] = []
    if measurements.ves_count is not None and measurements.ves_count > 0:
        ves_descriptor = "frequente" if metrics.frequent_ves else ""
        ectopy_parts.append(f"{ves_descriptor} ventriculaire extrasystolen (VES: {measurements.ves_count})".strip())
    
    if measurements.sves_count is not None and measurements.sves_count > 0:
        sves_descriptor = "frequente" if metrics.frequent_sves else ""
        ectopy_parts.append(
            f"{sves_descriptor} supraventriculaire extrasystolen (SVES: {measurements.sves_count})".strip()
        )

    if ectopy_parts:
        rhythm_findings.append("Er werden " + " en ".join(ectopy_parts) + " waargenomen.")

    # AV block
    if metrics.av_block_detected and measurements.av_block_type:
        rhythm_findings.append(f"Er werd {measurements.av_block_type} vastgesteld.")

    # No significant findings fallback
    if not rhythm_findings:
        rhythm_findings.append("Geen significante ritmestoornissen waargenomen.")

    lines.extend(rhythm_findings)

    # Other findings
    if measurements.other_findings and measurements.other_findings.strip():
        lines.append(f"Overige bevindingen: {measurements.other_findings.strip()}.")

    # Conclusion
    lines.append("\nConclusie:")
    conclusions: List[str] = []

    if metrics.afib_detected:
        conclusions.append("- Atriumfibrilleren gedocumenteerd")
    if metrics.brady_flag:
        conclusions.append("- Bradycardie")
    if metrics.tachy_flag:
        conclusions.append("- Tachycardie")
    if metrics.significant_pauses:
        conclusions.append("- Significante pauzes")
    if metrics.frequent_ves:
        conclusions.append("- Frequente ventriculaire extrasystolen")
    if metrics.frequent_sves:
        conclusions.append("- Frequente supraventriculaire extrasystolen")
    if metrics.av_block_detected:
        conclusions.append(f"- {measurements.av_block_type}")

    if not conclusions:
        conclusions.append("- Geen afwijkingen geregistreerd tijdens Holter-monitoring")

    lines.extend(conclusions)

    return "\n".join(lines)
