"""CIED follow-up reporting helpers."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from cardiac_report.models import CIEDReportInput, LeadMeasurements, PatientContext


def _join_nl(items: List[str]) -> str:
    items = [str(i) for i in items if i and str(i).strip() != ""]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} en {items[1]}"
    return f"{', '.join(items[:-1])} en {items[-1]}"


def _parse_pct(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        txt = str(value).strip()
        if txt == "":
            return None
        return int(float(txt))
    except Exception:
        return None


def _parse_int_nullable(value: Any) -> Optional[int]:
    try:
        if value is None:
            return None
        txt = str(value).strip()
        if txt == "":
            return None
        return int(float(txt))
    except Exception:
        return None


def _have_values(*fields: Any) -> bool:
    try:
        for field in fields:
            if field is not None and str(field).strip() != "":
                return True
    except Exception:
        return False
    return False


def _clean_str(value: Any, default: str = "n.v.t.") -> str:
    try:
        if value is None:
            return default
        txt = str(value).strip()
        return txt if txt else default
    except Exception:
        return default


def _optional_str(value: Any) -> Optional[str]:
    try:
        if value is None:
            return None
        txt = str(value).strip()
        return txt if txt else None
    except Exception:
        return None


def _coerce_patient(value: Any) -> Optional[PatientContext]:
    if isinstance(value, PatientContext):
        return value
    if isinstance(value, dict):
        try:
            sex = value.get("sex")
            if not sex:
                return None
            return PatientContext(
                sex=sex,
                patient_id=value.get("patient_id"),
                full_name=value.get("full_name"),
                date_of_birth=value.get("date_of_birth"),
                leeftijd=value.get("leeftijd"),
                bsa=value.get("bsa"),
                weight=value.get("weight"),
                length=value.get("length"),
            )
        except Exception:
            return None
    return None


def _coerce_lead_fields(data: Any) -> LeadMeasurements:
    if isinstance(data, LeadMeasurements):
        return data
    if isinstance(data, dict):
        return LeadMeasurements(
            sensing=data.get("sensing"),
            impedance=data.get("impedance"),
            threshold_v=data.get("threshold_v"),
            threshold_ms=data.get("threshold_ms"),
            polarity=data.get("polarity"),
            stable=data.get("stable"),
            location=data.get("location"),
        )
    return LeadMeasurements()


def _coerce_cied_input(raw: Union[CIEDReportInput, Dict[str, Any]]) -> CIEDReportInput:
    if isinstance(raw, CIEDReportInput):
        return raw
    if not isinstance(raw, dict):
        raise TypeError("CIED context must be a dataclass or dict")

    return CIEDReportInput(
        patient=_coerce_patient(raw.get("patient")),
        device_type=raw.get("device_type"),
        device_brand=raw.get("device_brand"),
        programming_mode=raw.get("programming_mode"),
        lower_rate=raw.get("lower_rate"),
        upper_tracking=raw.get("upper_tracking"),
        indication_text=raw.get("indication_text"),
        lead_ra=bool(raw.get("lead_ra")),
        lead_rv=bool(raw.get("lead_rv")),
        lead_lv=bool(raw.get("lead_lv")),
        other_leads=raw.get("other_leads"),
        sensing_ok=bool(raw.get("sensing_ok", True)),
        pacing_ok=bool(raw.get("pacing_ok", True)),
        impedance_ok=bool(raw.get("impedance_ok", True)),
        egm_events=raw.get("egm_events"),
        atrial_pacing_pct=raw.get("atrial_pacing_pct"),
        ventricular_pacing_pct=raw.get("ventricular_pacing_pct"),
        lv_pacing_pct=raw.get("lv_pacing_pct"),
        settings_changed=bool(raw.get("settings_changed", False)),
        patient_dependent=bool(raw.get("patient_dependent", False)),
        battery_status=raw.get("battery_status"),
        suggested_sensed_av=raw.get("suggested_sensed_av"),
        suggested_paced_av=raw.get("suggested_paced_av"),
        sensed_av_delay=raw.get("sensed_av_delay"),
        paced_av_delay=raw.get("paced_av_delay"),
        atrial_fields=_coerce_lead_fields(raw.get("atrial_fields")),
        vent_fields=_coerce_lead_fields(raw.get("vent_fields")),
        lv_fields=_coerce_lead_fields(raw.get("lv_fields")),
    )


def generate_cied_report(ctx: Union[CIEDReportInput, Dict[str, Any]]) -> str:
    """Return the textual report for a CIED follow-up."""
    ctx = _coerce_cied_input(ctx)

    device_type = ctx.device_type or "apparaat"
    device_brand = ctx.device_brand or ""
    programming_mode = ctx.programming_mode or ""
    lower_rate = ctx.lower_rate
    upper_tracking = ctx.upper_tracking
    indication_text = ctx.indication_text or ""
    lead_ra = ctx.lead_ra
    lead_rv = ctx.lead_rv
    lead_lv = ctx.lead_lv
    sensing_ok = ctx.sensing_ok
    pacing_ok = ctx.pacing_ok
    impedance_ok = ctx.impedance_ok
    egm_events = ctx.egm_events or "Geen events"
    atrial_pacing_pct = ctx.atrial_pacing_pct
    ventricular_pacing_pct = ctx.ventricular_pacing_pct
    lv_pacing_pct = ctx.lv_pacing_pct
    settings_changed = ctx.settings_changed
    patient_dependent = ctx.patient_dependent
    battery_status = ctx.battery_status or ""
    suggested_sensed_av = ctx.suggested_sensed_av
    suggested_paced_av = ctx.suggested_paced_av
    sensed_av_delay = ctx.sensed_av_delay
    paced_av_delay = ctx.paced_av_delay

    atrial_fields = ctx.atrial_fields or LeadMeasurements()
    vent_fields = ctx.vent_fields or LeadMeasurements()
    lv_fields = ctx.lv_fields or LeadMeasurements()

    try:
        prog_str = f"{programming_mode}-{int(lower_rate)}/{int(upper_tracking)}"
    except Exception:
        prog_str = ""

    indic = indication_text if indication_text else ""
    first_sentence = f"Correcte werking van {device_type} ({device_brand})"
    if prog_str:
        first_sentence += f" modus {prog_str}"
    if indic:
        first_sentence += f" ter behandeling van {indic}."
    else:
        first_sentence += "."

    meet_lines: List[str] = []

    if lead_ra and _have_values(
        atrial_fields.sensing,
        atrial_fields.threshold_v,
        atrial_fields.threshold_ms,
        atrial_fields.impedance,
    ):
        a_sens = _clean_str(atrial_fields.sensing)
        a_thr_v = _clean_str(atrial_fields.threshold_v)
        a_thr_ms = _clean_str(atrial_fields.threshold_ms)
        a_imp = _clean_str(atrial_fields.impedance)
        a_pol = atrial_fields.polarity or "n.v.t."
        a_stab = "stabiel" if atrial_fields.stable is not False else "onstabiel"
        a_loc = _optional_str(atrial_fields.location)
        loc_txt = f" Locatie: {a_loc}." if a_loc else ""
        meet_lines.append(
            f"Atrium: sensing {a_sens} mV, drempel {a_thr_v} V @ {a_thr_ms} ms ({a_pol}), impedantie {a_imp} Ω, {a_stab}.{loc_txt}"
        )

    if lead_rv and _have_values(
        vent_fields.sensing,
        vent_fields.threshold_v,
        vent_fields.threshold_ms,
        vent_fields.impedance,
    ):
        v_sens = _clean_str(vent_fields.sensing)
        v_thr_v = _clean_str(vent_fields.threshold_v)
        v_thr_ms = _clean_str(vent_fields.threshold_ms)
        v_imp = _clean_str(vent_fields.impedance)
        v_pol = vent_fields.polarity or "n.v.t."
        v_stab = "stabiel" if vent_fields.stable is not False else "onstabiel"
        v_loc = _optional_str(vent_fields.location)
        loc_txt = f" Locatie: {v_loc}." if v_loc else ""
        meet_lines.append(
            f"Ventrikel: sensing {v_sens} mV, drempel {v_thr_v} V @ {v_thr_ms} ms ({v_pol}), impedantie {v_imp} Ω, {v_stab}.{loc_txt}"
        )

    if lead_lv and _have_values(
        lv_fields.sensing,
        lv_fields.threshold_v,
        lv_fields.threshold_ms,
        lv_fields.impedance,
    ):
        lv_sens = _clean_str(lv_fields.sensing)
        lv_thr_v = _clean_str(lv_fields.threshold_v)
        lv_thr_ms = _clean_str(lv_fields.threshold_ms)
        lv_imp = _clean_str(lv_fields.impedance)
        lv_pol = lv_fields.polarity or "n.v.t."
        lv_stab = "stabiel" if lv_fields.stable is not False else "onstabiel"
        lv_loc = _optional_str(lv_fields.location)
        loc_txt = f" Locatie: {lv_loc}." if lv_loc else ""
        meet_lines.append(
            f"LV: sensing {lv_sens} mV, drempel {lv_thr_v} V @ {lv_thr_ms} ms ({lv_pol}), impedantie {lv_imp} Ω, {lv_stab}.{loc_txt}"
        )

    ap = _parse_pct(atrial_pacing_pct)
    vp = _parse_pct(ventricular_pacing_pct)
    lp = _parse_pct(lv_pacing_pct)
    pacing_parts: List[str] = []
    if ap is not None:
        pacing_parts.append(f"Atrium {ap}%")
    if vp is not None:
        pacing_parts.append(f"Ventrikel {vp}%")
    if lp is not None:
        pacing_parts.append(f"LV {lp}%")
    if pacing_parts:
        meet_lines.append("Pacing percentages: " + ", ".join(pacing_parts) + ".")

    ss_val = _parse_int_nullable(sensed_av_delay)
    if ss_val is not None:
        if suggested_sensed_av is not None:
            meet_lines.append(
                f"Sensed AV delay: {ss_val} ms (Rate-adaptive AV delay at peak UTR: {suggested_sensed_av} ms)."
            )
        else:
            meet_lines.append(f"Sensed AV delay: {ss_val} ms.")

    ps_val = _parse_int_nullable(paced_av_delay)
    if ps_val is not None:
        if suggested_paced_av is not None:
            meet_lines.append(
                f"Paced AV delay: {ps_val} ms (Rate-adaptive AV delay at peak UTR: {suggested_paced_av} ms)."
            )
        else:
            meet_lines.append(f"Paced AV delay: {ps_val} ms.")

    conclusion_parts: List[str] = []
    conclusion_parts.append(first_sentence)

    sp_parts: List[str] = []
    if sensing_ok:
        sp_parts.append("sensing")
    else:
        sp_parts.append("sensing: afwijkend")
    if pacing_ok:
        sp_parts.append("pacing")
    else:
        sp_parts.append("pacing: afwijkend")
    if impedance_ok:
        sp_parts.append("impedantie")
    else:
        sp_parts.append("impedantie: afwijkend")
    conclusion_parts.append("Goede en stabiele waardes voor " + _join_nl(sp_parts) + ".")

    if egm_events and egm_events != "Geen events":
        conclusion_parts.append(f"De EGM uitlezing toont: {egm_events}.")
    else:
        conclusion_parts.append("De EGM uitlezing toont geen events.")

    if settings_changed:
        conclusion_parts.append("Instellingen gewijzigd tijdens follow-up.")
    else:
        conclusion_parts.append("Instellingen ongewijzigd.")

    if patient_dependent:
        conclusion_parts.append("Patiënt is pacemakerafhankelijk.")
    else:
        conclusion_parts.append("Patiënt is niet afhankelijk.")

    batt_txt = battery_status.strip() if battery_status and battery_status.strip() != "" else "Batterijstatus niet gerapporteerd"
    conclusion_parts.append(f"Batterij: {batt_txt}.")

    final_parts: List[str] = []
    if meet_lines:
        final_parts.append("Meetwaarden:")
        final_parts.extend(meet_lines)
        final_parts.append("")
    final_parts.append("Conclusie:")
    final_parts.extend(conclusion_parts)

    return "\n".join(final_parts)
