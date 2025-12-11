"""Fietstest (bicycle stress test) domain helpers."""
from __future__ import annotations

from typing import List, Optional

from cardiac_report.calculations import get_vo2_reference_values, vo2_percentile_and_label
from cardiac_report.models import FietstestMeasurements, FietstestMetrics


def calculate_predicted_max_hr(age: Optional[float]) -> Optional[int]:
    """Return Tanaka-derived predicted max HR."""
    try:
        if age is None:
            return None
        return int(round(208 - 0.7 * float(age)))
    except Exception:
        return None


def calculate_vo2_from_watts(max_watt: Optional[float], weight: Optional[float]) -> Optional[float]:
    """Convert achieved wattage to estimated VO2 (ml·kg⁻¹·min⁻¹)."""
    try:
        if not max_watt or not weight or float(weight) <= 0:
            return None
        work_rate = float(max_watt) * 6.12  # kg·m·min⁻¹
        vo2 = 1.8 * work_rate / float(weight) + 7
        return round(vo2, 1)
    except Exception:
        return None


def compute_fietstest_metrics(params: FietstestMeasurements) -> FietstestMetrics:
    """Return derived values and summary lines for the fietsproef UI."""
    sex = params.sex
    age = params.leeftijd
    weight = params.weight
    max_watt = params.max_watt
    max_hr = params.max_hr

    predicted_max_hr = calculate_predicted_max_hr(age)
    pct_hr_display: Optional[float] = None
    if predicted_max_hr and max_hr and float(max_hr) > 0:
        try:
            pct_hr_display = round((float(max_hr) / float(predicted_max_hr)) * 100, 1)
        except Exception:
            pct_hr_display = None

    vo2_observed = calculate_vo2_from_watts(max_watt, weight)
    vo2_observed_text = f"Observed VO2: {vo2_observed} ml·kg⁻¹·min⁻¹" if vo2_observed is not None else ""

    pct_vs50 = None
    band = None
    band_text = None
    if vo2_observed is not None:
        pct_vs50, band, band_text = vo2_percentile_and_label(sex, age, vo2_observed)

    wpred = None
    wpred_pct = None
    try:
        ref = get_vo2_reference_values(sex, age)
        p50 = ref.get('p50') if ref else None
        if p50 is not None and weight and float(weight) > 0:
            work_rate_pred = float(weight) * (float(p50) - 7.0) / 1.8
            if work_rate_pred > 0:
                wpred = round(work_rate_pred / 6.12, 1)
                if wpred and max_watt and float(wpred) > 0 and float(max_watt) > 0:
                    wpred_pct = round((float(max_watt) / float(wpred)) * 100, 1)
    except Exception:
        wpred = None
        wpred_pct = None

    summary_lines: List[str] = []
    if predicted_max_hr:
        if pct_hr_display is not None:
            summary_lines.append(
                f"Max HR: {max_hr} bpm ({pct_hr_display}% of predicted {predicted_max_hr} bpm)"
            )
        elif max_hr is not None:
            summary_lines.append(f"Max HR: {max_hr} bpm (predicted {predicted_max_hr} bpm)")
    if vo2_observed is not None:
        if pct_vs50 is not None and band is not None and band_text is not None:
            summary_lines.append(
                f"{vo2_observed_text} — {pct_vs50}% vs 50e ({band}: {band_text})"
            )
        else:
            summary_lines.append(vo2_observed_text)
    if wpred is not None:
        if wpred_pct is not None:
            summary_lines.append(f"Wattage: {max_watt} W ({wpred_pct}% of predicted {wpred} W)")
        else:
            summary_lines.append(f"Predicted wattage: {wpred} W")

    return FietstestMetrics(
        predicted_max_hr=predicted_max_hr,
        pct_hr_display=pct_hr_display,
        vo2_observed=vo2_observed,
        vo2_observed_text=vo2_observed_text,
        vo2_percentile_pct=pct_vs50,
        vo2_band=band,
        vo2_band_text=band_text,
        wpred=wpred,
        wpred_pct=wpred_pct,
        summary_lines=summary_lines,
    )


def generate_fietstest_report(params: FietstestMeasurements, metrics: FietstestMetrics) -> str:
    """Create the textual report for the bicycle stress test."""
    start_watt = params.start_watt or 0
    increment_watt = params.increment_watt or 0
    max_watt = params.max_watt or 0
    duration_at_max = params.duration_at_max or 0
    max_hr = params.max_hr or 0
    weight = params.weight
    bp_evolutie = params.bp_evolutie or ""
    ritme = params.ritme or ""
    effort_type = params.effort_type or ""
    stop_criterium = params.stop_criterium or ""
    ecg_changes = params.ecg_changes or ""
    conclusion = params.conclusion or ""

    predicted_max_hr = metrics.predicted_max_hr
    pct_hr_display = metrics.pct_hr_display
    vo2_value = metrics.vo2_observed
    pct_vs50 = metrics.vo2_percentile_pct
    band = metrics.vo2_band
    band_text = metrics.vo2_band_text

    max_watt_text = (
        f"Maximale belasting tot {max_watt} Watt gedurende {duration_at_max} seconden."
        if max_watt and max_watt > 0
        else "Maximale belasting niet bereikt of niet gerapporteerd."
    )

    pct_text = ""
    if predicted_max_hr and max_hr and max_hr > 0:
        try:
            pct_val = pct_hr_display if pct_hr_display is not None else None
            if pct_val is None:
                pct_val = round((float(max_hr) / float(predicted_max_hr)) * 100, 1)
            pct_text = f" ({pct_val}% predicted)"
        except Exception:
            pct_text = ""

    vo2_text = ""
    if vo2_value is None:
        vo2_value = calculate_vo2_from_watts(max_watt, weight)
    if vo2_value is not None:
        vo2_text = f"VO2 (ml·kg⁻¹·min⁻¹): {vo2_value}"

    report: List[str] = []
    report.append(f"Start aan {start_watt} W. Opdrijven van de belasting met {increment_watt} W om de minuut.")
    report.append(max_watt_text)
    report.append(f"Maximale hartslag bedraagt {max_hr}/min{pct_text}")
    report.append(f"{bp_evolutie}. {ritme}.")
    report.append(f"{effort_type}. Het criterium voor staken betreft {stop_criterium}.")
    report.append("")
    report.append(f"Het ECG vertoont {ecg_changes} tijdens inspanning of recuperatie.")
    report.append("")
    report.append(f"Conclusie: {conclusion}.")

    if vo2_value is not None:
        if pct_vs50 is None or band is None or band_text is None:
            vo2_line = vo2_text
        else:
            vo2_line = (
                f"VO2: {vo2_value} ml·kg⁻¹·min⁻¹ ({pct_vs50}% predicted) — Percentiel: {band} ({band_text})"
            )
        report.insert(3, vo2_line)

    return "\n".join(report)


def summarize_fietstest_for_brief(params: FietstestMeasurements, metrics: FietstestMetrics) -> str:
    """Return a compact fietsproef summary for the consult letter."""

    parts: List[str] = []
    if params.max_watt:
        parts.append(f"Max belasting {params.max_watt:.0f} W")
    if params.max_hr:
        if metrics.pct_hr_display is not None:
            parts.append(f"HF {params.max_hr:.0f} bpm ({metrics.pct_hr_display:.0f}% voorspeld)")
        else:
            parts.append(f"HF {params.max_hr:.0f} bpm")
    if metrics.vo2_observed is not None:
        if metrics.vo2_percentile_pct is not None:
            parts.append(
                f"VO₂ {metrics.vo2_observed:.1f} ml·kg⁻¹·min⁻¹ ({metrics.vo2_percentile_pct:.0f}% vs p50)"
            )
        else:
            parts.append(f"VO₂ {metrics.vo2_observed:.1f} ml·kg⁻¹·min⁻¹")
    if params.conclusion:
        parts.append(params.conclusion.strip())

    return "; ".join(part for part in parts if part) or "Geen fietsproefgegevens beschikbaar."
