"""ECG metrics calculation and reporting helpers."""
from __future__ import annotations

from typing import List

from cardiac_report.models import ECGMeasurements, ECGMetrics


def compute_ecg_metrics(measurements: ECGMeasurements) -> ECGMetrics:
    """Derive convenience metrics for the ECG UI."""

    summary: List[str] = []

    qtcf = measurements.qtc_interval_ms
    if qtcf is None and measurements.qt_interval_ms and measurements.vent_rate:
        try:
            rr = 60.0 / float(measurements.vent_rate)
            qtcf = round(float(measurements.qt_interval_ms) / rr**0.5, 1)
        except Exception:
            qtcf = None

    tachy = bool(measurements.vent_rate and measurements.vent_rate > 100)
    brady = bool(measurements.vent_rate and measurements.vent_rate < 50)

    axis_deviation = None
    if measurements.qrs_axis_deg is not None:
        axis_val = measurements.qrs_axis_deg
        if axis_val < -30:
            axis_deviation = "Linkerasdeviatie"
        elif axis_val > 90:
            axis_deviation = "Rechterasdeviatie"
        else:
            axis_deviation = "Normale QRS-as"

    if measurements.rhythm_summary:
        summary.append(f"Ritme: {measurements.rhythm_summary}")
    if measurements.vent_rate is not None:
        summary.append(f"Frequentie: {measurements.vent_rate:.0f} bpm")
    if measurements.pr_interval_ms is not None:
        summary.append(f"PR {measurements.pr_interval_ms:.0f} ms")
    if measurements.qrs_duration_ms is not None:
        summary.append(f"QRS {measurements.qrs_duration_ms:.0f} ms")
    if measurements.qt_interval_ms is not None:
        qt_line = f"QT {measurements.qt_interval_ms:.0f} ms"
        if qtcf is not None:
            qt_line += f" (QTc {qtcf:.0f} ms)"
        summary.append(qt_line)
    if axis_deviation:
        summary.append(axis_deviation)

    return ECGMetrics(
        qtcf_ms=qtcf,
        tachy_flag=tachy,
        brady_flag=brady,
        axis_deviation=axis_deviation,
        summary_lines=summary,
    )


def generate_ecg_report(measurements: ECGMeasurements, metrics: ECGMetrics) -> str:
    """Generate a textual ECG report based on captured measurements."""

    lines: List[str] = []
    if measurements.recorded_at:
        lines.append(f"ECG geregistreerd op {measurements.recorded_at}.")
    else:
        lines.append("ECG registratie.")

    if measurements.rhythm_summary:
        lines.append(f"Ritme: {measurements.rhythm_summary}.")

    interval_parts: List[str] = []
    if measurements.vent_rate is not None:
        interval_parts.append(f"Frequentie {measurements.vent_rate:.0f} bpm")
    if measurements.pr_interval_ms is not None:
        interval_parts.append(f"PR {measurements.pr_interval_ms:.0f} ms")
    if measurements.qrs_duration_ms is not None:
        interval_parts.append(f"QRS {measurements.qrs_duration_ms:.0f} ms")
    if measurements.qt_interval_ms is not None:
        qt_line = f"QT {measurements.qt_interval_ms:.0f} ms"
        if metrics.qtcf_ms is not None:
            qt_line += f" (QTc {metrics.qtcf_ms:.0f} ms)"
        interval_parts.append(qt_line)
    if interval_parts:
        lines.append(", ".join(interval_parts) + ".")

    axis_parts: List[str] = []
    if measurements.p_axis_deg is not None:
        axis_parts.append(f"P-as {measurements.p_axis_deg:.0f}°")
    if measurements.qrs_axis_deg is not None:
        axis_parts.append(f"QRS-as {measurements.qrs_axis_deg:.0f}°")
    if measurements.t_axis_deg is not None:
        axis_parts.append(f"T-as {measurements.t_axis_deg:.0f}°")
    if axis_parts:
        lines.append(", ".join(axis_parts) + ".")

    if metrics.axis_deviation and metrics.axis_deviation not in lines[-1]:  # avoid duplicate sentences
        lines.append(metrics.axis_deviation + ".")

    if measurements.auto_report_text:
        lines.append("")
        lines.append("Automatische protocolering:")
        lines.append(measurements.auto_report_text.strip())

    if metrics.tachy_flag:
        lines.append("Frequentie in tachycard bereik (>100 bpm).")
    if metrics.brady_flag:
        lines.append("Frequentie in bradycard bereik (<50 bpm).")

    return "\n".join(lines)


def summarize_ecg_for_brief(measurements: ECGMeasurements, metrics: ECGMetrics) -> str:
    """Return a short ECG summary for inclusion in the consult brief."""

    parts: List[str] = []
    if measurements.rhythm_summary:
        parts.append(measurements.rhythm_summary.strip())
    if measurements.vent_rate is not None:
        parts.append(f"HF {measurements.vent_rate:.0f} bpm")
    if measurements.qrs_duration_ms is not None:
        parts.append(f"QRS {measurements.qrs_duration_ms:.0f} ms")
    if metrics.qtcf_ms is not None:
        parts.append(f"QTc {metrics.qtcf_ms:.0f} ms")
    elif measurements.qt_interval_ms is not None:
        parts.append(f"QT {measurements.qt_interval_ms:.0f} ms")
    if metrics.axis_deviation:
        parts.append(metrics.axis_deviation)

    text = "; ".join(part for part in parts if part)
    if measurements.recorded_at:
        prefix = f"ECG dd. {measurements.recorded_at}: "
    else:
        prefix = "ECG: " if text else ""
    summary = (prefix + text).strip()
    return summary or "Geen ECG-gegevens beschikbaar."
