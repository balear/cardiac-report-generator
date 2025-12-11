"""Data models used across the cardiac report package."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional

SessionState = Dict[str, Any]


@dataclass
class PatientContext:
    """Basic patient info that multiple modules depend on."""

    sex: str
    patient_id: Optional[str] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    leeftijd: Optional[float] = None
    bsa: Optional[float] = None
    weight: Optional[float] = None
    length: Optional[float] = None


@dataclass
class EchoReportInput:
    """Structured payload for the echo interpretation engine."""

    patient: PatientContext
    lv_hypertrofie_choice: Optional[str] = None
    lv_hypertrofie_auto: Optional[str] = None
    ivsd: Optional[float] = None
    lvpw: Optional[float] = None
    mass_index: Optional[float] = None
    rwt: Optional[float] = None
    lv_dilatatie_choice: Optional[str] = None
    lv_dilatatie_auto: Optional[str] = None
    lvidd: Optional[float] = None
    systolic_option: Optional[str] = None
    lvef: Optional[float] = None
    lv_diastolische_functie: Optional[str] = None
    la_choice: Optional[str] = None
    la_suggested: Optional[str] = None
    lavi: Optional[float] = None
    rv_hypertrofie: Optional[str] = None
    rvfwd_val: Optional[float] = None
    rvbd_val: Optional[float] = None
    rvmd_val: Optional[float] = None
    tapse: Optional[float] = None
    rv_dilatatie: Optional[str] = None
    rv_functie: Optional[str] = None
    pasp_text: Optional[str] = None
    ravi_val: Optional[float] = None
    ra_dilatatie: Optional[str] = None
    ak_morfologie: Optional[str] = None
    ak_calcificatie: Optional[str] = None
    ak_stenose: Optional[str] = None
    ak_regurgitatie: Optional[str] = None
    mk_regurgitatie: Optional[str] = None
    tk_regurgitatie: Optional[str] = None
    pk_regurgitatie: Optional[str] = None
    ivc_dilatatie: Optional[str] = None
    ivc_variatie: Optional[str] = None
    cvd: Optional[str] = None
    session_state: SessionState = field(default_factory=dict)

    def get_session_float(self, key: str) -> Optional[float]:
        """Helper to safely pull float values from the originating session."""

        try:
            raw = self.session_state.get(key, "")
            if raw is None:
                return None
            txt = str(raw).strip()
            if txt == "":
                return None
            return float(txt)
        except Exception:
            return None

    @property
    def bsa(self) -> Optional[float]:
        return self.patient.bsa

    @property
    def sex(self) -> str:
        return self.patient.sex

    @property
    def leeftijd(self) -> Optional[float]:
        return self.patient.leeftijd


@dataclass
class FietstestMeasurements:
    """Structured input for bicycle stress test interpretation."""

    patient: PatientContext
    start_watt: Optional[float] = None
    increment_watt: Optional[float] = None
    max_watt: Optional[float] = None
    duration_at_max: Optional[float] = None
    max_hr: Optional[float] = None
    bp_evolutie: Optional[str] = None
    ritme: Optional[str] = None
    effort_type: Optional[str] = None
    stop_criterium: Optional[str] = None
    ecg_changes: Optional[str] = None
    conclusion: Optional[str] = None

    @property
    def sex(self) -> str:
        return self.patient.sex

    @property
    def leeftijd(self) -> Optional[float]:
        return self.patient.leeftijd

    @property
    def weight(self) -> Optional[float]:
        return self.patient.weight


@dataclass
class FietstestMetrics:
    """Derived values shown in the bicycle stress test UI."""

    predicted_max_hr: Optional[int] = None
    pct_hr_display: Optional[float] = None
    vo2_observed: Optional[float] = None
    vo2_observed_text: Optional[str] = None
    vo2_percentile_pct: Optional[float] = None
    vo2_band: Optional[str] = None
    vo2_band_text: Optional[str] = None
    wpred: Optional[float] = None
    wpred_pct: Optional[float] = None
    summary_lines: List[str] = field(default_factory=list)


@dataclass
class ECGMeasurements:
    """Structured input extracted from ECG PDF or manual entry."""

    patient: PatientContext
    recorded_at: Optional[str] = None
    vent_rate: Optional[float] = None
    pr_interval_ms: Optional[float] = None
    qrs_duration_ms: Optional[float] = None
    qt_interval_ms: Optional[float] = None
    qtc_interval_ms: Optional[float] = None
    p_axis_deg: Optional[float] = None
    qrs_axis_deg: Optional[float] = None
    t_axis_deg: Optional[float] = None
    rhythm_summary: Optional[str] = None
    auto_report_text: Optional[str] = None
    acquisition_device: Optional[str] = None

    @property
    def sex(self) -> str:
        return self.patient.sex

    @property
    def patient_id(self) -> Optional[str]:
        return self.patient.patient_id


@dataclass
class ECGMetrics:
    """Derived ECG metrics for display."""

    qtcf_ms: Optional[float] = None
    tachy_flag: bool = False
    brady_flag: bool = False
    axis_deviation: Optional[str] = None
    summary_lines: List[str] = field(default_factory=list)


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
    summary_lines: List[str] = field(default_factory=list)


@dataclass
class LeadMeasurements:
    """Snapshot of per-lead measurements during a CIED follow-up."""

    sensing: Optional[str] = None
    impedance: Optional[str] = None
    threshold_v: Optional[str] = None
    threshold_ms: Optional[str] = None
    polarity: Optional[str] = None
    stable: Optional[bool] = True
    location: Optional[str] = None


@dataclass
class CIEDReportInput:
    """Structured payload for device follow-up reporting."""

    patient: Optional[PatientContext] = None
    device_type: Optional[str] = None
    device_brand: Optional[str] = None
    programming_mode: Optional[str] = None
    lower_rate: Optional[int] = None
    upper_tracking: Optional[int] = None
    indication_text: Optional[str] = None
    lead_ra: bool = False
    lead_rv: bool = False
    lead_lv: bool = False
    other_leads: Optional[str] = None
    sensing_ok: bool = True
    pacing_ok: bool = True
    impedance_ok: bool = True
    egm_events: Optional[str] = None
    atrial_pacing_pct: Optional[str] = None
    ventricular_pacing_pct: Optional[str] = None
    lv_pacing_pct: Optional[str] = None
    settings_changed: bool = False
    patient_dependent: bool = False
    battery_status: Optional[str] = None
    suggested_sensed_av: Optional[int] = None
    suggested_paced_av: Optional[int] = None
    sensed_av_delay: Optional[str] = None
    paced_av_delay: Optional[str] = None
    atrial_fields: LeadMeasurements = field(default_factory=LeadMeasurements)
    vent_fields: LeadMeasurements = field(default_factory=LeadMeasurements)
    lv_fields: LeadMeasurements = field(default_factory=LeadMeasurements)


@dataclass
class StudySnapshot:
    """Bundle of measurement contexts that can be stored or shared."""

    patient: Optional[PatientContext] = None
    echo: Optional[EchoReportInput] = None
    fietstest: Optional[FietstestMeasurements] = None
    cied: Optional[CIEDReportInput] = None
    ecg: Optional[ECGMeasurements] = None
    report_texts: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {}
        if self.patient:
            payload["patient"] = asdict(self.patient)
        if self.echo:
            payload["echo"] = self._asdict_drop(self.echo, {"session_state"})
        if self.fietstest:
            payload["fietstest"] = asdict(self.fietstest)
        if self.cied:
            payload["cied"] = asdict(self.cied)
        if self.ecg:
            payload["ecg"] = asdict(self.ecg)
        if self.report_texts:
            payload["report_texts"] = dict(self.report_texts)
        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StudySnapshot":
        if not data:
            return cls()

        patient = cls._coerce_patient(data.get("patient"))

        def _build_echo(payload: Any) -> Optional[EchoReportInput]:
            if not isinstance(payload, dict):
                return None
            values = dict(payload)
            values.pop("session_state", None)
            echo_patient = cls._coerce_patient(values.get("patient")) or patient
            if echo_patient is None:
                return None
            values["patient"] = echo_patient
            return EchoReportInput(**values)

        def _build_fietstest(payload: Any) -> Optional[FietstestMeasurements]:
            if not isinstance(payload, dict):
                return None
            values = dict(payload)
            ft_patient = cls._coerce_patient(values.get("patient")) or patient
            if ft_patient is None:
                return None
            values["patient"] = ft_patient
            return FietstestMeasurements(**values)

        def _build_cied(payload: Any) -> Optional[CIEDReportInput]:
            if not isinstance(payload, dict):
                return None
            values = dict(payload)
            cied_patient = cls._coerce_patient(values.get("patient")) or patient
            if cied_patient is None:
                return None
            values["patient"] = cied_patient
            values["atrial_fields"] = cls._coerce_lead(values.get("atrial_fields"))
            values["vent_fields"] = cls._coerce_lead(values.get("vent_fields"))
            values["lv_fields"] = cls._coerce_lead(values.get("lv_fields"))
            return CIEDReportInput(**values)

        def _build_ecg(payload: Any) -> Optional[ECGMeasurements]:
            if not isinstance(payload, dict):
                return None
            values = dict(payload)
            ecg_patient = cls._coerce_patient(values.get("patient")) or patient
            if ecg_patient is None:
                return None
            values["patient"] = ecg_patient
            return ECGMeasurements(**values)

        return cls(
            patient=patient,
            echo=_build_echo(data.get("echo")),
            fietstest=_build_fietstest(data.get("fietstest")),
            cied=_build_cied(data.get("cied")),
            ecg=_build_ecg(data.get("ecg")),
            report_texts=dict(data.get("report_texts", {}) or {}),
        )

    @staticmethod
    def _asdict_drop(obj: Any, drop_keys: Iterable[str]) -> Dict[str, Any]:
        data = asdict(obj)
        for key in drop_keys:
            data.pop(key, None)
        return data

    @staticmethod
    def _coerce_patient(data: Any) -> Optional[PatientContext]:
        if isinstance(data, PatientContext):
            return data
        if isinstance(data, dict):
            try:
                return PatientContext(**data)
            except TypeError:
                return None
        return None

    @staticmethod
    def _coerce_lead(data: Any) -> LeadMeasurements:
        if isinstance(data, LeadMeasurements):
            return data
        if isinstance(data, dict):
            try:
                return LeadMeasurements(**data)
            except TypeError:
                return LeadMeasurements()
        return LeadMeasurements()
