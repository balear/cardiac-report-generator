import streamlit as st
import math
import json
import datetime
import os
from typing import Any, Dict, List, Optional, Tuple
import streamlit.components.v1 as components
import requests
from streamlit_option_menu import option_menu

from cardiac_report.calculations import (
    bsa_mosteller,
    classify_ivsd,
    classify_lavi,
    classify_lvef,
    lvef_to_systolic_option,
    compute_lv_mass_g,
    compute_rwt,
    lv_mass_index_severity,
    determine_lv_geometry,
    classify_lvidd,
    classify_tapse,
    vo2_percentile_and_label,
    get_vo2_reference_values,
    mitral_regurgitation_severity,
)
from cardiac_report.formatting import color_status_html
from cardiac_report.reports import (
    compose_brief_letter,
    generate_echo_report,
    generate_guideline_recommendations,
    summarize_echo_for_brief,
)
from cardiac_report.models import (
    CIEDReportInput,
    EchoReportInput,
    FietstestMeasurements,
    FietstestMetrics,
    LeadMeasurements,
    PatientContext,
    StudySnapshot,
    ECGMeasurements,
    HolterMeasurements,
    HolterMetrics,
)
from cardiac_report.fietstest import (
    compute_fietstest_metrics,
    generate_fietstest_report,
    summarize_fietstest_for_brief,
)
from cardiac_report.cied import generate_cied_report
from cardiac_report.ecg import (
    compute_ecg_metrics,
    generate_ecg_report,
    summarize_ecg_for_brief,
)
from cardiac_report.holter import (
    compute_holter_metrics,
    generate_holter_report,
)
from cardiac_report.pdf_ingest.fietstest_pdf import parse_fietstest_pdf
from cardiac_report.pdf_ingest.ecg_pdf import parse_ecg_pdf
from cardiac_report.pdf_ingest.utils import PDF_DEPENDENCY_MESSAGE, pdf_dependency_available


def safe_rerun() -> None:
    """Trigger a Streamlit rerun in a backwards-compatible way.

    Prefer `st.experimental_rerun()` when present; otherwise stop the script
    so the next user interaction triggers a rerun.
    """
    try:
        st.experimental_rerun()
        return
    except Exception:
        # Older/newer Streamlit may not expose experimental_rerun.
        # Avoid calling `st.stop()` which halts rendering and makes
        # the page appear to disappear. Instead, silently return
        # so the current run continues and any session-state flags
        # (e.g. `generate_now`) are handled later in the script.
        return

API_BASE = os.getenv("BACKEND_URL", "").rstrip("/")

PATIENT_SIDEBAR_DEFAULTS = {
    "patient_identifier": "",
    "patient_name": "",
    "patient_dob": "",
    "patient_sex": "Man",
    "patient_length": 175,
    "patient_weight": 75,
    "patient_age": 50,
}

_PENDING_PREFILL_KEY = "__pending_patient_prefill__"
BACKEND_ENABLED = bool(API_BASE)


def check_backend_health() -> bool:
    if not BACKEND_ENABLED:
        return False
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=3)
        return resp.status_code == 200 and resp.json().get("status") == "ok"
    except Exception:
        return False


def ensure_patient_sidebar_defaults() -> None:
    """Seed session_state so we can overwrite sidebar fields programmatically."""

    for key, default in PATIENT_SIDEBAR_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def prefill_patient_sidebar(ctx: Optional[PatientContext]) -> None:
    """Queue parsed patient values; applied on next rerun before widgets render."""

    if ctx is None:
        return

    payload = {
        "patient_identifier": ctx.patient_id,
        "patient_name": ctx.full_name,
        "patient_dob": ctx.date_of_birth,
        "patient_sex": ctx.sex,
        "patient_length": ctx.length,
        "patient_weight": ctx.weight,
        "patient_age": ctx.leeftijd,
    }
    # Skip when sidebar already matches target values
    matches = True
    for key, value in payload.items():
        existing = st.session_state.get(key)
        if value is None:
            continue
        if existing != value:
            matches = False
            break
    if matches:
        return

    st.session_state[_PENDING_PREFILL_KEY] = payload
    safe_rerun()


# Show backend status in sidebar
ensure_patient_sidebar_defaults()
if BACKEND_ENABLED:
    healthy = check_backend_health()
    if healthy:
        st.sidebar.success("Backend: verbonden")
    else:
        st.sidebar.warning("Backend: niet bereikbaar")
else:
    st.sidebar.info("Backend: uitgeschakeld (lokale modus)")


def apply_pending_patient_prefill() -> None:
    payload = st.session_state.pop(_PENDING_PREFILL_KEY, None)
    if not payload:
        return
    for key, value in payload.items():
        if value is None:
            continue
        st.session_state[key] = value


def _patient_from_payload(payload: dict) -> PatientContext:
    return PatientContext(
        sex=payload.get("sex", "Man"),
        patient_id=payload.get("patient_id") or payload.get("his_patient_id"),
        full_name=payload.get("full_name") or payload.get("name"),
        date_of_birth=payload.get("date_of_birth") or payload.get("dob"),
        leeftijd=payload.get("leeftijd") or payload.get("patient_age"),
        bsa=payload.get("bsa"),
        weight=payload.get("weight"),
        length=payload.get("length"),
    )


def _authorized_headers() -> Dict[str, str]:
    token = os.getenv("BACKEND_API_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _post_pdf_to_backend(endpoint: str, file_bytes: bytes, filename: str) -> Optional[dict]:
    if not BACKEND_ENABLED:
        return None
    url = f"{API_BASE}{endpoint}"
    try:
        resp = requests.post(
            url,
            files={"file": (filename, file_bytes, "application/pdf")},
            headers=_authorized_headers(),
            timeout=30,
        )
        if resp.status_code != 200:
            st.warning(f"Backend gaf status {resp.status_code}: {resp.text}")
            return None
        return resp.json()
    except Exception as exc:
        st.warning(f"Backend niet bereikbaar: {exc}")
        return None


def _post_snapshot_to_backend(study_type: str, snapshot: StudySnapshot) -> Optional[int]:
    if not BACKEND_ENABLED:
        return None
    url = f"{API_BASE}/api/studies/{study_type}/from-snapshot"
    body = {
        "patient": snapshot.to_dict().get("patient", {}),
        "study_type": study_type,
        "study_datetime": None,
        "source": "manual",
        "payload": snapshot.to_dict(),
    }
    try:
        resp = requests.post(url, json=body, headers=_authorized_headers(), timeout=20)
        if resp.status_code != 200:
            st.warning(f"Backend save faalde ({resp.status_code}): {resp.text}")
            return None
        data = resp.json()
        return data.get("id")
    except Exception as exc:
        st.warning(f"Backend save error: {exc}")
        return None


def _fetch_patient_studies(patient_id: str) -> Optional[List[dict]]:
    if not BACKEND_ENABLED or not patient_id:
        return None
    url = f"{API_BASE}/api/patients/{patient_id}/studies"
    try:
        resp = requests.get(url, headers=_authorized_headers(), timeout=15)
        if resp.status_code != 200:
            st.warning(f"Backend gaf status {resp.status_code} bij ophalen studies: {resp.text}")
            return None
        return resp.json()
    except Exception as exc:
        st.warning(f"Kon patientstudies niet ophalen: {exc}")
        return None


def _remember_brief_section(
    key: str,
    text: str,
    patient_id: Optional[str],
    performed_on: Optional[str] = None,
) -> None:
    if not text:
        return
    bucket = st.session_state.setdefault("__brief_sections__", {})
    pid = patient_id or "__default__"
    patient_bucket = bucket.setdefault(pid, {})
    stamp = _timestamp_from_label(performed_on) or datetime.datetime.now().timestamp()
    patient_bucket[key] = {
        "text": text,
        "performed_on": performed_on,
        "_stamp": stamp,
    }


def _timestamp_from_label(label: Optional[str]) -> Optional[float]:
    if not label:
        return None
    try:
        dt_obj = datetime.datetime.fromisoformat(label)
    except ValueError:
        try:
            dt_obj = datetime.datetime.strptime(label, "%d-%m-%Y")
        except ValueError:
            return None
    return dt_obj.timestamp()


def _parse_iso_datetime(value: Optional[str]) -> Optional[datetime.datetime]:
    if not value:
        return None
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_iso_date(value: Optional[str]) -> Optional[str]:
    dt_obj = _parse_iso_datetime(value)
    if not dt_obj:
        return None
    return dt_obj.strftime("%d-%m-%Y")


def _study_order_stamp(study: Dict[str, Any]) -> float:
    dt_str = study.get("study_datetime")
    dt_obj = _parse_iso_datetime(dt_str)
    if dt_obj:
        return dt_obj.timestamp()
    try:
        return float(study.get("id", 0))
    except Exception:
        return 0.0


def _load_brief_sections(patient: PatientContext) -> Dict[str, Dict[str, Optional[str]]]:
    pid = (patient.patient_id or "__default__") if patient else "__default__"
    sections: Dict[str, Dict[str, Optional[str]]] = {}
    stored = st.session_state.get("__brief_sections__", {}).get(pid, {})
    for key, value in stored.items():
        sections[key] = dict(value)

    if BACKEND_ENABLED and patient and patient.patient_id:
        studies = _fetch_patient_studies(patient.patient_id) or []
        for study in studies:
            payload = study.get("payload") or {}
            report_texts = payload.get("report_texts") or {}
            stamp = _study_order_stamp(study)
            performed = _format_iso_date(study.get("study_datetime"))
            for key, text in report_texts.items():
                if not text:
                    continue
                existing_stamp = sections.get(key, {}).get("_stamp", -1)
                if stamp <= existing_stamp:
                    continue
                sections[key] = {
                    "text": text,
                    "performed_on": performed,
                    "_stamp": stamp,
                }

    for meta in sections.values():
        meta.pop("_stamp", None)
        meta.setdefault("performed_on", None)
    return sections


def show_report_actions(report_text: str, file_name: str = "echo_report.txt"):
    """Display report, offer download and copy-to-clipboard."""
    st.text_area("Verslag (kopieer en plak)", value=report_text, height=320)
    st.download_button("Download als TXT", report_text, file_name=file_name, mime="text/plain")
    # copy to clipboard button via simple JS
    escaped = json.dumps(report_text)
    html = f"""
    <button onclick='navigator.clipboard.writeText({escaped})'>Kopieer verslag naar klembord</button>
    """
    components.html(html, height=40)


def show_snapshot_download(label: str, snapshot: StudySnapshot, filename: str):
    """Offer a JSON snapshot download when payload contains data."""
    try:
        data = snapshot.to_dict()
    except Exception:
        data = {}
    if not data:
        return
    json_payload = json.dumps(data, ensure_ascii=False, indent=2)
    st.download_button(label, json_payload, file_name=filename, mime="application/json")


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Echo / Rapport Generator", layout="wide")
ensure_patient_sidebar_defaults()
apply_pending_patient_prefill()

st.title("Dr. A. Ballet Ultimate Cardiac Rapport Generator")

with st.sidebar:
    st.header("Patiëntgegevens")
    patient_identifier = st.text_input(
        "Patiënt ID",
        key="patient_identifier",
        placeholder="bv. HIS-nummer",
    )
    
    # Auto-complete patient data when ID is entered
    if patient_identifier and patient_identifier.strip() and BACKEND_ENABLED:
        if st.button("🔍 Zoek bestaande patiëntgegevens"):
            studies = _fetch_patient_studies(patient_identifier.strip())
            if studies and len(studies) > 0:
                # Get most recent study to extract patient demographics
                latest_study = sorted(studies, key=_study_order_stamp, reverse=True)[0]
                payload = latest_study.get("payload", {})
                if payload:
                    patient_data = payload.get("patient", {})
                    if patient_data:
                        # Prefill sidebar with existing patient data
                        if patient_data.get("full_name"):
                            st.session_state["patient_name"] = patient_data.get("full_name")
                        if patient_data.get("date_of_birth"):
                            st.session_state["patient_dob"] = patient_data.get("date_of_birth")
                        if patient_data.get("sex"):
                            st.session_state["patient_sex"] = patient_data.get("sex")
                        if patient_data.get("length"):
                            st.session_state["patient_length"] = int(patient_data.get("length"))
                        if patient_data.get("weight"):
                            st.session_state["patient_weight"] = int(patient_data.get("weight"))
                        if patient_data.get("leeftijd"):
                            st.session_state["patient_age"] = int(patient_data.get("leeftijd"))
                        st.success(f"✓ Patiëntgegevens geladen ({len(studies)} studies gevonden)")
                        safe_rerun()
                    else:
                        st.info("Geen opgeslagen patiëntgegevens gevonden")
            else:
                st.info("Geen studies gevonden voor dit patiënt-ID")
    
    patient_name = st.text_input("Naam patiënt", key="patient_name")
    dob_text = st.text_input(
        "Geboortedatum (dd-mm-jjjj)",
        key="patient_dob",
        placeholder="01-01-1970",
    )
    sex = st.selectbox(
        "Geslacht",
        ["Man", "Vrouw"],
        key="patient_sex",
    )
    length = st.number_input(
        "Lengte (cm)",
        min_value=100,
        max_value=220,
        value=int(st.session_state.get("patient_length", 175)),
        key="patient_length",
    )
    weight = st.number_input(
        "Gewicht (kg)",
        min_value=30,
        max_value=250,
        value=int(st.session_state.get("patient_weight", 75)),
        key="patient_weight",
    )
    leeftijd = st.number_input(
        "Leeftijd (jaar)",
        min_value=0,
        max_value=120,
        value=int(st.session_state.get("patient_age", 50)),
        key="patient_age",
    )
    bsa = bsa_mosteller(length, weight)
    st.markdown(f"**BSA (Mosteller):** {bsa:.2f} m²")
    
    st.markdown("---")
    # Apply pending module selection (set by reset) before instantiating the widget
    pending_module = st.session_state.pop("_pending_selected_module", None)
    if pending_module is not None:
        st.session_state["selected_module"] = pending_module

    # Module navigation with option_menu
    module = option_menu(
        menu_title="Module",
        options=["Echo", "Fietstest", "ECG", "Holter", "CIED follow-up", "Brief"],
        icons=["heart-pulse", "bicycle", "activity", "clock-history", "cpu", "envelope"],
        menu_icon="grid",
        default_index=["Echo", "Fietstest", "ECG", "Holter", "CIED follow-up", "Brief"].index(
            st.session_state.get("selected_module", "Echo")
        ) if st.session_state.get("selected_module", "Echo") in ["Echo", "Fietstest", "ECG", "Holter", "CIED follow-up", "Brief"] else 0,
        key="selected_module",
        styles={
            # lighter container to match the rest of the sidebar
            "container": {"padding": "6px", "background-color": "#f7f8fa", "border-radius": "6px"},
            # subdued icon color
            "icon": {"color": "#6b6f76", "font-size": "18px"},
            # normal link styling to blend with light container
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "4px", "color": "#222", "background-color": "transparent", "--hover-color": "#eef0f3"},
            # Pastel Sky selected: soft & airy
            "nav-link-selected": {"background-color": "#9ed9fb", "color": "#042f4a", "border-radius": "6px"},
            # icon highlight when selected + subtle glow
            "icon-selected": {
                "color": "#0b66f0",
                "text-shadow": "0 4px 12px rgba(11,102,240,0.18)",
                "filter": "drop-shadow(0 6px 10px rgba(11,102,240,0.12))",
            },
        }
    )
    
    st.markdown("---")
    # Reset knop om alle velden te wissen
    if st.button("🔄 Reset alle velden", type="secondary", use_container_width=True):
        # Bewaar alleen de module selectie
        current_module = st.session_state.get("selected_module", "Echo")
        # Wis alle session state keys behalve system keys
        keys_to_keep = {"selected_module", "__brief_sections__"}
        keys_to_delete = [k for k in st.session_state.keys() if k not in keys_to_keep and not k.startswith("_")]
        for k in keys_to_delete:
            del st.session_state[k]
        # Herstel defaults
        for key, default in PATIENT_SIDEBAR_DEFAULTS.items():
            st.session_state[key] = default
        # De widget `selected_module` bestaat al — plan de herselectie voor de volgende run
        st.session_state["_pending_selected_module"] = current_module
        safe_rerun()

# Trend visualization for historical patient data
if patient_identifier and patient_identifier.strip() and BACKEND_ENABLED:
    with st.expander("📊 Historische trends", expanded=False):
        studies = _fetch_patient_studies(patient_identifier.strip())
        if studies and len(studies) > 0:
            st.caption(f"{len(studies)} studie(s) gevonden voor deze patiënt")
            
            # Organize studies by type
            studies_by_type = {}
            for study in studies:
                study_type = study.get("study_type", "unknown")
                if study_type not in studies_by_type:
                    studies_by_type[study_type] = []
                studies_by_type[study_type].append(study)
            
            # Show trend charts based on current module
            if module == "Echo" and "echo" in studies_by_type:
                echo_studies = sorted(studies_by_type["echo"], key=_study_order_stamp)
                
                # Extract LVEF trend
                dates = []
                lvef_values = []
                for study in echo_studies:
                    dt_str = study.get("study_datetime")
                    dt_obj = _parse_iso_datetime(dt_str)
                    payload = study.get("payload", {})
                    lvef = payload.get("lvef")
                    if dt_obj and lvef:
                        dates.append(dt_obj.strftime("%d-%m-%Y"))
                        lvef_values.append(float(lvef))
                
                if lvef_values:
                    import pandas as pd
                    df = pd.DataFrame({"Datum": dates, "LVEF (%)": lvef_values})
                    st.subheader("LVEF Trend")
                    st.line_chart(df.set_index("Datum"))
            
            elif module == "Fietstest" and "fietstest" in studies_by_type:
                fiets_studies = sorted(studies_by_type["fietstest"], key=_study_order_stamp)
                
                # Extract max wattage trend
                dates = []
                watt_values = []
                for study in fiets_studies:
                    dt_str = study.get("study_datetime")
                    dt_obj = _parse_iso_datetime(dt_str)
                    payload = study.get("payload", {})
                    fietstest_data = payload.get("fietstest", {})
                    max_watt = fietstest_data.get("max_watt")
                    if dt_obj and max_watt:
                        dates.append(dt_obj.strftime("%d-%m-%Y"))
                        watt_values.append(float(max_watt))
                
                if watt_values:
                    import pandas as pd
                    df = pd.DataFrame({"Datum": dates, "Max Watt (W)": watt_values})
                    st.subheader("Fietsproef Prestatie Trend")
                    st.line_chart(df.set_index("Datum"))
            
            elif module == "Holter" and "holter" in studies_by_type:
                holter_studies = sorted(studies_by_type["holter"], key=_study_order_stamp)
                
                # Extract afib percentage trend
                dates = []
                afib_values = []
                for study in holter_studies:
                    dt_str = study.get("study_datetime")
                    dt_obj = _parse_iso_datetime(dt_str)
                    payload = study.get("payload", {})
                    afib_pct = payload.get("afib_percentage")
                    if dt_obj and afib_pct is not None:
                        dates.append(dt_obj.strftime("%d-%m-%Y"))
                        afib_values.append(float(afib_pct))
                
                if afib_values:
                    import pandas as pd
                    df = pd.DataFrame({"Datum": dates, "AFIB (%)": afib_values})
                    st.subheader("Atriumfibrilleren Trend")
                    st.line_chart(df.set_index("Datum"))
            
            # Show study history table
            st.subheader("Studie Geschiedenis")
            study_table = []
            for study in sorted(studies, key=_study_order_stamp, reverse=True):
                dt_str = study.get("study_datetime")
                formatted_date = _format_iso_date(dt_str) or "Onbekend"
                study_table.append({
                    "Datum": formatted_date,
                    "Type": study.get("study_type", "").capitalize(),
                    "Bron": study.get("source", "").capitalize(),
                })
            
            if study_table:
                import pandas as pd
                st.dataframe(pd.DataFrame(study_table), use_container_width=True)
        else:
            st.info("Geen historische studies gevonden voor deze patiënt")

    # Define placeholders for compact-metrics-derived variables so they exist regardless of selected module
    ak_vmax_val = ak_mean_val = ava_val = ava_idx = None
    ak_default_idx = 0
    mk_eroa_val = mk_regvol_val = mk_rf_val = lvids_val = None
    mk_default_idx = 0
    ivsd = lvpw = lvidd = lvids = lvef = None
    la_volume = None
    la_raw = None
    lavi = None
    la_suggested = None
    tapse = None
    pasp_raw = None
    lv_mass_g = None
    rwt = None
    lv_dilatatie_auto = None
    # patient gegevens remain in sidebar; PASP moved to main Metingen

patient_ctx = PatientContext(
    sex=sex,
    patient_id=patient_identifier.strip() or None,
    full_name=patient_name.strip() or None,
    date_of_birth=dob_text.strip() or None,
    leeftijd=leeftijd,
    bsa=bsa,
    weight=weight,
    length=length,
)

# -----------------------------
# Brief module (tekst-samenvatting)
# -----------------------------
if module == "Brief":
    st.header("Brief — consulttemplate")
    sections = _load_brief_sections(patient_ctx)

    consult_date = st.date_input("Consultdatum", value=st.session_state.get("brief_consult_date", datetime.date.today()), key="brief_consult_date")

    voorgeschiedenis = st.text_area("Voorgeschiedenis", value=st.session_state.get("brief_voorgeschiedenis", ""), height=120, key="brief_voorgeschiedenis")
    anamnese = st.text_area("Anamnese", value=st.session_state.get("brief_anamnese", ""), height=120, key="brief_anamnese")
    thuismedicatie = st.text_area("Thuismedicatie", value=st.session_state.get("brief_thuismedicatie", ""), height=120, key="brief_thuismedicatie")

    st.subheader("Klinisch onderzoek")
    c1, c2, c3 = st.columns(3)
    with c1:
        pols_val = st.number_input("Pols (bpm)", min_value=0, max_value=250, value=st.session_state.get("brief_pols", 0), key="brief_pols")
    with c2:
        bp_sys = st.number_input("Systolische BD (mmHg)", min_value=0, max_value=300, value=st.session_state.get("brief_bp_sys", 0), key="brief_bp_sys")
    with c3:
        bp_dia = st.number_input("Diastolische BD (mmHg)", min_value=0, max_value=200, value=st.session_state.get("brief_bp_dia", 0), key="brief_bp_dia")

    ausc_normaal = st.checkbox("Normale hartauscultatie", value=st.session_state.get("brief_ausc_normaal", True), key="brief_ausc_normaal")
    auscultatie = "Normale hartauscultatie." if ausc_normaal else st.text_input("Auscultatie (vrije tekst)", value=st.session_state.get("brief_auscultatie", ""), key="brief_auscultatie")

    bmi_val = None
    try:
        if patient_ctx.weight and patient_ctx.length and float(patient_ctx.length) > 0:
            bmi_val = round(float(patient_ctx.weight) / ((float(patient_ctx.length) / 100.0) ** 2), 1)
    except Exception:
        bmi_val = None

    st.subheader("Onderzoeken (volledige verslagen)")
    st.caption("Volledige verslagen uit de modules worden automatisch opgenomen in de brief; samenvattingen zijn verwijderd.")

    full_investigation_defs = [
        ("ECG", "full_ecg"),
        ("Fietsproef", "full_fietstest"),
        ("Echocardiografie", "full_echo"),
        ("Holter-monitoring", "full_holter"),
        ("Device uitlezing", "full_cied"),
    ]

    current_sections: Dict[str, Dict[str, Optional[str]]] = {}
    investigations: List[Dict[str, Any]] = []

    # Collect available full investigation texts, but do not render individual expanders here
    for label, key in full_investigation_defs:
        meta = sections.get(key, {})
        full_text = (meta.get("text") or "").strip()
        performed_on = meta.get("performed_on") or None
        current_sections[key] = {"text": full_text, "performed_on": performed_on}
        if full_text:
            investigations.append({
                "label": label,
                "text": full_text,
                "performed_on": performed_on,
                "enabled": True,
            })

    if not investigations:
        st.warning("Nog geen volledige verslagen gevonden. Gebruik eerst een module om een verslag te genereren.")

    full_keys = [key for _, key in full_investigation_defs]

    bespreking = st.text_area("Bespreking", value=st.session_state.get("brief_bespreking", ""), height=140, key="brief_bespreking")

    clinical_exam = {
        "pols": pols_val or None,
        "blood_pressure": (bp_sys or None, bp_dia or None),
        "weight": patient_ctx.weight,
        "length": patient_ctx.length,
        "bmi": bmi_val,
        "auscultation": auscultatie.strip() if auscultatie else None,
    }

    brief_text = compose_brief_letter(
        patient_ctx,
        consult_date,
        voorgeschiedenis,
        anamnese,
        thuismedicatie,
        clinical_exam,
        investigations,
        bespreking,
    )

    st.subheader("Gegenereerde brief")
    show_report_actions(brief_text, file_name="brief.txt")

    # Ensure any available full_* texts are included in the brief snapshot
    full_keys = ["full_ecg", "full_fietstest", "full_echo", "full_holter", "full_cied"]
    merged_sections = {k: v.get("text", "") for k, v in current_sections.items()}
    for fk in full_keys:
        if not merged_sections.get(fk):
            merged_sections[fk] = sections.get(fk, {}).get("text", "") or merged_sections.get(fk, "")

    snapshot = StudySnapshot(
        patient=patient_ctx,
        report_texts={
            "brief_letter": brief_text,
            "brief_voorgeschiedenis": voorgeschiedenis,
            "brief_anamnese": anamnese,
            "brief_thuismedicatie": thuismedicatie,
            "brief_bespreking": bespreking,
            **merged_sections,
        },
    )
    # snapshot download removed per UI simplification

    if st.button("Opslaan als brief in backend"):
        # Always remember the generated brief and any investigation/full texts in the local brief cache
        _remember_brief_section("brief_letter", brief_text, patient_ctx.patient_id, consult_date.isoformat())
        for inv in investigations:
            key = None
            for label, inv_key in full_investigation_defs:
                if label == inv.get("label"):
                    key = inv_key
                    break
            if key:
                _remember_brief_section(key, inv.get("text", ""), patient_ctx.patient_id, inv.get("performed_on"))

        for fk in full_keys:
            txt = merged_sections.get(fk) or sections.get(fk, {}).get("text", "")
            perf = sections.get(fk, {}).get("performed_on")
            if txt:
                # store under provided patient id or default bucket when None
                _remember_brief_section(fk, txt, patient_ctx.patient_id, perf)

        # Post to backend only when a patient id is provided
        if patient_ctx.patient_id:
            backend_id = _post_snapshot_to_backend("brief", snapshot)
            if backend_id:
                st.info(f"Brief opgeslagen in backend (study {backend_id}).")
        else:
            st.info("Brief bijgewerkt in lokale cache (geen patiënt-ID aanwezig).")
    st.stop()

# Compact metrics expander for quick input (writes to session_state keys)
if module == "Echo":
    with st.expander("Compact metrics — snelle invoer", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.text_input("IVSd (mm)", value="", placeholder="mm", key="ivsd")
            st.text_input("LVPWd (mm)", value="", placeholder="mm", key="lvpw")
            st.text_input("LVIDd (mm)", value="", placeholder="mm", key="lvidd")
            st.text_input("LVIDs (mm)", value="", placeholder="mm", key="lvids")
            st.text_input("LVEF (%)", value="60", placeholder="%", key="lvef")
            # Live LVESDi, LVIDs-classificatie, en Teichholz-EF suggestie
            try:
                lvidd_live = st.session_state.get('lvidd', "")
                lvids_live = st.session_state.get('lvids', "")
                lvidd_f = float(str(lvidd_live).strip()) if lvidd_live is not None and str(lvidd_live).strip() != "" else None
                lvids_f = float(str(lvids_live).strip()) if lvids_live is not None and str(lvids_live).strip() != "" else None

                lvesdi_live = None
                if lvids_f is not None and bsa and float(bsa) > 0:
                    lvesdi_live = round(lvids_f / float(bsa), 1)

                def classify_lvids(lvids_mm, lvids_idx, sex_val):
                    sev = 0  # 0 normaal, 1 mild, 2 matig, 3 ernstig
                    if lvids_mm is None and lvids_idx is None:
                        return 0
                    # Prefer mm and mm/m^2 thresholds per user specification
                    if sex_val == "Man":
                        # Severe
                        if (lvids_mm is not None and lvids_mm > 45) or (lvids_idx is not None and lvids_idx > 25):
                            sev = 3
                        # Moderate
                        elif (lvids_mm is not None and 44 < lvids_mm <= 45) or (lvids_idx is not None and 24 <= lvids_idx <= 25):
                            sev = max(sev, 2)
                        # Mild
                        elif (lvids_mm is not None and 41 <= lvids_mm <= 44) or (lvids_idx is not None and 22 <= lvids_idx < 24):
                            sev = max(sev, 1)
                    else:  # Vrouw
                        # Severe
                        if (lvids_mm is not None and lvids_mm > 41) or (lvids_idx is not None and lvids_idx > 26):
                            sev = 3
                        # Moderate
                        elif (lvids_mm is not None and 39 < lvids_mm <= 41) or (lvids_idx is not None and 24 <= lvids_idx <= 26):
                            sev = max(sev, 2)
                        # Mild
                        elif (lvids_mm is not None and 36 <= lvids_mm <= 39) or (lvids_idx is not None and 22 <= lvids_idx < 24):
                            sev = max(sev, 1)
                    return sev

                lvids_idx_live = None
                if lvids_f is not None and bsa and float(bsa) > 0:
                    lvids_idx_live = round(lvids_f / float(bsa), 2)

                # Also compute LVIDd index for live LVIDd classification display
                lvidd_idx_live = None
                if lvidd_f is not None and bsa and float(bsa) > 0:
                    lvidd_idx_live = round(lvidd_f / float(bsa), 1)

                sev_map = {0: "Normaal", 1: "Mild vergroot", 2: "Matig vergroot", 3: "Ernstig vergroot"}
                sev_lvids = classify_lvids(lvids_f, lvids_idx_live, sex)

                # Show LVIDd index first (preferred), then LVIDs index/classification.
                try:
                    if lvidd_idx_live is not None:
                        lvidd_label = classify_lvidd(lvidd_f, sex, bsa)
                        st.caption(f"LVIDd index: {lvidd_idx_live} mm/m² — {lvidd_label.capitalize()}")
                except Exception:
                    col1, col2 = st.columns(2)
        
                    # Parse compact metric inputs from session_state so automatic calculations can run
                    def _get_float(key):
                        raw = st.session_state.get(key, "")
                        try:
                            if raw is None or str(raw).strip() == "":
                                return None
                            return float(str(raw).strip())
                        except Exception:
                            return None
        
                    ivsd = _get_float("ivsd")
                    lvpw = _get_float("lvpw")
                    lvidd = _get_float("lvidd")
                    lvids = _get_float("lvids")
                    lvef = _get_float("lvef")
                    tapse = _get_float("tapse")
                    la_raw = st.session_state.get("la_volume", "")
                    try:
                        lavi = round(float(str(la_raw).strip()) / max(0.01, float(bsa)), 1) if la_raw is not None and str(la_raw).strip() != "" else None
                    except Exception:
                        lavi = None
                    try:
                        la_suggested = classify_lavi(lavi) if lavi is not None else None
                    except Exception:
                        la_suggested = None
        
                    try:
                        lvef_class = classify_lvef(lvef, sex) if lvef is not None else None
                    except Exception:
                        lvef_class = None
                    automatic_systolic = lvef_to_systolic_option(lvef_class) if lvef_class is not None else "goede globale en regionale systolische functie"

                # Prefer showing LVIDs index (from LVIDs / LVESDi) next
                if lvesdi_live is not None:
                    st.caption(f"LVIDs index: {lvesdi_live} mm/m² — {sev_map.get(sev_lvids, 'n.v.t.')}")
                elif lvids_idx_live is not None:
                    st.caption(f"LVIDs index: {lvids_idx_live} mm/m² — {sev_map.get(sev_lvids, 'n.v.t.')}")

                ef_teich = None
                if lvidd_f is not None and lvids_f is not None and lvidd_f > 0:
                    try:
                        lvidd_cm = lvidd_f / 10.0
                        lvids_cm = lvids_f / 10.0
                        edv = (7 / (2.4 + lvidd_cm)) * (lvidd_cm ** 3)
                        esv = (7 / (2.4 + lvids_cm)) * (lvids_cm ** 3)
                        if edv > 0:
                            ef_teich = round(((edv - esv) / edv) * 100, 1)
                    except Exception:
                        ef_teich = None

                if ef_teich is not None:
                    st.caption(f"Teichholz EF (LVIDd/LVIDs): ~{ef_teich}% (veld blijft manueel aanpasbaar)")
            except Exception:
                pass

        # Parse compact metric inputs from session_state so automatic calculations can run even when no errors above
        def _get_float(key):
            raw = st.session_state.get(key, "")
            try:
                if raw is None or str(raw).strip() == "":
                    return None
                return float(str(raw).strip())
            except Exception:
                return None

        ivsd = _get_float("ivsd")
        lvpw = _get_float("lvpw")
        lvidd = _get_float("lvidd")
        lvids = _get_float("lvids")
        lvef = _get_float("lvef")
        tapse = _get_float("tapse")
        la_raw = st.session_state.get("la_volume", "")
        try:
            lavi = round(float(str(la_raw).strip()) / max(0.01, float(bsa)), 1) if la_raw is not None and str(la_raw).strip() != "" else None
        except Exception:
            lavi = None
        try:
            la_suggested = classify_lavi(lavi) if lavi is not None else None
        except Exception:
            la_suggested = None

        try:
            lvef_class = classify_lvef(lvef, sex) if lvef is not None else None
        except Exception:
            lvef_class = None
        automatic_systolic = lvef_to_systolic_option(lvef_class) if lvef_class is not None else "goede globale en regionale systolische functie"
        with c2: 
            st.text_input("LA volume (mL)", value="", placeholder="mL", key="la_volume")
            # Live LAVI calculation beneath the LA volume input
            try:
                la_raw_live = st.session_state.get('la_volume', "")
                if la_raw_live is not None and str(la_raw_live).strip() != "":
                    lavi_live = round(float(str(la_raw_live).strip()) / max(0.01, float(bsa)), 1)
                    try:
                        lavi_label = classify_lavi(lavi_live)
                    except Exception:
                        lavi_label = ""
                    if lavi_label:
                        colored = color_status_html(lavi_label)
                        st.markdown(f"LAVI: {lavi_live} mL/m² — {colored}", unsafe_allow_html=True)
                    else:
                        st.caption(f"LAVI: {lavi_live} mL/m²")
                else:
                    # Hide LAVI line when no LA volume provided (user requested)
                    pass
            except Exception:
                st.caption("LAVI: niet beschikbaar")
            st.text_input("TAPSE (mm)", value="", placeholder="mm", key="tapse")
            st.text_input("E/A (ratio)", value="", placeholder="e.g. 1.2", key="ea")
            st.text_input("E/e' (ratio)", value="", placeholder="e.g. 12", key="ee")
        with c3:
            st.text_input("PASP (mmHg)", value="", key="pasp_raw") 
            # Show automatic LV calculations here when necessary inputs are present
            try:
                def _get_float_local(key):
                    raw = st.session_state.get(key, "")
                    try:
                        if raw is None or str(raw).strip() == "":
                            return None
                        return float(str(raw).strip())
                    except Exception:
                        return None

                ivsd_val = _get_float_local('ivsd')
                lvpw_val = _get_float_local('lvpw')
                lvidd_val = _get_float_local('lvidd')
                la_raw_val = st.session_state.get('la_volume', "")
                lavi_val = None
                try:
                    if la_raw_val is not None and str(la_raw_val).strip() != "" and bsa and float(bsa) > 0:
                        lavi_val = round(float(str(la_raw_val).strip()) / float(bsa), 1)
                except Exception:
                    lavi_val = None

                any_lv_calc = ivsd_val is not None and lvpw_val is not None and lvidd_val is not None
                if any_lv_calc or lavi_val is not None:
                    st.markdown("**Automatische berekeningen**")
                    # LV mass and related
                    if ivsd_val is not None and lvpw_val is not None and lvidd_val is not None:
                        try:
                            lv_mass_g_local = compute_lv_mass_g(ivsd_val, lvidd_val, lvpw_val)
                        except Exception:
                            lv_mass_g_local = None
                    else:
                        lv_mass_g_local = None

                    if lv_mass_g_local is not None and bsa and float(bsa) > 0:
                        try:
                            mass_index_local, mass_severity_local = lv_mass_index_severity(lv_mass_g_local, bsa, sex)
                        except Exception:
                            mass_index_local = None
                            mass_severity_local = None
                    else:
                        mass_index_local = None
                        mass_severity_local = None

                    if lvpw_val is not None and lvidd_val is not None:
                        try:
                            rwt_local = compute_rwt(lvpw_val, lvidd_val)
                        except Exception:
                            rwt_local = None
                    else:
                        rwt_local = None

                    # hypertrophy suggestion
                    try:
                        if mass_index_local is not None and mass_severity_local is not None and rwt_local is not None:
                            lv_hypertrophy_local = determine_lv_geometry(mass_index_local, mass_severity_local, rwt_local)
                        else:
                            lv_hypertrophy_local = None
                    except Exception:
                        lv_hypertrophy_local = None

                    # LVIDd dilatation
                    if lvidd_val is not None and bsa and float(bsa) > 0:
                        try:
                            lv_dilatation_local = classify_lvidd(lvidd_val, sex, bsa)
                        except Exception:
                            lv_dilatation_local = None
                    else:
                        lv_dilatation_local = None

                    # Display
                    st.write(f"LV massa: {int(round(lv_mass_g_local)) if lv_mass_g_local is not None else 'n.v.t.'} g")
                    st.write(f"LV massa index: {mass_index_local if mass_index_local is not None else 'n.v.t.'} g/m² ({mass_severity_local if mass_severity_local is not None else ''})")
                    st.write(f"RWT: {rwt_local if rwt_local is not None else 'n.v.t.'}")
                    st.write(f"LV hypertrofie (automatisch): {lv_hypertrophy_local if lv_hypertrophy_local is not None else 'n.v.t.'}")
                    st.write(f"LV dilatatie (automatisch): {lv_dilatation_local if lv_dilatation_local is not None else 'n.v.t.'}")
                    # LAVI wordt al live getoond onder 'LA volume' links; geen dubbele weergave hier
            except Exception:
                pass
 # Third compact metrics expander for Aorta (extra) placed above RV
if module == "Echo":
    with st.expander("Compact metrics — Aorta (extra)", expanded=False):
        ac = st.columns(1)
        with ac[0]:
            st.text_input("Aorta annulus diameter (AoA, mm)", value="", placeholder="mm", key="aoa")
            st.text_input("Aorta sinus valsalva (AoSV, mm)", value="", placeholder="mm", key="aosv")
            st.text_input("Aorta sinotubulaire junctie (AoSTJ, mm)", value="", placeholder="mm", key="aostj")
            st.text_input("Aorta ascendens (AscAo, mm)", value="", placeholder="mm", key="ascao")

        # live predicted lower/higher formulas and indexed interpretation
        try:
            male = 1 if sex == 'Man' else 0
            age = float(leeftijd)
            height = float(length)
            weight = float(weight)
        except Exception:
            male = 1 if sex == 'Man' else 0
            try:
                age = float(leeftijd)
            except Exception:
                age = 0.0
            try:
                height = float(length)
            except Exception:
                height = 0.0
            try:
                weight = float(weight)
            except Exception:
                weight = 0.0

        # Helper to format predicted ranges and live decision
        def _pred_and_index(meas_key, lower_formula, higher_formula, cutoff_mm_per_m2):
            raw = st.session_state.get(meas_key, "")
            try:
                lower = lower_formula(age, male, height, weight)
                higher = higher_formula(age, male, height, weight)
                lower = round(lower, 2)
                higher = round(higher, 2)
            except Exception:
                lower = None
                higher = None

            # measured and indexed
            meas_val = None
            indexed = None
            try:
                if raw is not None and str(raw).strip() != "":
                    meas_val = float(str(raw).strip())
                    if bsa and float(bsa) > 0:
                        indexed = round(meas_val / float(bsa), 2)
            except Exception:
                meas_val = None
                indexed = None

            # decision by indexed value
            decision = None
            try:
                if indexed is not None:
                    decision = 'Gedilateerd' if indexed > cutoff_mm_per_m2 else 'Niet gedilateerd'
            except Exception:
                decision = None

            return meas_val, indexed, lower, higher, decision

        # AoA formulas
        def _aoa_lower(age, male, h, w):
            return 10.828 + age * 0.001 + male * 0.871 + h * 0.013 + w * 0.020
        def _aoa_higher(age, male, h, w):
            return 14.970 + age * 0.020 + male * 1.278 + h * 0.037 + w * 0.034

        meas_aoa, idx_aoa, low_aoa, high_aoa, dec_aoa = _pred_and_index('aoa', _aoa_lower, _aoa_higher, 14)
        if low_aoa is not None and high_aoa is not None:
            st.caption(f"AoA predicted range (lower–higher): {low_aoa}–{high_aoa} mm")
        if meas_aoa is not None:
            if dec_aoa:
                colored = color_status_html(dec_aoa)
                st.markdown(f"AoA: {meas_aoa} mm — Indexed: {idx_aoa} mm/m² — {colored}", unsafe_allow_html=True)
            else:
                st.caption(f"AoA: {meas_aoa} mm — Indexed: {idx_aoa} mm/m²")

        # AoSV formulas
        def _aosv_lower(age, male, h, w):
            return 3.483 + age * 0.086 + male * 1.731 + h * 0.062 + w * 0.036
        def _aosv_higher(age, male, h, w):
            return 12.129 + age * 0.125 + male * 2.589 + h * 0.113 + w * 0.065

        meas_aosv, idx_aosv, low_aosv, high_aosv, dec_aosv = _pred_and_index('aosv', _aosv_lower, _aosv_higher, 20)
        if low_aosv is not None and high_aosv is not None:
            st.caption(f"AoSV predicted range (lower–higher): {low_aosv}–{high_aosv} mm")
        if meas_aosv is not None:
            if dec_aosv:
                colored = color_status_html(dec_aosv)
                st.markdown(f"AoSV: {meas_aosv} mm — Indexed: {idx_aosv} mm/m² — {colored}", unsafe_allow_html=True)
            else:
                st.caption(f"AoSV: {meas_aosv} mm — Indexed: {idx_aosv} mm/m²")

        # AoSTJ formulas
        def _aostj_lower(age, male, h, w):
            return 0.600 + age * 0.061 + male * 0.707 + h * 0.056 + w * 0.026
        def _aostj_higher(age, male, h, w):
            return 8.562 + age * 0.097 + male * 1.499 + h * 0.103 + w * 0.054

        meas_aostj, idx_aostj, low_aostj, high_aostj, dec_aostj = _pred_and_index('aostj', _aostj_lower, _aostj_higher, 16)
        if low_aostj is not None and high_aostj is not None:
            st.caption(f"AoSTJ predicted range (lower–higher): {low_aostj}–{high_aostj} mm")
        if meas_aostj is not None:
            if dec_aostj:
                colored = color_status_html(dec_aostj)
                st.markdown(f"AoSTJ: {meas_aostj} mm — Indexed: {idx_aostj} mm/m² — {colored}", unsafe_allow_html=True)
            else:
                st.caption(f"AoSTJ: {meas_aostj} mm — Indexed: {idx_aostj} mm/m²")

        # AscAo formulas
        def _ascao_lower(age, male, h, w):
            return 8.189 + age * 0.041 + male * 0.655 + h * -0.007 + w * 0.040
        def _ascao_higher(age, male, h, w):
            return 21.214 + age * 0.101 + male * 1.961 + h * 0.069 + w * 0.087

        meas_ascao, idx_ascao, low_ascao, high_ascao, dec_ascao = _pred_and_index('ascao', _ascao_lower, _ascao_higher, 17)
        if low_ascao is not None and high_ascao is not None:
            st.caption(f"AscAo predicted range (lower–higher): {low_ascao}–{high_ascao} mm")
        if meas_ascao is not None:
            if dec_ascao:
                colored = color_status_html(dec_ascao)
                st.markdown(f"AscAo: {meas_ascao} mm — Indexed: {idx_ascao} mm/m² — {colored}", unsafe_allow_html=True)
            else:
                st.caption(f"AscAo: {meas_ascao} mm — Indexed: {idx_ascao} mm/m²")

        # Allow manual override selection per site (defaults based on indexed decision)
        try:
            default_aoa_idx = 1 if dec_aoa == 'Gedilateerd' else 0
        except Exception:
            default_aoa_idx = 0
        aoa_dilatatie = st.selectbox("AoA dilatatie", ["Niet gedilateerd", "Gedilateerd"], index=default_aoa_idx)

        try:
            default_aosv_idx = 1 if dec_aosv == 'Gedilateerd' else 0
        except Exception:
            default_aosv_idx = 0
        aosv_dilatatie = st.selectbox("AoSV dilatatie", ["Niet gedilateerd", "Gedilateerd"], index=default_aosv_idx)

        try:
            default_aostj_idx = 1 if dec_aostj == 'Gedilateerd' else 0
        except Exception:
            default_aostj_idx = 0
        aostj_dilatatie = st.selectbox("AoSTJ dilatatie", ["Niet gedilateerd", "Gedilateerd"], index=default_aostj_idx)

        try:
            default_ascao_idx = 1 if dec_ascao == 'Gedilateerd' else 0
        except Exception:
            default_ascao_idx = 0
        ascao_dilatatie = st.selectbox("AscAo dilatatie", ["Niet gedilateerd", "Gedilateerd"], index=default_ascao_idx)

        # Live AO summary preview (same format as report) so user sees it before generating
        try:
            ao_items_preview = []
            if aoa_val is not None:
                if aoa_idx is not None:
                    ao_items_preview.append(f"AoA {int(round(aoa_val))} mm, {aoa_idx:.1f} mm/m²")
                else:
                    ao_items_preview.append(f"AoA {int(round(aoa_val))} mm")
            if aosv_val is not None:
                if aosv_idx is not None:
                    ao_items_preview.append(f"AoSV {int(round(aosv_val))} mm, {aosv_idx:.1f} mm/m²")
                else:
                    ao_items_preview.append(f"AoSV {int(round(aosv_val))} mm")
            if aostj_val is not None:
                if aostj_idx is not None:
                    ao_items_preview.append(f"AoSTJ {int(round(aostj_val))} mm, {aostj_idx:.1f} mm/m²")
                else:
                    ao_items_preview.append(f"AoSTJ {int(round(aostj_val))} mm")
            if ascao_val is not None:
                if ascao_idx is not None:
                    ao_items_preview.append(f"AscAo {int(round(ascao_val))} mm, {ascao_idx:.1f} mm/m²")
                else:
                    ao_items_preview.append(f"AscAo {int(round(ascao_val))} mm")

            if ao_items_preview:
                overall_preview = "Aorta gedilateerd" if any([x for x in [aoa_idx, aosv_idx, aostj_idx, ascao_idx] if x is not None and x > 0 and ((x > 14 and 'AoA' in ao_items_preview[0]) or True)]) else "Aorta niet gedilateerd"
                # The overall flag above is a simple placeholder; detailed abnormal lines shown in full report
                st.info(f"AO: {overall_preview} ({', '.join(ao_items_preview)}).")
        except Exception:
            pass

 # Second compact metrics expander for RV-specific quick input (collapsed by default)
if module == "Echo":
    with st.expander("Compact metrics — RV (extra)", expanded=False):
        rc1 = st.columns(1)
        with rc1[0]:
            st.text_input("RV free wall thickness (RVFWd, mm)", value="", placeholder="mm", key="rvfwd")
            st.text_input("RV basal diameter (RVBDd, mm)", value="", placeholder="mm", key="rvbd")
            st.text_input("RV mid diameter (RVMDd, mm)", value="", placeholder="mm", key="rvmd")
            st.text_input("RA volume (mL)", value="", placeholder="mL", key="ra_volume")
        # Live RAVI calculation beneath the RA volume input
        try:
            ra_raw_live = st.session_state.get('ra_volume', "")
            if ra_raw_live is not None and str(ra_raw_live).strip() != "":
                ravi_live = round(float(str(ra_raw_live).strip()) / max(0.01, float(bsa)), 1)
                # simple sex-specific interpretation
                try:
                    if sex == 'Man':
                        ravi_interp = 'Gedilateerd' if ravi_live > 32 else 'Niet gedilateerd'
                    else:
                        ravi_interp = 'Gedilateerd' if ravi_live > 28 else 'Niet gedilateerd'
                except Exception:
                    ravi_interp = ''
                if ravi_interp:
                    colored = color_status_html(ravi_interp)
                    st.markdown(f"RAVI: {ravi_live} mL/m² — {colored}", unsafe_allow_html=True)
                else:
                    st.caption(f"RAVI: {ravi_live} mL/m²")
            else:
                st.caption("RAVI: n.v.t. (laat leeg voor geen berekening)")
        except Exception:
            st.caption("RAVI: niet beschikbaar")
        
# Fourth compact metrics expanders: separate small metric panels for each valve
if module == "Echo":
    # Aortaklep
    with st.expander("Compact metrics — Aortaklep (extra)", expanded=False):
        st.text_input("AK max velocity (m/s)", value="", placeholder="m/s", key="ak_vmax")
        st.text_input("AK mean gradient (mmHg)", value="", placeholder="mmHg", key="ak_mean")
        st.text_input("AVA (cm²)", value="", placeholder="cm²", key="ava")
        st.text_input("Stroke Volume (SV, mL)", value="", placeholder="mL", key="sv")

        # Live AVA index and suggested AK stenose severity preview
        try:
            _ak_vmax = st.session_state.get('ak_vmax', "")
            _ak_mean = st.session_state.get('ak_mean', "")
            _ava = st.session_state.get('ava', "")
            ak_v = float(str(_ak_vmax).strip()) if _ak_vmax is not None and str(_ak_vmax).strip() != "" else None
            ak_m = float(str(_ak_mean).strip()) if _ak_mean is not None and str(_ak_mean).strip() != "" else None
            ava_f = float(str(_ava).strip()) if _ava is not None and str(_ava).strip() != "" else None
            ava_idx_live = None
            if ava_f is not None and bsa and float(bsa) > 0:
                ava_idx_live = round(ava_f / float(bsa), 2)

            # severity rules (0 none,1 mild,2 mod,3 severe)
            sev = 0
            if ak_v is not None:
                if ak_v >= 4.0:
                    sev = max(sev, 3)
                elif 3.0 <= ak_v < 4.0:
                    sev = max(sev, 2)
                elif 2.6 <= ak_v < 3.0:
                    sev = max(sev, 1)
            if ak_m is not None:
                if ak_m >= 40:
                    sev = max(sev, 3)
                elif 20 <= ak_m < 40:
                    sev = max(sev, 2)
                elif ak_m < 20:
                    sev = max(sev, 1)
            if ava_f is not None:
                if ava_f <= 1.0:
                    sev = max(sev, 3)
                elif 1.0 < ava_f <= 1.5:
                    sev = max(sev, 2)
                elif ava_f > 1.5:
                    sev = max(sev, 1)
            if ava_idx_live is not None:
                if ava_idx_live <= 0.6:
                    sev = max(sev, 3)
                elif 0.6 < ava_idx_live <= 0.85:
                    sev = max(sev, 2)
                elif ava_idx_live > 0.85:
                    sev = max(sev, 1)

            severity_names = {0: 'Geen stenose', 1: 'Milde stenose', 2: 'Matige stenose', 3: 'Ernstige stenose'}
            if ava_idx_live is not None:
                idx_txt = f", AVA index {ava_idx_live:.2f} cm²/m²"
            else:
                idx_txt = ""

            parts = []
            if ak_v is not None:
                parts.append(f"Vmax {ak_v:.2f} m/s")
            if ak_m is not None:
                parts.append(f"MeanG {int(round(ak_m))} mmHg")
            if ava_f is not None:
                parts.append(f"AVA {ava_f:.2f} cm²{idx_txt}")

            # include SVi in preview when available
            try:
                _sv = st.session_state.get('sv', "")
                if _sv is not None and str(_sv).strip() != "":
                    sv_f = float(str(_sv).strip())
                    svi_live = round(sv_f / float(bsa), 1) if bsa and float(bsa) > 0 else None
                    if svi_live is not None:
                        parts.append(f"SVi {svi_live:.1f} mL/m²")
                        # low stroke volume indicator
                        if svi_live <= 35:
                            parts.append("(laag slagvolume)")
            except Exception:
                pass

            # Propagate preview severity into main selection/session so the report matches preview
            try:
                ak_default_idx = int(sev)
                if 'ak_stenose' not in st.session_state or not st.session_state.get('ak_stenose'):
                    st.session_state['ak_stenose'] = severity_names.get(sev)
            except Exception:
                pass

            if parts:
                try:
                    colored = color_status_html(severity_names.get(sev))
                    st.markdown(f"AK preview: {colored} ({', '.join(parts)})", unsafe_allow_html=True)
                except Exception:
                    st.info(f"AK preview: {severity_names.get(sev)} ({', '.join(parts)})")
        except Exception:
            pass

    # Mitralisklep
    with st.expander("Compact metrics — Mitralisklep (extra)", expanded=False):
        st.text_input("MK EROA (cm²)", value="", placeholder="cm²", key="mk_eroa")
        st.text_input("MK RegVol (mL)", value="", placeholder="mL", key="mk_regvol")
        st.text_input("MK RF (%)", value="", placeholder="%", key="mk_rf")

        # Live mitral regurgitation severity preview (EROA, RegVol, RF)
        try:
            _eroa = st.session_state.get('mk_eroa', "")
            _regvol = st.session_state.get('mk_regvol', "")
            _rf = st.session_state.get('mk_rf', "")

            eroaf = float(str(_eroa).strip()) if _eroa is not None and str(_eroa).strip() != "" else None
            regvolf = float(str(_regvol).strip()) if _regvol is not None and str(_regvol).strip() != "" else None
            rf_f = float(str(_rf).strip()) if _rf is not None and str(_rf).strip() != "" else None

            sev_mk = 0  # 0=none/unknown, 1=mild, 2=moderate, 3=severe
            if eroaf is not None:
                if eroaf >= 0.4:
                    sev_mk = max(sev_mk, 3)
                elif 0.2 <= eroaf < 0.4:
                    sev_mk = max(sev_mk, 2)
                elif eroaf < 0.2:
                    sev_mk = max(sev_mk, 1)
            if regvolf is not None:
                if regvolf >= 60:
                    sev_mk = max(sev_mk, 3)
                elif 30 <= regvolf < 60:
                    sev_mk = max(sev_mk, 2)
                elif regvolf < 30:
                    sev_mk = max(sev_mk, 1)
            if rf_f is not None:
                if rf_f > 50:
                    sev_mk = max(sev_mk, 3)
                elif 30 <= rf_f <= 50:
                    sev_mk = max(sev_mk, 2)
                elif rf_f < 30:
                    sev_mk = max(sev_mk, 1)

            sev_names_mk = {0: 'Niet ingedeeld', 1: 'Milde regurgitatie', 2: 'Matige regurgitatie', 3: 'Ernstige regurgitatie'}
            mk_parts = []
            if eroaf is not None:
                mk_parts.append(f"EROA {eroaf:.2f} cm²")
            if regvolf is not None:
                mk_parts.append(f"RegVol {int(round(regvolf))} mL")
            if rf_f is not None:
                mk_parts.append(f"RF {rf_f:.0f}%")
            if mk_parts:
                # Propagate preview severity into main selection/session so the report matches preview
                try:
                    mk_default_idx = int(sev_mk)
                    mk_label_map = {
                        0: 'Geen regurgitatie',
                        1: 'Milde mitralis regurgitatie',
                        2: 'Matige mitralis regurgitatie',
                        3: 'Ernstige mitralis regurgitatie',
                    }
                    if 'mk_regurgitatie' not in st.session_state or not st.session_state.get('mk_regurgitatie'):
                        st.session_state['mk_regurgitatie'] = mk_label_map.get(sev_mk)
                except Exception:
                    pass
                try:
                    colored = color_status_html(sev_names_mk.get(sev_mk, 'Niet ingedeeld'))
                    st.markdown(f"MK preview: {colored} ({', '.join(mk_parts)})", unsafe_allow_html=True)
                except Exception:
                    st.info(f"MK preview: {sev_names_mk.get(sev_mk, 'Niet ingedeeld')} ({', '.join(mk_parts)})")
        except Exception:
            pass

    # Tricuspidalisklep
    with st.expander("Compact metrics — Tricuspidalisklep (extra)", expanded=False):
        st.text_input("TK EROA (cm²)", value="", placeholder="cm²", key="tk_eroa")
        st.text_input("TK RegVol (mL)", value="", placeholder="mL", key="tk_regvol")
        st.text_input("TK RF (%)", value="", placeholder="%", key="tk_rf")
        st.text_input("TK VCW (cm)", value="", placeholder="cm", key="tk_vcw")

        # Live tricuspid regurgitation severity preview
        try:
            _eroa = st.session_state.get('tk_eroa', "")
            _regvol = st.session_state.get('tk_regvol', "")
            _rf = st.session_state.get('tk_rf', "")
            eroaf = float(str(_eroa).strip()) if _eroa is not None and str(_eroa).strip() != "" else None
            regvolf = float(str(_regvol).strip()) if _regvol is not None and str(_regvol).strip() != "" else None
            rf_f = float(str(_rf).strip()) if _rf is not None and str(_rf).strip() != "" else None

            sev_tk = 0
            if eroaf is not None:
                if eroaf >= 0.4:
                    sev_tk = max(sev_tk, 3)
                elif 0.2 <= eroaf < 0.4:
                    sev_tk = max(sev_tk, 2)
                elif eroaf < 0.2:
                    sev_tk = max(sev_tk, 1)
            _vcw = st.session_state.get('tk_vcw', "")
            vcwf = float(str(_vcw).strip()) if _vcw is not None and str(_vcw).strip() != "" else None

            if regvolf is not None:
                if regvolf >= 45:
                    sev_tk = max(sev_tk, 3)
                elif 30 <= regvolf < 45:
                    sev_tk = max(sev_tk, 2)
                elif regvolf < 30:
                    sev_tk = max(sev_tk, 1)
            if vcwf is not None:
                if vcwf >= 0.7:
                    sev_tk = max(sev_tk, 3)
                elif 0.3 <= vcwf < 0.7:
                    sev_tk = max(sev_tk, 2)
                elif vcwf < 0.3:
                    sev_tk = max(sev_tk, 1)
            if rf_f is not None:
                if rf_f > 50:
                    sev_tk = max(sev_tk, 3)
                elif 30 <= rf_f <= 50:
                    sev_tk = max(sev_tk, 2)
                elif rf_f < 30:
                    sev_tk = max(sev_tk, 1)

            tk_names = {0: 'Niet ingedeeld', 1: 'Milde regurgitatie', 2: 'Matige regurgitatie', 3: 'Ernstige regurgitatie'}
            parts = []
            if eroaf is not None:
                parts.append(f"EROA {eroaf:.2f} cm²")
            if regvolf is not None:
                parts.append(f"RegVol {int(round(regvolf))} mL")
            if rf_f is not None:
                parts.append(f"RF {rf_f:.0f}%")
            if vcwf is not None:
                parts.append(f"VCW {vcwf:.2f} cm")
            if parts:
                try:
                    tk_default_idx = int(sev_tk)
                    tk_label_map = {
                        0: 'Geen regurgitatie',
                        1: 'Milde tricuspidalis regurgitatie',
                        2: 'Matige tricuspidalis regurgitatie',
                        3: 'Ernstige tricuspidalis regurgitatie',
                    }
                    if 'tk_regurgitatie' not in st.session_state or not st.session_state.get('tk_regurgitatie'):
                        st.session_state['tk_regurgitatie'] = tk_label_map.get(sev_tk)
                except Exception:
                    pass
                try:
                    colored = color_status_html(tk_names.get(sev_tk))
                    st.markdown(f"TK preview: {colored} ({', '.join(parts)})", unsafe_allow_html=True)
                except Exception:
                    st.info(f"TK preview: {tk_names.get(sev_tk)} ({', '.join(parts)})")
        except Exception:
            pass

    # Pulmonalisklep
    with st.expander("Compact metrics — Pulmonalisklep (extra)", expanded=False):
        st.text_input("PK EROA (cm²)", value="", placeholder="cm²", key="pk_eroa")
        st.text_input("PK RegVol (mL)", value="", placeholder="mL", key="pk_regvol")
        st.text_input("PK RF (%)", value="", placeholder="%", key="pk_rf")
        st.text_input("PK DT RegJet (ms)", value="", placeholder="ms", key="pk_dt_regjet")
        st.text_input("PK PHT RegJet (ms)", value="", placeholder="ms", key="pk_pht_regjet")
        st.text_input("PK PR index", value="", placeholder="ratio (0-1)", key="pk_pr_index")

        # Live pulmonal regurgitation severity preview
        try:
            _eroa = st.session_state.get('pk_eroa', "")
            _regvol = st.session_state.get('pk_regvol', "")
            _rf = st.session_state.get('pk_rf', "")
            eroaf = float(str(_eroa).strip()) if _eroa is not None and str(_eroa).strip() != "" else None
            regvolf = float(str(_regvol).strip()) if _regvol is not None and str(_regvol).strip() != "" else None
            rf_f = float(str(_rf).strip()) if _rf is not None and str(_rf).strip() != "" else None

            sev_pk = 0
            if eroaf is not None:
                if eroaf >= 0.4:
                    sev_pk = max(sev_pk, 3)
                elif 0.2 <= eroaf < 0.4:
                    sev_pk = max(sev_pk, 2)
                elif eroaf < 0.2:
                    sev_pk = max(sev_pk, 1)
            if regvolf is not None:
                if regvolf >= 60:
                    sev_pk = max(sev_pk, 3)
                elif 30 <= regvolf < 60:
                    sev_pk = max(sev_pk, 2)
                elif regvolf < 30:
                    sev_pk = max(sev_pk, 1)
            if rf_f is not None:
                if rf_f > 50:
                    sev_pk = max(sev_pk, 3)
                elif 30 <= rf_f <= 50:
                    sev_pk = max(sev_pk, 2)
                elif rf_f < 30:
                    sev_pk = max(sev_pk, 1)

            # Additional PK-specific metrics from user table
            _dt = st.session_state.get('pk_dt_regjet', "")
            _pht = st.session_state.get('pk_pht_regjet', "")
            _pr = st.session_state.get('pk_pr_index', "")
            dtf = float(str(_dt).strip()) if _dt is not None and str(_dt).strip() != "" else None
            phtf = float(str(_pht).strip()) if _pht is not None and str(_pht).strip() != "" else None
            prf = float(str(_pr).strip()) if _pr is not None and str(_pr).strip() != "" else None

            # Interpret DT / PHT / PR index thresholds conservatively based on provided table
            if dtf is not None:
                # Short DT suggests more severe regurgitation
                if dtf < 260:
                    sev_pk = max(sev_pk, 3)
                elif dtf < 400:
                    sev_pk = max(sev_pk, 2)
                else:
                    sev_pk = max(sev_pk, 1)
            if phtf is not None:
                # Short PHT suggests severe
                if phtf < 100:
                    sev_pk = max(sev_pk, 3)
                elif phtf < 200:
                    sev_pk = max(sev_pk, 2)
                else:
                    sev_pk = max(sev_pk, 1)
            if prf is not None:
                # Low PR index implies more severe PR (thresholds from provided table)
                if prf < 0.77:
                    sev_pk = max(sev_pk, 3)
                elif prf < 0.9:
                    sev_pk = max(sev_pk, 2)
                else:
                    sev_pk = max(sev_pk, 1)

            pk_names = {0: 'Niet ingedeeld', 1: 'Milde regurgitatie', 2: 'Matige regurgitatie', 3: 'Ernstige regurgitatie'}
            parts = []
            if eroaf is not None:
                parts.append(f"EROA {eroaf:.2f} cm²")
            if regvolf is not None:
                parts.append(f"RegVol {int(round(regvolf))} mL")
            if rf_f is not None:
                parts.append(f"RF {rf_f:.0f}%")
            if dtf is not None:
                parts.append(f"DT {int(round(dtf))} ms")
            if phtf is not None:
                parts.append(f"PHT {int(round(phtf))} ms")
            if prf is not None:
                parts.append(f"PR-index {prf:.2f}")
            if parts:
                try:
                    pk_default_idx = int(sev_pk)
                    pk_label_map = {
                        0: 'Geen regurgitatie',
                        1: 'Milde pulmonalis regurgitatie',
                        2: 'Matige pulmonalis regurgitatie',
                        3: 'Ernstige pulmonalis regurgitatie',
                    }
                    if 'pk_regurgitatie' not in st.session_state or not st.session_state.get('pk_regurgitatie'):
                        st.session_state['pk_regurgitatie'] = pk_label_map.get(sev_pk)
                except Exception:
                    pass
                try:
                    colored = color_status_html(pk_names.get(sev_pk))
                    st.markdown(f"PK preview: {colored} ({', '.join(parts)})", unsafe_allow_html=True)
                except Exception:
                    st.info(f"PK preview: {pk_names.get(sev_pk)} ({', '.join(parts)})")
        except Exception:
            pass
# header for LV/LA choices intentionally removed per user request

# If user selected the Fietstest module, show separate UI and stop further echo rendering
if 'module' in globals() and module == "Fietstest":
    st.header("Fietstest / Protocol")
    st.markdown("Vul het protocol in en genereer de standaardtekst voor opname in het verslag.")

    uploaded_pdf = st.file_uploader("Importeer fietsproef PDF", type=["pdf"])
    pdf_ingest_ready = pdf_dependency_available()
    if not pdf_ingest_ready:
        st.info(f"PDF import tijdelijk niet beschikbaar: {PDF_DEPENDENCY_MESSAGE}")
    parsed_patient_ctx = None
    parsed_measurements = None
    parse_warnings: List[str] = []

    if uploaded_pdf is not None:
        if not pdf_ingest_ready:
            st.error("Kon PDF niet verwerken omdat pdfplumber ontbreekt.")
        else:
            raw_bytes = uploaded_pdf.getvalue()
            backend_resp = _post_pdf_to_backend("/api/ingest/fietstest-pdf", raw_bytes, uploaded_pdf.name)

            if backend_resp:
                patient_payload = backend_resp.get("patient") or {}
                measurement_payload = backend_resp.get("measurements") or {}
                parse_warnings = backend_resp.get("warnings") or []

                if patient_payload:
                    parsed_patient_ctx = _patient_from_payload(patient_payload)
                    if parsed_patient_ctx and parsed_patient_ctx.bsa is None and parsed_patient_ctx.length and parsed_patient_ctx.weight:
                        parsed_patient_ctx = PatientContext(
                            sex=parsed_patient_ctx.sex,
                            patient_id=parsed_patient_ctx.patient_id,
                            full_name=parsed_patient_ctx.full_name,
                            date_of_birth=parsed_patient_ctx.date_of_birth,
                            leeftijd=parsed_patient_ctx.leeftijd,
                            bsa=bsa_mosteller(parsed_patient_ctx.length, parsed_patient_ctx.weight),
                            weight=parsed_patient_ctx.weight,
                            length=parsed_patient_ctx.length,
                        )

                target_ctx = parsed_patient_ctx or patient_ctx
                if measurement_payload and target_ctx:
                    parsed_measurements = FietstestMeasurements(
                        patient=target_ctx,
                        start_watt=measurement_payload.get("start_watt"),
                        increment_watt=measurement_payload.get("increment_watt"),
                        max_watt=measurement_payload.get("max_watt"),
                        duration_at_max=measurement_payload.get("duration_at_max"),
                        max_hr=measurement_payload.get("max_hr"),
                        bp_evolutie=measurement_payload.get("bp_evolutie"),
                        ritme=measurement_payload.get("ritme"),
                        effort_type=measurement_payload.get("effort_type"),
                        stop_criterium=measurement_payload.get("stop_criterium"),
                        ecg_changes=measurement_payload.get("ecg_changes"),
                        conclusion=measurement_payload.get("conclusion"),
                    )
            else:
                parsed_patient_ctx, parsed_measurements, parse_warnings = parse_fietstest_pdf(raw_bytes)
                if parsed_patient_ctx:
                    parsed_bsa = parsed_patient_ctx.bsa
                    if parsed_bsa is None and parsed_patient_ctx.length and parsed_patient_ctx.weight:
                        parsed_bsa = bsa_mosteller(parsed_patient_ctx.length, parsed_patient_ctx.weight)
                    parsed_patient_ctx = PatientContext(
                        sex=parsed_patient_ctx.sex,
                        patient_id=parsed_patient_ctx.patient_id,
                        full_name=parsed_patient_ctx.full_name,
                        date_of_birth=parsed_patient_ctx.date_of_birth,
                        leeftijd=parsed_patient_ctx.leeftijd,
                        bsa=parsed_bsa,
                        weight=parsed_patient_ctx.weight,
                        length=parsed_patient_ctx.length,
                    )
            if parsed_patient_ctx:
                prefill_patient_sidebar(parsed_patient_ctx)
                st.success("PDF succesvol ingelezen. Gegevens zijn vooraf ingevuld.")
            if parse_warnings:
                for warning in parse_warnings:
                    st.warning(warning)

    active_patient_ctx = parsed_patient_ctx or patient_ctx

    def _prefill_int(value: Optional[float], fallback: int) -> int:
        try:
            return int(round(float(value))) if value is not None else fallback
        except Exception:
            return fallback

    def _prefill_select(options: List[str], value: Optional[str], default_idx: int = 0) -> int:
        if value is None:
            return default_idx
        lowered = value.lower()
        for idx, option in enumerate(options):
            if option.lower() in lowered or lowered in option.lower():
                return idx
        return default_idx

    start_watt_default = _prefill_int(parsed_measurements.start_watt if parsed_measurements else None, 50)
    increment_default = _prefill_int(parsed_measurements.increment_watt if parsed_measurements else None, 25)
    max_watt_default = _prefill_int(parsed_measurements.max_watt if parsed_measurements else None, 0)
    duration_default = _prefill_int(parsed_measurements.duration_at_max if parsed_measurements else None, 60)
    max_hr_default = _prefill_int(parsed_measurements.max_hr if parsed_measurements else None, 0)

    start_watt = st.number_input("Startbelasting (W)", min_value=0, max_value=500, value=st.session_state.get("fiets_start_watt", start_watt_default), key="fiets_start_watt")
    increment_watt = st.number_input("Opdrijven (W per minuut)", min_value=5, max_value=200, value=st.session_state.get("fiets_increment_watt", increment_default), key="fiets_increment_watt")
    max_watt = st.number_input("Maximale belasting bereikt (W)", min_value=0, max_value=2000, value=st.session_state.get("fiets_max_watt", max_watt_default), key="fiets_max_watt")
    duration_at_max = st.number_input("Duur bij maximale belasting (seconden)", min_value=0, max_value=600, value=st.session_state.get("fiets_duration_at_max", duration_default), key="fiets_duration_at_max")
    max_hr = st.number_input("Maximale hartslag (bpm)", min_value=0, max_value=300, value=st.session_state.get("fiets_max_hr", max_hr_default), key="fiets_max_hr")

    bp_options = ["Normale bloeddrukevolutie", "Abnormale bloeddrukevolutie"]
    bp_idx = _prefill_select(bp_options, parsed_measurements.bp_evolutie if parsed_measurements else None)
    bp_evolutie = st.selectbox("Bloeddrukevolutie", bp_options, index=st.session_state.get("fiets_bp_idx", bp_idx) if "fiets_bp_evolutie" not in st.session_state else bp_options.index(st.session_state.get("fiets_bp_evolutie", bp_options[bp_idx])) if st.session_state.get("fiets_bp_evolutie") in bp_options else bp_idx, key="fiets_bp_evolutie")

    ritme_options = ["Geen ritmestoornissen", "Ritmestoornissen tijdens test"]
    ritme_idx = _prefill_select(ritme_options, parsed_measurements.ritme if parsed_measurements else None)
    ritme = st.selectbox("Ritme/ritmestoornissen", ritme_options, index=ritme_options.index(st.session_state.get("fiets_ritme", ritme_options[ritme_idx])) if st.session_state.get("fiets_ritme") in ritme_options else ritme_idx, key="fiets_ritme")

    effort_options = ["Significant doorgevoerd", "Submaximale inspanning"]
    parsed_effort_idx = _prefill_select(effort_options, parsed_measurements.effort_type if parsed_measurements else None)

    # Suggest effort_type automatic when maximal HR < 80% of predicted, but allow manual override
    try:
        default_effort_idx = parsed_effort_idx
        fietstest_age = active_patient_ctx.leeftijd if active_patient_ctx.leeftijd is not None else leeftijd
        predicted_max_hr_live = 208 - 0.7 * float(fietstest_age)
        if predicted_max_hr_live and max_hr and max_hr > 0:
            if float(max_hr) < 0.8 * float(predicted_max_hr_live):
                default_effort_idx = 1
    except Exception:
        default_effort_idx = parsed_effort_idx or 0

    effort_type = st.selectbox("Type inspanning", effort_options, index=effort_options.index(st.session_state.get("fiets_effort_type", effort_options[default_effort_idx])) if st.session_state.get("fiets_effort_type") in effort_options else default_effort_idx, key="fiets_effort_type")

    stop_options = ["vermoeidheid", "maximale fietsproef", "dyspnee", "angor", "ECG afwijkingen"]
    stop_idx = _prefill_select(stop_options, parsed_measurements.stop_criterium if parsed_measurements else None)
    stop_criterium = st.selectbox("Criterium voor staken", stop_options, index=stop_options.index(st.session_state.get("fiets_stop_criterium", stop_options[stop_idx])) if st.session_state.get("fiets_stop_criterium") in stop_options else stop_idx, key="fiets_stop_criterium")

    ecg_options = [
        "geen significante veranderingen",
        "J-punt depressie",
        "upsloping ST-segment depressie",
        "horizontale ST-segment depressie met J-80 >1mm",
        "down-sloping ST-segment depressie met J-80 >1mm"
    ]
    ecg_idx = _prefill_select(ecg_options, parsed_measurements.ecg_changes if parsed_measurements else None)
    ecg_changes = st.selectbox("ECG tijdens inspanning/recuperatie", ecg_options, index=ecg_options.index(st.session_state.get("fiets_ecg_changes", ecg_options[ecg_idx])) if st.session_state.get("fiets_ecg_changes") in ecg_options else ecg_idx, key="fiets_ecg_changes")

    conclusion_options = ["Normale fietsproef", "Abnormale fietsproef"]
    conclusion_idx = _prefill_select(conclusion_options, parsed_measurements.conclusion if parsed_measurements else None)
    conclusion = st.selectbox("Conclusie", conclusion_options, index=conclusion_options.index(st.session_state.get("fiets_conclusion", conclusion_options[conclusion_idx])) if st.session_state.get("fiets_conclusion") in conclusion_options else conclusion_idx, key="fiets_conclusion")

    measurements = FietstestMeasurements(
        patient=active_patient_ctx,
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

    metrics: FietstestMetrics = compute_fietstest_metrics(measurements)
    predicted_max_hr = metrics.predicted_max_hr
    pct_hr_display = metrics.pct_hr_display
    vo2_observed = metrics.vo2_observed
    vo2_observed_text = metrics.vo2_observed_text
    pct_vs50_ui = metrics.vo2_percentile_pct
    band_ui = metrics.vo2_band
    band_text_ui = metrics.vo2_band_text
    Wpred = metrics.wpred
    Wpred_pct = metrics.wpred_pct
    summary_lines = metrics.summary_lines

    if summary_lines:
        st.markdown("**Directe berekeningen:**")
        for s in summary_lines:
            st.write("- ", s)

    brief_fietstest = summarize_fietstest_for_brief(measurements, metrics)
    final = generate_fietstest_report(measurements, metrics)
    snapshot = StudySnapshot(patient=active_patient_ctx, fietstest=measurements)
    snapshot.report_texts["brief_fietstest"] = brief_fietstest
    snapshot.report_texts["full_fietstest"] = final
    # snapshot download removed per UI simplification

    if st.button("Genereer fietsproef verslag"):
        _remember_brief_section(
            "brief_fietstest",
            brief_fietstest,
            active_patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        _remember_brief_section(
            "full_fietstest",
            final,
            active_patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        backend_study_id = _post_snapshot_to_backend("fietstest", snapshot)
        if backend_study_id:
            st.info(f"Opgeslagen naar backend (study {backend_study_id}).")
        st.subheader("Gegenereerd Fietstest Verslag")
        show_report_actions(final)
    st.stop()


if 'module' in globals() and module == "ECG":
    st.header("ECG Analyse")
    st.markdown("Importeer een ECG-rapport of vul de waarden manueel in.")

    uploaded_pdf = st.file_uploader("Importeer ECG PDF", type=["pdf"])
    pdf_ingest_ready = pdf_dependency_available()
    if not pdf_ingest_ready:
        st.info(f"PDF import tijdelijk niet beschikbaar: {PDF_DEPENDENCY_MESSAGE}")
    parsed_patient_ctx = None
    parsed_measurements = None
    parse_warnings: List[str] = []

    if uploaded_pdf is not None:
        if not pdf_ingest_ready:
            st.error("Kon PDF niet verwerken omdat pdfplumber ontbreekt.")
        else:
            raw_bytes = uploaded_pdf.getvalue()
            backend_resp = _post_pdf_to_backend("/api/ingest/ecg-pdf", raw_bytes, uploaded_pdf.name)

            if backend_resp:
                patient_payload = backend_resp.get("patient") or {}
                measurement_payload = backend_resp.get("measurements") or {}
                parse_warnings = backend_resp.get("warnings") or []

                if patient_payload:
                    parsed_patient_ctx = _patient_from_payload(patient_payload)
                    if parsed_patient_ctx and parsed_patient_ctx.bsa is None and parsed_patient_ctx.length and parsed_patient_ctx.weight:
                        parsed_patient_ctx = PatientContext(
                            sex=parsed_patient_ctx.sex,
                            patient_id=parsed_patient_ctx.patient_id,
                            full_name=parsed_patient_ctx.full_name,
                            date_of_birth=parsed_patient_ctx.date_of_birth,
                            leeftijd=parsed_patient_ctx.leeftijd,
                            bsa=bsa_mosteller(parsed_patient_ctx.length, parsed_patient_ctx.weight),
                            weight=parsed_patient_ctx.weight,
                            length=parsed_patient_ctx.length,
                        )

                target_ctx = parsed_patient_ctx or patient_ctx
                if measurement_payload and target_ctx:
                    parsed_measurements = ECGMeasurements(
                        patient=target_ctx,
                        recorded_at=measurement_payload.get("recorded_at"),
                        vent_rate=measurement_payload.get("vent_rate"),
                        pr_interval_ms=measurement_payload.get("pr_interval_ms"),
                        qrs_duration_ms=measurement_payload.get("qrs_duration_ms"),
                        qt_interval_ms=measurement_payload.get("qt_interval_ms"),
                        qtc_interval_ms=measurement_payload.get("qtc_interval_ms"),
                        p_axis_deg=measurement_payload.get("p_axis_deg"),
                        qrs_axis_deg=measurement_payload.get("qrs_axis_deg"),
                        t_axis_deg=measurement_payload.get("t_axis_deg"),
                        rhythm_summary=measurement_payload.get("rhythm_summary"),
                        auto_report_text=measurement_payload.get("auto_report_text"),
                        acquisition_device=measurement_payload.get("acquisition_device"),
                    )
                study_id = backend_resp.get("study_id")
                if study_id:
                    st.info(f"ECG opgeslagen in backend (study {study_id}).")
            else:
                parsed_patient_ctx, parsed_measurements, parse_warnings = parse_ecg_pdf(raw_bytes)
                if parsed_patient_ctx:
                    parsed_patient_ctx = PatientContext(
                        sex=parsed_patient_ctx.sex,
                        patient_id=parsed_patient_ctx.patient_id,
                        full_name=parsed_patient_ctx.full_name,
                        date_of_birth=parsed_patient_ctx.date_of_birth,
                        leeftijd=parsed_patient_ctx.leeftijd,
                        bsa=parsed_patient_ctx.bsa,
                        weight=parsed_patient_ctx.weight,
                        length=parsed_patient_ctx.length,
                    )
            if parsed_patient_ctx:
                prefill_patient_sidebar(parsed_patient_ctx)
                st.success("ECG PDF succesvol ingelezen. Velden vooraf ingevuld.")
            if parse_warnings:
                for warning in parse_warnings:
                    st.warning(warning)

    active_patient_ctx = parsed_patient_ctx or patient_ctx

    def _prefill_float(value: Optional[float], fallback: float) -> float:
        try:
            return float(value) if value is not None else fallback
        except Exception:
            return fallback

    def _value_or_none(value: float) -> Optional[float]:
        return value if value > 0 else None

    def _format_axis(value: Optional[float]) -> str:
        if value is None:
            return ""
        try:
            return f"{float(value):.0f}"
        except Exception:
            return ""

    def _parse_optional_float(text_value: str) -> Optional[float]:
        stripped = text_value.strip().replace(",", ".")
        if stripped == "":
            return None
        try:
            return float(stripped)
        except Exception:
            return None

    recorded_at_default = parsed_measurements.recorded_at if parsed_measurements else ""
    recorded_at = st.text_input("Registratiedatum", value=recorded_at_default)

    vent_rate = st.number_input("Vent. frequentie (bpm)", min_value=0.0, max_value=300.0, value=_prefill_float(parsed_measurements.vent_rate if parsed_measurements else None, 0.0))
    pr_interval = st.number_input("PR (ms)", min_value=0.0, max_value=400.0, value=_prefill_float(parsed_measurements.pr_interval_ms if parsed_measurements else None, 0.0))
    qrs_duration = st.number_input("QRS (ms)", min_value=0.0, max_value=400.0, value=_prefill_float(parsed_measurements.qrs_duration_ms if parsed_measurements else None, 0.0))
    qt_interval = st.number_input("QT (ms)", min_value=0.0, max_value=600.0, value=_prefill_float(parsed_measurements.qt_interval_ms if parsed_measurements else None, 0.0))
    qtc_interval = st.number_input("QTc (ms)", min_value=0.0, max_value=650.0, value=_prefill_float(parsed_measurements.qtc_interval_ms if parsed_measurements else None, 0.0))

    p_axis_text = st.text_input("P-as (°)", value=_format_axis(parsed_measurements.p_axis_deg if parsed_measurements else None))
    qrs_axis_text = st.text_input("QRS-as (°)", value=_format_axis(parsed_measurements.qrs_axis_deg if parsed_measurements else None))
    t_axis_text = st.text_input("T-as (°)", value=_format_axis(parsed_measurements.t_axis_deg if parsed_measurements else None))

    rhythm_default = parsed_measurements.rhythm_summary if parsed_measurements else ""
    rhythm_summary = st.text_area("Ritme omschrijving", value=rhythm_default, height=80)

    auto_text_default = parsed_measurements.auto_report_text if parsed_measurements else ""
    auto_report_text = st.text_area("Automatische protocolering", value=auto_text_default, height=120)

    device_default = parsed_measurements.acquisition_device if parsed_measurements else ""
    acquisition_device = st.text_input("Toestel", value=device_default)

    measurements = ECGMeasurements(
        patient=active_patient_ctx,
        recorded_at=recorded_at or None,
        vent_rate=_value_or_none(vent_rate),
        pr_interval_ms=_value_or_none(pr_interval),
        qrs_duration_ms=_value_or_none(qrs_duration),
        qt_interval_ms=_value_or_none(qt_interval),
        qtc_interval_ms=_value_or_none(qtc_interval),
        p_axis_deg=_parse_optional_float(p_axis_text),
        qrs_axis_deg=_parse_optional_float(qrs_axis_text),
        t_axis_deg=_parse_optional_float(t_axis_text),
        rhythm_summary=rhythm_summary or None,
        auto_report_text=auto_report_text or None,
        acquisition_device=acquisition_device or None,
    )

    metrics = compute_ecg_metrics(measurements)
    if metrics.summary_lines:
        st.markdown("**Automatische berekeningen:**")
        for line in metrics.summary_lines:
            st.write("- ", line)

    brief_ecg = summarize_ecg_for_brief(measurements, metrics)
    final = generate_ecg_report(measurements, metrics)
    snapshot = StudySnapshot(patient=active_patient_ctx, ecg=measurements)
    snapshot.report_texts["brief_ecg"] = brief_ecg
    snapshot.report_texts["full_ecg"] = final
    # snapshot download removed per UI simplification

    if st.button("Genereer ECG verslag"):
        # Always remember ECG texts locally (patient_id may be None and will map to default bucket)
        _remember_brief_section(
            "brief_ecg",
            brief_ecg,
            active_patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        _remember_brief_section(
            "full_ecg",
            final,
            active_patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        backend_study_id = _post_snapshot_to_backend("ecg", snapshot)
        if backend_study_id:
            st.info(f"Opgeslagen naar backend (study {backend_study_id}).")
        st.subheader("Gegenereerd ECG Verslag")
        show_report_actions(final)
    st.stop()


# -----------------------------
# CIED Follow-up Module
# -----------------------------
if 'module' in globals() and module == "CIED follow-up":
    st.header("CIED Follow-up")
    st.markdown("Vul apparaatgegevens en meetwaarden in voor het follow-up verslag.")

    cied_device_options = ["conduction system pacemaker", "pacemaker", "ICD", "CRT-P", "CRT-D", "Andere"]
    device_type = st.selectbox("Type apparaat", cied_device_options, index=cied_device_options.index(st.session_state.get("cied_device_type", "conduction system pacemaker")) if st.session_state.get("cied_device_type") in cied_device_options else 0, key="cied_device_type")
    cied_brand_options = ["Biotronik", "Medtronic", "Boston-Scientific", "Abbott", "Sorin"]
    device_brand = st.selectbox("Merk", cied_brand_options, index=cied_brand_options.index(st.session_state.get("cied_device_brand", "Biotronik")) if st.session_state.get("cied_device_brand") in cied_brand_options else 0, key="cied_device_brand")
    # Programming mode and rate settings
    cied_mode_options = ["DDD", "DDDR", "DDD-CLS", "VVI", "VVIR", "AAI", "AAIR", "Andere"]
    programming_mode = st.selectbox("Programmering modus", cied_mode_options, index=cied_mode_options.index(st.session_state.get("cied_programming_mode", "DDD")) if st.session_state.get("cied_programming_mode") in cied_mode_options else 0, key="cied_programming_mode")
    lower_rate = st.number_input("Lower rate (bpm)", min_value=30, max_value=120, value=st.session_state.get("cied_lower_rate", 60), key="cied_lower_rate")
    # compute and show myPACE suggestion immediately under lower_rate
    try:
        mypace_suggest = None
        lvef_raw = st.session_state.get("lvef", "")
        try:
            lvef_val = float(str(lvef_raw).strip()) if str(lvef_raw).strip() != "" else None
        except Exception:
            lvef_val = None
        if length and lvef_val is not None and float(lvef_val) > 0:
            # formula: ((Height_cm * -0.37) + 135) * sqrt(sqrt(LVEF/50))
            factor = None
            try:
                ratio = float(lvef_val) / 50.0
                if ratio > 0:
                    factor = math.sqrt(math.sqrt(ratio))
            except Exception:
                pass
            if factor is not None:
                mypace_val = ((float(length) * -0.37) + 135.0) * factor
                mypace_suggest = int(round(mypace_val))
    except Exception:
        mypace_suggest = None
    if mypace_suggest is not None:
        st.caption(f"myPACE (if HFpEF) suggested lower rate: {mypace_suggest} bpm")

    upper_tracking = st.number_input("Upper tracking rate (bpm)", min_value=80, max_value=210, value=st.session_state.get("cied_upper_tracking", 130), key="cied_upper_tracking")
    # predicted max HR and upper suggestion shown under upper_tracking
    try:
        upper_suggest = None
        predicted_max_hr = None
        if leeftijd is not None:
            try:
                predicted_max_hr = round(208 - 0.7 * float(leeftijd))
                upper_suggest = int(round(predicted_max_hr * 0.85))
            except Exception:
                upper_suggest = None
    except Exception:
        upper_suggest = None
    if upper_suggest is not None:
        try:
            st.caption(f"Suggested upper tracking rate: {upper_suggest} bpm (≈85% of predicted max HR {predicted_max_hr} bpm)")
        except Exception:
            st.caption(f"Suggested upper tracking rate: {upper_suggest} bpm")
    
    # AV delay inputs (ms) - optional (blank by default)
    sensed_av_delay = st.text_input("Sensed AV delay (ms)", value="", placeholder="Laat leeg indien onbekend", key="sensed_av_delay")
    paced_av_delay = st.text_input("Paced AV delay (ms)", value="", placeholder="Laat leeg indien onbekend", key="paced_av_delay")
    # compute optimal AV reduction: 5 ms per 10 bpm increment between lower and upper tracking
    try:
        hr_diff = int(upper_tracking) - int(lower_rate)
        av_reduction = int(round((hr_diff / 10.0) * 5.0)) if hr_diff > 0 else 0
        # parse baseline AV delays if provided
        def parse_int_nullable(s):
            try:
                if s is None:
                    return None
                ss = str(s).strip()
                if ss == "":
                    return None
                return int(float(ss))
            except Exception:
                return None

        base_sensed = parse_int_nullable(sensed_av_delay)
        base_paced = parse_int_nullable(paced_av_delay)
        suggested_sensed_av = max(50, base_sensed - av_reduction) if base_sensed is not None else None
        suggested_paced_av = max(50, base_paced - av_reduction) if base_paced is not None else None
        # Build caption: always show av_reduction; show rate-adaptive values only if baseline provided
        cap_parts = [f"Optimal AV delay reduction: {av_reduction} ms (≈5 ms per 10 bpm)."]
        if suggested_sensed_av is not None:
            cap_parts.append(f"Rate-adaptive sensed AV delay at peak UTR: {suggested_sensed_av} ms")
        if suggested_paced_av is not None:
            cap_parts.append(f"Rate-adaptive paced AV delay at peak UTR: {suggested_paced_av} ms")
        # Compute optimal PVARP when upper tracking rate and sensed AV delay known
        try:
            if base_sensed is not None and upper_tracking is not None and str(upper_tracking).strip() != "":
                utr_val = int(float(upper_tracking))
                if utr_val > 0:
                    pvarp_opt = int(round(60000.0 / utr_val - base_sensed - 20.0))
                    if pvarp_opt < 0:
                        pvarp_opt = 0
                    cap_parts.append(f"Optimal PVARP: {pvarp_opt} ms (60000 / UTR - sensed AV delay - 20 ms)")
        except Exception:
            pass
        st.caption(" ".join(cap_parts))
        # Recommend sensed AV delay = paced AV delay - 30 ms (show and allow apply)
        try:
            # use parse_int_nullable from this scope
            def parse_int_nullable_local(s):
                try:
                    if s is None:
                        return None
                    ss = str(s).strip()
                    if ss == "":
                        return None
                    return int(float(ss))
                except Exception:
                    return None

            base_paced_local = parse_int_nullable_local(paced_av_delay)
            base_sensed_local = parse_int_nullable_local(sensed_av_delay)
            if base_paced_local is not None:
                recommended_sensed_from_paced = max(50, base_paced_local - 30)
                if base_sensed_local is None or base_sensed_local != recommended_sensed_from_paced:
                    st.caption(f"Recommended sensed AV delay based on paced AV delay: {recommended_sensed_from_paced} ms (paced - 30).")
                    if st.button("Apply recommended sensed AV delay"):
                        st.session_state["sensed_av_delay"] = str(recommended_sensed_from_paced)
        except Exception:
            pass
    except Exception:
        av_reduction = None
        suggested_sensed_av = None
        suggested_paced_av = None
    cied_indication_options = [
        "sinusknoopdysfunctie",
        "paroxysmaal AV-blok",
        "permanent AV-blok",
        "permanente voorkamerfibrillatie met traag ventriculair antwoord",
        "Andere",
    ]
    indication_sel = st.selectbox("Indicatie / reden voor implantatie", cied_indication_options, index=cied_indication_options.index(st.session_state.get("cied_indication_sel", "sinusknoopdysfunctie")) if st.session_state.get("cied_indication_sel") in cied_indication_options else 0, key="cied_indication_sel")
    if indication_sel == "Andere":
        indication_text = st.text_input("Andere indicatie, specificeer", value=st.session_state.get("cied_indication_text", ""), key="cied_indication_text")
    else:
        indication_text = indication_sel

    # Leads presence selection (RA and RV default checked)
    st.markdown("**Leads aanwezig**")
    leads_col1, leads_col2, leads_col3 = st.columns(3)
    with leads_col1:
        lead_ra = st.checkbox("RA", value=st.session_state.get("cied_lead_ra", True), key="cied_lead_ra")
        lead_rv = st.checkbox("RV", value=st.session_state.get("cied_lead_rv", True), key="cied_lead_rv")
    with leads_col2:
        lead_lv = st.checkbox("LV (coronary sinus)", value=st.session_state.get("cied_lead_lv", False), key="cied_lead_lv")
    with leads_col3:
        other_leads = st.text_input("Andere leads (specificeer)", value=st.session_state.get("cied_other_leads", ""), key="cied_other_leads")

    st.markdown("**Algemene metingen**")
    col_a, col_b = st.columns(2)
    with col_a:
        sensing_ok = st.checkbox("Sensing OK (globaal)", value=st.session_state.get("cied_sensing_ok", True), key="cied_sensing_ok")
        pacing_ok = st.checkbox("Pacing OK (globaal)", value=st.session_state.get("cied_pacing_ok", True), key="cied_pacing_ok")
    with col_b:
        impedance_ok = st.checkbox("Impedanties OK (globaal)", value=st.session_state.get("cied_impedance_ok", True), key="cied_impedance_ok")
        cied_egm_options = ["Geen events", "Atriale events", "Ventriculaire events", "Andere"]
        egm_events = st.selectbox("EGM events", cied_egm_options, index=cied_egm_options.index(st.session_state.get("cied_egm_events", "Geen events")) if st.session_state.get("cied_egm_events") in cied_egm_options else 0, key="cied_egm_events")

    # Pacing percentages (optional — laat leeg als onbekend)
    colp1, colp2, colp3 = st.columns(3)
    with colp1:
        atrial_pacing_pct = st.text_input("Atrium pacing (%)", value=st.session_state.get("cied_atrial_pacing_pct", ""), placeholder="% leeg laat veld weg", key="cied_atrial_pacing_pct")
    with colp2:
        ventricular_pacing_pct = st.text_input("Ventrikel pacing (%)", value=st.session_state.get("cied_ventricular_pacing_pct", ""), placeholder="% leeg laat veld weg", key="cied_ventricular_pacing_pct")
    with colp3:
        if 'lead_lv' in locals() and lead_lv:
            lv_pacing_pct = st.text_input("LV pacing (%)", value=st.session_state.get("cied_lv_pacing_pct", ""), placeholder="% leeg laat veld weg", key="cied_lv_pacing_pct")
        else:
            lv_pacing_pct = ""

    settings_changed = st.checkbox("Instellingen gewijzigd (ten opzichte van vorige follow-up)", value=st.session_state.get("cied_settings_changed", False), key="cied_settings_changed")
    patient_dependent = st.checkbox("Patiënt afhankelijk", value=st.session_state.get("cied_patient_dependent", False), key="cied_patient_dependent")

    battery_status = st.text_input("Batterijstatus (bv. 2.9V, 2+ jaar resterend)", value=st.session_state.get("cied_battery_status", ""), key="cied_battery_status")

    # Per-lead detailed inputs
    st.markdown("**Leads — detailwaarden**")
    # Atrial lead details
    if lead_ra:
        st.markdown("**Atrium (RA) — waarden**")
        col1, col2, col3 = st.columns(3)
        with col1:
            atrial_sensing = st.text_input("Atrium sensing (mV)", value=st.session_state.get("cied_atrial_sensing", ""), key="cied_atrial_sensing")
            atrial_impedance = st.text_input("Atrium impedantie (Ω)", value=st.session_state.get("cied_atrial_impedance", ""), key="cied_atrial_impedance")
        with col2:
            atrial_threshold_v = st.text_input("Atrium drempel (V)", value=st.session_state.get("cied_atrial_threshold_v", ""), key="cied_atrial_threshold_v")
            atrial_threshold_ms = st.text_input("Atrium drempel (ms)", value=st.session_state.get("cied_atrial_threshold_ms", ""), key="cied_atrial_threshold_ms")
        with col3:
            cied_polarity_options = ["Unipolair", "Bipolair"]
            atrial_polarity = st.selectbox("Atrium polariteit", cied_polarity_options, index=cied_polarity_options.index(st.session_state.get("cied_atrial_polarity", "Bipolair")) if st.session_state.get("cied_atrial_polarity") in cied_polarity_options else 1, key="cied_atrial_polarity")
            atrial_stable = st.checkbox("Atrium stabiel", value=st.session_state.get("cied_atrial_stable", True), key="cied_atrial_stable")
        # optional location for atrial lead
        atrial_location = st.text_input("Atrium locatie (bv. RAA)", value=st.session_state.get("cied_atrial_location", ""), key="cied_atrial_location")
    else:
        atrial_sensing = atrial_impedance = atrial_threshold_v = atrial_threshold_ms = atrial_polarity = None
        atrial_stable = None
        atrial_location = ""

    # Ventricular lead details
    if lead_rv:
        st.markdown("**Ventrikel (RV) — waarden**")
        col1, col2, col3 = st.columns(3)
        with col1:
            vent_sensing = st.text_input("Ventrikel sensing (mV)", value=st.session_state.get("cied_vent_sensing", ""), key="cied_vent_sensing")
            vent_impedance = st.text_input("Ventrikel impedantie (Ω)", value=st.session_state.get("cied_vent_impedance", ""), key="cied_vent_impedance")
        with col2:
            vent_threshold_v = st.text_input("Ventrikel drempel (V)", value=st.session_state.get("cied_vent_threshold_v", ""), key="cied_vent_threshold_v")
            vent_threshold_ms = st.text_input("Ventrikel drempel (ms)", value=st.session_state.get("cied_vent_threshold_ms", ""), key="cied_vent_threshold_ms")
        with col3:
            vent_polarity = st.selectbox("Ventrikel polariteit", cied_polarity_options, index=cied_polarity_options.index(st.session_state.get("cied_vent_polarity", "Bipolair")) if st.session_state.get("cied_vent_polarity") in cied_polarity_options else 1, key="cied_vent_polarity")
            vent_stable = st.checkbox("Ventrikel stabiel", value=st.session_state.get("cied_vent_stable", True), key="cied_vent_stable")
        vent_location = st.text_input("Ventrikel locatie (bv. LBBB)", value=st.session_state.get("cied_vent_location", ""), key="cied_vent_location")
    else:
        vent_sensing = vent_impedance = vent_threshold_v = vent_threshold_ms = vent_polarity = None
        vent_stable = None
        vent_location = ""

    # LV (coronary sinus) lead details (shown only if LV lead present)
    if lead_lv:
        st.markdown("**LV (CS) — waarden**")
        col1, col2, col3 = st.columns(3)
        with col1:
            lv_sensing = st.text_input("LV sensing (mV)", value=st.session_state.get("cied_lv_sensing", ""), key="cied_lv_sensing")
            lv_impedance = st.text_input("LV impedantie (Ω)", value=st.session_state.get("cied_lv_impedance", ""), key="cied_lv_impedance")
        with col2:
            lv_threshold_v = st.text_input("LV drempel (V)", value=st.session_state.get("cied_lv_threshold_v", ""), key="cied_lv_threshold_v")
            lv_threshold_ms = st.text_input("LV drempel (ms)", value=st.session_state.get("cied_lv_threshold_ms", ""), key="cied_lv_threshold_ms")
        with col3:
            lv_polarity = st.selectbox("LV polariteit", cied_polarity_options, index=cied_polarity_options.index(st.session_state.get("cied_lv_polarity", "Bipolair")) if st.session_state.get("cied_lv_polarity") in cied_polarity_options else 1, key="cied_lv_polarity")
            lv_stable = st.checkbox("LV stabiel", value=st.session_state.get("cied_lv_stable", True), key="cied_lv_stable")
        lv_location = st.text_input("LV locatie (bv. CS lat)", value=st.session_state.get("cied_lv_location", ""), key="cied_lv_location")
    else:
        lv_sensing = lv_impedance = lv_threshold_v = lv_threshold_ms = lv_polarity = None
        lv_stable = None
        lv_location = ""

    atrial_fields = LeadMeasurements(
        sensing=atrial_sensing,
        impedance=atrial_impedance,
        threshold_v=atrial_threshold_v,
        threshold_ms=atrial_threshold_ms,
        polarity=atrial_polarity,
        stable=atrial_stable,
        location=atrial_location,
    )
    vent_fields = LeadMeasurements(
        sensing=vent_sensing,
        impedance=vent_impedance,
        threshold_v=vent_threshold_v,
        threshold_ms=vent_threshold_ms,
        polarity=vent_polarity,
        stable=vent_stable,
        location=vent_location,
    )
    lv_fields = LeadMeasurements(
        sensing=lv_sensing,
        impedance=lv_impedance,
        threshold_v=lv_threshold_v,
        threshold_ms=lv_threshold_ms,
        polarity=lv_polarity,
        stable=lv_stable,
        location=lv_location,
    )

    cied_context = CIEDReportInput(
        patient=patient_ctx,
        device_type=device_type,
        device_brand=device_brand,
        programming_mode=programming_mode,
        lower_rate=lower_rate,
        upper_tracking=upper_tracking,
        indication_text=indication_text,
        lead_ra=lead_ra,
        lead_rv=lead_rv,
        lead_lv=lead_lv,
        other_leads=other_leads,
        sensing_ok=sensing_ok,
        pacing_ok=pacing_ok,
        impedance_ok=impedance_ok,
        egm_events=egm_events,
        atrial_pacing_pct=atrial_pacing_pct,
        ventricular_pacing_pct=ventricular_pacing_pct,
        lv_pacing_pct=lv_pacing_pct,
        settings_changed=settings_changed,
        patient_dependent=patient_dependent,
        battery_status=battery_status,
        suggested_sensed_av=suggested_sensed_av,
        suggested_paced_av=suggested_paced_av,
        sensed_av_delay=sensed_av_delay,
        paced_av_delay=paced_av_delay,
        atrial_fields=atrial_fields,
        vent_fields=vent_fields,
        lv_fields=lv_fields,
    )

    final = generate_cied_report(cied_context)
    cied_snapshot = StudySnapshot(patient=patient_ctx, cied=cied_context)
    cied_snapshot.report_texts["full_cied"] = final

    # snapshot download removed per UI simplification
    if st.button("Genereer CIED verslag"):
        # Always remember full CIED locally (patient_id may be None)
        _remember_brief_section(
            "full_cied",
            final,
            patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        backend_study_id = _post_snapshot_to_backend("cied", cied_snapshot)
        if backend_study_id:
            st.info(f"Opgeslagen naar backend (study {backend_study_id}).")
        st.subheader("Gegenereerd CIED Verslag")
        show_report_actions(final)
        st.stop()

    # End CIED module — prevent rendering of subsequent modules when CIED selected
    st.stop()

# -----------------------------
# Holter Monitoring Module
# -----------------------------
if 'module' in globals() and module == "Holter":
    st.header("Holter-monitoring")
    st.markdown("Vul de Holter-resultaten in en genereer het verslag.")

    st.subheader("Registratie-informatie")
    c1, c2 = st.columns(2)
    with c1:
        recording_date = st.date_input("Registratiedatum", value=st.session_state.get("holter_recording_date", datetime.date.today()), key="holter_recording_date")
    with c2:
        recording_duration = st.number_input("Registratieduur (uur)", min_value=1, max_value=168, value=st.session_state.get("holter_recording_duration", 24), key="holter_recording_duration")

    st.subheader("Hartfrequentie analyse")
    c1, c2, c3 = st.columns(3)
    with c1:
        avg_hr = st.number_input("Gemiddelde HR (bpm)", min_value=0, max_value=300, value=st.session_state.get("holter_avg_hr", 75), key="holter_avg_hr")
    with c2:
        min_hr = st.number_input("Minimale HR (bpm)", min_value=0, max_value=300, value=st.session_state.get("holter_min_hr", 45), key="holter_min_hr")
    with c3:
        max_hr_holter = st.number_input("Maximale HR (bpm)", min_value=0, max_value=300, value=st.session_state.get("holter_max_hr", 120), key="holter_max_hr")

    st.subheader("Ritme-analyse")
    c1, c2 = st.columns(2)
    with c1:
        afib_percentage = st.number_input("Atriumfibrilleren (%)", min_value=0.0, max_value=100.0, value=st.session_state.get("holter_afib_percentage", 0.0), step=0.1, key="holter_afib_percentage")
    with c2:
        av_block_options = ["Geen", "1e graads AV-blok", "2e graads AV-blok type I (Wenckebach)", "2e graads AV-blok type II", "3e graads AV-blok (totaal)"]
        av_block_type = st.selectbox("AV-blok", av_block_options, index=av_block_options.index(st.session_state.get("holter_av_block_type", "Geen")) if st.session_state.get("holter_av_block_type") in av_block_options else 0, key="holter_av_block_type")

    st.subheader("Pauzes")
    c1, c2 = st.columns(2)
    with c1:
        pauses_count = st.number_input("Aantal pauzes", min_value=0, max_value=10000, value=st.session_state.get("holter_pauses_count", 0), key="holter_pauses_count")
    with c2:
        longest_pause_ms = st.number_input("Langste pauze (ms)", min_value=0, max_value=30000, value=st.session_state.get("holter_longest_pause_ms", 0), key="holter_longest_pause_ms")

    st.subheader("Ectopie")
    c1, c2 = st.columns(2)
    with c1:
        ves_count = st.number_input("VES (ventriculaire extrasystolen)", min_value=0, max_value=100000, value=st.session_state.get("holter_ves_count", 0), key="holter_ves_count")
    with c2:
        sves_count = st.number_input("SVES (supraventriculaire extrasystolen)", min_value=0, max_value=100000, value=st.session_state.get("holter_sves_count", 0), key="holter_sves_count")

    other_findings = st.text_area("Overige bevindingen", value=st.session_state.get("holter_other_findings", ""), height=100, key="holter_other_findings")

    measurements = HolterMeasurements(
        patient=patient_ctx,
        recording_date=recording_date.strftime("%d-%m-%Y"),
        recording_duration_hours=recording_duration,
        avg_hr=avg_hr if avg_hr > 0 else None,
        min_hr=min_hr if min_hr > 0 else None,
        max_hr=max_hr_holter if max_hr_holter > 0 else None,
        afib_percentage=afib_percentage if afib_percentage > 0 else None,
        pauses_count=pauses_count if pauses_count > 0 else None,
        longest_pause_ms=longest_pause_ms if longest_pause_ms > 0 else None,
        ves_count=ves_count if ves_count > 0 else None,
        sves_count=sves_count if sves_count > 0 else None,
        av_block_type=av_block_type if av_block_type != "Geen" else None,
        other_findings=other_findings.strip() if other_findings.strip() else None,
    )

    metrics: HolterMetrics = compute_holter_metrics(measurements)

    if metrics.summary_lines:
        st.markdown("**Samenvatting:**")
        for s in metrics.summary_lines:
            st.write("- ", s)

    # Generate report
    final = generate_holter_report(measurements, metrics)

    # Brief summary (simplified version for consultation letter)
    brief_holter_lines = []
    if measurements.recording_duration_hours:
        brief_holter_lines.append(f"Holter-monitoring ({measurements.recording_duration_hours}u)")
    if measurements.avg_hr:
        brief_holter_lines.append(f"Gem. HR: {measurements.avg_hr} bpm")
    if metrics.afib_detected:
        brief_holter_lines.append(f"AFIB: {measurements.afib_percentage}%")
    if metrics.significant_pauses:
        brief_holter_lines.append("Significante pauzes")
    if metrics.frequent_ves:
        brief_holter_lines.append(f"Frequente VES ({measurements.ves_count})")
    if metrics.frequent_sves:
        brief_holter_lines.append(f"Frequente SVES ({measurements.sves_count})")
    
    brief_holter = "; ".join(brief_holter_lines) if brief_holter_lines else "Holter-monitoring uitgevoerd"

    snapshot = StudySnapshot(patient=patient_ctx)
    snapshot.report_texts["brief_holter"] = brief_holter
    snapshot.report_texts["full_holter"] = final

    if st.button("Genereer Holter verslag"):
        _remember_brief_section(
            "brief_holter",
            brief_holter,
            patient_ctx.patient_id,
            recording_date.isoformat(),
        )
        _remember_brief_section(
            "full_holter",
            final,
            patient_ctx.patient_id,
            recording_date.isoformat(),
        )
        backend_study_id = _post_snapshot_to_backend("holter", snapshot)
        if backend_study_id:
            st.info(f"Opgeslagen naar backend (study {backend_study_id}).")
        st.subheader("Gegenereerd Holter Verslag")
        show_report_actions(final)
        st.stop()

    # End Holter module
    st.stop()

# layout columns for summary/status widgets
if module == "Echo":
    with st.expander("1. Keuzes LV en LA", expanded=False):
        col1, col2 = st.columns(2)

    try:
        lvef_class = classify_lvef(float(lvef), sex) if lvef is not None and str(lvef).strip() != "" else None
    except Exception:
        lvef_class = None
    automatic_systolic = lvef_to_systolic_option(lvef_class) if lvef_class is not None else "goede globale en regionale systolische functie"

    with col1:
        # Automatic LV geometry calculations (use values above) — only if measurements present
        if ivsd is not None and lvidd is not None and lvpw is not None:
            lv_mass_g = compute_lv_mass_g(ivsd, lvidd, lvpw)
            rwt = compute_rwt(lvpw, lvidd)
            mass_index, mass_severity = lv_mass_index_severity(lv_mass_g, bsa, sex)
            lv_hypertrofie_auto = determine_lv_geometry(mass_index, mass_severity, rwt)
        else:
            lv_mass_g = None
            rwt = None
            mass_index = None
            mass_severity = None
            # default to normal when measurements not provided
            lv_hypertrofie_auto = "Normotroof"

        if lvidd is not None:
            lv_dilatatie_auto = classify_lvidd(lvidd, sex, bsa)
        else:
            # default to not dilated when LVIDd missing
            lv_dilatatie_auto = "niet gedilateerd"

        # Allow manual overrides while showing automatic suggestions
        lv_hypertrofie_choice = st.selectbox(
            "LV hypertrofie (automatisch geselecteerd)",
            [
                lv_hypertrofie_auto,
                "Eccentrisch hypertroof",
                "Verdikt interventriculair septum",
                "Concentrische remodeling",
                "Eccentrische remodeling",
                "Overig (specificeer)"
            ],
            index=0,
        )
        if lv_hypertrofie_choice == "Overig (specificeer)":
            lv_hypertrofie_choice = st.text_input("Specificeer LV hypertrofie", value="")

        lv_dilatatie_choice = st.selectbox(
            "LV dilatatie (automatisch geselecteerd)",
            [
                lv_dilatatie_auto,
                "niet gedilateerd",
                "mild gedilateerd",
                "matig gedilateerd",
                "ernstig gedilateerd",
                "Overig (specificeer)"
            ],
            index=0,
        )
        if lv_dilatatie_choice == "Overig (specificeer)":
            lv_dilatatie_choice = st.text_input("Specificeer LV dilatatie", value="")
        # Systolic function selectbox (suggested from LVEF) - placed here above diastolic function
        systolic_options_local = [
            "goede globale en regionale systolische functie",
            "mild verminderde globale systolische functie",
            "matig verminderde globale systolische functie",
            "ernstig verminderde globale systolische functie",
        ]
        try:
            default_systolic_idx = systolic_options_local.index(automatic_systolic) if automatic_systolic in systolic_options_local else 0
        except Exception:
            default_systolic_idx = 0
        systolic_option = st.selectbox("Systolische functie (gesuggereerd op basis van LVEF)", systolic_options_local, index=default_systolic_idx)
        # Automatic diastolic function suggestion based on E/A, E/e', LAVI and PASP
        ea = st.session_state.get("ea", None)
        ee = st.session_state.get("ee", None)
        try:
            pasp_val = None
            if st.session_state.get("pasp_raw", "") is not None and str(st.session_state.get("pasp_raw", "")).strip() != "":
                pasp_val = float(st.session_state.get("pasp_raw"))
        except Exception:
            pasp_val = None

        # default suggestion
        diastolic_suggestion = "Normale diastolische functie met normale vullingsdrukken in het linker atrium"
        try:
            if ea is not None:
                ea_val = float(ea)
                # Grade 1: E/A < 0.8
                if ea_val < 0.8:
                    diastolic_suggestion = "Diastolische dysfunctie graad 1 met normale vullingsdrukken in het linker atrium"
                # Grade 3: E/A > 2
                elif ea_val > 2:
                    diastolic_suggestion = "Diastolische dysfunctie graad 3 met ernstig gestegen vullingsdrukken in het linker atrium"
                else:
                    # between 0.8 and 2: check criteria (need >=2 true)
                    criteria = 0
                    try:
                        if ee is not None and float(ee) > 13:
                            criteria += 1
                    except Exception:
                        pass
                    try:
                        if lavi is not None and float(lavi) > 34:
                            criteria += 1
                    except Exception:
                        pass
                    try:
                        if pasp_val is not None and float(pasp_val) > 31:
                            criteria += 1
                    except Exception:
                        pass

                    if criteria >= 2:
                        diastolic_suggestion = "Diastolische dysfunctie graad 2 met gestegen vullingsdrukken in het linker atrium"
                    else:
                        diastolic_suggestion = "Normale diastolische functie met normale vullingsdrukken in het linker atrium"
        except Exception:
            diastolic_suggestion = "Normale diastolische functie met normale vullingsdrukken in het linker atrium"

        diastolic_options = [
            "Normale diastolische functie met normale vullingsdrukken in het linker atrium",
            "Diastolische dysfunctie graad 1 met normale vullingsdrukken in het linker atrium",
            "Diastolische dysfunctie graad 2 met gestegen vullingsdrukken in het linker atrium",
            "Diastolische dysfunctie graad 3 met ernstig gestegen vullingsdrukken in het linker atrium",
        ]
        try:
            default_idx = diastolic_options.index(diastolic_suggestion)
        except Exception:
            default_idx = 0

        lv_diastolische_functie = st.selectbox("Diastolische functie", diastolic_options, index=default_idx)
    with col2:
        # LA dilatatie selectbox (allow manual override; default to suggested or 'Niet gedilateerd')
        if la_suggested is not None:
            la_options = [la_suggested, "Niet gedilateerd", "Mild gedilateerd", "Matig gedilateerd", "Ernstig gedilateerd", "Overig (specificeer)"]
        else:
            la_options = ["Niet gedilateerd", "Mild gedilateerd", "Matig gedilateerd", "Ernstig gedilateerd", "Overig (specificeer)"]
        try:
            default_la_idx = 0
        except Exception:
            default_la_idx = 0
        la_choice = st.selectbox("LA dilatatie (automatisch geselecteerd)", la_options, index=default_la_idx)
        if la_choice == "Overig (specificeer)":
            la_choice = st.text_input("Specificeer LA dilatatie", value="")
# Suggest RV function from TAPSE (available from compact metrics / metingen)
rv_function_auto = classify_tapse(tapse)

# Parse RV free wall thickness (RVFWd) from compact metrics (blank by default)
rvfwd_val = None
try:
    rvfwd_raw = st.session_state.get('rvfwd', "")
    if rvfwd_raw is not None and str(rvfwd_raw).strip() != "":
        rvfwd_val = float(str(rvfwd_raw).strip())
    else:
        rvfwd_val = None
except Exception:
    rvfwd_val = None

# Parse RV basal and mid diameters (blank by default)
rvbd_val = None
rvmd_val = None
try:
    rvbd_raw = st.session_state.get('rvbd', "")
    if rvbd_raw is not None and str(rvbd_raw).strip() != "":
        rvbd_val = float(str(rvbd_raw).strip())
    else:
        rvbd_val = None
except Exception:
    rvbd_val = None

try:
    rvmd_raw = st.session_state.get('rvmd', "")
    if rvmd_raw is not None and str(rvmd_raw).strip() != "":
        rvmd_val = float(str(rvmd_raw).strip())
    else:
        rvmd_val = None
except Exception:
    rvmd_val = None

# Parse RA volume and compute RAVI (mL/m^2) when available
ravi_val = None
ra_volume_val = None
try:
    ra_raw = st.session_state.get('ra_volume', "")
    if ra_raw is not None and str(ra_raw).strip() != "":
        ra_volume_val = float(str(ra_raw).strip())
        try:
            if bsa and bsa > 0:
                ravi_val = round(ra_volume_val / float(bsa), 1)
        except Exception:
            ravi_val = None
    else:
        ra_volume_val = None
        ravi_val = None
except Exception:
    ra_volume_val = None
    ravi_val = None

# Parse Aorta measurements and compute indexed values (mm/m^2)
aoa_val = None
aosv_val = None
aostj_val = None
ascao_val = None
aoa_idx = None
aosv_idx = None
aostj_idx = None
ascao_idx = None
try:
    aoa_raw = st.session_state.get('aoa', "")
    if aoa_raw is not None and str(aoa_raw).strip() != "":
        aoa_val = float(str(aoa_raw).strip())
        if bsa and float(bsa) > 0:
            aoa_idx = round(aoa_val / float(bsa), 1)
    aosv_raw = st.session_state.get('aosv', "")
    if aosv_raw is not None and str(aosv_raw).strip() != "":
        aosv_val = float(str(aosv_raw).strip())
        if bsa and float(bsa) > 0:
            aosv_idx = round(aosv_val / float(bsa), 1)
    aostj_raw = st.session_state.get('aostj', "")
    if aostj_raw is not None and str(aostj_raw).strip() != "":
        aostj_val = float(str(aostj_raw).strip())
        if bsa and float(bsa) > 0:
            aostj_idx = round(aostj_val / float(bsa), 1)
    ascao_raw = st.session_state.get('ascao', "")
    if ascao_raw is not None and str(ascao_raw).strip() != "":
        ascao_val = float(str(ascao_raw).strip())
        if bsa and float(bsa) > 0:
            ascao_idx = round(ascao_val / float(bsa), 1)
except Exception:
    aoa_val = None
    aosv_val = None
    aostj_val = None
    ascao_val = None
    aoa_idx = None
    aosv_idx = None
    aostj_idx = None
    ascao_idx = None


with st.expander("2. Keuzes RV en RA", expanded=False):
    col4, col5 = st.columns(2)
    with col4:
        # Determine default index for RV hypertrofie: default Normotroof, but if RVFWd > 6 → Hypertroof
        try:
            default_rv_idx = 0
            # Reference: RVFWd >5 mm considered hypertrofie by default
            if rvfwd_val is not None and rvfwd_val > 5:
                default_rv_idx = 1
        except Exception:
            default_rv_idx = 0
        rv_hypertrofie = st.selectbox("RV hypertrofie", ["Normotroof", "Hypertroof"], index=default_rv_idx)

        # Determine default for RV dilatatie: normal unless diameters exceed thresholds
        try:
            default_rvd_idx = 0
            # RV basal diameter normal <=41 mm ; >41 -> dilatatie
            if rvbd_val is not None and rvbd_val > 41:
                default_rvd_idx = 1
            # RV mid diameter normal <=35 mm ; >35 -> dilatatie
            if rvmd_val is not None and rvmd_val > 35:
                default_rvd_idx = 1
        except Exception:
            default_rvd_idx = 0
        rv_dilatatie = st.selectbox("RV dilatatie", ["niet gedilateerd", "gedilateerd"], index=default_rvd_idx)
        # RV functie - suggest based on TAPSE but allow manual override
        rv_options = [
            "goede longitudinale systolische functie",
            "mild verminderde longitudinale systolische functie",
            "matig verminderde longitudinale systolische functie",
            "ernstig verminderde longitudinale systolische functie",
        ]
        try:
            default_idx = rv_options.index(rv_function_auto) if rv_function_auto in rv_options else 0
        except Exception:
            default_idx = 0
        rv_functie = st.selectbox("RV functie (gesuggereerd op basis van TAPSE)", rv_options, index=default_idx)
        # Determine default for RA dilatatie using RAVI and sex-specific cutoffs
        try:
            default_ra_idx = 0
            if ravi_val is not None:
                try:
                    # sex is 'Man' or 'Vrouw'
                    if sex == "Man" and ravi_val > 32:
                        default_ra_idx = 1
                    elif sex != "Man" and ravi_val > 28:
                        default_ra_idx = 1
                except Exception:
                    default_ra_idx = 0
        except Exception:
            default_ra_idx = 0
        ra_dilatatie = st.selectbox("RA dilatatie", ["Niet gedilateerd", "Gedilateerd"], index=default_ra_idx)

    with col5:
        # intentionally left blank for alignment; valve controls are moved to 'Keuzes Kleppen'
        st.write("")

with st.expander("3. Keuzes Kleppen", expanded=False):
    ak_morfologie = st.selectbox("AK morfologie", ["Normale tricuspiede morfologie", "Bicuspiede morfologie"], index=0)
    ak_calcificatie = st.selectbox("AK calcificatie", ["Geen calcificatie", "Milde sclerose", "Milde calcificatie", "Matige calcificatie", "Ernstige calcificatie"], index=0)
    ak_stenose = st.selectbox("AK stenose", ["Geen stenose", "Milde stenose", "Matige stenose", "Ernstige stenose"], index=ak_default_idx if 'ak_default_idx' in globals() else 0)
    ak_regurgitatie = st.selectbox("AK regurgitatie", [
        "Geen regurgitatie",
        "Milde aorta regurgitatie",
        "Matige aorta regurgitatie",
        "Ernstige aorta regurgitatie",
    ], index=0)

    mk_regurgitatie = st.selectbox("MK regurgitatie", [
        "Geen regurgitatie",
        "Milde mitralis regurgitatie",
        "Matige mitralis regurgitatie",
        "Ernstige mitralis regurgitatie",
    ], index=mk_default_idx if 'mk_default_idx' in locals() else 0)

    tk_regurgitatie = st.selectbox("TK regurgitatie", [
        "Geen regurgitatie",
        "Milde tricuspidalis regurgitatie",
        "Matige tricuspidalis regurgitatie",
        "Ernstige tricuspidalis regurgitatie",
    ], index=tk_default_idx if 'tk_default_idx' in globals() else 0)

    pk_regurgitatie = st.selectbox("PK regurgitatie", [
        "Geen regurgitatie",
        "Milde pulmonalis regurgitatie",
        "Matige pulmonalis regurgitatie",
        "Ernstige pulmonalis regurgitatie",
    ], index=pk_default_idx if 'pk_default_idx' in globals() else 0)

# Conditional extra inputs for richtlijn-gestuurde aanbevelingen
try:
    # Determine severity flags from current selections/metrics
    severe_mr = "Ernstige mitralis regurgitatie" in mk_regurgitatie or (mk_default_idx if 'mk_default_idx' in locals() else 0) == 3
    severe_as = "Ernstige stenose" in ak_stenose or (ak_default_idx if 'ak_default_idx' in globals() else 0) == 3
    show_reco_inputs = severe_mr or severe_as
except Exception:
    severe_mr = False
    severe_as = False
    show_reco_inputs = False

if show_reco_inputs:
    with st.expander("Aanvullende input voor aanbevelingen", expanded=False):
        if severe_mr:
            st.markdown("**Ernstige mitralisregurgitatie** (optionele parameters)")
            st.checkbox("Symptomen bij MR", key="mr_sympt")
            st.checkbox("Voorkamerfibrillatie", key="af_present")
            st.caption("We gebruiken ook LVEF, LVESD/LVESDi, sPAP en LAVI indien ingevuld.")
        if severe_as:
            st.markdown("**Ernstige aortaklepstenose** (optionele parameters)")
            st.checkbox("Symptomen bij AS", key="as_sympt")
            st.checkbox("SBP-daling >20 mmHg bij inspanning", key="as_sbp_drop")
            st.number_input("Calcificatiescore (Agatston)", min_value=0, max_value=10000, value=0, step=50, key="as_calc_score")
            st.number_input("Vmax progressie (m/s/jaar)", min_value=0.0, max_value=2.0, value=0.0, step=0.05, key="as_vmax_prog")
            st.number_input("BNP/NT-proBNP (pg/mL)", min_value=0, max_value=100000, value=0, step=50, key="as_bnp")

with st.expander("Keuzes CVD", expanded=False):
    ivc_dilatatie = st.selectbox("IVC", ["niet gedilateerd", "gedilateerd"], index=0)
    ivc_variatie = st.selectbox("Ademhalingsvariatie", ["met bewaarde ademhalingsvariatie", "met verminderde ademhalingsvariatie", "zonder ademhalingsvariatie"], index=0)
    cvd = st.selectbox("CVD (mmHg)", ["3", "8", "15+"], index=0)


# -----------------------------
# Automatic derived values
# -----------------------------
lvef_class = None
automatic_systolic = "goede globale en regionale systolische functie"
if lvef is not None:
    try:
        lvef_class = classify_lvef(lvef, sex)
        automatic_systolic = lvef_to_systolic_option(lvef_class)
    except Exception:
        lvef_class = None
        automatic_systolic = "goede globale en regionale systolische functie"

# show suggested systolic option but let user override
systolic_option = automatic_systolic

# (la_suggested already computed earlier)

# Compute PASP-derived pulmonary pressure text
def parse_cvd_value(cvd_str: str) -> float:
    try:
        if isinstance(cvd_str, str) and cvd_str.endswith("+"):
            return float(cvd_str.rstrip("+"))
        return float(cvd_str)
    except Exception:
        return 0.0

cvd_num = parse_cvd_value(cvd)
pasp_text = ""
try:
    pasp_raw_val = st.session_state.get("pasp_raw", None)
except Exception:
    pasp_raw_val = None

if pasp_raw_val is None or str(pasp_raw_val).strip() == "":
    pasp_available = False
    pasp_text = "Geen adequaat TR-signaal voor PASP"
else:
    pasp_available = True
    try:
        pasp_val = float(pasp_raw_val)
    except Exception:
        pasp_val = None
        pasp_available = False

    if pasp_available and pasp_val is not None:
        total_pasp = round(pasp_val + cvd_num)
        if total_pasp > 35:
            pasp_text = f"Pulmonale hypertensie met PASP {total_pasp} mmHg."
        else:
            pasp_text = f"Normale pulmonale drukken met PASP {total_pasp} mmHg."
    else:
        pasp_text = "Geen adequaat TR-signaal voor PASP"


echo_context = EchoReportInput(
    patient=patient_ctx,
    lv_hypertrofie_choice=lv_hypertrofie_choice,
    lv_hypertrofie_auto=lv_hypertrofie_auto,
    ivsd=ivsd,
    lvpw=lvpw,
    mass_index=mass_index,
    rwt=rwt,
    lv_dilatatie_choice=lv_dilatatie_choice,
    lv_dilatatie_auto=lv_dilatatie_auto,
    lvidd=lvidd,
    systolic_option=systolic_option,
    lvef=lvef,
    lv_diastolische_functie=lv_diastolische_functie,
    la_choice=la_choice,
    la_suggested=la_suggested,
    lavi=lavi,
    rv_hypertrofie=rv_hypertrofie,
    rvfwd_val=rvfwd_val,
    rvbd_val=rvbd_val,
    rvmd_val=rvmd_val,
    tapse=tapse,
    rv_dilatatie=rv_dilatatie,
    rv_functie=rv_functie,
    pasp_text=pasp_text,
    ravi_val=ravi_val,
    ra_dilatatie=ra_dilatatie,
    ak_morfologie=ak_morfologie,
    ak_calcificatie=ak_calcificatie,
    ak_stenose=ak_stenose,
    ak_regurgitatie=ak_regurgitatie,
    mk_regurgitatie=mk_regurgitatie,
    tk_regurgitatie=tk_regurgitatie,
    pk_regurgitatie=pk_regurgitatie,
    ivc_dilatatie=ivc_dilatatie,
    ivc_variatie=ivc_variatie,
    cvd=cvd,
    session_state=st.session_state,
)
brief_echo = summarize_echo_for_brief(echo_context)
final = generate_echo_report(echo_context)
echo_snapshot = StudySnapshot(patient=patient_ctx, echo=echo_context)
echo_snapshot.report_texts["brief_echo"] = brief_echo
echo_snapshot.report_texts["full_echo"] = final

    # snapshot download removed per UI simplification


if st.button("Genereer verslag"):
    # Always remember echo texts locally (patient_id may be None)
    _remember_brief_section(
        "brief_echo",
        brief_echo,
        patient_ctx.patient_id,
        datetime.date.today().isoformat(),
    )
    _remember_brief_section(
        "full_echo",
        final,
        patient_ctx.patient_id,
        datetime.date.today().isoformat(),
    )
    st.subheader("Gegenereerd Verslag")
    show_report_actions(final)

    # Also copy the generated report to the clipboard (user gesture present)
    try:
        escaped = json.dumps(final)
        copy_html = f"""
        <script>
        (async function() {{
            try {{
                await navigator.clipboard.writeText({escaped});
            }} catch (e) {{
                console.warn('Clipboard write failed', e);
            }}
        }})();
        </script>
        """
        components.html(copy_html, height=0)
        st.success("Verslag gekopieerd naar klembord")
    except Exception:
        # If copy fails silently, keep going
        pass

    recs = generate_guideline_recommendations(echo_context)
    if recs:
        st.subheader("Aanbevelingen (richtlijn-gestuurd)")
        rec_text = "\n".join([f"- {r}" for r in recs])
        st.markdown(rec_text)
        show_report_actions(rec_text)

# Support triggering generation from compact-metrics quick button via session flag
if st.session_state.pop("generate_now", False):
    try:
        # replicate same actions as the main generate button
        _remember_brief_section(
            "brief_echo",
            brief_echo,
            patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        _remember_brief_section(
            "full_echo",
            final,
            patient_ctx.patient_id,
            datetime.date.today().isoformat(),
        )
        # Make the generated final available to the top-level generate area
        # and mark it as not-yet-copied so the main area can auto-copy it.
        st.session_state["generated_final"] = final
        st.session_state["generated_final_copied"] = False
        st.subheader("Gegenereerd Verslag")
        show_report_actions(final)
        # copy to clipboard
        try:
            escaped = json.dumps(final)
            copy_html = f"""
            <script>
            (async function() {{
                try {{
                    await navigator.clipboard.writeText({escaped});
                }} catch (e) {{
                    console.warn('Clipboard write failed', e);
                }}
            }})();
            </script>
            """
            components.html(copy_html, height=0)
            st.success("Verslag gekopieerd naar klembord")
        except Exception:
            pass

        recs = generate_guideline_recommendations(echo_context)
        if recs:
            st.subheader("Aanbevelingen (richtlijn-gestuurd)")
            rec_text = "\n".join([f"- {r}" for r in recs])
            st.markdown(rec_text)
            show_report_actions(rec_text)
    except Exception:
        # don't break UI if generation fails from compact button
        st.warning("Automatisch genereren mislukt")

# Display any report generated from the compact quick-button in the
# main "Genereer verslag" area and auto-copy it once.
generated_final = st.session_state.pop("generated_final", None)
if generated_final:
    st.subheader("Gegenereerd Verslag")
    show_report_actions(generated_final)
    # Auto-copy once (avoid repeating on subsequent renders)
    copied = st.session_state.pop("generated_final_copied", False)
    if not copied:
        try:
            escaped = json.dumps(generated_final)
            copy_html = f"""
            <script>
            (async function() {{
                try {{
                    await navigator.clipboard.writeText({escaped});
                }} catch (e) {{
                    console.warn('Clipboard write failed', e);
                }}
            }})();
            </script>
            """
            components.html(copy_html, height=0)
            st.success("Verslag gekopieerd naar klembord")
            st.session_state["generated_final_copied"] = True
        except Exception:
            pass

