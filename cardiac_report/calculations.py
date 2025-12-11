"""Clinical calculations and classifications used across the cardiac report app."""
from __future__ import annotations

import math
from typing import Optional, Tuple


# VO2 percentile reference values (FRIEND registry) for cycle ergometer
# Stored as: ref_values[sex]['age_bucket'] = {'p95':..., 'p75':..., 'p50':..., 'p25':..., 'p5':...}
_REF_VALUES = {
    'Man': {
        20: {'p95':54.0,'p75':48.0,'p50':43.0,'p25':38.0,'p5':33.0},
        30: {'p95':50.0,'p75':44.0,'p50':40.0,'p25':35.0,'p5':30.0},
        40: {'p95':47.0,'p75':41.0,'p50':36.0,'p25':32.0,'p5':28.0},
        50: {'p95':43.0,'p75':38.0,'p50':33.0,'p25':29.0,'p5':25.0},
        60: {'p95':38.0,'p75':34.0,'p50':30.0,'p25':26.0,'p5':22.0},
        70: {'p95':34.0,'p75':30.0,'p50':26.0,'p25':23.0,'p5':20.0},
    },
    'Vrouw': {
        20: {'p95':43.0,'p75':38.0,'p50':34.0,'p25':30.0,'p5':26.0},
        30: {'p95':40.0,'p75':36.0,'p50':32.0,'p25':28.0,'p5':24.0},
        40: {'p95':36.0,'p75':32.0,'p50':29.0,'p25':26.0,'p5':22.0},
        50: {'p95':33.0,'p75':30.0,'p50':27.0,'p25':24.0,'p5':20.0},
        60: {'p95':30.0,'p75':27.0,'p50':24.0,'p25':21.0,'p5':18.0},
        70: {'p95':27.0,'p75':25.0,'p50':22.0,'p25':19.0,'p5':17.0},
    }
}


def bsa_mosteller(length_cm: float, weight_kg: float) -> float:
    """Mosteller formula for body surface area."""
    return math.sqrt((length_cm * weight_kg) / 3600.0)


def classify_ivsd(ivsd_mm: float, sex: str) -> str:
    if sex == "Man":
        if ivsd_mm <= 10:
            return "Normotroof"
        if ivsd_mm <= 13:
            return "Mild concentrisch hypertroof"
        if ivsd_mm <= 16:
            return "Matig concentrisch hypertroof"
        return "Ernstig concentrisch hypertroof"
    # Vrouw
    if ivsd_mm <= 9:
        return "Normotroof"
    if ivsd_mm <= 12:
        return "Mild concentrisch hypertroof"
    if ivsd_mm <= 15:
        return "Matig concentrisch hypertroof"
    return "Ernstig concentrisch hypertroof"


def classify_lavi(lavi_ml_m2: float) -> str:
    if lavi_ml_m2 <= 34:
        return "Niet gedilateerd"
    if lavi_ml_m2 <= 41:
        return "Mild gedilateerd"
    if lavi_ml_m2 <= 48:
        return "Matig gedilateerd"
    return "Ernstig gedilateerd"


def classify_lvef(lvef_pct: float, sex: str) -> str:
    if lvef_pct < 30:
        return "Ernstig"
    if 30 <= lvef_pct <= 40:
        return "Matig"
    if sex == "Man":
        if 41 <= lvef_pct <= 51:
            return "Mild"
    else:
        if 41 <= lvef_pct <= 53:
            return "Mild"
    if sex == "Man":
        if 52 <= lvef_pct <= 72:
            return "Normaal"
    else:
        if 54 <= lvef_pct <= 74:
            return "Normaal"
    if lvef_pct < 41:
        return "Matig"
    return "Mild"


def lvef_to_systolic_option(lvef_class: str) -> str:
    mapping = {
        "Normaal": "goede globale en regionale systolische functie",
        "Mild": "mild verminderde globale systolische functie",
        "Matig": "matig verminderde globale systolische functie",
        "Ernstig": "ernstig verminderde globale systolische functie",
    }
    return mapping.get(lvef_class, "goede globale en regionale systolische functie")


def compute_lv_mass_g(ivsd_mm: float, lvidd_mm: float, lvpwd_mm: float) -> float:
    ivs = ivsd_mm / 10.0
    lvidd = lvidd_mm / 10.0
    lvpw = lvpwd_mm / 10.0
    lv_mass = 0.8 * (1.04 * ((ivs + lvidd + lvpw) ** 3 - (lvidd ** 3))) + 0.6
    return round(lv_mass, 1)


def compute_rwt(lvpwd_mm: float, lvidd_mm: float) -> float:
    try:
        return round((2.0 * lvpwd_mm) / lvidd_mm, 3)
    except Exception:
        return 0.0


def lv_mass_index_severity(lv_mass_g: float, bsa_m2: float, sex: str) -> Tuple[float, str]:
    mass_index = lv_mass_g / max(0.1, bsa_m2)
    mass_index = round(mass_index, 1)
    if sex == "Man":
        if mass_index < 115:
            return mass_index, "Normaal"
        if 116 <= mass_index <= 131:
            return mass_index, "Mild"
        if 132 <= mass_index <= 148:
            return mass_index, "Matig"
        return mass_index, "Ernstig"
    if mass_index < 95:
        return mass_index, "Normaal"
    if 95 <= mass_index <= 108:
        return mass_index, "Mild"
    if 109 <= mass_index <= 121:
        return mass_index, "Matig"
    return mass_index, "Ernstig"


def determine_lv_geometry(mass_index: float, severity_key: str, rwt: float) -> str:
    if severity_key != "Normaal":
        if rwt > 0.42:
            return f"{severity_key} concentrisch hypertroof"
        if rwt < 0.32:
            return f"{severity_key} eccentrisch hypertroof"
        return f"{severity_key} gemengd hypertroof"
    if rwt > 0.42:
        return "Concentrische remodeling"
    if rwt < 0.32:
        return "Eccentrische remodeling"
    return "Normotroof"


def classify_lvidd(lvidd_mm: float, sex: str, bsa_m2: Optional[float] = None) -> str:
    """Classify LVIDd using indexed thresholds when BSA is provided.

    If `bsa_m2` is supplied and > 0, LVIDd is evaluated as mm/m^2 using the
    thresholds requested by the user. If BSA is not available, falls back to
    the previous absolute-mm thresholds.
    """
    # Use indexed thresholds when possible
    try:
        if bsa_m2 is not None and float(bsa_m2) > 0:
            lvidd_idx = round(float(lvidd_mm) / float(bsa_m2), 1)
        else:
            lvidd_idx = None
    except Exception:
        lvidd_idx = None

    # Indexed thresholds (mm/m^2)
    if lvidd_idx is not None:
        if sex == "Man":
            if lvidd_idx < 31:
                return "niet gedilateerd"
            if 31 <= lvidd_idx <= 34:
                return "mild gedilateerd"
            if 34 < lvidd_idx <= 36:
                return "matig gedilateerd"
            return "ernstig gedilateerd"
        # Vrouw
        if lvidd_idx < 32:
            return "niet gedilateerd"
        if 32 <= lvidd_idx <= 35:
            return "mild gedilateerd"
        if 35 < lvidd_idx <= 37:
            return "matig gedilateerd"
        return "ernstig gedilateerd"

    # Fallback: previous absolute-mm thresholds when index not available
    if sex == "Man":
        if lvidd_mm < 58:
            return "niet gedilateerd"
        if 59 <= lvidd_mm <= 63:
            return "mild gedilateerd"
        if 64 <= lvidd_mm <= 68:
            return "matig gedilateerd"
        return "ernstig gedilateerd"
    if lvidd_mm < 52:
        return "niet gedilateerd"
    if 53 <= lvidd_mm <= 56:
        return "mild gedilateerd"
    if 57 <= lvidd_mm <= 61:
        return "matig gedilateerd"
    return "ernstig gedilateerd"


def classify_tapse(tapse_mm: float) -> str:
    try:
        t = float(tapse_mm)
    except Exception:
        return "Onbekend"
    if t > 17:
        return "goede longitudinale systolische functie"
    if 13 <= t <= 17:
        return "mild verminderde longitudinale systolische functie"
    if 11 <= t < 13:
        return "matig verminderde longitudinale systolische functie"
    return "ernstig verminderde longitudinale systolische functie"


def vo2_percentile_and_label(sex: str, age: float, vo2_mlkg: float):
    try:
        a = int(age)
    except Exception:
        a = 50
    if a < 20:
        bucket = 20
    elif a < 30:
        bucket = 20
    elif a < 40:
        bucket = 30
    elif a < 50:
        bucket = 40
    elif a < 60:
        bucket = 50
    elif a < 70:
        bucket = 60
    else:
        bucket = 70
    sex_key = 'Man' if sex == 'Man' else 'Vrouw'
    try:
        ref = _REF_VALUES[sex_key][bucket]
    except Exception:
        return None, None, None
    p95 = ref['p95']
    p75 = ref['p75']
    p50 = ref['p50']
    p25 = ref['p25']
    p5 = ref['p5']
    try:
        percent_vs50 = round((float(vo2_mlkg) / float(p50)) * 100, 1)
    except Exception:
        percent_vs50 = None
    band = None
    band_text = None
    if vo2_mlkg >= p95:
        band = ">=95%"
        band_text = "Uitstekende inspanningscapaciteit"
    elif vo2_mlkg >= p75:
        band = "75-95%"
        band_text = "Bovengemiddelde inspanningscapaciteit"
    elif vo2_mlkg >= p25:
        band = "25-75%"
        band_text = "Normale inspanningscapaciteit"
    elif vo2_mlkg >= p5:
        band = "5-25%"
        band_text = "Ondergemiddelde inspanningscapaciteit"
    else:
        band = "<5%"
        band_text = "Slechte inspanningscapaciteit"
    return percent_vs50, band, band_text


def get_vo2_reference_values(sex: str, age: float):
    """Return the reference percentile dict for the provided sex/age bucket."""
    try:
        a = int(age)
    except Exception:
        a = 50
    if a < 20:
        bucket = 20
    elif a < 30:
        bucket = 20
    elif a < 40:
        bucket = 30
    elif a < 50:
        bucket = 40
    elif a < 60:
        bucket = 50
    elif a < 70:
        bucket = 60
    else:
        bucket = 70
    sex_key = 'Man' if sex == 'Man' else 'Vrouw'
    return _REF_VALUES.get(sex_key, {}).get(bucket)


def mitral_regurgitation_severity(eroa: Optional[float], regurgitant_volume: Optional[float], regurgitant_fraction: Optional[float]) -> int:
    """Return a coarse MR severity class (0 none → 3 severe)."""
    severity = 0
    try:
        if eroa is not None:
            if eroa >= 0.4:
                severity = max(severity, 3)
            elif 0.2 <= eroa < 0.4:
                severity = max(severity, 2)
            elif eroa < 0.2:
                severity = max(severity, 1)
        if regurgitant_volume is not None:
            if regurgitant_volume >= 60:
                severity = max(severity, 3)
            elif 30 <= regurgitant_volume < 60:
                severity = max(severity, 2)
            elif regurgitant_volume < 30:
                severity = max(severity, 1)
        if regurgitant_fraction is not None:
            if regurgitant_fraction > 50:
                severity = max(severity, 3)
            elif 30 <= regurgitant_fraction <= 50:
                severity = max(severity, 2)
            elif regurgitant_fraction < 30:
                severity = max(severity, 1)
    except Exception:
        pass
    return severity
