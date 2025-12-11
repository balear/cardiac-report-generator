"""Report builders and guideline-driven recommendation helpers."""
from __future__ import annotations

import datetime as dt
from dataclasses import fields
from typing import Any, Dict, List, Optional, Sequence, Union

from cardiac_report.calculations import mitral_regurgitation_severity
from cardiac_report.models import EchoReportInput, PatientContext


def _get_session_float(ctx: EchoReportInput, key: str) -> Optional[float]:
    return ctx.get_session_float(key)


def _coerce_echo_input(context: Union[EchoReportInput, Dict[str, Any]]) -> EchoReportInput:
    """Allow legacy dict payloads to be converted to an EchoReportInput."""

    if isinstance(context, EchoReportInput):
        return context

    patient = PatientContext(
        sex=context.get("sex", "Man"),
        patient_id=context.get("patient_id"),
        full_name=context.get("full_name"),
        date_of_birth=context.get("date_of_birth"),
        leeftijd=context.get("leeftijd"),
        bsa=context.get("bsa"),
        weight=context.get("weight"),
        length=context.get("length"),
    )

    data: Dict[str, Any] = {}
    for field in fields(EchoReportInput):
        if field.name == "patient":
            continue
        if field.name == "session_state":
            data[field.name] = context.get("session_state", {})
        else:
            data[field.name] = context.get(field.name)

    return EchoReportInput(patient=patient, **data)


def generate_echo_report(context: Union[EchoReportInput, Dict[str, Any]]) -> str:
    """Generate the narrative echo report from collected UI context."""

    ctx = _coerce_echo_input(context)
    bsa = ctx.bsa

    report: List[str] = []
    lv_parts: List[str] = []

    hypertrophy_label = ctx.lv_hypertrofie_choice or ctx.lv_hypertrofie_auto
    if hypertrophy_label:
        lv_parts.append(str(hypertrophy_label))

    meas: List[str] = []
    if ctx.ivsd is not None:
        meas.append(f"IVSd {ctx.ivsd} mm")
    if ctx.lvpw is not None:
        meas.append(f"LVPWd {ctx.lvpw} mm")
    if ctx.mass_index is not None:
        meas.append(f"LVMI {ctx.mass_index} g/m²")
    if ctx.rwt is not None:
        meas.append(f"RWT {ctx.rwt}")
    if meas:
        lv_parts.append("(" + ", ".join(meas) + ")")

    dil_label = ctx.lv_dilatatie_choice or ctx.lv_dilatatie_auto
    if dil_label:
        if ctx.lvidd is not None:
            lv_parts.append(f"{dil_label} (LVIDd {ctx.lvidd} mm)")
        else:
            lv_parts.append(str(dil_label))

    syst_txt = ctx.systolic_option or ""
    if ctx.lvef is not None:
        syst_txt = syst_txt + f" (LVEF {ctx.lvef}%)"
    if syst_txt:
        lv_parts.append("met " + syst_txt)

    report.append("LV: " + ", ".join(lv_parts) + ".")

    diastolic_line = ctx.lv_diastolische_functie or ""
    extras: List[str] = []
    ea_val = _get_session_float(ctx, "ea")
    ee_val = _get_session_float(ctx, "ee")
    if ea_val is not None:
        extras.append(f"E/A {ea_val:.1f}")
    if ee_val is not None:
        extras.append(f"E/e' {ee_val:.1f}")
    if extras:
        diastolic_line = f"{diastolic_line} ({', '.join(extras)})"
    report.append(diastolic_line + ".")

    la_label = ctx.la_choice or ctx.la_suggested or "Niet gedilateerd"
    if ctx.lavi is not None:
        report.append(f"LA: {la_label}. (LAVI {ctx.lavi} mL/m²).")
    else:
        report.append(f"LA: {la_label}.")

    def _indexed(val: Optional[float]) -> Optional[float]:
        try:
            if val is None:
                return None
            if bsa and float(bsa) > 0:
                return round(float(val) / float(bsa), 1)
        except Exception:
            return None
        return None

    try:
        ao_items: List[str] = []
        ao_abnormals: List[str] = []
        aoa_val = _get_session_float(ctx, 'aoa')
        aosv_val = _get_session_float(ctx, 'aosv')
        aostj_val = _get_session_float(ctx, 'aostj')
        ascao_val = _get_session_float(ctx, 'ascao')
        aoa_idx = _indexed(aoa_val)
        aosv_idx = _indexed(aosv_val)
        aostj_idx = _indexed(aostj_val)
        ascao_idx = _indexed(ascao_val)

        if aoa_val is not None:
            if aoa_idx is not None:
                ao_items.append(f"AoA {int(round(aoa_val))} mm, {aoa_idx:.1f} mm/m²")
                if aoa_idx > 14:
                    ao_abnormals.append(
                        f"Aorta annulus (AoA) is gedilateerd ({int(round(aoa_val))} mm, {aoa_idx:.1f} mm/m²)."
                    )
            else:
                ao_items.append(f"AoA {int(round(aoa_val))} mm")

        if aosv_val is not None:
            if aosv_idx is not None:
                ao_items.append(f"AoSV {int(round(aosv_val))} mm, {aosv_idx:.1f} mm/m²")
                if aosv_idx > 20:
                    ao_abnormals.append(
                        f"Aorta sinus valsalva (AoSV) is gedilateerd ({int(round(aosv_val))} mm, {aosv_idx:.1f} mm/m²)."
                    )
            else:
                ao_items.append(f"AoSV {int(round(aosv_val))} mm")

        if aostj_val is not None:
            if aostj_idx is not None:
                ao_items.append(f"AoSTJ {int(round(aostj_val))} mm, {aostj_idx:.1f} mm/m²")
                if aostj_idx > 16:
                    ao_abnormals.append(
                        f"Aorta sinotubulaire junctie (AoSTJ) is gedilateerd ({int(round(aostj_val))} mm, {aostj_idx:.1f} mm/m²)."
                    )
            else:
                ao_items.append(f"AoSTJ {int(round(aostj_val))} mm")

        if ascao_val is not None:
            if ascao_idx is not None:
                ao_items.append(f"AscAo {int(round(ascao_val))} mm, {ascao_idx:.1f} mm/m²")
                if ascao_idx > 17:
                    ao_abnormals.append(
                        f"Aorta ascendens (AscAo) is gedilateerd ({int(round(ascao_val))} mm, {ascao_idx:.1f} mm/m²)."
                    )
            else:
                ao_items.append(f"AscAo {int(round(ascao_val))} mm")

        if ao_items:
            overall = "Aorta gedilateerd" if ao_abnormals else "Aorta niet gedilateerd"
            report.append(f"AO: {overall} ({', '.join(ao_items)}).")
            for abnormal in ao_abnormals:
                report.append(abnormal)
    except Exception:
        pass

    report.append("")

    rv_label = str(ctx.rv_hypertrofie or "")
    detail_parts: List[str] = []
    if ctx.rvfwd_val is not None:
        detail_parts.append(f"RVFWd {int(round(ctx.rvfwd_val))}mm")
    if ctx.rvbd_val is not None:
        detail_parts.append(f"RVBDd {int(round(ctx.rvbd_val))}mm")
    if ctx.rvmd_val is not None:
        detail_parts.append(f"RVMDd {int(round(ctx.rvmd_val))}mm")
    if detail_parts:
        rv_label = f"{rv_label} ({'; '.join(detail_parts)})"

    tapse = ctx.tapse
    rv_dilatatie = ctx.rv_dilatatie or ""
    rv_functie = ctx.rv_functie or ""
    pasp_text = ctx.pasp_text or ""
    if tapse is not None:
        tapse_txt = f"TAPSE {tapse} mm"
        report.append(f"RV: {rv_label}, {rv_dilatatie} met {rv_functie} ({tapse_txt}). {pasp_text}")
    else:
        report.append(f"RV: {rv_label}, {rv_dilatatie} met {rv_functie}. {pasp_text}")

    ravi_val = ctx.ravi_val
    ra_dilatatie = ctx.ra_dilatatie or ""
    if ravi_val is not None:
        report.append(f"RA: {ra_dilatatie}. (RAVI {ravi_val} mL/m²).")
    else:
        report.append(f"RA: {ra_dilatatie}.")

    report.append("")

    ak_meas_parts: List[str] = []
    ak_v = _get_session_float(ctx, 'ak_vmax')
    ak_m = _get_session_float(ctx, 'ak_mean')
    ak_ava = _get_session_float(ctx, 'ava')
    if ak_m is not None:
        ak_meas_parts.append(f"MeanG {int(round(ak_m))} mmHg")
    if ak_v is not None:
        ak_meas_parts.insert(0, f"Vmax {ak_v:.2f} m/s")
    if ak_ava is not None:
        ava_idx_val: Optional[float] = None
        try:
            if bsa and float(bsa) > 0:
                ava_idx_val = round(ak_ava / float(bsa), 2)
        except Exception:
            ava_idx_val = None
        if ava_idx_val is not None:
            ak_meas_parts.append(f"AVA {ak_ava:.2f} cm², {ava_idx_val:.2f} cm²/m²")
        else:
            ak_meas_parts.append(f"AVA {ak_ava:.2f} cm²")

    sv_raw = _get_session_float(ctx, 'sv')
    if sv_raw is not None:
        svi_val: Optional[float] = None
        try:
            if bsa and float(bsa) > 0:
                svi_val = round(sv_raw / float(bsa), 1)
        except Exception:
            svi_val = None
        if svi_val is not None:
            ak_meas_parts.append(f"SV {int(round(sv_raw))} mL, SVi {svi_val:.1f} mL/m²")
        else:
            ak_meas_parts.append(f"SV {int(round(sv_raw))} mL")

    lflg_note = ""
    try:
        mean_g = ak_m
        svi_val_report = None
        if sv_raw is not None and bsa and float(bsa) > 0:
            svi_val_report = round(sv_raw / float(bsa), 1)
        ava_idx_report = None
        if ak_ava is not None and bsa and float(bsa) > 0:
            ava_idx_report = round(ak_ava / float(bsa), 2)
        if ((ak_ava is not None and ak_ava < 1.0) or (ava_idx_report is not None and ava_idx_report < 0.6)) \
            and (mean_g is not None and mean_g < 40) and (svi_val_report is not None and svi_val_report <= 35):
            lflg_note = " (low-flow low-gradient patroon: AVA <1.0 cm² of indexed <0.6 cm²/m² met mean <40 mmHg en SVi <=35 mL/m²)"
    except Exception:
        lflg_note = ""

    # Determine automatic AK stenosis grading if user hasn't provided one
    ak_stenose_label = ctx.ak_stenose or ""
    try:
        # compute indexed AVA if possible
        ava_idx_report = None
        if ak_ava is not None and bsa and float(bsa) > 0:
            ava_idx_report = round(ak_ava / float(bsa), 2)
        # Very severe
        if (ak_v is not None and ak_v > 5.0) or (ak_m is not None and ak_m > 60):
            auto_label = "Zeer ernstige stenose"
        # Severe criteria (consistent with guideline thresholds)
        elif ((ak_v is not None and ak_v >= 4.0) or (ak_m is not None and ak_m >= 40)
              or (ak_ava is not None and ak_ava < 1.0) or (ava_idx_report is not None and ava_idx_report < 0.6)):
            auto_label = "Ernstige stenose"
        # Moderate
        elif ((ak_v is not None and ak_v >= 3.0) or (ak_m is not None and ak_m >= 20)
              or (ak_ava is not None and ak_ava <= 1.5) or (ava_idx_report is not None and ava_idx_report <= 0.85)):
            auto_label = "Matige stenose"
        # Mild
        elif ((ak_v is not None and ak_v >= 2.5) or (ak_m is not None and ak_m >= 10)
              or (ak_ava is not None and ak_ava <= 2.0)):
            auto_label = "Milde stenose"
        else:
            auto_label = "Geen stenose"
        if not ak_stenose_label:
            ak_stenose_label = auto_label
    except Exception:
        if not ak_stenose_label:
            ak_stenose_label = ""

    ak_line = f"AK: {ctx.ak_morfologie or ''}. {ctx.ak_calcificatie or ''}. {ak_stenose_label}{lflg_note}"
    if ak_meas_parts:
        ak_line += f" ({', '.join(ak_meas_parts)})"
    ak_line += f". {ctx.ak_regurgitatie or ''}."
    report.append(ak_line)

    mk_meas_parts: List[str] = []
    mk_eroa = _get_session_float(ctx, 'mk_eroa')
    mk_regvol = _get_session_float(ctx, 'mk_regvol')
    mk_rf = _get_session_float(ctx, 'mk_rf')
    if mk_eroa is not None:
        mk_meas_parts.append(f"EROA {mk_eroa:.2f} cm²")
    if mk_regvol is not None:
        mk_meas_parts.append(f"RegVol {int(round(mk_regvol))} mL")
    if mk_rf is not None:
        mk_meas_parts.append(f"RF {mk_rf:.0f}%")
    mk_line = f"MK: Normale morfologie. {ctx.mk_regurgitatie or ''}."
    if mk_meas_parts:
        mk_line = mk_line[:-1] + f" ({', '.join(mk_meas_parts)})."
    report.append(mk_line)

    tk_meas_parts: List[str] = []
    tk_eroa = _get_session_float(ctx, 'tk_eroa')
    tk_regvol = _get_session_float(ctx, 'tk_regvol')
    tk_rf = _get_session_float(ctx, 'tk_rf')
    tk_vcw = _get_session_float(ctx, 'tk_vcw')
    if tk_eroa is not None:
        tk_meas_parts.append(f"EROA {tk_eroa:.2f} cm²")
    if tk_regvol is not None:
        tk_meas_parts.append(f"RegVol {int(round(tk_regvol))} mL")
    if tk_rf is not None:
        tk_meas_parts.append(f"RF {tk_rf:.0f}%")
    if tk_vcw is not None:
        tk_meas_parts.append(f"VCW {tk_vcw:.2f} cm")

    tk_line = f"TK: Normale morfologie. {ctx.tk_regurgitatie or ''}."
    if tk_meas_parts:
        tk_line = tk_line[:-1] + f" ({', '.join(tk_meas_parts)})."
    report.append(tk_line)

    report.append(f"PK: Normale morfologie. {ctx.pk_regurgitatie or ''}.")

    # Include PK quantitative measurements when present
    pk_meas_parts: List[str] = []
    pk_eroa = _get_session_float(ctx, 'pk_eroa')
    pk_regvol = _get_session_float(ctx, 'pk_regvol')
    pk_rf = _get_session_float(ctx, 'pk_rf')
    pk_dt = _get_session_float(ctx, 'pk_dt_regjet')
    pk_pht = _get_session_float(ctx, 'pk_pht_regjet')
    pk_pr_index = _get_session_float(ctx, 'pk_pr_index')
    if pk_eroa is not None:
        pk_meas_parts.append(f"EROA {pk_eroa:.2f} cm²")
    if pk_regvol is not None:
        pk_meas_parts.append(f"RegVol {int(round(pk_regvol))} mL")
    if pk_rf is not None:
        pk_meas_parts.append(f"RF {pk_rf:.0f}%")
    if pk_dt is not None:
        try:
            pk_meas_parts.append(f"DT {int(round(pk_dt))} ms")
        except Exception:
            pk_meas_parts.append(f"DT {pk_dt}")
    if pk_pht is not None:
        try:
            pk_meas_parts.append(f"PHT {int(round(pk_pht))} ms")
        except Exception:
            pk_meas_parts.append(f"PHT {pk_pht}")
    if pk_pr_index is not None:
        pk_meas_parts.append(f"PR-index {pk_pr_index:.2f}")

    if pk_meas_parts:
        # Replace the previously appended simple PK line with a richer one
        # Remove the last appended simple PK line and append enhanced version
        if report and report[-1].startswith("PK:"):
            report.pop()
        pk_line = f"PK: Normale morfologie. {ctx.pk_regurgitatie or ''}"
        pk_line += f" ({', '.join(pk_meas_parts)})."
        report.append(pk_line)

    report.append("Pericardium is normaal zonder effusie.")
    report.append("Endocardium geen tekens van infectie.")
    report.append(f"IVC is {ctx.ivc_dilatatie or ''} {ctx.ivc_variatie or ''}. CVD bedraagt {ctx.cvd or ''} mmHg.")

    return "\n".join(report)


def generate_guideline_recommendations(context: Union[EchoReportInput, Dict[str, Any]]) -> List[str]:
    """Return guideline-driven recommendations list for the current study."""

    ctx = _coerce_echo_input(context)
    bsa = ctx.bsa
    sex = ctx.sex
    leeftijd = ctx.leeftijd
    ak_stenose = ctx.ak_stenose or ""
    mk_regurgitatie = ctx.mk_regurgitatie or ""
    ak_morfologie = ctx.ak_morfologie or ""

    recs: List[str] = []

    try:
        lvef_val = _get_session_float(ctx, "lvef")
        lvids_v = _get_session_float(ctx, "lvids")
        lvidd_v = _get_session_float(ctx, "lvidd")
        lvesdi_v = None
        if lvids_v is not None and bsa and float(bsa) > 0:
            lvesdi_v = round(lvids_v / float(bsa), 1)

        la_vol_raw = _get_session_float(ctx, "la_volume")
        lavi_v = None
        if la_vol_raw is not None and bsa and float(bsa) > 0:
            lavi_v = round(la_vol_raw / float(bsa), 1)

        pasp_v = _get_session_float(ctx, "pasp_raw")

        ak_vmax = _get_session_float(ctx, 'ak_vmax')
        ak_mean_g = _get_session_float(ctx, 'ak_mean')
        ak_ava_v = _get_session_float(ctx, 'ava')
        ak_ava_idx_v = None
        if ak_ava_v is not None and bsa and float(bsa) > 0:
            ak_ava_idx_v = round(ak_ava_v / float(bsa), 2)
        sv_v = _get_session_float(ctx, 'sv')
        svi_v = None
        if sv_v is not None and bsa and float(bsa) > 0:
            svi_v = round(sv_v / float(bsa), 1)

        mk_eroa_v = _get_session_float(ctx, 'mk_eroa')
        mk_regvol_v = _get_session_float(ctx, 'mk_regvol')
        mk_rf_v = _get_session_float(ctx, 'mk_rf')
    except Exception:
        return recs

    mk_sev = mitral_regurgitation_severity(mk_eroa_v, mk_regvol_v, mk_rf_v)
    severe_mr = "Ernstige mitralis regurgitatie" in str(mk_regurgitatie) or mk_sev == 3

    def severe_as_detected() -> bool:
        try:
            if "Ernstige stenose" in str(ak_stenose):
                return True
            if ak_vmax is not None and ak_vmax >= 4.0:
                return True
            if ak_mean_g is not None and ak_mean_g >= 40:
                return True
            if ak_ava_v is not None and ak_ava_v < 1.0:
                return True
            if ak_ava_idx_v is not None and ak_ava_idx_v < 0.6:
                return True
        except Exception:
            pass
        return False

    severe_as = severe_as_detected()

    lflg = False
    try:
        if ((ak_ava_v is not None and ak_ava_v < 1.0) or (ak_ava_idx_v is not None and ak_ava_idx_v < 0.6)) \
            and (ak_mean_g is not None and ak_mean_g < 40) and (svi_v is not None and svi_v <= 35):
            lflg = True
    except Exception:
        lflg = False

    if severe_mr:
        recs.append("Ernstige primaire mitralisregurgitatie vastgesteld.")
        if ctx.session_state.get('mr_sympt', False):
            recs.append("Mitralisklepchirurgie is aangewezen bij ernstige primaire MR met symptomen (I-B).")
        if lvef_val is not None and lvef_val <= 60:
            recs.append("Chirurgie aangewezen: LVEF ≤60% (I-B).")
        if lvids_v is not None and lvids_v > 40:
            recs.append("Chirurgie aangewezen: LVESD >40 mm (I-B).")
        if lvesdi_v is not None and lvesdi_v >= 20:
            recs.append("Chirurgie aangewezen: LVESDi ≥20 mm/m² (I-B).")
        if pasp_v is not None and pasp_v > 50:
            recs.append("Pulmonale hypertensie met sPAP >50 mmHg (IIa-B).")
        if lavi_v is not None and lavi_v > 60:
            recs.append("LA dilatatie (LAVI >60 mL/m²) (IIa-B).")
        if ctx.session_state.get('af_present', False):
            recs.append("Voorkamerfibrillatie bij ernstige MR (IIa-B).")
        recs.append("Chirurgisch klepherstel heeft de voorkeur (I-B).")
        recs.append("Minimaal invasieve klepchirurgie kan overwogen worden (IIb).")
        if ctx.session_state.get('mr_sympt', False):
            recs.append("TEER kan worden overwogen bij symptomatische ernstige MR met hoog chirurgisch risico en geschikte anatomie.")

    if severe_as:
        recs.append("Ernstige aortaklepstenose vastgesteld.")
        if ctx.session_state.get('as_sympt', False):
            recs.append("Interventie aangewezen bij symptomatische ernstige AS (I-B).")
        if lflg:
            recs.append("Low-flow low-gradient patroon met ernstig stenoseprofiel.")
        if lvef_val is not None:
            if lvef_val < 50:
                recs.append("Interventie aangewezen bij LVEF <50% zonder andere oorzaak (I-B).")
            elif lvef_val < 55:
                recs.append("Interventie te overwegen bij LVEF <55% zonder andere oorzaak (IIa).")
        if ctx.session_state.get('as_sbp_drop', False):
            recs.append("Bloeddrukdaling >20 mmHg bij inspanning (IIa).")
        if ak_mean_g is not None and ak_mean_g > 60:
            recs.append("Zeer ernstige AS: mean gradiënt >60 mmHg (IIa).")
        if ak_vmax is not None and ak_vmax > 5.0:
            recs.append("Zeer ernstige AS: Vmax >5.0 m/s (IIa).")
        calc = ctx.session_state.get('as_calc_score', 0)
        try:
            if calc and ((sex == 'Man' and calc > 2000) or (sex != 'Man' and calc > 1200)):
                recs.append("Ernstige calcificatie ondersteunt interventie (IIa).")
        except Exception:
            pass
        prog = ctx.session_state.get('as_vmax_prog', 0.0)
        try:
            if prog and prog > 0.3:
                recs.append("Vmax-progressie >0.3 m/s/jaar (IIa).")
        except Exception:
            pass
        bnp_val = ctx.session_state.get('as_bnp', 0)
        try:
            if bnp_val and bnp_val > 0:
                recs.append("Verhoogde BNP/NT-proBNP ondersteunt interventie (IIa).")
        except Exception:
            pass

        try:
            age_int = int(leeftijd)
        except Exception:
            age_int = None
        if age_int is not None:
            if age_int >= 70:
                recs.append("TAVI aanbevolen bij geschikte anatomie (I-A).")
            else:
                recs.append("SAVR aanbevolen bij leeftijd <70 jaar en laag operatierisico (I-B). TAVI kan worden overwogen afhankelijk van anatomie/risico (IIa/IIb).")

    try:
        ao_vals: List[float] = []
        ao_idx_vals: List[float] = []
        for key in ['aoa', 'aosv', 'aostj', 'ascao']:
            val = _get_session_float(ctx, key)
            if val is None:
                continue
            ao_vals.append(val)
            if bsa and float(bsa) > 0:
                ao_idx_vals.append(round(val / float(bsa), 1))
        max_ao = max(ao_vals) if ao_vals else None
        max_ao_idx = max(ao_idx_vals) if ao_idx_vals else None
        bicuspid = 'bicus' in str(ak_morfologie).lower()
        if max_ao is not None:
            if max_ao >= 55:
                recs.append("Aorta ascendens ≥55 mm: chirurgie aanbevolen (I-B).")
            elif max_ao >= 50:
                if bicuspid or sex == 'Man':
                    recs.append("Aorta ascendens ≥50 mm: overweeg chirurgie (IIa), zeker bij bicuspide anatomie of man.")
                else:
                    recs.append("Aorta ascendens ≥50 mm: overweeg chirurgie (IIa).")
            if max_ao >= 45 and ("Ernstige stenose" in str(ak_stenose) or severe_as):
                recs.append("Bij indicatie voor klepchirurgie en AscAo ≥45 mm: gelijktijdige aortachirurgie overwegen (IIa).")
            if 45 <= max_ao < 50:
                recs.append("AscAo 45-49 mm: controle CT/MRI/echo om de 6-12 maanden.")
            elif 40 <= max_ao < 45:
                recs.append("AscAo 40-44 mm: controle beeldvorming jaarlijks.")
            elif max_ao_idx is not None and max_ao_idx > 17 and max_ao < 40:
                recs.append("AscAo index >17 mm/m²: overweeg jaarlijkse opvolging ondanks absolute <40 mm.")
            elif max_ao is not None and max_ao >= 37:
                recs.append("AscAo 37-39 mm: herbeoordeling binnen 2-3 jaar indien stabiel.")
            if 30 <= max_ao < 40:
                recs.append("Aorta 30-40 mm: TTE elke 3 jaar.")
            if 40 <= max_ao <= 44:
                recs.append("Aorta 40-44 mm: baseline CT/MR aorta + TTE controle in 1 jaar; bij groei >3 mm/jaar bevestigen met CT/MR en daarna elke 6 maanden TTE; bij groei <3 mm/jaar TTE elke 2 jaar.")
            if 45 <= max_ao <= 49:
                recs.append("Aorta 45-49 mm: baseline CT/MR aorta en TTE elke 6 maanden.")
            if 50 <= max_ao <= 52:
                recs.append("Aorta 50-52 mm: baseline CT/MR aorta; bij hoog-risico kenmerken (familiale aorta-event, ongecontroleerde hypertensie, leeftijd <50 j) kan chirurgie overwogen worden (IIb); anders elke 6 maanden nieuwe beeldvorming; bij groei >3 mm/jaar chirurgie overwegen.")
            if 50 <= max_ao <= 54:
                recs.append("Aorta 50-54 mm: baseline CT/MR aorta; bij wortel-fenotype en bicuspide klep chirurgie (I); bij wortel-fenotype en tricuspide klep chirurgie te overwegen (IIb).")
            if max_ao > 55:
                recs.append("Aorta >55 mm: chirurgie (I).")
            recs.append("Bij aorta-aneurysma of thoracale dissectie met HTAD-risicofactoren genetische testing aangewezen (<60 j, geen klassieke risicofactoren, familiaal plots overlijden, andere aneurysmata, familiale TAD, syndromale kenmerken Marfan/Loeys-Dietz/Ehlers-Danlos).")
    except Exception:
        pass

    return recs


def summarize_echo_for_brief(context: Union[EchoReportInput, Dict[str, Any]]) -> str:
    """Return a compact echo summary suitable for the brief letter."""

    ctx = _coerce_echo_input(context)
    bsa = ctx.bsa
    parts: List[str] = []

    systolic_parts: List[str] = []
    if ctx.systolic_option:
        systolic_parts.append(ctx.systolic_option)
    if ctx.lvef is not None:
        systolic_parts.append(f"LVEF {ctx.lvef:.0f}%")
    if systolic_parts:
        parts.append(" ".join(systolic_parts))

    if ctx.lv_dilatatie_choice:
        parts.append(f"LV: {ctx.lv_dilatatie_choice}.")
    if ctx.la_choice or ctx.la_suggested:
        la_label = ctx.la_choice or ctx.la_suggested
        parts.append(f"LA: {la_label}.")

    if ctx.ak_stenose:
        parts.append(f"AK: {ctx.ak_stenose}.")
    else:
        # compute automatic AK stenosis label for brief summary when not provided
        try:
            ak_v = _get_session_float(ctx, 'ak_vmax')
            ak_m = _get_session_float(ctx, 'ak_mean')
            ak_ava = _get_session_float(ctx, 'ava')
            ava_idx_val = None
            if ak_ava is not None and bsa and float(bsa) > 0:
                ava_idx_val = round(ak_ava / float(bsa), 2)
            if (ak_v is not None and ak_v > 5.0) or (ak_m is not None and ak_m > 60):
                auto_label = 'Zeer ernstige stenose'
            elif ((ak_v is not None and ak_v >= 4.0) or (ak_m is not None and ak_m >= 40)
                  or (ak_ava is not None and ak_ava < 1.0) or (ava_idx_val is not None and ava_idx_val < 0.6)):
                auto_label = 'Ernstige stenose'
            elif ((ak_v is not None and ak_v >= 3.0) or (ak_m is not None and ak_m >= 20)
                  or (ak_ava is not None and ak_ava <= 1.5) or (ava_idx_val is not None and ava_idx_val <= 0.85)):
                auto_label = 'Matige stenose'
            elif ((ak_v is not None and ak_v >= 2.5) or (ak_m is not None and ak_m >= 10)
                  or (ak_ava is not None and ak_ava <= 2.0)):
                auto_label = 'Milde stenose'
            else:
                auto_label = 'Geen stenose'
            parts.append(f"AK: {auto_label}.")
        except Exception:
            pass
    if ctx.mk_regurgitatie:
        parts.append(f"MK: {ctx.mk_regurgitatie}.")
    if ctx.tk_regurgitatie:
        parts.append(f"TK: {ctx.tk_regurgitatie}.")
    if ctx.pk_regurgitatie:
        parts.append(f"PK: {ctx.pk_regurgitatie}.")

    if ctx.pasp_text:
        parts.append(ctx.pasp_text.strip())

    text = " ".join(part.strip() for part in parts if part).strip()
    return text or "Geen echogegevens beschikbaar."


def compose_brief_letter(
    patient: PatientContext,
    consult_date: Optional[dt.date],
    voorgeschiedenis: str,
    anamnese: str,
    thuismedicatie: str,
    clinical_exam: Dict[str, Any],
    investigations: Sequence[Dict[str, Any]],
    bespreking: str,
) -> str:
    """Compose the full consult letter using the provided sections."""

    def _fmt_block(value: Optional[str]) -> str:
        if not value:
            return "-"
        text = str(value).strip()
        return text or "-"

    def _find_section(label_substrs: List[str]) -> Optional[Dict[str, Any]]:
        for sec in investigations:
            lab = (sec.get("label") or "").lower()
            for s in label_substrs:
                if s.lower() in lab:
                    return sec
        return None

    name = patient.full_name or "uw patiënt"
    date_txt = consult_date.strftime("%d-%m-%Y") if consult_date else "vandaag"

    lines: List[str] = []
    lines.append("Geachte collega")
    lines.append("")
    lines.append(f"Wij zagen uw patiënt op de raadpleging cardiologie op {date_txt}.")
    lines.append("")

    # Voorgeschiedenis
    lines.append("Voorgeschiedenis")
    lines.append("-------------------------")
    lines.append(_fmt_block(voorgeschiedenis))
    lines.append("")

    # Anamnese
    lines.append("Anamnese")
    lines.append("-------------------------")
    lines.append(_fmt_block(anamnese))
    lines.append("")

    # Huidige Medicatie
    lines.append("Huidige Medicatie")
    lines.append("-------------------------")
    lines.append(_fmt_block(thuismedicatie))
    lines.append("")

    # Klinisch onderzoek
    pols = clinical_exam.get("pols")
    bp = clinical_exam.get("blood_pressure") or (None, None)
    ausc = clinical_exam.get("auscultation")

    lines.append("Klinisch onderzoek")
    lines.append("-------------------------")
    exam_lines: List[str] = []
    if pols is not None:
        exam_lines.append(f"Pols {int(round(pols))}/min.")
    if bp and bp[0] is not None and bp[1] is not None:
        exam_lines.append(f"Bloeddruk {int(round(bp[0]))}/{int(round(bp[1]))} mmHg.")
    if ausc:
        exam_lines.append(f"Hartauscultatie: {ausc.strip()}")
    # default general inspection line
    exam_lines.insert(0, "Algemene inspectie: normale indruk")
    lines.extend(exam_lines)
    lines.append("")

    # Investigations in preferred order
    # ECG
    ecg_sec = _find_section(["ecg", "elektrocardiogram"]) or {}
    if ecg_sec:
        perf = ecg_sec.get("performed_on")
        label = f"Elektrocardiogram in rust ({perf})" if perf else "Elektrocardiogram in rust"
        lines.append(label)
        lines.append("-------------------------")
        lines.append(ecg_sec.get("text", "-"))
        lines.append("")

    # Fietstest / Cyclo-ergometrie
    fietstest_sec = _find_section(["fietstest", "cyclo", "ergometrie"]) or {}
    if fietstest_sec:
        perf = fietstest_sec.get("performed_on")
        label = f"Cyclo-ergometrie ({perf})" if perf else "Cyclo-ergometrie"
        lines.append(label)
        lines.append("-------------------------")
        ft_text = fietstest_sec.get("text", "-")
        lines.append(ft_text)
        lines.append("")

    # Echo
    echo_sec = _find_section(["echo", "transthoracale", "transthoracische"]) or {}
    if echo_sec:
        perf = echo_sec.get("performed_on")
        label = f"Transthoracale Echocardiografie ({perf})" if perf else "Transthoracale Echocardiografie"
        lines.append(label)
        lines.append("-------------------------")
        lines.append(echo_sec.get("text", "-"))
        lines.append("")

    # Device controle
    cied_sec = _find_section(["cied", "device", "pacemaker"]) or {}
    if cied_sec:
        perf = cied_sec.get("performed_on")
        label = f"Device controle ({perf})" if perf else "Device controle"
        lines.append(label)
        lines.append("-------------------------")
        lines.append(cied_sec.get("text", "-"))
        lines.append("")

    # Holter
    holter_sec = _find_section(["holter"]) or {}
    if holter_sec:
        perf = holter_sec.get("performed_on")
        label = f"Holter ({perf})" if perf else "Holter"
        lines.append(label)
        lines.append("-------------------------")
        lines.append(holter_sec.get("text", "-"))
        lines.append("")

    # Bespreking
    lines.append("Bespreking")
    lines.append("-------------------------")
    lines.append(_fmt_block(bespreking))
    lines.append("")
    lines.append("Met collegiale hoogachting,")
    lines.append("Dr. A. Ballet Cardiologie")

    return "\n".join(lines).strip() + "\n"
