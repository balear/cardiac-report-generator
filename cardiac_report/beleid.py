"""Beleid module.

Bevat klinische scenario's en bijhorende plannen.

Deze module exporteert `CLINICAL_SCENARIOS` zodat `app.py` de scenario's kan laden
zonder een grote inline dictionary.
"""

from __future__ import annotations

from typing import Dict, List


ClinicalScenario = Dict[str, object]


CLINICAL_SCENARIOS: Dict[str, ClinicalScenario] = {
    
    "Aritmogene rechter ventrikel cardiomyopathie (ARVC)": {
        "description": "Diagnostiek, behandeling en ICD-indicaties bij ARVC",
        "plan": [
            """
Aritmogene rechter ventrikel cardiomyopathie
Genetische counseling en testen bij vermoeden of bevestigde diagnose van ARVC (I).
Geen zware inspanningen bij patiënten met pathogene mutatie en zonder fenotype (IIb)
Betablokker therapie bij patiënten met ARVC (IIb)
Indicatie voor ICD zo aritmogene syncope (IIa), ernstige RV of LV systolische dysfunctie (IIa), matige RV of LV systolische dysfunctie en inducerbaarheid op EFO (IIa).
Bij verdachte symptomen e.g. syncope of palpitaties is een EFO studie te overwegen. (IIb)
Behandeling van SMVT of ICD shocks ondanks BB moet katheter ablatie overwogen worden in gespecialiseerde centra (IIa).
Bij vermoeden van ARVC is een cardiale MR aangewezen (I).
""",
        ],
    },
    "Intraveneus ijzer / Injectafer (Ferric carboxymaltose)": {
        "description": "Klinische criteria en dosering voor intraveneuze ijzertoediening (Injectafer) bij hartfalen/ijzerdeficiëntie",
        "plan": [
            """
Intraveneus ijzer moet overwogen worden (klasse IIa, LOE A) bij symptomatische HFrEF-patiënten en ijzerdeficiëntie
- serum ferritine <100µg/l, of
- serum ferritine 100-299µg/l en transferrine saturatie <20%
Injectafer® wordt nu ook terugbetaald voor cardiologen bij hartfalen bij de ambulante patiënt: 
Anemie (man Hb < 13 g/dl, vrouw Hb < 12 g/dl) door bewezen en gedocumenteerde ijzer-malobsorptie (indien voorgeschreven voor chronische inflammatie zoals hartfalen, chronisch nierlijden, …)
Dosering: 
50-70kg en Hemoglobine >10g/dl
1000mg IV eenmalig week 1 
>70kg en Hemoglobine >10g/dL
1000mg IV week 1 en 500mg IV week 2. 
50-70kg en Hemoglobine <10g/dL
1000mg IV week 1 en 500mg IV week 2. 
>70kg en Hemoglobine < 10g/dl 
1000mg IV week 1 en 1000mg IV week 2. 
De toediening gebeurt via opname in het daghospitaal.
Patiënt dient 10 weken na toediening Injectafer® voor een bloedcontrole te gaan in het ziekenhuis of bij de huisdokter teneinde om de werking van de intraveneuze ijzertoediening te kunnen evalueren.
""",
        ],
    },
    "Dyspnee Workup dr. Ballet": {
        "description": "Uitgebreide dyspneu-workup volgens dr. Ballet",
        "plan": [
            """
Labo met complete celtelling, nierfunctie, elektrolyten, CK,  TSH, T4, ijzerstatus, HbA1C, glucose en NT-proBNP. 
CT coronairen of coronarografie zo vermoeden van coronair lijden. 
Holter monitoring bij vermoeden aritmie. 
RX thorax F/P of Low dose CT thorax
Volledige longfunctie (Spirometrie met reversibiliteit,  flow-volume loop, longvolumes, diffusiecapaciteit en bodybox luchtwegweerstand) + FeNO bij vermoeden astma. 
Electrocardiogram (ECG)  
Transthoracale echocardiografie (TTE) - (HFpEF/HFrEF, pericardiale ziekten, pulmonale hypertensie)
Fietsproef 
CT coronairen of coronarografie zo vermoeden van coronair lijden. 
Ligfiets echocardiografie (indicatie bij dyspnee van onbekende origine, vermoeden myocardischemie, mitralisklepregurgitatie, pulmonale hypertensie, low gradient aorta stenose, LVOT obstructie en MR bij HOCM) 
Cardiopulmonale exercise testing (CPET) te plannen zo bovenstaande negatief. 
Rechter hartcatheterisatie (RHC) bij vermoeden pulmonale hypertensie plan.. Diagnose zo mPAP >20 mmHg. 
CT sinussen bij vermoeden bovenste luchtweg probleem
Spierbiopsie bij vermoeden van myopathie. 
V/Q scan bij voorgeschiedenis (CTEPH) of vermoeden longembolen. 
Gastroscopie bij vermoeden GERD. 
Cardiale MRI Bij vermoeden cardiomyopathie 
Botscan zo vermoeden amyloïdose
""",
        ],
    },
    "Atriumflutter": {
        "description": "Beleid bij atriumflutter: anticoagulatie, cardioversie en ablatie-overwegingen",
        "plan": [
            """
Atriumflutter
Atriumflutter  zonder concomitante aanwezigheid van atriumfibrillatie moet overwogen worden voor anticoagulatie maar de drempel is onduidelijk (IIa-C).
Atriale pacing is aangewezen voor terminatie van atriale flutter in aanwezigheid van atriale lead (I-B).
Elektrische cardioversie is aangewezen met lage energie <100 J.
Katheterablatie moet overwogen worden na een eerste episode van symptomatische typische atriumflutter (IIa-B).  Zo geen duidelijk reversibele oorzaak is er een zeer hoge kans op recidief. Anti-aritmica zijn minder effectief dan katheterablatie. Bij katheterablatie is er 95% kans op volledig curatief succes zonder recidief.

Katheterablatie is aanbevolen bij symptomatische, herhaalde episodes van CTI-afhankelijke atriumflutter (I-A).
Katheterablatie is aanbevolen bij symptomatische, herhaalde episodes van CTI-onafhankelijke atriumflutter in ervaren centrum (I-B).
Katheterablatie is aanbevolen bij persistente atriumflutter voor tachycardiomyopathie (I-B)
""",
        ],
    },
    
    "Chronisch hartfalen HFrEF": {
        "description": "Klassiek pharmacologisch beleid en doelstellingen voor chronisch hartfalen met verminderde ejectiefractie (HFrEF)",
        "plan": [
            """
Chronisch hartfalen HFrEF

Beta blocker 
Bisoprolol 2.5mg 1x/d - target 10mg 1x/d
Carvedilol 6.25mg 2x/d - target 12.5mg 2x/d
Dosis verdubbelen elke 2 weken. 
Mineralocorticoid Receptor Antagonists (MRA)
Aldactone  (Spironolactone) 25mg 1x/d - target 50mg 1x/d
Controle bloedname met nierfunctie en elektrolieten na 1 en 4 weken. Dosis verdubbelen na 4 weken. 
Angiotensin Receptor-Neprilysin Inhibitor (ARNI)
Entresto ® (Valsartan/Sacubutril) 49/51mg 2x/d - target 97/103mg 2x/d
Controle bloedname met nierfunctie en  elektrolieten na 2 weken. Dosis verdubbelen elke 2 weken. 
If - current Inhibitor
Procoralan (Ivabradine) 5mg 2x/d - Target 7.5mg 2x/d.
Sodium-Glucose Cotransporter 2 inhibitors (SGLT-2 inh)
Forxiga 10mg 1x/d.
""",
        ],
    },
    "Cardiale Amyloidose": {
        "description": "Diagnostiek en beslisregels voor cardiale amyloidose (AL en ATTR)",
        "plan": [
            """
Cardiale Amyloidose
Bij vermoeden van een clonale plasma cel aandoening (e.g. multipel myeloom, AL amyloidose, MGUS, Waldenstrom macroglobulinemie):
- Thoracale 99mTc-HMDP bot scintigrafie met SPECT
- Complete celtelling (CBC)
- Serum calcium en creatinine
- Serum electroforese met immunofixatie
- Serum free light chain (FLC assay beter dan urinaire SPEP) - abnormale FLC ratio is hoger risico op progressie
- Serum IgG, IgA, IgM  (zo gereduceerd = mogelijk maligne)
- 24 uurs urinecollectie met serum elektroforese en immunofixatie (verplicht zo serum elektroforese, immunofixatie of FLC afwijkend)
- Serum albumine, serum LDH, serum beta 2-microglobuline
- Serum transthyretine

In functie van bevindingen nog aan te vullen met cardiale MRI.
-> Zo IgG type, monoclonaal eiwit <1.5 g/dL en normale FLC ratio en geen symptomen suggestief voor monoclonale plasma cel aandoening: geen andere workup.
Anders -> Beenmergpunctie (incl. aspiratie en biopsie met immunofenotypering, conventionele cytogenetica en FISH), beeldvorming van botten (full body low dose CT).
Workup-indicaties bij anemie, nierfunctiestoornis of abnormale eiwitten zoals beschreven.

Beoordeling scintigrafie en vervolg:
- Scintigrafie toont geen cardiale uptake en beoordelingen voor monoklonale proteïnen zijn negatief: kans op cardiale amyloïdose zeer klein; overweeg alternatieve diagnose.
- Scintigrafie toont graad 1 uptake en tekenen/symptomen/beeldvorming suggestief voor cardiale amyloidose: indicatie voor histologische bevestiging (cardiale/extracardiale).
- Scintigrafie toont geen cardiale uptake en ten minste een van de monoklonale proteïnetests is abnormaal: AL-amyloïdose uitsluiten; CMR kan betrokkenheid bevestigen.
- Scintigrafie toont cardiale uptake en beoordelingen voor monoklonale eiwitten zijn negatief: bij graad 2 of 3 kan ATTR-CA worden bevestigd; vervolg met genetisch onderzoek om ATTRv vs ATTRwt te onderscheiden.
- Scintigrafie toont cardiale uptake en ten minste één monoklonaal proteïnetest is abnormaal: overweeg gelijktijdige MGUS, AL-amyloïdose of co-existentie van AL en ATTR.

Behandeling:
- Behandeling van ATTR-gerelateerde cardiale amyloïdose: Tafamidis 61mg 1x/d.

""",
        ],
    },
    "Gedilateerde cardiomyopathie": {
        "description": "Evaluatie en genetica bij gedilateerde cardiomyopathie (DCM)",
        "plan": [
            """
Gedilateerde cardiomyopathie
Evaluatie naar coronairlijden, bindweefselstoornis, endocriene dysfunctie, medicatie/toxine geïnduceerd. 
Cardiale MRI pet contrast ter evaluatie van etiologie en substraat risico voor VA/SCD. (IIa)
Zo familiale voorgeschiedenis van DCM/HNDCM of plotse dood (<50 jaar, eerste graadsverwant) of AV block <50 jaar dan moet genetische analyse (I) anders moet dit in overweging genomen worden (IIa). 
CT coronairen of coronarografie
- Labo met nierfunctie, ionogram, calcium, CK, fosfaat, ferritine, leverenzymen, NT-proBNP, TSH, T4, troponine. 
- Urinecollectie met urinaire biochemie (creatinine, proteïne)
- 24u holter
- Tweede lijn: carnitine profiel, vrije vetzuren, lactaat, serum antistoffen, serum ACE, thiamine, virale serologie, serum aminozuren, urinaire aminozuren. 
- MRI met contrast zo vermoeden van cardiomyopathie
- Genetica analyse is aangewezen zo patiënt voldoet aan diagnostische criteria van een cardiomyopathie en in gevallen waarin het de diagnose, prognose, therapeutische stratificatie of reproductief beheer van de patiënt mogelijk maakt, of wanneer dit genetische cascade testing mogelijk maakt van hun familieleden die anders die anders aan langetermijnbewaring zouden worden onderworpen.

Bij sudden cardiac death of ventriculair aritmie genetisch onderzoek naar DSC2, DSP, FLNC, PKP2. (CMP panel)
Bij conductie stoornissen met of zonder ventriculaire aritmie, spierkrampen of spierzwakte genetisch onderzoek naar EMD, LMNA. (quasi 100% penetrantie, hoog risico op ventriculaire aritmie, lagere drempel voor ICD)
Bij progressieve spierzwakte test voor BAG3, DES, FHL1, FLNC, LDB3, MYOT, TTN.
Bij spierzwakte, moeilijkheden met wandelen en gestegen CK, test voor DMD.
Bij  neutropenie, myopathie test voor TAZ.
Bij andere test voor BAG3, DES, DSP, FLNC, LMNA, MYH7, PLN, RBM20, SCN5A, TNNC1, TNNT2, TTN. 
""",
        ],
    },
    "Hypertrofe cardiomyopathie": {
        "description": "Evaluatie, genetica en indicaties bij hypertrofe cardiomyopathie (HCM)",
        "plan": [
            """
Hypertrofe cardiomyopathie
- Evaluatie naar hypertensie, chronische nierziekte, athlete’s heart en WT/AL amyloidose. 
- Bij WPW, SVT of AV block test voor PRKAG2
- Bij carpal tunnel, neuropathie test voor TTR (hereditaire transthyretin amyloidose) 
- Bij ataxie, scoliose, diabetes, visus/spraak/gehoorsprobelmeen test voor FXN (Friedreich)
- Bij lactaatacidose, epilepsie en beroertes test voor MTTL1 (Mitochondriaal)
- Bij massieve LVH, progressieve conductie problemen, intelectuele achterstand test voor LAMP2. (Danon, X-linked, man>vrouw)
- Bij progressieve conductie problemen, nierfalen, tintelingen vingers, hyperhidrosis test voor GLA (Fabry, X-linked, man>vrouw) met alpha-galactosidase A activiteit. 
- Bij Pulmonaal stenose, secundum ASD, klein gestalte, craniofaciale problemen test voor BRAF, KRAS, PTPN11, RAFT1, SOS1 (Noonan syndroom)
- Bij andere test voor ACT1, MYBPC3, MYH7, MYL2, MYL3, TNNI3, TNNT, TPM1. 
Een cardiale MRI is aangewezen
""",
        ],
    },
    "Nieuw voorkamerfibrilleren": {
        "description": "Uitgebreide work-up, therapie en ablatie-indicaties bij nieuw voorkamerfibrilleren",
        "plan": [
            """
- Labo met complete celtelling, nierfunctie, leverenzymen, elektrolieten, fosfaat, calcium, PTH, TSH, T4, HbA1C, glucose en NT-proBNP. (I) Bij hypertensie of ander vermoeden ook aldosterone en renine.
- 12 lead electrocardiogram (I)
- Transthoracale echocardiografie (I)
- Inspanningselectrocardiogram
- Strikte controle van risicofactoren en triggers (obesitas, fysiek inactiviteit, roken, alcohol, diabetes en hypertensie). (I)
- Het is redelijk om bij alle patiënten te screenen naar obstructief slaapapneu, hoewel de rol van behandeling van sleep disordered breathing (SDB) in behoud van sinusritme onduidelijk is. (IIb)
- Optimalisatie van bloeddrukcontrole met target 120-129/70-79 mmHg om progressie van AF en cardiovasculaire events te verminderen, mogelijk benefit voor AF met ACE-inhibitor/ARB. (I-B)
- Gewichtsverlies is aangewezen in patiënten met overgewicht (BMI >25kg/m²) of obesitas (BMI >30kg/m²) om tot normaal gewicht te komen BMI 20-25 kg/m².
- Start SGLT-2 inhibitor bij patiënten met hartfalen ongeacht de ejectiefractie om risico op hospitalisatie en cardiovasculaire sterfte te reduceren (IA)
- Bij diabetes is adequate glycemische controle noodzakelijk om de burden en progressie van AF te reduceren best met SGLT-2 of GLP-1 bij overgewicht.
- Reductie van alcohol naar minder dan 30 gram alcohol per week om risico op nieuwe episodes van voorkamerfibrillatie te reduceren.

Additief:
- CT coronairen of coronarografie bij vermoeden coronair lijden, helpt ook voor opstart flecaïnide.
- CT-PA of V/Q scan bij vermoeden longembolen.
- Zo jonge leeftijd (voor 30 jaar) best een EFO voor re-entrant supraventriculaire tachyaritmiën te detecteren en ableren. (IIb)
- Zo jonge leeftijd (voor 45 jaar) zonder duidelijke risicofactoren, best verwijzing voor genetica en surveillance voor cardiomyopathie en aritmogene syndromen. (IIb) AF komt vaak voor in Long QT, Short QT, Brugada, CPVT, ARVC, DCM, WPW en HCM.
- Ambulante ECG monitoring om burden en ventriculair antwoord te evalueren.
- Cardiale MRI bij vermoeden van atriale of ventriculaire cardiomyopathie en om interventionele procedures te plannen
- MRI hersenen en cognitieve testen om cardiovasculaire schade en risico op dementie te evalueren.
- Ajmaline proef kan overwogen worden zo VKF op jonge leeftijd <40 jaar zonder duidelijke oorzaak.
- Zo familiaal voorkomen op jonge leeftijd (<60 jaar) kan een genetische analyse SCN5A, KCNQ1, MYL4, truncating TT) mogelijk nuttig zijn.


Therapie:
Steeds anticoagulatie: Bij CHADSVA van 2 of meer. En sterk overwegen bij CHADSVA van 1.
- Lixiana 60mg 1x/d - verlaag dosis bij CrCl <50 ml/min/1.73m².
- Eliquis 5mg 2x/d - verlaag dosis bij 2 of meer: leeftijd >80, gewicht <60kg, sCreat >1.5mg/dL. Geen gecombineerd gebruik met p-glycoproteïne of krachtige CYP3A4 inhibitors.
- Anticoagulatie is ook steeds aangewezen bij cardiale amyloïdose of hypertrofe cardiomyopathie ongeacht CHADSVA score.
- Anticoagulatie moet altijd gestart worden minstens 3 weken voor katheterablatie om tromboembolisch risico en stroke te reduceren. (I-C) Ononderbroken orale anticoagulatie tijdens procedure is aangeraden. (I-A)
- Anticaogulatie moet altijd nog 2 maanden genomen worden na katheterablatie om ischemische beroerte en trombo-embolie te voorkomen (I-C) nadien is dit afhankelijk van CHADSVA en niet van procedureel succes of symptomen. (I-C)
-  Anticoagulatie is noodzakelijk gedurende ten minste 4 weken bij alle patiënten na elektrische of farmacologische cardioversie (ook bij CHADSVA = 0) en langdurig bij patiënten met trombo-embolische risicofactor(en), ongeacht of sinusritme wordt bereikt. Enkel als AF minder lang dan <24u CHADSVA =0 dan is anticoagulatie optioneel.
-  Een TEE is noodzakelijk zo VKF al langer dan 24u aanwezig en de patiënt nog geen 3 weken van adequate antistolling heeft gehad.

Rate control therapie is aanbevolen, als initiële therapie in de acute setting, als aanvulling op ritmecontrole therapieën of als enige behandelingsstrategie om de hartfrequentie onder controle te houden en de symptomen te verminderen.
Calcium-antagonist (of BB) bij LVEF >40%.
- Progor (Diltiazem) verlengde afgifte 180-360mg 1x/d.  Time to peak 10-14 uur. Halfwaarde tijd 6-9 uur.
Beta-blocker (of digoxin) bij LVEF <40%.
- Bisoprolol 5mg 1x/d.

Indicaties voor rhythm control
- Bij verminderde systolische functie en persistente VKF (I)
- Bij symptomatische VKF (IIa)
- Bij recente diagnose van VKF om hospitalisatie, beroerte en mortaliteit te verlagen (IIa)
- Bij hartfalen om symptomatische en prognostische redenen (mortaliteit en hospitalisatie) (IIa)
- Om progressie van VKF tegen te gaan (IIb)
- Bij HFrEF is early en agressieve rhythm controle aangewezen via catheter ablatie (I-B)
- Bij onduidelijkheid of er symptomen aanwezig zijn, kan trial met rhythm control (IIb)
- Om het risico op dementie en structureel hartlijden tegen te gaan (IIb)
- Anti-aritmica kunnen nuttig zijn of afib in vroege fase na ablatie te voorkomen (IIa)

Antiarrhythmic drugs - Cardioversie VKF
- Apoxard (Flecainide) (2mg/kg) 200mg over 15 mins – Voorkeur bij recente onset als farmacologisch gewenst, niet bij ernstige hypertroof van linkerventrikel, HFrEF of coronairlijden hartlijden, ischemie of hartfalen - Succes 59-78%.
- Cordarone (Amiodarone) 300 mg IV opgelost in 250 mL 5% glucose over 30 min. - Succes 31-51% (AF) - 63-73 %(AFL) bij voorkeur via centrale katheter. Kan nadien gevolgd worden door 900-1200mg IV cordarone best opgelost in 500ml glucose 5% via centrale katheter.

Farmacologische cardioversie is niet aangeraden voor patiënten met sinusknoopdysfunctie, atrioventriculaire conductieproblemen of verlengd QTc (>500ms) tenzij goede overwegen van proaritmogeen effect en risico op bradycardie.

Antiarrhythmic drugs - Rhythm control VKF
-  Apocard retard (Flecainide) 200mg 1x/d - Niet bij structureel hartlijden, ischemie of hartfalen
-  Cordarone (Amiodarone) 200mg 3x/d voor 4 weken, nadien 200mg 1x/d

Indicaties voor catheterablatie
- Als eerstelijns therapie na shared decision making met patiënt bij patiënt met paroxysmale voorkamerfibrillatie om symptomen, nieuwe episodes en progressie van AF tegen te gaan (I-A).
- Als eerstelijns therapie na shared decision making met patiënt bij patiënt met persistente voorkamerfibrillatie om symptomen, nieuwe episodes en progressie van AF te tegen te gaan (IIb-C).
- Bij falen, intolerantie of anti-aritmica niet gewenst, is katheterablatie geïndiceerd bij paroxysmale of persistente artriumfibrillatie ter reductie van symptomen, nieuwe episodes en progressie van AF. (I-A)
- Bij HFrEF is early en agressieve rhythm controle aangewezen via catheter ablatie (I-B)
- Bij falen of intolerantie voor één klasse I of III anti-aritmicum ter behandeling van symptomen bij persistente VKF (I-A)
- Bij symptomatische of klinisch significante atriumflutter is ablatie geindiceerd (I-A)
- Bij jonge patiënten met weinig comorbiditeit kan catheter ablatie als eerste lijn gebruikt worden ter behandeling van symptomen (IIa)
- Bij asymptomatische VKF kan catheterablatie in selecte patiënten (bij jongere patiënten met weinig comorbideit) als eerstelijns therapie gebruikt worden om progressie van VKF en complicaties tegen te gaan. (IIb)
- Bij intolerantie voor betablocker (IIa)
- Bij symptomatische paroxysmale AF (IIa)
- Bij persistente AF als alternatief voor anti-aritmica (IIb)

- Bij AF en HFrEf met hoge kans op tachycardiomyopathie, ongeacht symptomen van AF. (I-B)
- Bij AF en HFrEF zou catheter ablatie overwogen moeten worden om HF hospitalisaties en overleving/prognose te verbeteren (IIa-B).
- Bij AF en AF-gerelateerde bradycardie of conversiepauzes kan katheterablatie overwogen worden om symptomen te verbeteren en om pacemaker implantatie te vermijden (IIa-C)

Het natuurlijke verloop van de aandoening en de therapeutische opties werden besproken. We opteren voor een pulmonale vene isolatie (PVI) om symptomen, nieuwe episodes en progressie van voorkamerfibrillatie tegen te gaan.  Het succespercentage met volledig verdwijnen van de klinische ritmestoornis is 80% na een eerste procedure. De mogelijke complicaties werden besproken namelijk vasculaire complicaties (<1%), pericardeffusie (<1%),  thrombo-embolie (<1%).
Indicaties voor redo catheterablatie
- Bij recidief na een eerste AF ablatie, vormt er zicht een indicatie voor redo catheterablatie (met behandeling van PV-LA reconnectie of additionele triggers) of anti-aritmische medicatie. Er is wel een voorkeur voor redo ablatie, gezien betere efficaciteit. Dit kan om symptomen te verbeteren, recidief te voorkomen of om progressie van AF te reduceren.(I)
- Recidief na eerste AF ablatie, zo symptomen beter waren na eerste ablatie. (IIa)
- Zo goede isolatie van de pulmonaalvenen kan best een isolatie van posterior wall en/of reductie van effective atrial surface area met RF of PFA.
""",
        ],
    },
    "Amiodarone (Cordarone)": {
        "description": "Rhythm control, dosering, bijwerkingen en monitoring voor Amiodarone (Cordarone)",
        "plan": [
            """
Amiodarone (Cordarone)
Rhythm control - Alternatief (kan gebruikt worden voor acute rate controle bij hartfalen, heeft weinig negatief inotroop effect en werkt beter dan digoxin).
- Cordarone (Amiodarone) 300mg IV over 15-30 minuten
- Nadien Cordarone (Amiodarone) 1200mg-3000mg  IV over 24 uur.

Bij switch naar orale dosis:
- Cordarone (Amiodarone) 200mg PO 3x/d gedurende 4 weken.
- Nadien, Cordarone (Amiodarone) 200mg PO 1x/d verder
- Cave: Tot 20% van patiënten ontwikkeld schildklierproblemen.

- Hypothyroidie, zo nodig behandelen met L-thyroxine. Zo geen onderliggende Hashimoto (Anti-TPO antistoffen testen) dan reversiebel na staken.
- Hypêrthyroidie is relatief zeldzaam, bij vermoeden best consult endocrinologie. dd. Graves exacerbatie door jodium, dan staken van amiodarone en start strumazol/PTU. dd. thyroiditis, dan staken amiodarone en behandelen met corticoiden. zo geen van beide dan start strumazol/PTU en corticoiden.
- Nausea, anorexie en constipatie.
- Levertoxiciteit (AST en ALT voornamelijk te volgen, ALP minimaal), reversiebel na staken.
- AST en ALT opvolgen zo <2x ULN is in orde.
- Neurologische toxiciteit: zwakte, tremor, myopathie, polyneuropathie en ataxie.
- Pulmonale toxiciteit treedt meestal het eerste jaar op (dyspnee, acute of subacute hoest en soms koorts) hoger risico met hogere dosis of langere behandeling - Longfunctie toont restrictie en verminderde DlCO. CT matglas en reticulaire abnormaliteit. Staken van Amiodarone en Corticoiden.
- Corneale microdeposits
- Fotosensitiviteit
- Occulaire neuropathie
- Risico op sinusbradycardie, AV block, QTc verlengen (zelden aritmogeen, OK zo QTcB <500ms).
- Halfwaarde tijd 55 (tot 142) dagen.
- Jaarlijks klinische controle met ECG en evaluatie oftalmologische, neurologische, pneumologische  en dermatologische bijwerkingen (bij hoesten of dyspnee: RX thorax F/P).
- Baseline bepaling van schildklier (TSH, T4), leverenzymen (Bilirubine, AST, ALT, ALP, GGT) en RX thorax F/P.
- Controle van schildklier (TSH, T4) en leverenzymen (Bilirubine, AST, ALT, ALP, GGT, significant zo >2x ULN) na 3 maanden bij opstart of dosis verhoging. Nadien elke 6 maanden of vroeger bij klachten.
""",
        ],
    },
    "Apocard Retard (Flecaïnide verlengde afgifte)": {
        "description": "Apocard Retard (Flecaïnide verlengde afgifte) - dosering, contra-indicaties, bijwerkingen en Ballet aanpak",
        "plan": [
            """
Apocard Retard (Flecaïnide verlengde afgifte)
Aanbevolen dosis Apocard (Flecaïnide verlengde afgifte) start 100-200mg PO 1x/d (Ideale dosis ESC guidelines is 200mg 1x/d verlengde afgifte) . Onderhoud 200-300 mg per dag. 
Acuut voor een cardioversie VKF: - Flecainide 2mg/kg IV over 15 mins - Niet bij structureel hartlijden, ischemie of hartfalen - Succes 59-78%  of Oral loading dose Flecainide 300mg PO.
Contra-indicatie bij Brugada syndroom,  Voorgeschiedenis myocardinfarct, ernstige LV dysfunctie, ernstig kleplijden, ernstige bradycardie, bundeltakblok of 2de graads AV blok. 
Best co-administratie met AV nodaal blockerende medicatie bij patiënten met VK flutter of VKF. 
Controle ECG 1 a 2 weken na opstart of verhogen van dosering. 
zo ΔQRS > 25% of abnormale fietsproef (nieuw BBB, delta QRS >25% of QRS >130ms) dan andere medicatie of dosis verlaging. 
Verhoogd risico bij QRS >120ms, eGFR < 30 ml/min/1.73m², elektrolietafwijkingen. 
Mogelijke bijwerkingen zijn duizeligheid en visusstoornissen door anesthetisch effect op natrium channel. Hoofdpijn, metalen smaak en gastro-intestinale symptomen zijn zeldzaam. 

Goede absorptie 90%. Piek serum na 1-3 uur (oraal, instant). Hepatische metabolisatie (CYP2D6, CYP1A2), halfwaardetijd 20u (12-27u), verlengd bij hartfalen, nierfalen of leverziekten. Verlengde afgifte: Piek serum na 26 uur en stabiele spiegel na 4-5 dagen. Betere compliante en verminderd risico op bijwerkingen en interactie met andere medicatie. 


Blockeren van open-state inward Na+ channel Nav 1.5 in rate en voltage dependent manier in His-purkinje weefsel en ventriculaire myocyten. Blockeren van delayed rectifier K+ current (Ikr) en Kito bij hogere dosissen. 
Verlengen van actie potentieel en refractaire periode in cardiomyocyten. 
Verkorten van actie potentiaal en refractaire periode van his-purkinje systeem. 

Ultimate approach Ballet: 
Dosering approach loading dose van 250mg (200mg zo gewicht <70 kg)
Controle ECG na 90-120 min met controle bloeddruk
Uitsluiten Brugada ECG patroon en AV block
Zo ΔQRS 20ms, dan 200mg verlengde afgifte 1x/d (of 100mg 2x/d)
Zo ΔQRS 20-40ms of QRS >120ms, dan 100mg verlengde afgifte 1x/d (of 50mg 2x/d)
Zo ΔQRS >40ms of QRS >130ms, of brugada patroon dan stop Flecainide. 
""",
        ],
    },
    "Propafenone (Rhytmonorm)": {
        "description": "Propafenone (Rhytmonorm) - dosering, contra-indicaties, bijwerkingen en monitoring",
        "plan": [
            """
Propafenone (Rhytmonorm)
- Rytmonorm (Propfenone) 150mg 3x/d. (Mag tot 300mg 3x/d)
- Niet bij ischemisch hartlijden, verminderde LV functie, ernstige nier of leverdysfunctie. 
- Best co-administratie met AV nodaal blockerende medicatie bij patiënten met VK flutter of VKF. e.g. Progor (Diltiazem) verlengde afgifte 180-360mg 1x/d.  Time to peak 10-14 uur. Halfwaarde tijd 6-9 uur. 
- Te stoppen bij QRS verberdering >25%, LBBB of QRS >120ms. 
- Opgespast bij sinoatriaal/atrioventriculaire conductie stoornissen. 
- Kan concentratie van warfarine/acenocoumarine en digoxine verhogen in combinatie. 
- Controle ECG na 1 a 2 weken. 
""",
        ],
    },
    "Vernakalant (Brinavess)": {
        "description": "Vernakalant (Brinavess) - farmacologische cardioversie dosing and contraindications",
        "plan": [
            """
Vernakalant (Brinavess)
- Farmacologische cardioversie met Vernakalant (Brinavess) 3mg/kg over 10 minuten, zo geen cardioversie in 15 minuten dan nieuwe dosis van 2mg/kg over 10 minuten. Bij cardioversie tijdens toediening nog steeds de volledige dosis toe te dienen.
- Staken van infusie bij abrupte daling van bloeddruk, bradycardie met sinuspauzes of nieuw AV-block/bundeltakblok.
- Contra-indicatie bij acuut coronair syndroom.
- Is eerste keus voor farmacologische conversie zeker zo recente onset van VKF <7 dagen.
""",
        ],
    },
    "Thoraxpijn op SEH (HEART-score)": {
        "description": "Risicostratificatie en beleid bij thoraxpijn volgens HEART-score",
        "plan": [
            "**HEART-score bepalen**:",
            "  - History (anamnese): 0–2 punten",
            "  - ECG: 0–2 punten",
            "  - Age: 0–2 punten",
            "  - Risk factors (DM, roken, hypertensie, hyperchol., fam. anamnese): 0–2 punten",
            "  - Troponin: 0–2 punten",
            "**HEART 0–3 (laag risico)**:",
            "  - Ontslag mogelijk, poliklinische follow-up, leefstijladviezen",
            "**HEART 4–6 (matig risico)**:",
            "  - Opname observatie, troponine herhalen na 3–6 uur",
            "  - Fietstest of CT-coronairs overweging",
            "**HEART 7–10 (hoog risico)**:",
            "  - Opname CCU, invasieve diagnostiek (coronair angiogram) overwegen",
            "  - DAPT + statine starten, cardioloog consulteren",
        ],
    },
    "Cardiovasculaire preventie": {
        "description": "Algemene adviezen en leefstijladviezen voor cardiovasculair risicomanagement (ESC 2023)",
        "plan": [
            "**Algemene adviezen (ESC 2023)**:",
            "- Arteriële hypertensie: richtwaarde systolische bloeddruk 120–129 mmHg",
            "- Dyslipidemie: LDL-cholesterol <55 mg/dL (of <40 mg/dL bij ≥2 CV-events); triglyceriden <150 mg/dL; streef ApoB <65 mg/dL",
            "- Diabetes: streef HbA1c <7% via leefstijl en medicatie met bewezen cardiovasculair voordeel",
            "",
            "**Leefstijl**:",
            "- Lichaamsgewicht: streef BMI <25 kg/m² via dieet, beweging en indien nodig verwijzing naar diëtist",
            "- Lichaamsbeweging: minimaal 150 minuten/ week aerobe activiteit plus krachttraining",
            "- Dieet: rijk aan groenten, fruit, volwaardige granen, onverzadigde vetten en magere eiwitten; beperk verzadigde vetten",
            "- Alcohol: beperk tot <100 gram/week",
            "- Nicotine: dringend adviseren tot onmiddellijke en volledige rookstop",
            "",
            "**Risicofactoroptimalisatie en medicamenteuze maatregelen**:",
            "- Behandel hypertensie volgens doelwaarden; start of optimaliseer antihypertensiva indien nodig",
            "- Start statine/LDL-verlagende therapie bij hoge risico-patiënten volgens lokale richtlijnen",
            "- Overweeg SGLT2-remmers en/of GLP-1 agonisten bij diabetes en/of hoog cardiovasculair risico wanneer geïndiceerd",
            "",
            "**Monitoring en follow-up**:",
            "- Controleer bloeddruk, lipidenprofiel en HbA1c periodiek (interval afhankelijk van stabiliteit)",
            "- Bij therapie-introductie of dosisaanpassing: controle na 4–12 weken",
            "- Gebruik gedeelde besluitvorming; verwijs naar preventie-/leefstijlprogramma's indien beschikbaar",
        ],
    },
    "Hypertensie work-up (primair)": {
        "description": "Uitgebreide evaluatie en behandeling bij nieuw ontdekte hypertensie",
        "plan": [
            "**Thuismeting**: gemiddelde 2×/dag gedurende 7 dagen (streef <135/85 mmHg)",
            "**Anamnese**: duur klachten, hoofdpijn, neus bloeden, familieanamnese",
            "**Secundaire hypertensie** screenen:",
            "  - Nierfunctie (creatinine, eGFR), urinesediment, albumine/creat-ratio",
            "  - TSH (hypo-/hyperthyreoidie)",
            "  - Renine/aldosteron-ratio (bij hypoK of therapieresistent)",
            "  - Slaapapneu-screening (Epworth, ronchopathie)",
            "**Orgaanschade**:",
            "  - ECG (LVH, oude infarcten)",
            "  - Echo hart (LV-massa, diastole)",
            "  - Fundoscopie (bij ernstige HT)",
            "**Cardiovasculair risicoprofiel**: lipiden, glucose, roken",
            "**Leefstijladviezen**: zoutbeperking, gewichtsverlies, beweging, alcoholmatiging",
            "**Medicatie** (bij persisteren >140/90):",
            "  - Eerste keus: ACE-remmer of calciumantagonist of thiazide",
            "  - Combinatietherapie bij onvoldoende effect",
            "**Follow-up**: 4–6 weken na start, daarna 3-maandelijks tot goed ingesteld",
        ],
    },
    "Post-MI secundaire preventie": {
        "description": "Beleid en medicatie na myocardinfarct ter preventie van recidief",
        "plan": [
            "**DAPT**: acetylsalicylzuur 80mg + P2Y12-remmer (ticagrelor 90mg 2×/d of prasugrel 10mg 1×/d) gedurende 12 maanden",
            "**Statine**: atorvastatine 80mg of rosuvastatine 40mg (LDL-doel <1,4 mmol/L, liefst <1,0)",
            "**Bètablokker**: bisoprolol, metoprolol, carvedilol (zeker bij LVEF <40%)",
            "**ACE-remmer** (bij LVEF <40% of hypertensie/DM): ramipril, perindopril",
            "**Eplerenon** overwegen bij LVEF <40% + tekenen HF of DM",
            "**Leefstijl**: stoppen met roken, cardiale revalidatie, mediterraan dieet",
            "**Bloeddruk**: streef <140/90 (indien DM/CKD: <130/80)",
            "**Glucose**: HbA1c <7% bij diabetici, SGLT2-remmer overwegen",
            "**Follow-up**:",
            "  - Polikliniek 6 weken (echo-controle, medicatie-check)",
            "  - Jaarlijkse controle met lipiden, nierfunctie, echo (bij LV-dysfunctie)",
        ],
    },
    "Syncope work-up": {
        "description": "Diagnostisch stappenplan bij syncope (bewustzijnsverlies)",
        "plan": [
            "**Anamnese**: prodromale symptomen, triggers (opstaan, mictie, hoesten), duur, herstel",
            "**Heteroanamnese**: convulsies, tongbeet, incontinentie (DD epilepsie)",
            "**Lichamelijk onderzoek**: orthostatische hypotensie (RR liggend/staand), cardiaal/neurologisch",
            "**ECG**: geleidingsstoornissen (AV-blok), aritmieën (QTc, Brugada, pre-excitatie)",
            "**Bloedonderzoek**: Hb, glucose, elektrolyten",
            "**Hoog-risico kenmerken** (opname indicatie):",
            "  - Inspanningsgebonden syncope",
            "  - Hartfalen/structureel hartlijden",
            "  - Familie-anamnese plotse dood <40 jaar",
            "  - ECG-afwijkingen (QTc >460ms, Brugada, ARVD)",
            "**Aanvullend** (afhankelijk van verdenking):",
            "  - Echocardiografie (structureel hartlijden)",
            "  - Holter / event recorder (aritmiedetectie)",
            "  - Tilt-table test (vasovagale syncope)",
            "  - EPO (elektrische stimulatie bij geleidingsstoornis)",
            "  - Neurologisch consult (indien verdenking epilepsie/CVA)",
            "**Behandeling**: oorzaakspecifiek (PM bij bradycardie, ICD bij maligne aritmie, vochtinname/compressiekousen bij orthostatisme)",
        ],
    },
    "AVNRT": {
        "description": "AV-nodale re-entry tachycardie — typische en atypische vormen en behandeling",
        "plan": [
            """
Typische AVNRT (HA <70ms, VA (His) <60ms, AH/HA >1
Atypische AVNRT (HA >70ms, VA (His) >60ms, AH/HA variabel)
Vagale maneuvers zijn aangewezen zo patiënt niet in hospitaal is of zo hemodynamisch stabiel (I-B).
Zo vagale maneuvers ineffectief dan IV adenosine (I-B).
Katheterablatie is aangewezen als herhaalde, symptomatische episodes van AVNRT (I-B).
Zo minimaal symptomatische, korte en spontaan overgaande episodes is therapie niet noodzakelijk (IIa-C).
""",
        ],
    },
    "Pre-excitatie": {
        "description": "Beleid bij pre-excitatie / WPW — risicostratificatie en ablatie-overwegingen",
        "plan": [
            """
Elektrofysiologisch onderzoek (incl. isoprenaline) voor risicostratificatie met catheterablatie zo hoog risico eigenschappen (SPERRI <250ms, AP ERP <250ms, multipele AP, inductie van AP-gemedieerde tachycardie).
Katheterablatie kan eigenlijk altijd overwogen worden, zelfs bij low-risk asymptomatische pre-excitatie in ervaren centra naargelang voorkeur van patiënt (IIb-C).
Shortest Pre-excited R-R interval van 250 ms is misschien een betrouwbaardere merker voor risico-inschatting.
""",
        ],
    },
    "Palpitaties workup dr. Ballet": {
        "description": "Standaard werkup voor palpitaties volgens dr. Ballet",
        "plan": [
            """
 Labo met complete celtelling, nierfunctie, leverenzymen, elektrolyten, fosfaat, calcium, Hs-cTn, CK,  TSH, T4, HbA1C, glucose en NT-proBNP. Bij vrouwen evt. B-HCG.
 12 lead electrocardiogram (I) (ideaal ook high precordial met V1-V2 in 2/3de intercostaal ruimte)
 Transthoracale echocardiografie (I)
 Inspanningselectrocardiogram 
 Zo nodig longziekte uitsluiten: Volledige longfunctie (Spirometrie met reversibiliteit,  flow-volume loop, longvolumes, diffusiecapaciteit en bodybox luchtwegweerstand) + FeNO bij vermoeden astma. 
 Holter monitoring 
 Zo zeer infrequente episodes eventueel langere holter of ILR. 
 Zo non-invasieve evaluatie inconclusief EP study. 
 Zo gedocumenteerde SVT of minimale pre-excitatie op ECG kan een adenosine proef nuttig zijn. 
 Zo brugada type 2 of 3 op ECG, familiale voorgeschiedenis van SCD of BrS kan een ajmaline proef nuttig zijn. 
""",
        ],
    },
    "Syncope Workup dr. Ballet": {
        "description": "Uitgebreide syncope-workup volgens dr. Ballet",
        "plan": [
            """
Syncope Workup Ballet
Anamnese en heteroanamnese
Klinisch onderzoek incl. bloeddruk liggend/staand
ECG (ook hoog rechts precordiaal, zeker zo familiale voorgeschiedenis zo Brugada type 2 of 3 kan ajmaline proef overwogen worden)
Zo type 2 of 3 brugada patroon of familiale voorgeschiedenis van plotse dood of van brugada syndroom vormt er zich een indicatie voor ajmaline test.
TTE
Fietsproef.
Carotis sinus massage bij patiënten ouder dan 40 jaar. (Carotid sinus syndrome-CSS is bevestigd zo bradycardia (asystole) and/or hypotension that reproduce spontaneous symptoms). Zo positief is er indicatie voor pacemaker.
Tilt testing zo vermoeden van reflex syncope, orthostatische hypotensie, POTS of PPS (Klasse IIa-B indicatie) Zo asystole tijdens tiltest is er indicatie voor DDD-PM. Zo tilt positief maatregelen tegen hypotensieve neiging.
24u bloeddruk meting bij frequente episodes suspect voor reflex syncope, persistente of intermittente hypotensie  <90-100 mmHg of lage gemiddelde bloeddruk <110 mmHg heeft een zeer hoge specificiteit voor vasodepressor reflex syncope (35% sens, 94% spec)
24 u bloeddruk meting bij vermoeden autonoom falen (om nachtelijke hypertensie te detecteren) of om orthostatische hypotensie op te sporten (Klasse I-B indicatie).

Holter monitoring zo frequente episodes >1 keer per week
Tilt test bij vermoeden van orthostatische of reflex syncope
Bloedname wanneer klinisch relevant (Hemoglobine, O² sat en ABG, Hs-cTn-T, D-dimeren, NT-proBNP, tryptase, plasma ACTH, ochtend cortisol )
Bij flushing een 5-HIAA urinaire test
RX thorax F/P of CT thorax wanneer klinisch relevant
MRI hart zo syncope met vermoedelijk cardiaal structurele origine, zo echocardiografie niet diagnostisch;
MRI hersenen zo parkinsonisme, ataxia of cognitief deficit. (I-C)
Screening voor paraneoplastische antistoffen en anti-ganglionische acetylcholine receptor antistoffen zo acuut multi domein autonoom falen. (I-B)
Een verwijzing naar neuroloog zo syncope door autonoom falen (IC)
Een verwijzing naar neuroloog zo vermoeden epilepsie (IC)
Bij enige vorm van structureel hartlijden best elektrofysiologisch onderzoek overwegen.
Bij status na AVR is er universeel scarring aanwezig peri-aortaal, tot 34% van VT’s zijn daarom peri-aortaal. Bundel branch re-entry kan hierbij een VT mechanisme zijn (in 7%) door schade aan His-Purkinje systeem na TAVI.  Bij patiënten met syncope of VT kort na valvulaire heelkunde moet een overweging gemaakt worden voor elektrofysiologische studie ter identificatie en ablatie van BBR-VT (I-C) zeker als dit kort (1 maand) na een TAVR/SAVR plaatsvindt.
Holter met 5-lead configuratie  (LA(L), RA(R), LL (LF), RL (N), precordiaal) met afleiding  I, II,  III en V1 kan nuttig zijn om morfologie en origine van ventriculaire extrasystolen te achterhalen.
Holter met 3-lead configuritatie (I, II, III) is de standaard holter

Bloeddruk liggend - staand:
- Bloeddruk meten in lig na 5 minuten liggen.
- Bloeddruk meting na 2 minuten rustig staan,  (significant zo daling systolisch >20 mmhg of diastolisch >10mmhg)
- Bloeddruk meting na 5 minuten rustig staan,  (significant zo daling systolisch >20 mmhg of diastolisch >10mmhg)

Elektrofysiologisch onderzoek
Bij syncope en myocard infarct of andere scar-related condition zonder etiologie na non-invasieve onderzoeken (I-B), zo inductie van sustained VT is er een indicatie voor ICD.
Bij syncope en bifasciculair blok zonder etiologie na non-invasieve onderzoeken (IIa), zo verlengde HV interval of 2de of 3de graads His-Purkinje block tijdens incrementele pacing is er indicatie voor permanente pacemaker (IB)
Bij syncope voorafgegaan door palpitaties  zonder etiologie na non-invasieve onderzoeken (IIb)
Bij syncope en asymptomatische sinusbradycardie waarbij  non-invasieve onderzoeken geen correlatie kunnen aantonen tussen bradycardie en symptomen. Zo een verlengde gecorrigeerde cSNRT >500-550ms moet pacemaker therapie overwogen worden. (IIb)
De waarde van het elektrofysiologisch onderzoek is laag, zo normaal ECG, geen structureel hartlijden en geen palpitaties.
Bij bifasciculair blok is het risico op AVB ongeveer 1% per jaar, zo syncope is het risico >10%.  Zo normale of licht verlengde HV is de oorzaak vak nog steeds door een brady-aritmie zoals paroxysmaal AVB dat opgespoord kan worden met ILR.

Implantable loop recorder
ILR is geïndiceerd zo meer dan 1 syncope van onbekende origine, in afwezigheid van high risk criteria en hoge kans op nieuwe episode gedurende levenstijd van device (I-A)
ILR is geïndiceerd  zo syncope met high risk criteria zonder duidelijke etiologie na uitgebreide evaluatie, zonder indicatie voor ICD of pacemaker (I-A)
ILR kan overwogen worden bij vermoeden reflex syncope maar met frequente en ernstige syncopale episodes (IIa-B)
ILR mag overwogen worden bij epilepsie waarbij behandeling niet effectief is (IIb-B)
ILR mag overwogen worden bij onverklaard vallen (IIb-B)
 Bij voorgeschiedenis van thrombo-embolisch event, kan een ILR overwogen worden (IIa-B)

RIZIV terugbetaling ILR: De verstrekking 172572-172583 kan enkel in aanmerking komen voor een tegemoetkoming van de verplichte verzekering indien de rechthebbende aan de volgende criteria voldoet:

- De rechthebbende vertoont recidiverende syncopes van onbekende oorsprong ondanks een exhaustief niet-invasief bilan, en er bestaat een risico op recidieve tijdens de theoretische levensduur van het hulpmiddel.
of
- De rechthebbende vertoont syncope, zelfs geïsoleerd, in aanwezigheid van mogelijke verzwarende factoren zoals vermeld in de internationale richtlijnen en na exhaustief niet-invasief en eventueel invasief bilan.
of
- De rechthebbende vertoont tekenen van cryptogeen CVA/TIA wanneer een volledige diagnostiek, met daarin begrepen minstens een continue registratie van de elektrische cardiale activiteit gedurende een week, de oorzaak van het CVA/TIA niet heeft kunnen achterhalen en waarbij het aantonen van atriale fibrillatie het instellen van orale anticoagulatie tot gevolg zou hebben.

Vasodepressor syncope 
Vermijden van gekende triggers 
Voldoende hydrateren zeker bij inspanning, ziekte of werken in warme omgeving. Drinken van 500ml water na het ontwaken met een dagelijks streefdoel van 1.5 liter tot 3 liter water. Dit mag ook een elektrolyten bevattende drank zijn. 
Voldoende zoutinname. Streefdosis van 6 tot 10 gram zout per dag (tenzij contra-indicatie) 
Benen kruisen en  gelijktijdig aanspannen van been-, buik- en bilspieren (zeer effectief).
Krachtig in de handen knijpen en armen uit mekaar trekken. 
Compressie kousen 
Plat gaan liggen zo prodromale klachten
Medicamenteuze therapie kan overwogen zo niet voldoende effect e.g. Fludrocortisone zo orthostatische vorm van reflex syncope, met laag normale waardes van bloeddruk in rust. 
Magistraal voorschrift Fludrocortisonacetaat - gelules met 0,1 mg. Initiele dosis is gewoonlijk 0.5-0.1mg met target 0.2mg 1x/d.  
""",
        ],
    },
    "ILR RIZIV Criteria": {
        "description": "RIZIV terugbetaling criteria voor Implantable Loop Recorder (ILR)",
        "plan": [
            """
De rechthebbende vertoont recidiverende syncopes van onbekende oorsprong ondanks een exhaustief niet-invasief bilan, en er bestaat een risico op recidive tijdens de theoretische levensduur van het hulpmiddel.
of
De rechthebbende vertoont syncope, zelfs geïsoleerd, in aanwezigheid van mogelijke verzwarende factoren zoals vermeld in de internationale richtlijnen en na exhaustief niet-invasief en eventueel invasief bilan.
of
De rechthebbende vertoont tekenen van cryptogeen CVA/TIA wanneer een volledige diagnostiek, met daarin begrepen minstens een continue registratie van de elektrische cardiale activiteit gedurende een week, de oorzaak van het CVA/TIA niet heeft kunnen achterhalen en waarbij het aantonen van atriale fibrillatie het instellen van orale anticoagulatie tot gevolg zou hebben.

Een ILR kan slechts eenmaal tijdens de levensduur van de rechthebbende worden vergoed.
""",
        ],
    },
    "Perioperatieve management CIED": {
        "description": "Aanpak van pacemaker/ICD rond chirurgische ingrepen",
        "plan": [
            """
Zo chirurgie >15cm verwijderd van pacemaker en pacemaker bereikbaar voor magneet applicatie tijdens procedure bij patiënt die niet afhankelijk is van pacing dan kan procedure doorgaan zonder herprogrammatie met applicatie van magneet zo nodig (e.g. asystolie of hemodynamisch relevante bradycardie tijdens elektrocauterisatie).
Zo pacemaker afhankelijk (geen escape ritme of hartslag <50/min met symptomen) dan magneet applicatie tijdens hele procedure.  Magneet geeft asynchrone pacing (DOO/VOO/AOO) bij de pacemaker.
Zo chirurgie >15cm verwijderd van ICD en ICD bereikbaar voor magneet applicatie tijdens procedure kan procedure doorgaan zonder herprogrammatie zo patiënt niet afhankelijk van pacing (geen escape ritme of hartslag <50/min met symptomen) met magneetapplicatie tijdens gehele procedure. Magneet applicatie bij ICD pauzeert detectie en/of therapie van tachyaritmie zonder invloed op pacing.
Zo chirurgie <15cm van ICD, of ICD niet bereikbaar voor magneet of afhankelijkheid van pacing dan herprogrammatie van ICD naar asynchrone pacing e.g. DOO met deactivatie van tachytherapie.

Voorkeur voor bipolaire elektrocauterisatie (eerder dan unipolaire) en plaatsen van pad zo ver mogelijk van device (e.g. contra-laterale dij).  Korte bursts van cauterisatie. Bij procedures onder de navel of met bipolaire elektrocauterisatie is risico op elektromagnetische interferentie zeer laag.

Pacemaker uitlezing is noodzakelijk, zo procedure met risico op elektromagnetische interferentie of device beschadiging of bij vermoeden van device dysfunctie tijdens procedure.
""",
        ],
    },
    "Device indicaties": {
        "description": "Indicaties en overwegingen voor pacemaker, ICD, CRT en tijdelijke pacing",
        "plan": [
            """
Bradycardie indicatie
Etiologische oppuntstelling (TSH, T4, lyme titer, digitalis spiegel, calcium, kalium, pH) (Klasse IA)
Bij nachtelijke bradycardie of AV block best ook slaapstudie (klasse IC)
Bij infrequent syncope (e.g. < 1 x per maand) implantatie van ILR (IA)
Bij vroege onset (<50 jaar) of familiale voorgeschiedenis, dan genetische test.
Bij infiltratie cardiomyopathie of scar, imaging met MRI, CT of PET
Bij syncope met bifasciculair block EFO of fietsproef of empirische implantatie bij fraile oude patiënten.
Bij vermoeden vasodepressor syncope - CSM/tilt test
Bij inspanningsgebonden klachten - fietsproef
Progressieve cardiale conductie ziekte (PCCD) is gediagnostisceerd zo onverklaard progressief conductie abnormaliteiten in jonge patiënt (<50 jaar) met structureel normaal hart in afwezigheid van skeletale myopathie, zeker zo familiale voorgeschiedenis.

Sinusknoopdysfunctie
Zo symptomen ten gevolge van sinusknoop dysfunctie (I-A)
Zo noodzakelijk in de context van brady-tachy syndroom voor farmacologische behandeling van tachycardie, tenzij ablatie mogelijk is (IB)
Niet zo transiënte oorzaak of asymptomatisch (IIIC)

Atrioventriculaire conductiedysfunctie
Bij sinusaal ritme met permanent of paroxysmaal 3de graads, 2de graads type 2, infranodaal 2:1 of hooggradig AV block ongeacht symptomen (IC)
Bij atriale tachycardie/VKF en permanent of paroxysmale derde graads of hooggradig AV block ongeacht symptomen (IC)
Bij onverklaarde syncope met bifasculair block, op voorwaarde dat HV interval >70ms is of 2de of 3de graads intra- of infra-his block tijdens incrementele atriale pacing, of abnormale respons bij farmacologische proef. (IB)
Bij alternating bundeltakblock ongeacht symptomen (IC)
Zo AVB nog aanwezig meer dan 5 dagen na infarct of cardiale chirurgie.(IC)
Volledig of hooggradig AVB langer dan 24-48u na TAVI (IB)
Alternating BTB na TAVI (IC)
Bij voorkeur steeds conduction system pacing (CSP) - LBBAP.

Reflex syncope
Spontane gedocumenteerde symptomatische asystole pauze > 3 seconden of assymptomatische pauze > 6 seconden door sinusarrest of AV block. (IA)
Cardio-inhibitoire carotid sinus syndrome (IA)
Asystole syncope tijdens tilt testing (IA)
Niet zo geen cardio-inhibitoire component, zo geen gedocumenteerde bradycardie of bewijs conductiestoornis (IIIC)

CRT
Bij patiënten in sinus ritme met LVEF <  35% met QRSd > 150ms, LBBB morfologie ondanks optimale medicamenteuze therapie (IA)
Bij noodzaak aan pacing wegens AV block bij LVEF <40% ongeacht NYHA klasse.

Tijdelijke pacing
Indicatie zo hemodynamisch onstabielie bradycardie refractair aan medicamenteuze therapie met chronotropische medicatie (IC)
Bij reversiebele etiologie van hemodynamisch onstabiele bradycardie (I)

Antibacteriële envelope (RIZIV criteria)
Gedocumenteerde infectie van ICD of PM
Immun gecompromiteerd (actieve chemotherapie, methylprednisolone >16mg/d gedurende langer dan 2 weken, immunosurpressieve therapie na orgaantransplantatie)
PADIT score >= 7
PADIT score >=6 en heparine bridging, COPD gold 3 of 4, hemodialyse.
""",
        ],
    },
    "Idiopathische VES": {
        "description": "Beleid bij idiopathische ventriculaire extrasystolen (VES/PVC) en VT van vermoedelijk idiopathische oorsprong",
        "plan": [
            """
Idiopathische VES / PVC-beleid
- Echocardiografie met evaluatie van LV-functie is vereist bij PVC's/VES.
- Regelmatige controle van LV-functie is vereist bij patiënten met een PVC-burden > 10% (I-C).
- Cardiale MRI overwegen bij VES/VT die niet typisch idiopathische kenmerken hebben (IIa-C). Atypische kenmerken: oudere leeftijd, RBBB-morfologie, VT consistent met re-entry.

Therapie en ablatie:
- Bij symptomatische RVOT- of fasciculaire VES/VT is er een klasse I indicatie voor catheterablatie; ablatie verdient de voorkeur boven chronische medicatie (I).
- Bij symptomatische VES met andere morfologie dan RVOT of fasciculair: voorkeur voor bètablokker of calciumantagonist (I), met ablatie als tweede lijn (IIa) of flecaïnide als optie (IIa) afhankelijk van kliniek en contra-indicaties.
- Bij vermoeden van PVC-geïnduceerde cardiomyopathie is cardiale MRI te overwegen (IIa).
- Bij LV-dysfunctie ten gevolge van premature ventricular complex-induced cardiomyopathy is ablatie altijd klasse I indicatie; medicatie (bètablokker of bij matige LV-dysfunctie eventueel flecaïnide) kan overwogen worden (IIa). Geen CCB of amiodaron bij deze indicatie (III).

Andere overwegingen:
- Ablatie van VES overwegen bij suboptimale CRT veroorzaakt door een monomorfe VES met hoge burden (IIa).
- Bij frequente monomorfe VES die mogelijk bijdragen aan cardiomyopathie bij patiënten met structureel hartlijden, moet ablatie overwogen worden (IIa).
- Als PVC-correctie correleert met hartslag of neemt toe bij inspanning is voorkeur voor adrenerg werkende bètablokker; bij geen duidelijke correlatie kan klasse Ic (flecaïnide) effectiever zijn.
- Bij fasciculaire VES/VT is er eerder voorkeur voor calciumantagonisten vanwege effectiviteit bij fasciculaire tachycardieën.
""",
        ],
    },
    "ICD RIZIV Criteria": {
        "description": "RIZIV terugbetalingscriteria en indicaties voor implantatie van een hartdefibrillator (ICD)",
        "plan": [
            """
ICD RIZIV Criteria
1. Hartstilstand (datum te vermelden op de klinische samenvatting alsook of er sprake is
van “out of hospital”) ten gevolge van ventrikelfibrillatie of –tachycardie, niet te wijten
aan een acuut myocardinfarct noch aan een voorbijgaande of reversibele oorzaak
(elektrolietenstoornis, geneesmiddelen, trauma).

2. Plotse syncope, die na uitsluiting van andere oorzaken vermoedelijk van aritmogene
oorsprong is (datum te vermelden op de klinische samenvatting) zonder
gedocumenteerde tachyaritmie: bij een patiënt met gecorrigeerd congenitaal
ventriculair hartlijden en induceerbare sustained ventriculaire aritmie tijdens
elektrofysiologisch onderzoek. Deze indicatie wordt enkel vergoed in een centrum dat erkend is voor het zorgprogramma cardiale pathologie C.

3. Spontaan opgetreden sustained ventrikeltachycardie (> 30 seconden en > 100/min
of, indien korter, met noodzaak tot cardioversie) met syncope of presyncope omwille
van hemodynamische weerslag (datum te vermelden op de klinische samenvatting):
- 3.1. met onderliggend structureel hartlijden
- 3.2. zonder onderliggend structureel hartlijden, maar niet geschikt voor andere
therapie (expliciet de reden vermelden waarom medicatie of ablatie niet
mogelijk is).

4. Plotse syncope die na uitsluiting van andere oorzaken vermoedelijk van aritmogene
oorsprong is (datum te vermelden op de klinische samenvatting) zonder
gedocumenteerde tachyaritmie :
- 4.1. bij een patiënt met ischemische cardiomyopathie (na een vroeger
doorgemaakt myocardinfarct), zonder revasculariseerbare ischemie, maar
syncope niet te wijten aan hartinfarct, noch aan revasculariseerbare ischemie, en
meer dan 72 u na hartinfarct, LVEF ≤ 50%, en induceerbare sustained
monomorfe ventriculaire tachycardie tijdens elektrofysiologisch onderzoek;
- 4.2. bij een patiënt met niet-ischemische gedilateerde cardiomyopathie en
ejectiefractie < 35% die een syncope vertoont (datum te vermelden op de
klinische samenvatting) zonder gedocumenteerde ventriculaire tachyaritmie.
Ventriculaire tachyaritmie wordt als waarschijnlijke etiologie weerhouden. De
motivatie vereist:
 - nauwkeurige beschrijving van de omstandigheden van de syncope,
 - nauwkeurige beschrijving van het structureel hartlijden,
 - gedetailleerde argumentatie voor de aanwezigheid van een maligne
ventriculaire aritmie als oorzaak van de syncope en tegen een nietaritmische oorzaak;
- 4.3. bij een patiënt gekend met lang QT-syndroom onder een adequate behandeling
met betablokkers;
- 4.4. bij een patiënt met een spontaan (niet door klasse 1 antiaritmica geïnduceerd)
type 1 Brugada ECG patroon;
- 4.5. bij een patiënt met een catecholaminerg getriggerd polymorf VT syndroom
(CPVT) onder behandeling met betablokkers;
- 4.6. bij een patiënt met familiale hypertrofische cardiomyopathie waarbij het risico op
plotse dood, berekend met de risico-calculator van de Europese vereniging van
cardiologie (2014 ESC Guidelines on Diagnosis and Management of
Hypertrophic Cardiomyopathy, O’Mahony C et al Eur Heart J (2014) 35 (30):
2010-2020), groter of gelijk is aan 6% op 5 jaar;
- 4.7. bij een patiënt gekend met een zekerheidsdiagnose van aritmogene rechter
ventrikeldysplasie onder behandeling met betablokkers, sotalol of amiodarone.

1.b. indicaties (verder genoemd “electieve” indicaties) waarvoor :
- minder evidentie bestaat
- of waarvoor een minder goede kosten-baten verhouding bestaat
- of die klinisch minder urgent zijn.
 Het zijn “preventieve” indicaties bij rechthebbenden die geen belangrijke comorbiditeit
hebben en die afgezien van hun cardiale ritmeproblemen een levensverwachting hebben
van minstens vier jaar.
Ongeacht de bepalingen opgenomen onder artikel 2, 2. kan er voor de indicaties
opgenomen onder artikel 2, 1b gedurende de periode van 4 jaar na de implantatie van een
CRT-P, geen CRT-D terugbetaald worden noch aan de patiënt gefactureerd worden,
behalve in het geval van niet-ischemische cardiomyopathie met weinig comorbiditeiten.

5. Familiale of genetische aandoeningen met een gekend geassocieerd risico op
ventriculaire aritmieën, en met een omstandig gemotiveerd hoog risico op plotse dood
op basis van de internationale richtlijnen:
- 5.1. lang QT syndroom;
- 5.2. Brugada syndroom;
- 5.3. hypertrofische cardiomyopathie;
- 5.4. aritmogene rechter ventrikeldysplasie;
- 5.5. andere familiale (vermoedelijke genetische) oorzaken met een verhoogd risico
op ventriculaire aritmie.
- 6. Bewezen cardiale sarcoïdose met induceerbare sustained ventriculaire aritmieën.
- 7. Primaire preventie bij cardiomyopathie

7.1. Ischemische cardiomyopathie (na een vroeger doorgemaakt myocardinfarct), zonder
revasculariseerbare ischemie, ten vroegste 40 dagen na het acuut infarct of 3 maanden na
succesvolle revascularisatie (CABG of PCI) of 3 maanden na optimale therapie voor hartfalen,
en:
- met een LV ejectiefractie ≤ 30% en NYHA-klasse I
- of met een LV ejectiefractie ≤ 35% en NYHA-klasse II of III.

7.2. Ischemische cardiomyopathie (na een vroeger doorgemaakt myocardinfarct),
zonder revasculariseerbare ischemie, ten vroegste 40 dagen na het acuut infarct
of 3 maanden na succesvolle revascularisatie (CABG of PCI) of 3 maanden na
optimale therapie voor hartfalen, met een LV ejectiefractie ≤ 40%, met spontane
non-sustained ventrikeltachycardie en induceerbare sustained ventriculaire
aritmie tijdens elektrofysiologisch onderzoek.

7.3. Niet-ischemische gedilateerde cardiomyopathie met een LV ejectiefractie ≤
35%, NYHA klasse II of III ondanks optimale therapie voor hartfalen sinds meer
dan 3 maanden.
In het medisch dossier van de patiënt moeten alle elementen bewaard worden die de
indicatie voor de implantatie van een hartdefibrillator verantwoorden.

2. Criteria voor de patiënt om in aanmerking te komen voor de terugbetaling van een
resynchronisatietherapie:
- 2.1.a. NYHA klasse II of III niettegenstaande optimale medicamenteuze
behandeling gedurende ≥ 3 maanden na diagnose van cardiomyopathie
 EN
- QRS-complex ≥ 130ms (onafhankelijk van het soort bundle branch block,
 dus zowel bij left, right of aspecific bundle branch block)
OF
- ventriculaire pacing (met verwachte pacingnood > 40%)
- 2.1.b. een kandidaat zijn voor ablatie van de bundel van His (AVjunctie) omwille van
ongecontroleerde atriale ritmestoornissen ongeacht de NYHA klasse en EF.

3. De volgende specifieke criteria zijn van kracht:
- 3.1. Een expliciete motivatie, te vermelden op de klinische samenvatting, is vereist zo een
ander toestel dan een VVI-ICD wordt ingeplant, gebaseerd op de patiënt
karakteristieken en evidentie van klinische studies.
- 3.2. Indien de verstrekker motiveert dat de revascularisatie niet succesvol is/was, dient dit
aangetoond te worden door het operatie- of interventieprotocol of door bijkomende
functionele testen.
- 3.3. De volgende gegevens dienen geregistreerd te worden in de online-toepassing::
- Indien van toepassing wat is de linkerkamerejectiefractie? – De meting ervan moet
gebaseerd te zijn op echocardiografie en/of angiografie en/of isotopenscintigrafie
en/of cardiale MRI.
- leed de rechthebbende aan atriale fibrillatie in het jaar voorafgaande aan de
implantatie? Zo ja, dan moet het type voorkamerfibrillatie opgegeven worden:
paroxysmale, persisterende dan wel permanente voorkamerfibrillatie?
- vertoont de rechthebbende een indicatie voor pacing op atriaal niveau, op
ventriculair niveau of op beide niveaus?
- in welke NYHA klasse hartfalen (ondanks optimale medicamenteuze therapie)
bevindt de rechthebbende zich?
- welke is de QRS-duur op ECG? QRS ≤ 129ms, tussen 130ms en 149ms of ≥
150ms?
- vertoont de rechthebbende een totale LBBB (left bundle branch block) spontaan of
pacing geïnduceerd (verwachte pacingnood > 40%)?
- had de rechthebbende een pacemaker? Indien ja, het type en de datum van de
implantatie van de pacemaker vermelden;
- had de rechthebbende een LVAD? Indien ja, het type en de datum van de plaatsing
van de LVAD vermelden;
- lijdt de rechthebbende aan één van de volgende comorbiditeiten:
- Diabetes
- COPD
- Vroeger CVA / TIA / andere neurologische aandoening
- Oncologische aandoening: te specificeren
- Nierfalen: zo ja, welke is de Glomerular Filtration Rate (in ml/min), ureum,
creatinine (mg/100ml)

3.4. De parameters (NYHA, LVEF, …) dienen, indien mogelijk, geactualiseerd te worden
in de online-toepassing in het geval van vervangingen.
4. De contra-indicaties voor het inplanten van een hartdefibrillator zijn:
(Rechthebbenden met een van deze contra-indicaties komen derhalve niet in aanmerking
voor een tegemoetkoming van de verplichte verzekering voor geneeskundige verzorging
op basis van onderhavige overeenkomst.)
4.1. Aanhoudende of zeer frequent recidiverende ventrikeltachycardie of –fibrillatie die een
rationeel gebruik van een defibrillator onmogelijk maken;
4.2. Ventriculaire aritmieën behandelbaar door radiofrequente katheterablatie, zoals snel
voortgeleide voorkamerfibrillatie in het kader van een Wolff-Parkinson-White
syndroom, rechterventrikel uitstroombaar VT, idiopatische linkerventrikel VT,
bundeltak re-entry VT, ...;
4.3. Significante psychiatrische aandoeningen die kunnen verergeren door het inplanten
van een toestel of die een systematische follow-up in de weg zouden kunnen staan;
4.4. Voor de “urgente” indicaties (artikel 2.1.a) : terminale rechthebbenden met een
levensverwachting van minder dan 1 jaar of die zich bevinden in NYHA klasse IV
hartfalen; voor de electieve indicaties (artikel 2.1.b) : rechthebbenden met een
levensverwachting van minder dan 4 jaar omwille van de comorbiditeiten.
4.5. Enkel voor de indicaties onder artikel 2.1.b bestaat de bijkomende contra-indicatie:
 aantasting van de nierfunctie met GFR < 15 ml/min of patiënt in dialyse. Deze
contra-indicatie vervalt als de patiënt geactiveerd is op de transplantatielijst.

Erfelijke cardiomyopathie met LVEF <50%:
- PLN mutatie: ICD indicatie volgens risicomodel (p.Arg14del risk calculator, afkapwaarde
>5% 5-jaars risico op SCD)
- LMNA mutatie: ICD indicatie conform risicomodel (LMNA-risk VTA calculator, afkapwaarde
>5% 5-jaars risico op SCD)
- FLNC mutatie: ICD indicatie indien LVEF <45%, NSVT op holter
- RBM20 en DSP mutatie

""",
        ],
    },
    "Ventriculaire tachycardie en plotse dood": {
        "description": "Beleid bij ventriculaire aritmieën, genetica en risicobeoordeling voor plotse dood",
        "plan": [
            """
Ventriculaire tachycardie en plotse dood
- Genetische analyse is aangewezen bij een nieuwe diagnose of aandoening vastgesteld bij een levende of overleden persoon met vermoedelijke genetische basis en hoog risico op ventriculaire aritmie of plotse dood (I-B).

Diagnostiek bij nieuw vastgestelde ventriculaire aritmieën (bijv. frequente PVCs, NSVT, sustained monomorphic VT):
- 12-lead ECG en transthoracale echocardiografie zijn verplicht bij nieuwe ventriculaire aritmieën (I-C).
- Cardiale MRI moet overwogen worden voor evaluatie van structureel hartlijden en arrhythmogene substrate (IIa-B).
- Holtermonitoring van ten minste 24 uur wordt aanbevolen voor ritmedocumentatie en burden-assessment (IIa).
- Indien vermoeden op ischemische etiologie: sluit coronaire hartziekte uit volgens lokale pathways.

Therapeutische en invasieve overwegingen:
- Bij de eerste episode van sustained monomorphic VT kan een elektrofysiologisch onderzoek met elektroanatomische mapping en, indien geïndiceerd, mapping-geguide biopsie overwogen worden voor etiologische opheldering en gerichte therapie (IIb-C).

Documentatie en verslaglegging:
- Noteer data van relevante gebeurtenissen (bijv. datum SMVT, datum hartstilstand) en de context (out-of-hospital vs in-hospital) in de klinische samenvatting.
- Bewaar alle beeldvorming, ECG's en holtermetingen in het dossier ter ondersteuning van vervolgbeslissingen (ablatie, ICD-implantatie, genetica).
""",
        ],
    },
    "Brugada syndroom (BrS)": {
        "description": "Diagnose, genetica, provocatieprotocol en behandeling van Brugada syndroom",
        "plan": [
            """
Brugada syndroom (BrS)
Diagnose:
- Type-1 Brugada ECG-patroon: coved/ST-elevatie met T-golfinversie in ten minste één rechter precordiale afleiding (V1 of V2) gepositioneerd in 2e–4e intercostale ruimte, spontaan of na farmacologische provocatie.

Genetica:
- Genetische testing voor het SCN5A-gen is aangewezen bij probands met klinische verdenking op BrS (I-C).
- Autosomaal dominante overerving; SCN5A verklaart ~20–30% van klinische gevallen. Afwezigheid van één causatief gen sluit diagnose niet uit.
- Genetische testen zijn ook geïndiceerd bij familieleden van een succesvol getest proband.

Diagnostische overwegingen en score:
- Shanghai-score kan ondersteuning bieden (≥3.5 definite/probable; 2–3 possible; <2 nondiagnostic).

Indicaties voor testing / klinische triggers:
- Cardiale arrest of verdachte syncope
- Familiale voorgeschiedenis van BrS of plotse onverklaarde dood
- Type 2/3 Brugada patroon met aanvullende ECG-afwijkingen of symptomen

Ajmaline (sodium-channel blocker) protocol:
- Contra-indicaties: zwangerschap, 2e/3e graads AV-blok, hypertrofe cardiomyopathie, hartfalen.
- Patiënt nuchter; externe defibrillator aanwezig; atropine en isoprenaline standby.
- Dosis: ajmaline 1 mg/kg IV, max 100 mg, in stapjes (bolus/infusie) met ECG-monitoring elke minuut; registreer V1/V2 hoog geplaatst.
- Stopcriteria: optreden van coved-type type-1 ST-elevatie (>2 mm), polymorfe VES/VT, sinusarrest, 2°/3° AV-blok, QRS-verlenging >30% of significante hypotensie.

Behandeling en follow-up:
- Vermijd geneesmiddelen die ST-elevatie in rechter precordialen kunnen verergeren (brugadadrugs.org); vermijd excessief alcohol; behandel koorts snel.
- Jaarlijkse cardiologische controle; instructies aan patiënt om onmiddellijk presyncope/syncope te melden.
- Familieonderzoek: ECG incl. hoge precordialen; overweeg SCB-provocatie en genetische testing.
- ICD-implantatie is geïndiceerd bij SCA-survivors of gedocumenteerde sustained VT; kan nuttig zijn bij BrS met syncope vermoedelijk van cardiogene oorsprong; niet geïndiceerd in asymptomatische patiënten louter op basis van familieanamnese.
- Ablatie kan overwogen worden bij electrical storm of herhaalde geschikte ICD-shocks; epicardiale ablatie van RVOT-substraat kan ECG- en aritmieverbetering geven.

Aanvullend onderzoek:
- Cardiale MRI kan overwogen worden bij complexe gevallen om RVOT-structuur te beoordelen.
- EFO met ventriculaire stimulatie kan behulpzaam zijn in risicostratificatie.
- Holter (inclusief hoge precordiale leads) kan nuttig om temporele/spatiale variatie van ST-elevatie en associatie met aritmieën te documenteren.
""",
        ],
    },
    "CPVT (Catecholaminerge polymorfe VT)": {
        "description": "Diagnose, testprotocol en behandeling van catecholaminerge polymorfe ventriculaire tachycardie (CPVT)",
        "plan": [
            """
CPVT (Catecholaminerge polymorfe VT)
Diagnose:
- CPVT wordt vermoed bij een structureel normaal hart met normaal rust-ECG en inspannings- of catecholamine-geïnduceerde bidirectionele of polymorfe VES/VT, typisch bij patiënten <40 jaar. Bij normale coronarografie kan diagnose ook bij >40 jaar gesteld worden.
- Diagnostische bevestiging kan ook door het aantonen van een pathogene mutatie (bv. RyR2, CASQ2) of bij familieleden van een index-patiënt met bidirectionele/polymorfe VES/VT.
- Meest frequente vormen: CPVT1 (AD, RyR2) en CPVT2 (AR, CASQ2); genetische verklaring in ~60% van gevallen.

Testing / provocatie:
- Adrenaline/epinephrine-test kan overwogen worden voor diagnose van CPVT indien een inspanningstest niet uitvoerbaar is. Kan ook nuttig zijn bij vermoeden van ARVC, LQTS en andere adrenerge gevoelige aandoeningen.
- UZA-protocol: epinefrine-infusie via perifeer infuus, start 0.05 mcg/kg/min, verhogen naar 0.10, 0.20, 0.30, 0.40 in 5-min intervallen; 12-lead ECG baseline en voor elke dosis; stopcriteria: SBP <80 of >200 mmHg, nonsustained VT, polymorfe VT, >10 PVC/min, nieuwe T-wave alternans of intolerantie.
- Mayo-protocol (progressief): start 0.025 mcg/kg/min 10 min, verhoog naar 0.05, 0.10, 0.20 mcg/kg/min in 5-min stappen; stop criteria vergelijkbaar.
- Bij significante vervolgklachten na infusie: korte IV bètablokker (bijv. metoprolol) per protocol; na 30 min washout kan sodium-channel blocker test (procainamide) overwogen worden.

Behandeling en follow-up:
- Sportbeperkingen: vermijd intensieve/competitieve inspanning en stressvolle situaties.
- Bètablokkers zijn geïndiceerd bij alle symptomatische CPVT-patiënten; voorkeur voor niet-selectieve waar aangewezen.
- ICD: bij patiënten met hartstilstand, recidiverende syncope of polymorfe/bidirectionele VT ondanks optimale medicatie — ICD nooit als monotherapie, altijd in combinatie met bètablokker.
- Flecaïnide kan als add-on nuttig zijn bij doorbraakaritmieën ondanks bètablokkers.
- Left cardiac sympathetic denervation (LCSD) kan overwogen worden bij persistente polymorfe/bidirectionele VT ondanks bètablokkers of bij intolerantie voor bètablokkers.

Genetica en familieonderzoek:
- Overweeg genetische testing (RyR2, CASQ2, etc.) bij proband en cascade-screening in de familie bij positieve bevindingen.
""",
        ],
    },
    "LQTS (Long QT syndroom)": {
        "description": "Diagnose, genetica en behandeling van congenitaal en verworven lang QT-syndroom",
        "plan": [
            """
LQTS (Long QT syndroom)
Diagnose:
- LQTS wordt vermoed bij herhaalde QTc > 480 ms zonder symptomen of bij LQTS-diagnostische score > 3 (I-C).
- Overweeg LQTS bij herhaalde QTc tussen 460–480 ms bij aritmogene syncope zonder secundaire oorzaak (IIa).

Genetica:
- Genetische analyse (ped-panel, incl. KCNQ1, KCNH2, SCN5A) is aangewezen bij bewezen LQTS (I-C) en aanbevolen bij sterke klinische verdenking (bv. QTcB >480 puberteit, >500 ms volwassen).

Behandeling:
- Vermijd QT-verlengende medicatie (www.qtdrugs.org) en corrigeer electrolyten.
- Niet-cardioselectieve bètablokkers zijn geïndiceerd bij gedocumenteerd verlengd QT om het aritmogeen risico te verlagen (I-B).
- Bij LQT3-mutatie overweeg mexiletine (I-C).
- Indicatie voor ICD: cardiac arrest (I-B) of symptomatische aritmogene syncope/hemodynamisch niet-getolereerde ventriculaire aritmie (I-B). ICD kan overwogen worden bij herhaalde syncope ondanks bètablokker of bij hoge-risico genotype/QTc kenmerken (IIa/IIb).

Opmerkingen:
- Ongeveer 95% van klassieke LQTS wordt veroorzaakt door loss-of-function mutaties in LQT1–3 (KCNQ1, KCNH2, SCN5A) die IKr beïnvloeden.
- Cascade-genetica is aanbevolen bij positieve vondst.
""",
        ],
    },
    "Breed QRS tachycardie acute behandeling": {
        "description": "Acute aanpak van brede QRS-tachycardie; diagnostiek en eerste behandeling",
        "plan": [
            """
Breed QRS tachycardie — acute behandeling
- Bij hemodynamische instabiliteit: elektrische cardioversie is aangewezen (I).
- Onderzoek en behandel reversible oorzaken bij elke patiënt met ventriculaire aritmie (elektrolietenstoornissen, ischemie, hypoxie, koorts, medicatie) (I-B).
- Indien hemodynamisch stabiel en SVT waarschijnlijk: overweeg vagale manoeuvres of adenosine (IIa).
- Bij gekend structureel hartlijden: elektrische cardioversie (I); bij hoog anesthetisch risico kan farmacologische cardioversie (amiodaron of procainamide) overwogen worden (IIa/IIb).
- Bij gekende outflow tract VT: behandel met bètablokker (I).
- Bij fasciculaire VT: verapamil is aangewezen (I).

Electrical storm / herhaalde ICD-shocks:
- Behandel volgens lokale protocol: sedatie, optimaliseer apparaatprogrammering, IV amiodaron, bètablokkers, urgent ablatie waar beschikbaar; zoek en behandel ischemie.

Polymorfe VT / specifieke entiteiten:
- Bij ischemie: behandel overeenkomstig STEMI-protocol.
- Polymorfe VT getriggerd door unifocale VES: overweeg catheterablatie (IIa) of quinidine (IIb).
- Bij verworven verlengd QT: verwijder triggers, corrigeer magnesium en kalium, isoprenaline en pacing indien nodig (I).
- Brugada of ERS: isoprenaline, quinidine of ablatie overwegen (IIa).
- Idiopathische VF: isoprenaline, verapamil of ablatie van VES-triggers (IIa).
- Long QT / CPVT: bètablokker, pacing en correctie van magnesium/kalium (I). Voor LQTS1/2/CPVT voorkeur voor nadolol/propranolol; LQTS3 kan respons hebben op mexiletine; SQTS/idiopathische VF/ERS/Brugada quinidine.

Herhaalde monomorfe VT:
- Optimaliseer ICD-programmering (I).
- Bètablokker (bij voorkeur non-selectieve zoals propranolol) en sedatie; amiodaron (I).
- Indien refractair aan medische therapie: VT-ablatie (I).
- Corrigeer kalium en magnesium.

Diagnostiek en follow-up na SCA of ernstige aritmie:
- Zoek onderliggende structurele, channelopathische, metabole of toxicologische oorzaken.
- Indien vermoeden myocardiale ischemie: urgente coronarografie bij indicatie (I-C) of STEMI (I-A). Anders geen routine urgente coronarografie.
- Coronaire imaging (CCTA of coronarografie) in tweede lijn (I-B).
- CT-hersenen en thorax bij geen duidelijke cardiale oorzaak op ECG/echo (IIa).
- Toxicologie en genetica bloedname (I-B).
- Uitlezing van CIED (I-B), herhaalde 12-lead ECG (incl. high precordial leads) en continue monitoring (I-C).
- TTE bij elke SCA-survivor (I-C); CMR met LGE bij SCA-survivor zonder oorzaak (I-B).
- Fietsproef nuttig bij SCA-survivor zonder oorzaak (I-B) (CPVT, congenitaal lang QT, ARVC).

Aanvullend onderzoek bij afwezigheid van structureel hartlijden:
- Elektrofysiologisch onderzoek met provocatietesten (adrenaline, sodium channel blocker) aanbevolen; ajmaline/Na-channel blokker test bij SCA-survivor zonder duidelijke oorzaak (I-B).
- Acetylcholine/ergonovine/hyperventilatie test kan overwogen worden voor coronaire vasospasme (IIb).

Indicatie voor ICD: alleen bij levensverwachting van goede kwaliteit ≥ 1 jaar (I-C).
""",
        ],
    },
    "Early Repolarization (ER) - Vroege repolarisatie syndroom": {
        "description": "Diagnosecriteria en behandeling van Early Repolarization (ER) syndrome",
        "plan": [
            """
Early Repolarization (ER) — Vroege repolarisatie syndroom
Diagnose:
- ER-syndroom wordt gediagnosticeerd bij J-punt elevatie ≥ 1 mm in ten minste 2 anatomisch aangrenzende inferior of laterale leads bij een patiënt met een onverklaarde episode van VF of polymorfe VT.
- ER-patroon kan ook op standaard 12-leads worden gezien (J-punt elevatie ≥ 1 mm in 2 anatomisch aangrenzende inferior of laterale leads) en verdient verdere evaluatie.

Behandeling / indicaties voor ICD:
- ICD-implantatie is geïndiceerd bij overlevenden van een SCA veroorzaakt door VF (SCA survivor).
- ICD kan overwogen worden bij patiënten met een ER-patroon en syncope wanneer er symptomatische familieleden zijn met vergelijkbare aritmieën.
- ICD kan overwogen worden bij asymptomatische patiënten met een high-risk ER-ECG-patroon (bv. hoge J-golf amplitude, horizontaal of down-sloping ST-segment).
- ICD-implantatie is niet aanbevolen louter op basis van een ER-patroon: het ER-patroon is veel voorkomend en het absolute risico op VF is meestal laag; behandel en voorkom ischemie en andere triggers primair.

Overige opmerkingen:
- ER vermoedelijk polygeen en beïnvloed door niet-genetische factoren.
- Cardiovasculair risicomanagement en behandeling van ischemie zijn belangrijk omdat ischemie het risico op VF verhoogt.
""",
        ],
    },
    "Short QT syndroom (SQTS)": {
        "description": "Diagnosecriteria en behandeling bij Kort QT-syndroom",
        "plan": [
            """
Short QT syndroom (SQTS)
Diagnose:
- SQTS wordt gediagnosticeerd bij een QTc ≤ 330 ms.
- SQTS kan ook worden vastgesteld bij QTc < 360 ms gecombineerd met een pathogene mutatie, familiale voorgeschiedenis van SQTS, familiale voorgeschiedenis van plotse dood <40 jaar, of overleving van VT/VF zonder structureel hartlijden.

Behandeling en ICD-indicaties:
- ICD-implantatie is geïndiceerd bij overlevenden van SCA of bij gedocumenteerde VT (met of zonder syncope).
- ICD-implantatie kan overwogen worden bij asymptomatische patiënten met SQTS en een familiale voorgeschiedenis van SCD.
- Farmacotherapie: quinidine of sotalol kan overwogen worden in asymptomatische patiënten met SQTS en familiale voorgeschiedenis van SCD om het aritmogeen risico te reduceren.

Opmerkingen:
- Alert zijn voor secundaire oorzaken van QT-verkorting en documenteer familiaire voorgeschiedenis en genetische tests waar relevant.
""",
        ],
    },
    "Behandeling van ANOCA/INOCA endotypes": {
        "description": "Behandeling en protocol voor invasieve coronaire functionele testen bij ANOCA/INOCA",
        "plan": [
            """
Behandeling van ANOCA/INOCA endotypes
Bij persistente symptomen bij patiënten met vermoeden van ANOCA/INOCA en slechte levenskwaliteit zijn invasieve coronaire functionele testen aangewezen om potentieel behandelbare endotypes te identificeren en om symptomen te verbeteren (I-B) 
Hierbij stapsgewijs acetylcholine in opstijgende dosis toediening intracoronair gewoonlijk LAD: 
Macrovasculaire spasme is aanwezig zo klachten, ECG veranderen en angiographische vernauwing >90% op coronarografie tijdens functionele invasieve coronaire testen na acetylcholine. Diltiazem 180-360mg 1x/d, tweede lijn nitraten, derde lijn Nicorandil. 
Microvasculaire spasme is aanwezig zo klachten, ECG veranderen en angiographische vernauwing <90% op coronarografie tijdens functionele invasieve coronaire testen na acetlycholine. Diltiazem 180-360mg 1x/d, tweede lijn Amlodipine, derde lijn nitraten.
Nitroglycerine zal effect van acetylcholine tegengaan en laat toe om endotheel onafhankelijke epicardiale coronaire vasodiltatie te evalueren. 
Adenosine (of Papaverine) is een endotheel onafhankelijk microvasculaire coronaire vasodilator en laat toe op microvasculaire functie te beoordelen. Bij microvasculaire dysfunctie op basis van abnormale vasodilatatie is de CFR verlaagd (CFR<2.5) met verhoogde microvasculaire weerstand (IMR>25 en HMR>2.5) na adenosine. CCB (Amlodipine werkt goed), Betablokker, Ranolazine, Trimetazidine, Ivabradine. 
Agressieve risicofactor reductie en gebruikt van statines en ACE-inhibitors (IA)

Protocol acetylcholine 
RCA/LCA (dominant):
2mcg acetylcholine intracoronair - pauze 60 seconden. 
20mcg acetylcholine intracoronair - pauze 60 seconden. 
50mcg acetylcholine intracoronair - pauze 60 seconden. 
LCA (non-dominant):
2mcg acetylcholine intracoronair - pauze 60 seconden. 
20mcg acetylcholine intracoronair - pauze 60 seconden. 
50mcg acetylcholine intracoronair - pauze 60 seconden. 
100mcg acetylcholine intracoronair - pauze 60 seconden. 
Positief zo symptomen, ECG veranderingen en >90% stenose op angiografie met flow limitatie. 
""",
        ],
    },
    "Acuut Hartfalen opname protocol": {
        "description": "Opname- en behandelprotocol bij acuut hartfalen",
        "plan": [
            """
Acuut Hartfalen opname protocol:
- Opname cardiologie aan telemetrie monitoring.
- Burinex 4mg IV en Diamox 500mg IV op spoed.
- Burinex 2mg IV 2x/d om 8u en 12u verder
- Diamox (Acetozalamide) 500mg IV 1x/d gedurende 3 dagen 
- Start Forxiga 10mg 1x/d 
- Start Aldactone 25mg 1x/d of Soldactone (canreonaat) 200mg IV 1x/d
- Glucose 5% 500cc + 3gr MgSO4 + 40 mmol KCl aan 20cc/u (zo kalium <4 mmol/L)
- Chlorthalidone 50mg 1x/d (te overwegen zo eGFR <30 ml/min/1.73m² of natrium >145 mmol/L)


- Bij long oedeem: Start Vasodilator - Cedocard drip voor veneuze decongestie en afterload reductie - (Isorbide dinitraat) (50mg/50ml in spuitpomp) drip IV aan 1mg/u te verhogen tot 10mg/u met target systolische bloeddruk <110 mmHg. Alternatief is Minitran 15mg/24u

Target diuretica therapie: 
- Twee uur na initiele bolus, urine biochemie (met [UNa+], [UK+], [UOsm])
- Zes uur na initiele bolus, urine output evaluatie.
- Urinary spot sodium - Na 2 uur >50-70 mEq/L
- Urinaire output - Na 6 uur >100-150 mL/u
- Zo niet behalen van target de dosis burinex te verdubbelen tot maximale dosis, of associatie andere type diuretica.
1ste lijn: Acetazolamide (Diamox ®) eg 500mg bolus bovenop lisdiureticum
2de lijn: Thiazidediureticum (Indapamide ®) eg 2.5mg/dag
3de lijn: Empaglifozine (Jardiance ®) eg 10mg/dag

- Morgen coronarografie
- Morgen TTE
- Dagelijks wegen. 
- Dagelijks labo met ionogram en nierfunctie. 
- Urinedebiet opvolgen
- Zoutarm dieet
- Clexane (Enoxaparine) 40mg (0.4ml) 1x/d (tenzij reeds indicatie voor therapeutische anticoagulatie)

- Zuurstof therapie zo nodig bij SpO2<90% of PaO2 <60 mmHg, met target O² sat >92% bij een rustige ademhalingsfrequentie.  
- Ketonen (POCT analyse) zo bicarbonaat verlaagd en SGLT-2 inname. 
- Glucose dagprofiel (GDP) opvolgen 4x/d zo diabeet. 
- Hartfalen educatie
- Kinesitherapie/revalidatie aan bed
- Sociale dienst 
- Consult diëtiste
- Stop Diamox zo natrium >145 mmol/L of HCO³ <22 mmol/L. 
- Stop MRA zo kalium >5 mmol/L. 

- Gezien anemie (hemoglobine <13 g/dL): Evaluatie door middel van complete celtelling, reticulocyten, ferritine, transferrine saturatie, vitamine B12 en foliumzuur.
Target hemoglobine 10.0-11.5 g/dl met laagst noodzakelijke EPO dosis. Verhoogd thrombo-embolisch risico bij hemoglobine waardes >13g/dL.
Evaluatie door middel van complete celtelling, reticulocyten, ferritine, transferrine saturatie, vitamine B12 en foliumzuur.

- Gezien CNI: Labo met serum fosfaat, calcium, PTH en vitamine D ter evaluatie CKD-MBD.  

Frequente comorbiditeit bij hartfalen (ESC 2021)
- Anemie en ijzerdeficiëntie - Injectafer ® (Ferric carboxymaltose) 1gr IV  
- Jicht en artritis - Zyloric® (Allopurinol) 300mg 1x/d 
- Erectiele dysfunctie - Viagra® (Sildenafil) 50mg 1x/d zo nodig  - niet met nitraten. 
- Depressie - Sipralexa® (Escitalopram) 10mg 1x/d 
- Hypochloremie (<96 mmol/l) - Diamox (Acetozolamide) 500mg 2x/d
- OSAS en COPD - Longfunctie, Inhalatie therapie, CPAP. 
- Daling van nierfunctie <50% tov baseline bij een serum creatinine (sCreat) <3mg/dL is te tolereren. 
- Frailty, cachexie en sarcopenie - Nutritionele ondersteuning (dietiste), kinesitherapie, cardiale revalidatie. 
- Obesitas - Gewichtsverlies, anti-diabetica, dieetmaatregelen. 
- Schildklierstoornissen
- Diabetes - Start SGLT-2 inhibitor of GLP-1 antagonist. 
- Secondary (functional) mitral regurgitation - OMT, CRT
- Voorkamerfibrillatie - Cathteter ablatie zo duidelijke associatie deterioratie van symptomen hartfalen bij paroxysmale of persistente VKF. 
Proton pomp inhibitors
- Pantomed ® (Pantoprazole) 40mg 1x/d bij patiënten met gestegen risico op bloedingen
Hypomagnesiëmie bij diuretica
- Magnepamyl forte ® (Magnesiumcitraat 667mg) 1x/d
""",
        ],
    },
    "Chronisch coronair syndroom": {
        "description": "Diagnostiek, risicostratificatie en revascularisatie-indicaties bij chronisch coronair syndroom (CCS)",
        "plan": [
            """
Chronisch coronair syndroom

Thoracale pijn uitgelokt door emotionele stress, dyspnee of duizelingen bij inspanning, pijn in de arm, kaak of nek moeten overwogen worden als potentionele angor equivalenten (IIa-B)
Een 12-lead ECG is noodzakelijk in alle patiënten met thoracale pijn (I-C)
Een transthoracale echocardiografie is aangwezen (I-B)
Inspanningselectrocardiogram (I-C)
RX thorax ter evaluatie van longziekten en andere thoracale oorzaken van thoracalepijn (IIa)
Holter zo vermoeden van aritmie of vasospastische angor. (IIa)
Labo met cytologie, nierfunctie, ionogram volledig lipiden profiel incl. lipoproteïne (a), schildklierbilan, Hs-CRP, fibrinogeen en HbA1C. (I-A)
Bij very low pre-test probability (<5%) is geen verdere diagnostische test noodzakelijk
Bij low or moderate pre-test probability (5%-50%) is een CCTA aanbevolen om obstructief CAD te evalueren en risico op MACE (I-A) Bij nierfalen (eGFR <30 ml/min/1.73m², ernstige coronaire verkalkingen, snelle onregelmatige hartslag, obesitas, incoperatief met commando's om de adem in te houden is alternatief noodzakelijk. 
Bij moderate or high pre-test probability (15%-85%) is stress echocardiografie aangewezen om myocardiale ischemie aan te tonen en risico op MACE te evalueren. (I-B) Zo slecht echogeen is alternatief nucleaire imaging.  
Bij hoge pre-test probablitiy (>85%) is coronarografie aangewezen zo ernstige symptomen refractair aan medicatie, angor bij kleine inspanning of hoog risico op MACE. (IC)
Bij nieuwe plots opgekomen symptomen die zeer suspect zijn voor obstructief coronairlijden en die optreden bij kleine inspanning is coronarografie aangewezen (IC)

Revascularisatie indicaties
Hoofdstam: Revascularisatie is aangewezen bij functioneel significant hoofdstamletsel met ≥50% stenose om overleving te verbeteren (I-A). Zo laag chirurgisch risico door middel van CABG gezien lager risico op hartinfarct en nieuwe revascularisatie (I-A) Zo weinig complex letsel (SYNTAX <22) kan PCI gebruikt worden gezien minder invasief en non-inferior op vlak van overleving (I-A)

Meertakslijden + Diabetes: Revascularisatie is aangewezen zo onvoldoende response bij GDMT,  CABG heeft sterke voorkeur om overleving te verbeteren (I-A) Zo hoog chirurgisch risico kan multi-vessel PCI overwogen worden over medicaal beleid om symptomen en MACE te reduceren (IIa)

Drietaksziekte zonder diabetes: Revascularisatie is aangewezen bij functioneel significant drietaksziekte met ≥70% stenose om symptomen te verbeteren, cardiovasculaire mortaliteit reduceren en het risico op myocardinfarct. (I-A) CABG is aanbevolen om overleving en symptomen te verbeteren (I-A) PCI kan ook overwogen worden zo lage tot matige anatomische complexiteit (I-A)

Eentaksziekte of tweetaksziekte inclusief proximale LAD met ≥70% stenose en FFR-CT ≤0,8: CABG of PCI aanbevolen boven medische therapie om de symptomen en outcomes te verbeteren zo onvoldoende respons op medische therapie. (I-A)



Éénvatziekte of tweetaksziekte zonder proximale LAD: Bij symptomatische CCS-patiënten met significante eenvatziekte of tweetaksziekte zonder proximale LAD wordt zo onvoldoende respons op medicamenteuze therapie PCI aanbevolen om de symptomen te verbeteren (I-A)
Coronarografie 
Intracoronaire drukmeting is aanwezen om functionele ernst van matige letsels te beoordelen bij niet-hoofdstam letsels alvorens revascularisatie (I-A)
Een matig hoofdstamletsels kan best geëvalueerd worden door middel van FFR/iFR of IVUS alvorens revascularisatie (IIa-B) 
Een FFR/iFR bij hyperemie is significant zo significant ≤0.8 or ≤0.89 respectievelijk per definitie is dit ratio Pdistaal/Paorta bij hyperemie.(I-A)
Systematische FFR meting is niet aanbevolen, enkel bij matige letsels (III-A)

Medicamenteuze therapie
Kortwerkende nitraten (e.g. Cedocard) zijn aangewezen voor onmiddellijke verlichting van angor. (IB)
Een calciumchannelblokker (Diltiazem retard 180mg 1x/d) of betablokker (e.g. Nebivolol 5mg 1x/d) is aangewezen in eerste lijn (I-B)
Zo onvoldoende controle met beta-blokker en CCB kan langwerkend nitraat gebruikt worden (IIa). 
Ivabradine kan overwogen worden bij LVEF <40% als add on (IIa-B)
Agressieve risicofactor reductie en gebruikt van statines en ACE-inhibitors (IA)
""",
        ],
    },
        "Aortaklepstenose": {
                "description": "Indicaties voor interventie, type klep en antitrombotisch beleid bij aortaklepstenose",
                "plan": [
                        """
Aortaklepstenose
- Interventie is aangewezen bij ernstige symptomatische high-gradient aortaklepstenose (mean >40 mmHg, Vmax>4 m/s en AVA <1 cm² of <0.6cm²/m²) of bij ernstige symptomatische low-flow (SVi <35mL/m²) gradient (mean <40 mmHg) met verminderde LVEF <50% en:
- Bij symptomen - Class IB
- Bij LVEF <50% (zonder andere oorzaak) - Class IB
- Bij LVEF <55% (zonder andere oorzaak) - IIa
- Bij bloeddrukdaling >20 mmHg bij inspanning - Class IIa
- Bij ernstige AS  mean >60 mmHg, Vmax >5m/s IIa
- Ernstige calcificatie (>2000 man, >1200 vrouw) en Vmax progressie >0.3m/s/jaar.
- Verhoogde BNP/NT-proBNP ongeacht symptomen of criteria - Class IIa

Type klep en chirurgie
- TAVI is aanbevolen bij oudere patiënten >70 jaar bij tricuspiede aortaklepstenose zo anatomie geschikt is (IA)
- Non-transfemorale TAVI moet overwogen worden bij patiënten die niet geschikt zijn voor chirurgie zonder transfemorale toegang (IIa)
- TAVI kan overwogen worden bij ernstige bicuspiede aortaklepstenose in patiënten met verhoogd chirurgisch risico als anatomie geschikt is. (IIb)
- SAVR bij jonge patiënten (<70 jaar en STS-PROM/EuroSCOREII<4%) zo chirurgisch risico laag is (IB).


- Mechanische chirurgische klep indicatie zo :
    Wens van de geïnformeerde patiënt zo geen contra-indicatie voor langdurige anticoagulatie. (I)
    Bij patiënten <60 jaar voor aortale positie en bij patiënten <65 jaar voor protheses in mitralis positie. (IIa)
    Zo goede levensverwachting een geen contra-indicatie voor langdurige anticoagulatie (IIa)
    Zo reeds mechanische klep in andere positie (IIa)
    Zo voorafbestaand indicatie voor levenslange anticoagulatie (IIb)

Biologische chirurgische klep indicatie zo:
    Wens van de geïnformeerde patiënt (I)
    Zo adequate anticoagulatie met VKA onwaarschijnlijk, hoog bloedingsrisico of korte levensverwachting (I)
    Bij patiënten >65 jaar voor aortale positie of >70 voor mitralis positie. (IIa)
    Bij vrouwen met zwangerschapswens (IIa)

Concomitante chirurgie
    SAVR is aangewezen bij ernstige aortaklepstenose (AVA <1.0cm², mean >40 mmHg) bij primaire indicatie voor CABG, andere klepchirurgie of aortachirurgie ongeacht symptomen (I-C)
    SAVR moet overwogen worden bij matige aortaklepstenose (AVA 1.0-1.5 cm², mean 25-40 mmHg) bij primaire indicatie voor CABG, andere klepchirurgie of aortachirurgie ongeacht symptomen (IIa-C).

Coronairen:
- CABG bij primaire indicatie voor valvulaire chirurgie en coronaire stenose >70%  (of >50% stenose van hoofdstam).  I-C
- CABG moet overwogen worden bij indicatie voor valvulaire chirurgie en coronaire stenose van 50-70%.
- PCI moet overwogen worden bij indicatie voor TAVI en stenose >90% in coronair met diameter >=2.5mm.
- PCI kan overwogen worden bij TEER (e.g. Mitraclip) en coronaire stenose >70% in proximaal segment van majeure coronaire tak.
- Bij aorta ascendens >45mm zou gelijktijdige aortachirurgie overwogen moeten worden.

Anti-plaatjes - antico
- Lage dosis aspirine is aangewezen gedurende 12 maanden na TAVI in patiënten zonder indicatie voor anticoagulatie.  (I)
- Lage dosis aspirine levenslang moet overwogen worden na TAVI patiënten zonder indicatie voor anticoagulatie.  (IIa)
- NOAC monotherapie na TAVI bij patiënten met indicatie voor anticoagulatie (I)
- Na chirurgische biologische aortaklep moet lage dosis aspirine of OAC met VKA overwogen worden voor 3 maanden (IIa).
- Na chirurgische biologische mitralis- of tricuspidalisklep moet OAC met VKA overwogen worden voor 3 maanden (IIa).
- Na biologische aorta- of mitralisklep kan levenslang asaflow overwogen worden (IIb).
- Bij anemie/bloedingsneiging/vermoeden Heyde dan VWF antigen, activiteit en collagen binding als eerste uitwerking.

Mixed valve disease
- Interventie is aangewezen bij symptomatische patiënten met gemengde matige aortaklepstenose (AVA >1cm²) en matige regurgitatie met mean gradiënt >40 mmHg of Vmax >4 m/s. (I)
- Interventie is aangewezen bij asymptomatische patiënten met gemengde matige aortaklepstenose (AVA >1cm²) en matige regurgitatie met Vmax >4cm/s en LVEF <50% zonder andere verklaring (I)
""",
                ],
        },
        "Aortaklepinsufficiëntie (AI)": {
            "description": "Indicaties voor chirurgie, aorta-aneurysma en genetica bij aortaklepinsufficiëntie",
            "plan": [
                """
    Aortaklepinsufficiëntie (AI)

    Indicatie voor chirurgie bij ernstig aortaklepinsufficiëntie en:
    - Symptomen (klasse IB)
    - LVESD >50 mm of LVESDi >25 mm/m² of LVEF <50% ongeacht symptomen - Klasse IB
    - Chirurgie kan overwogen worden bij asymptomatische patiënten met ernstig en LVESDi >22 mm/m², LVESVI>45 ml/m² of LVEF <55% bij laag chirurgisch risico - Klasse IIb
    - Andere indicatie voor cardiale heelkunde (CABG, Aorta, andere klep, …) ongeacht symptomen - Klasse IC
    - Bij indicatie voor chirurgie aan aortaklep met aorta ascendens >45mm zou gelijktijdige aortachirurgie overwogen moeten worden.
    - Aorta aneurysma beoordelen met CT of MRI om asymmetrie uit te sluiten en baseline afmetingen te bepalen bij vermoeden op TTE. (I-C)

    Indicatie voor chirurgie bij aneurysma van aortawortel of tubulair aorta ascendens aneurysma ongeacht de ernst van aortaklepinsufficiëntie:
    - Valve-sparing aortic root replacement bij jonge patiënten - Klasse IB
    - Marfan syndroom met aorta ascendens >= 50 mm - Klasse I-C
    - Aorta ascendens of aortawortel >55 mm - Klasse I-B
    - Aorta ascendens >45 mm bij Marfan en andere risicofactor (TGFBR1 of TGFBR2 mutatie) - Klasse IIa
    - Aorta ascendens >50 mm bij bicuspiede aortaklep - Klasse IIa
    - Bij indicatie voor chirurgie aan aortaklep met aorta ascendens >45mm zou gelijktijdige aortachirurgie overwogen moeten worden.

    - Zo aneurysma van aortawortel of aorta ascendens of dissectie van thoracale aorta is een familiale anamnese aangewezen naar thoracale aorta dissectie, plots dood en perifere en intracraniale aneurysmas.
    - Zo aneurysma van aortawortel of aorta ascendens of dissectie van thoracale aorta en risicofactor voor HTAD (hypertensie, aortacoarctatie, bicuspiede klep) is een genetica analyse aanbevolen met genetische counseling (I-B) - TAAA gen panel.
    - Bij diagnose van bicuspiede aortaklep is het aangewezen om 1ste graadsverwanten te screenen voor bicuspiede aortaklep (IB)
    """,
            ],
        },
        "Acuut coronair syndroom": {
        "description": "Diagnostiek en acute behandeling bij acuut coronair syndroom (ACS): STEMI en NSTEMI",
        "plan": [
            """
Acuut coronair syndroom (ACS)

Diagnostiek:
- Herhaal hs-cTn staal op 0 uur en 1 uur (assay-specifieke cut-offs). Bij twijfel derde staal op 3 uur.
- Low rule-out: < 5 ng/L en delta < 2 ng/L
- High rule-in: > 64 ng/L of delta ≥ 6 ng/L
- ECG met extra leads (V3R, V4R, V7–V9) bij vermoeden inferior infarct of totale occlusie wanneer standaardleads niet concludent zijn.
- ECG STEMI-criteria: J-punt elevatie in 2 anatomisch aangrenzende leads ≥2.5 mm in mannen <40 jaar, ≥2.0 mm in mannen ≥40 jaar, ≥1.5 mm in vrouwen in V2–V3, of ≥1 mm in andere leads; of >0.5 mm in V4R, V3R, V7–V9 (exclusief LBBB of LVH interpretatie).
- RX-thorax en transthoracale echocardiografie voor andere oorzaken en beoordeling globale/regionale functie, klepafwijkingen en pericard.

Acute management (algemene principes):
- Onderzoek en behandel reversibele oorzaken (ischemie, elektrolieten, hypoxie, koorts, medicatie) (I-B).
- Bij hemodynamische instabiliteit: directe elektrische cardioversie/revascularisatie strategie.
- Immediate invasieve strategie bij cardiogene shock, recidiverende/hevige pijn ondanks therapie, levensbedreigende aritmieën, mechanische complicaties, acuut hartfalen door ischemie, terugkerende dynamische ST/T veranderingen, of persistente ST-elevatie.

Medicatie (NSTEMI-specifiek vermeld):
- Aspegic 250 mg IV eenmalig, daarna acetylsalicylzuur 80 mg 1×/d.
- Bij geen invasieve evaluatie binnen 24 uur: fondaparinux 2.5 mg SC 1×/d (I-A) ± overweeg P2Y12-inhibitor (IIb).
- Bij invasieve evaluatie binnen 24 uur: UFH 70 IU/kg IV of enoxaparine 1 mg/kg SC 2×/d.
- Analgetica/vasodilatoren: cedocard pomp IV of sublinguaal, morfine 2.5–5 mg SC indien nodig.
- Bètablokkers: seloken (metoprolol) 5 mg IV iedere 5 min tot max 15 mg indien pols >60 en systolische BD >120 en geen hartfalen (IIa).
- Zuurstof alleen indien SaO2 < 90%.
- PPI (pantoprazol) indien hoog bloedingsrisico.
- Statine-introductie en andere secundaire preventieve maatregelen.

Antitrombotische/antiplatelet overwegingen bij ACS/STEMI:
- Bij STEMI: heparine bolus (70 IU/kg, max 5.000 IU) en overweeg loading met ticagrelor 180 mg als PPCI-strategie (IIb) of indien NSTEMI zonder vroege invasieve evaluatie (IIb).
- Clopidogrel 600 mg kan gebruikt worden bij hoog leeftijd/hoog bloedingsrisico als alternatief voor ticagrelor.
- Routine pre-treatment met P2Y12 niet aanbevolen bij NSTEMI als coronair anatomie onbekend en vroege invasieve strategie gepland (III).

Revascularisatie:
- Primaire PCI (PPCI) bij STEMI.
- Bij hemodynamische instabiliteit / cardiogene shock: culprit-only PCI is aangewezen (I-B).
- Volledige revascularisatie bij hemodynamisch stabiele STEMI: binnen indexprocedure of binnen 45 dagen afhankelijk van angiografische ernst (I-A).
- NSTEMI met multivessel disease: volledige revascularisatie overwegen, bij voorkeur tijdens indexprocedure (IIa).

Speciale situaties:
- MINOCA: indien geen culpible vessel op angiografie, is CMR geïndiceerd om etiologie te achterhalen (I-B). Onderzoek voor myocarditis, takotsubo, apicale HCM, non-ischemische CMP en AMI.

Documentatie en follow-up:
- Documenteer timing van troponines, ECG- wijzigingen, en interventies.
- Bewaar beeldvorming en coronair anatomie voor vervolgbeslissingen (DAPT-keuze, revascularisatieplanning).
""",
        ],
    },
    "Aorta Aneurysma opvolging": {
        "description": "Richtlijnen voor follow-up en beeldvorming van thoracale aorta aneurysma",
        "plan": [
            """
Aorta Aneurysma opvolging

Zo 30-40mm dan elke 3 jaar TTE.
Zo 40-44mm dan baseline CT of MR aorta en controle TTE in 1 jaar, zo toename >3mm/jaar dan bevestigen met CT of MR aorta en zo bevestigd elke 6 maanden TTE.
Zo 40-44mm dan baseline CT of MR aorta en controle TTE in 1 jaar, zo toename <3mm/jaar dan controle TTE elke 2 jaar.
Zo 45-49mm dan dan baseline CT of MR aorta en controle TTE elke 6 maanden.
Zo 50-52mm dan baseline CT of MR aorta, zo hoog risico eigenschappen (familiale voorgeschiedenis van acute aorta events, ongecontroleerde hypertensie, leeftijd<50 jaar) dan kan chirurgie overwogen worden (IIb) anders elke 6 maanden nieuwe beeldvorming.
Zo 50-52mm zonder hoog risico eigenschappen dan CT of MR aorta in 6 maanden, zo toename >3mm/jaar dan chirurgie. Zo <3mm/jaar dan elke 6 maanden nieuwe beeldvormingen.
Zo 50-54mm dan baseline CT of MR aorta, zo wortel fenotype en bicuspiede klep dan chirurgie (I)
Zo 50-54mm dan baseline CT of MR aorta, zo wortel fenotype en tricuspiede klep kan chirurgie overwogen worden (IIb).
Zo >55mm dan chirurgie (I)

Zo aorta aneurysma of thoracale aorta dissectie met risicofactoren voor HTAD is genetische testingen aangewezen. (<60 jaar, geen klassieke risicofactoren, onverklaard plots overlijden familiaal, intracraniële of perifere aneurysmas, familiale TAD, syndromale kenmerken van Marfan, Loeys-Dietz of Ehler-Danlos).
""",
        ],
    },
    "Primaire mitralis regurgitatie": {
        "description": "Indicaties voor mitralisklepchirurgie en aanpak bij primaire mitralisklepregurgitatie",
        "plan": [
            """
Primaire mitralis regurgitatie

Mitralisklepchirurgie is aangewezen bij ernstige primaire mitralisklepregurgitatie en:
- Symptomen - (I-B)
- LV dysfunctie met LVEF <=60% of LVESD >40 mm of LVESDI >=20mm/m²  -  (I-B)
- Pulmonale hypertensie met sPAP in rust >50 mmHg - (IIa-B)
- LA dilatatie (LAVI >60 ml/m² of LA diam >=55mm)  - (IIa-B)
- Voorkamerfibrillatie - (IIa-B)
Chirurgisch klepherstel heeft de voorkeur als chirurgische techniek (I-B).
Minimaal invasieve klepchirurgie kan overwogen worden om hospitalisatieduur te verkorten en snelheid van herstel te bevorderen (IIb).
- TEER bij symptomatische patiënten met ernstig PMR, hoog chirurgisch risico en echocardiografisch in aanmerking komen.
""",
        ],
    },
    "Secundair mitralisregurgitatie": {
        "description": "Beleid en interventiecriteria bij secundaire (functionele) mitralisklepregurgitatie",
        "plan": [
            """
Secundair mitralisregurgitatie
Mitralisklepchirurgie is aangewezen bij primaire indicatie voor CABG en ernstige ventriculaire secundaire mitralisklepregurgitatie. (I-B)
Mitralisklepchirurgie kan overwogen worden bij primaire indicatie voor CABG en matige ventriculaire secundaire mitralisklepregitatie bij. (IIb)
PCI gevolgd door TEER na herevaluatie van MR kan overwogen worden bij symptomatische patiënten met ernstige ventriculaire secundaire mitralisklepregitatie en non-complex CAD (IIb).

M-TEER is aangewezen bij hemodynamisch stabiele, symptomatische patiënten met verminderde LVEF <50% en persistente ernstige ventriculaire secundaire mitralisklepregitatie ondanks optimalisatie van guideline directed medical therapy (GDMT) en cardiale resynchronisatie therapie (CRT) waar mogelijk en voldoen aan specifiek klinische en echocardiografische criteria (I-A):
Anatomie geschikt voor M-TEER
NYHA >=II
LVEF 20-50%
LVESD <=70mm
Minstens 1 hospitalisatie voor hartfalen of NT-proBNP >1000 pg/mL
sPAP <70 mmHg
Geen ernstige RV dysfunctie
Geen eindstadium hartfalen
Geen CAD met indicatie voor revascularisatie
Geen ernstige aortaklep of tricuspidalisklep pathologie.
Geen hypertrofe, restrictieve of infiltratieve cardiomyopathie.

Mitralisklepchirurgie in combinatie met chirurgische AF ablatie en LAA sluiting kan overwogen worden bij ernstige atriale secundaire mitralisklepregurgitatie met persisterende symptomen ondanks optimale medicamenteuze therapie (incl. ritmecontrole).
M-TEER kan overwogen worden bij patiënten met ernstige symptomatische atriale secundaire mitralisklepregitatie die te hoog risico zijn voor chirurgie na optimialisatie van medicatie (incl. ritmecontrole).
""",
        ],
    },
    "Mitralis stenose": {
        "description": "Indicaties en beleid bij mitralis stenose (MS)",
        "plan": [
            """
Mitralis stenose
- Indicatie voor percutane commissurotomie (PMC) bij symptomatische patiënten met ernstig degeneratieve of reumatische mitralisklepstenose (MS) zo geen klinische of anatomische ongunstige eigenschappen (NYHA 4, ernstige PHT, Cormier score group 3, Wilkins' Echo Score >8, ernstig TR, …) of contra-indicatie voor PMC.

Klepchirurgie is aangewezen bij symptomatische patiënten met ernstig MS en contra-indicatie voor PMC:
- MVA >1.5cm² (Tenzij symptomen niet verklaard kunnen worden door andere pathologie dan MS).
- LA thrombus (zo thrombus in LAA kan PMC nog wel overwogen worden bij contra-indicatie voor chirurgie of bij urgente indicatie voor interventie bij patiënten die 1-3 maanden OAC kunnen nemen op voorwaarde dat controle TEE resolutie van thrombus toont).
- Meer dan milde mitralisklepregurgitatie.
- Ernstige of bi-commissurale calcificatie.
- Afwezigheid van commissurale fusie.
- Ernstige AV pathologie of gecombineerde TV stenose met indicatie voor chirurgie.
- Concomitante CAD met indicatie voor CABG.

- Percutane commissurotomie (PMC) moet overwogen worden bij asymptomatische patiënten zonder ongunstige klinische of anatomische eigenschappen (NYHA 4, ernstige PHT, Cormier score groep 3, Wilkins' Echo Score >8, ernstig TR, …) en:
  - Hoog trombo-embolisch risico (voorgeschiedenis systemische embolisatie, dense spontaan contrast in LA of nieuwe diagnose of paroxysmale VKF) - (IIa)
  - Hoog risico op hemodynamisch decompensatie (sPAP >50 mmhg in rust, noodzaak tot majeure niet-cardiale chirurgie, actieve zwangerschap of zwangerschapswens) -(IIa)

Transcatheter mitral valve implantation (TMVI) kan overwogen worden bij uitgesproken MAC en ernstige MV dysfunctie zo lokale expertise in complexe MV chirurgie en transcatheter behandeling (IIb)
""",
        ],
    },
        "Tricuspidalis regurgitatie": {
                "description": "Beleid en indicaties bij tricuspidalisklepregurgitatie (TR)",
                "plan": [
                        """
Tricuspidalis regurgitatie
Bij primaire indicatie voor linkszijdige klepchirurgie vormt er zich een indicatie voor concomitante tricuspidalisklep chirurgie (klepherstel indien mogelijk) zo:
- Ernstige primaire of secundaire TR (I)
- Matige primaire of secundaire TR ter preventie van TR progressie en RV remodelling (IIa)
- Milde secundaire TR met annulus dilatatie (>=40mm of > 21mm/m²) ter preventie van progressie van TR en RV remodelling (IIb)

Tricuspidalisklepchirurgie (klepherstel indien mogelijk) is aangewezen bij ernstige symptomatische primaire tricuspidalisklepregurgitatie zonder ernstige RV dysfunctie (TAPSE <10mm, RV TDI s’ <6cm/s, 3D RVEF <35%, of FAC <22%) of ernstige pulmonale hypertensie (mPAP >35 mmHg, PVR >5WU). (I)
Tricuspidalisklepchirurgie (klepherstel indien mogelijk) moet overwogen worden bij asymptomatische ernstige primaire tricuspidalisklepregurgitatie met beperkte RV dilatatie of dysfunctie maar zonder ernstige RV dysfunctie (TAPSE <10mm, RV TDI s’ <6cm/s, 3D RVEF <35%, of FAC <22%) of ernstige pulmonale hypertensie (mPAP >35 mmHg, PVR >5WU). (IIa)
Tricuspidalisklepchirurgie (klepherstel indien mogelijk) moet overwogen worden bij patiënten met ernstige secundaire TR en symptomen of RV dilatatie of RV dysfunctie zonder ernstige LV/RV dysfunctie of PHT.
Transcatheter TV treatment moet overwogen worden ter bevordering van quality of life (QOL) en RV remodelling bij ernstige symptomatische TR ondanks optimale medicamenteuze therapie in afwezigheid van ernstige RV dysfunctie of pre-capillaire PHT (mPAP >20 mmHg, PVR >2WU, PAWP <15 mmHg).

- Indicatie voor chirurgie bij primair ernstig TR en:
    - Indicatie voor linkszijdige valvulaire heelkunde - Klasse I C
    - Symptomatisch geïsoleerd ernstig primair TR en afwezigheid van ernstig RV dysfunctie - Klasse I C

- Indicatie voor chirurgie bij primair matig TR en:
    - Indicatie voor linkszijdige valvulaire heelkunde - Klasse IIa
    - Asymptomatisch of mild symptomatisch geïsoleerd primair TR met RV dilatatie - Klasse IIa

Secundaire tricuspidalis regurgitatie:
- Indicatie voor chirurgie bij ernstig secundaire TR met indicatie voor linkszijdige valvulaire heelkunde - Klasse I B
- Overwegen van chirurgie bij mild of matig secundair TR met gedilateerde annulus (>40 mm of >21mm/m²) met indicatie voor linkszijdige valvulaire heelkunde - Klasse IIa
- Overwegen van chirurgie bij ernstig secundair TR met symptomen of RV dilatatie in de afwezigheid van RV dysfunctie of LV dysfunctie of pulmonale hypertensie.
Transcatheter behandeling kan overwogen worden bij symptomatisch ernstig secundair TR in inoperabele patiënten na overleg in Heart Team.
""",
                ],
        },
                "Hypertensie guidelines 2024": {
                "description": "Diagnostische criteria en behandelprincipes voor hypertensie (2024)",
                "plan": [
                    """
        Hypertensie guidelines 2024
        Diagnostische criteria voor hypertensie zijn 140/90 mmHg op raadpleging of 135/85 mmHg op thuismeting. Diagnostische bevestiging is best via zelfmeting of 24u bloeddrukmeting. Tussen 120/70 en 135/85 mmHg is er sprake van verhoogde bloeddruk.

        Diagnose van hypertensie zo op automatische 24 uur bloeddrukmeting (ABPM) >130/80 mmHg gemiddeld over 24u of >120/70 mmHg gemiddeld nachtelijk.
        Diagnose van hypertensie zo op gemiddelde metingen thuis >135/85 mmHg op thuismeting met gevalideerd automatisch toestel met manchet rond arm (HBPM).

        Zo gemeten bloeddruk op raadpleging 120-139/70-89 mmHg dan best ambulante bloeddruk volgen met thuismeting met gevalideerd automatisch toestel met manchet rond arm (HBPM) of automatische 24 uur bloeddrukmeting (ABPM) of, indien niet mogelijk, door herhaalde metingen op raadpleging.
        Zo gemeten bloeddruk op raadpleging 140-159/90-99 mmHg kan de diagnose van hypertensie best gebaseerd worden op ambulante bloeddrukmeting met een gevalideerd automatisch toestel met manchet rond arm of, indien niet mogelijk, door meerdere metingen op raadpleging.

        Bij patiënten jonger dan 40 jaar met hypertensie kan best een screening gebeuren naar secundaire oorzaken. Tenzij bij obesitas kan best eerst een slaapstudie gepland worden.

        Een 12-lead ECG bij elke patiënt met hypertensie.
        Labo met creatinine, eGFR, aldosteron en renine alsook een urine staal met creatinine en eiwit/albumine bij elke patiënt met hypertensie.

        Target voor systolische bloeddruk is 120 mmHg en <129 mmHg. Correcte ambulante meting met gevalideerd en gekalibreerd bloeddrukmeter met een manchet om bovenarm (bijv. Omron, Withings). Bij intolerantie geldt het ALARA-principe (as low as reasonably achievable).

        Medicamenteuze behandeling voor elke patiënt met bloeddruk >140/90 mmHg ongeacht cardiovasculair risico. (IA)
        Medicamenteuze behandeling bij bloeddruk >130/90 mmHg bij verhoogd cardiovasculair risico en geen effect van leefstijlaanpassingen gedurende 3 maanden (IA).

        Evaluatie voor orthostatische hypotensie bij opstart van nieuwe antihypertensieve medicatie is aangewezen bij elke patiënt. Meet patiënt na 5 minuten liggend, vervolgens staand na 1 minuut en na 3 minuten.

        Screening voor primair hyperaldosteronisme met aldosteron en renine in alle patiënten met bloeddruk >140/90 mmHg (IIa/B).

        Levenslang continueren van antihypertensieve medicatie, zelfs voorbij 85 jaar indien goed getolereerd (IA). Bij oudere patiënten >85 jaar met frailty of beperkte levensverwachting kan behandeling pas gestart worden vanaf 140/90 mmHg; bij voorkeur gebruik langwerkende calciumantagonist of ACE-remmer. Diuretica, bètablokkers en alfa-blokkers vermijden waar mogelijk.
        """,
                ],
            },
            "Uitwerking secundaire hypertensie": {
                "description": "Werkup en beslisregels voor secundaire hypertensie",
                "plan": [
                    """
        Uitwerking secundaire hypertensie

        Indicatie voor evaluatie van secundaire oorzaken bij:
        - Bloeddruk >160/100 mmHg onder de leeftijd van 40 jaar.
        - Bloeddruk >180/110 mmHg ongeacht leeftijd.
        - Acuut ontstaan of snel progressieve arteriële hypertensie.
        - Resistente hypertensie of hypertensive emergency.

        Aanvullende tests:
        - Urineanalyse van sediment (erythrocyten, leucocyten, microscopisch onderzoek).
        - 24u urinecollectie met creatinine, totaal eiwit, natrium, kalium, 24u aldosteron, 24u cortisol. (Patiënt moet 5 g zout/dag vanaf 3 dagen voor en inclusief dag van de test).
        - 24u urine met metanefrines (positief >400 µg/24u), normetanefrines (positief >900 µg/24u) en VMA. Let op interferentie met ethanol, TCA, amfetamines en adrenerge medicatie.
        - Laboratorium: creatinine, ionogram, lipidenprofiel, calcium, fosfaat, HbA1c, PRC, PAC, cortisol, ACTH, PTH, TSH, T4. (Patiënt minimaal 2 uur uit bed en 5–15 minuten zittend voor bloedafname).
        - Overweeg oftalmologisch nazicht.

        Beeldvorming en functieonderzoek:
        - Echografie nieren incl. duplex, resistentie-index (RI), corticale dikte en lengte. Bij hoge verdenking CT-angio nieren.
        - Bij vermoeden OSAS: polysomnografie; gebruik ABPM om non-dipping of reverse-dipper patroon te evalueren.
        - Meet altijd bloeddruk links en rechts en op de benen bij verdenking coarctatio.

        Specifieke interpretaties (aldosteron/renine):
        - Plasma renine concentratie (PRC) en 24u aldosteron (5 g zout vanaf 3 dagen voor test).
        - PRC >8 µIU/ml en 24u aldosteron <6 µg/24u → weinig aanwijzing voor primair aldosteronisme.
        - PRC <8 µIU/ml en 24u aldosteron 6–12 µg/24u → mogelijk renine-onafhankelijke aldosterone productie; overweeg proefbehandeling met spironolactone 25 mg 1x/d.
        - PRC <8 µIU/ml en 24u aldosteron >12 µg/24u bij 24u natriumexcretie ≈200 mmol → consistent met primair hyperaldosteronisme; vervolgonderzoek met adrenale CT.
        - 24u urinair aldosterone: sensitiviteit ~96%, specificiteit ~93%.

        CAVE:
        - Anti-hypertensiva (ACEi, ARB, MRA) kunnen vals-negatieven veroorzaken; doorgaans voortzetten i.v.m. risico's bij staken. Start MRA bij voorkeur na testen.
        - Voor PRC/PRA: patiënt minimaal 2 uur uit bed en 5–15 min zittend voor bloedafname.
        - PAC vaak >10 ng/dL; >20 ng/dL is duidelijk positief. PAC/PRC ratio verdacht bij >35 (pmol/µIU) en positief boven ~91 pmol/µIU.

        Praktische interferentie-aanpak (medicatie tijdens workup):
        - Overweeg hydralazine 50 mg 2x/d en terazosine 5 mg 's avonds om antihypertensieve beïnvloeding te minimaliseren.
        - Dagelijks 2x bloeddruk meten en noteren.

        Behandelstappen bij zeer hoge bloeddruk (>180 mmHg):
        Stap 1: start lodixal 240 mg per dag.
        Stap 2: ophogen hydralazine tot 4x1 co per dag indien nodig.

        Primair aldosteronisme:
        - Bij resistente hypertensie ondanks eerstelijnstherapie moet opstart van spironolactone overwogen worden, ook zonder formele diagnose (IIa).
        - Bij intolerantie voor spironolactone: eplerenone als alternatief (IIa). Amiloride kan aanvullend of vervangend worden gebruikt.
        - Natriumarm dieet als aanvulling.
        - Unilaterale PA (APA) → laparoscopische adrenalectomie overwegen bij geselecteerde patiënten (genezing of significante verbetering in 35–60%).
        - Bilaterale PA → medicamenteuze therapie primair.

        Renovasculaire hypertensie:
        - Renale angioplastie (zonder stent) overwegen bij FMD met hemodynamisch significante nierslagadervernauwing (IIa).
        - Angioplastie ± stenting kan overwogen worden bij atherosclerotische hemodynamische stenose met specifieke klinische indicaties (IIb).
        """,
                ],
            },
            "Pericarditis/Pericardiale effusie dr. Ballet ultimate protocol": {
                "description": "Diagnostiek en behandeling van pericarditis en pericardiale effusie volgens dr. Ballet",
                "plan": [
                    """
        Pericarditis / Pericardiale effusie - dr. Ballet ultimate protocol
        Bij iedereen:
        - Labo met complete celtelling (CBC), nierfunctie, leverenzymen, ferritine, totaal eiwit, LDH, HIV, HCV, TSH, T4, CRP, CK, troponine)
        - RX thorax F/P of CT thorax (ter evaluatie longlijden, pleurale effusie, massas, bij CT ook pericardiale dikte, calcificaties, focale pericardiale effusie, compositie van pericardvocht obv. atenuatie/HU)
        - Transthoracale echocardiografie: evaluatie effusie (>20mm), tamponade of hemodynamische impact
        - Pericardiocentese of cardiale chirurgie zo tamponade, symptomatische matig of ernstige effusie niet responsief aan medische therapie of bij vermoeden onbekende bacteriële of neoplastische etiologie. (I)
        - Op indicatie ook labo met ANA, ANCA, ACE, IGRA test, HCV, HBV, HIV, serologie Coxiella burnetii, serologie Borrelia
        - Op indicatie 24 uur urinecollectie met urinair calcium

        Bij analyse pericardvocht:
        - Totaal eiwit (serum en vocht), LDH (serum en vocht), celtelling
        - Cytologie (groot volume vocht en snelle analyse verhoogt diagnostische opbrengst)
        - PCR voor TB
        - Mycobacteriële kweken, fungale kweken, aerobe en anaerobe kweken (in hemocultuur fles)
        - Overweeg PCR enterovirus, adenovirus, parvovirus B19, HHV-6, CMV, EBV
        - Overweeg CEA
        - Overweeg zuurvaste kleuring

        Bij klassieke pericarditis:
        - Aspegic 1000mg 3x/d gedurende 1-2 weken, duur in functie van symptomen en CRP daling. Verlaag dosis met 500mg elke 1-2 weken. (I)
        - Colchicine 0.5mg 1x/d (<70kg) of 0.5mg 2x/d (>70kg) gedurende 3 maanden. Halveer dosis bij invaliderende bijwerkingen (diarree). (I)
        - Corticosteroiden + Colchisine zo inadequate effect NSAID, NSAID niet gewenst of intolerantie, op voorwaarde dat infectieuze oorzaak uitgesloten is (IIb)
        - Zware inspanningen vermijden tot verdwijnen symptomen, normalisatie CRP, ECG en TTE. Bij atleten minstens 3 maanden restrictie van zware inspanning. (IIb)
        - IVIG of Anakinra of Azathioprine zijn derde lijn
        - Pericardectomie is vierde lijn
        - Behandeling gericht op onderliggende etiologie

        Bij klassieke pericarditis met gestegen hs-cTn-T (myopericarditis):
        - Coronarografie, indien geïndiceerd, om acuut coronair syndroom uit te sluiten (I)
        - MRI om myocardiale aantasting te bewijzen (I)
        - Hospitalisatie voor diagnose en monitoring (I)
        - Zware inspanningen vermijden gedurende minstens 6 maanden (I)
        - Anti-inflammatoire medicatie op laagst effectieve dosis (colchicine ± andere) voor thoracale pijncontrole (IIa)

        - Pericardiocentese of cardiale chirurgie zo tamponade, symptomatisch matig of ernstige effusie niet responsief aan medische therapie of bij vermoeden onbekende bacteriële of neoplastische etiologie. (I)
        - Bij vermoeden van constrictie: MRI en/of CT ter evaluatie van pericardiale verdikking (>3-4mm), pericardiale calcificaties, ventriculaire interafhankelijkheid
        - Bij transiënte constrictie (2-3 maanden) empirische anti-inflammatoire therapie
        - Bij effusieve-constrictieve pericarditis: pericardiocentese gevolgd door medische therapie
        - Bij chronische constrictie na 3-6 maanden: pericardiectomie en gerichte medische therapie
        """,
                ],
            },
                "Endocarditis": {
                    "description": "Beeldvorming en beleid bij endocarditis",
                    "plan": [
                        """
    Endocarditis

    Beeldvorming. 
    Graag afname van 3 sets hemoculturen (aeroob en anaeroob), ideaal via afzonderlijk venipuncties met tussenpozen van 30-60 minuten. 
    Typische pathogenen zijn orale streptococci, , Streptococcus gallolyticus, HACEK groep orofaryngeale commensalen (Haemophilus aphrophilus, Aggregatibacter actinomycetemcomitans, Cardiobacterium hominis, Eikenella corrodens, Kingella species), S. aureus, E. faecalis. Majeur criterium is een typische kiem uit 2 afzonderlijke hemocultuurflessen. 
    Zo cultuur negatief en suspect voor endocarditis evaluatie naar BCNIE (C. burnetii Bartonella spp. Aspergillus spp. L. pneumophila Brucella spp. M. pneumoniae). 
    Zo cultuur negatief kan ook 16S rRNA PCR getest worden, kost wel 150 euro aan de patiënt.
    Transthoracale echocardiografie is eerste lijn bij vermoeden van infectieuze endocarditis (I-B)
    Transoesofageale ehcocardiografie is aangeraden bij alle patiënten met klinisch vermoeden en non diagnostische TTE.  (I-B) Ook bij positieve TTE is TEE aangewezen voor complementaire evaluatie. 
    TEE is altijd aangewezen bij vermoeden van infectieuze endocarditis bij patiënten met kleprothese en CIED. (I-B)
    Bij CIED en possible endocarditis (1 major + 1 minor of 3 minor criteria) is naast herhaling van TTE en TEE ook een Full-body [18F]FDG-PET-CT(A) aangewezen voor evaluatie van pocket infectie of septische pulmonaire embolen (I) of om lead infectie (IIb). 
    Zo  blijvend hoog vermoeden zijn TTE en TEE te herhalen na 5-7 dagen zo blijvend hoge verdenking. (I-C)
    Een nieuwe TEE is te herhalen alvorens switch van intraveneuze antibiotica naar orale antibiotica (IB) 
    Een nieuwe TEE is nodig bij vermoeden van een nieuwe complicatie (nieuw geruis, embolisatie, persisterende koorts en bacteriëmie, nieuw hartfalen, conductieproblemen zoals AVB) (I-B)
    Cardiale CT angio is een optie ter detectie van valvulaire letsels om IE van natieve kleppen te bevestigen (I-B) Kan ook gebruikt worden om paravalvulaire of periprothetische complicaties als echocardiografie niet conclusief is (I-B)
    Full-body [18F]FDG-PET-CT(A) is aangewezen bij extracardiale symptomen ter identificatie van perifere letsels bij bewezen IE, of om diagnose te bevestigen zo echocardiografie niet conclusief (I-B)
    Full-body [18F]FDG-PET-CT(A) is aangewezen bij “possible” IE 
    MRI met en zonder gadolinium (of CT zo geen MRI beschikbaar) zo vermoeden van neurologische complicaties (I-B)
    MRI of PET/CT van rug of gewrichten, zo vermoeden van spondylodiscitis of vertrebrale osteomyelitis of septische arthritis. (I-C)
    TTE en TEE zijn aangewezen zo typische kiem aanwezig in hemoculturen bij septische arthritis of spondylodiscitis (I-C)
    Medische therapie: 
    Emprische therapie bij community-acquired NVE of late PVE (>12 maand na chirurgie) met Amoxicilline 2gr 6x/d IV, Flucloxaciline 2gr 6x/d IV en Gentamicine 3mg/kg 1x/d  IV. (IIa-C)
    Empirische therapie bij vroege PVE(<12 maanden na chirurgie) of nosocomiale of non-nocosomiale gezondheidzorg geassocieerde IE dan start vancomycine 30mg/kg/dag IV in 2 dosissen of bij voorkeur continue infusie in combinatie met Gentamicine 3mg/kg/dag IV of Ceftriaxone 2gr 2x/d IV. (IIb-C)
    Nadien gericht aan pathogeen. Duur is afhankelijk van pathogeen en complicaties. 
    Bij NVE is 4 weken therapie gewoonlijk voldoende (I-B) en soms maar 2 weken zo ongecompliceerde NVE. (I-B) 
    Bij PVE is 6 weken therapie noodzakelijk. (I-B)

    Chirurgie
    Emergente heelkunde (binnen 24u) is vereist bij refractair longoedeem of cardiogene shock (I-B)
    Urgente heelkunde (binnen 3-5 dagen)  is vereist bij ernstige acute regurgitatie of obstructie met symptomen van hartfalen of hemodynamische intolerantie (I-B)
    Urgente heelkunde (binnen 3-5 dagen)  is vereist bij vegetaties >10mm met reeds 1 of meer embolische episodes ondanks adequate therapie (I-B) of andere indicatie voor heelkunde (I-C). 
    Urgente heelkunde (binnen 3-5 dagen)  kan overwogen worden bij vegetaties >10mm zonder ernstige klepdysfunctie en zonder embolische episodes bij laag chirurgisch risico (IIb-B)
    Urgente heelkunde (binnen 3-5 dagen)  bij ongecontroleerde infectie (abces, aneurysma, fistel, groei vegetatie, dehiscentie, nieuw AVB) (I-B) bij persisterend positieve HC na 1 week van adequate antibiotica therapie en adequate controle van metastatische foci (IIa-B) of bij PVE door S. Aureus of non-HACEK gram negatieve bacteriën. (IIa-C)
    Coronarografie is aangewezen preoperatief bij hoog risico op coronairlijden (I-C) of via CCTA zo aortaklepvegetaties (I-B)
    Chirurgie is aangewezen voor vroege PVE (<6 maanden na klepchirurgie) met nieuwe klepvervanging en volledig debridement (I-C)
    Volledige extractie van CIED zonder vertraging is aangewezen bij bewezen CIED endocarditis onder empirische therapie (I-B) Herimplantatie kan best op een andere plaats gebeuren en zo lang mogelijk wachten na extractie, zo symptomen en tekens van infectie verdwenen zijn en reeds >72u negatieve hemoculturen zo geen vegetaties of reeds >=2 weken zo vegetaties aanwezig (I-C).
    Volledige extractie van CIED moet overwogen worden bij valvulaire IE, zelfs zo geen definitieve aantasting van CIED. (IIa)

    Ambulante therapie
    Outpatient parenteral (OPAT) of orale antibiotica kan overwogen worden bij linkszijdgide IE door Streptococcus spp., E. faecalis, S. aureus, or CoNS na een adequate IV antibiotica behandeling van minstens 10 dagen (of 7 dagen na chirurgie) zo klinisch stabiel, geen tekens van abcedatie en geen klepafwijkingen met indicatie voor heelkunde op TEE. (IIa-A)
    Profylaxe 
    Antibiotica profylaxe met Amoxicilline 2gr oraal (of 50 mg/kg oraal bij kinderen) of bij penicilline allergie met Cephalexin 2gr is aangewezen bij orale chirurgie of manipulatie van gingivale of periapicale regio van de tanden en :
    Elke patiënt met chirurgisch geïmplanteerde hartklep of met enige vorm van chirurgisch materiaal gebruikt voor klepherstel. (I-C)
    Na transcatheter implantatie van aortaklep (TAVI) of pulmonalisklep (I-C)
    Na transcatheter herstel van mitralis of tricuspidalisklep (IIa-C) 
    Na harttransplantatie (IIb-C)
    Bij onbehandelde cyanotische CHD en patiënten behandeld met palliatieve shunts, conduits of andere protheses. Na correctie is profylaxe enkel nodig gedurende eerste 6 maanden na procedure (IC)
    Bij invasieve procedure van respiratoir, gastro-intestinaal, genituournair of musculoskeletaal systeem kan profylaxe overwogen worden bij hoor risico patiënten. (IIb-C)
    """,
                    ],
                },
                    "Atherosclerose en lipiden": {
                    "description": "Volledig lipidenprofiel en atherosclerose management",
                    "plan": [
                        """
    Atherosclerose en lipiden

    Volledig lipiden profiel met Totaal cholesterol, HDL, LDL, Apolipoproteïne A1, Apolipoproteïne B, Lipoproteïne (a). 
    We plannen 24 uur bloeddrukmeting. 
    Nuchtere bloedname met nuchtere glycemie en HbA1C. 

    Referentiewaarden: 
    High -  LDL-C 2.6 mmol/L (100 mg/dL)  Non-HDL-C 3.4 mmol/L (131 mg/dL) Apo B 100 mg/dL
    Moderate - LDL-C 1.8 mmol/L (70 mg/dL) Non-HDL-C 2.6 mmol/L (100 mg/dL) Apo B 80 mg/dL
    Low LDL-C 1.4 mmol/L (55 mg/dL) Non-HDL-C 2.2 mmol/L (85 mg/dL) Apo B 65 mg/dL

    Apolipoproteïne A1 correleert met HDL normaalwaarde 75-160 mg/dL. Hoe hoger hoe beter. 
    Lipoproteïne (a) atherogeen en thrombogeen, ideaal < 10 nmol/L, minor 30-90 mmol/L, moderate 90-200mmol/L, high 200-400 mmol/L, very high >400 mmol/L. 

    Suvezen (Rosuvastatine/Ezetemibe) 20mg/10mg 1x/d om 20u – 's avonds – voorkeur. Controle lever enzymen (ALT) enkel zo klinische indicatie (vermoeden hepatotoxiciteit) na 8 weken en is enkel significant zo >3x ULN.  CK bepaling niet noodzakelijk tenzij bij myalgie, spierzwakte of gekende spieraandoening. 
    Controle van LDL-C na 3 maanden. 
    Rosuvastatine heeft krachtigere anti-inflammatoire en endotheel stabiliserende effecten dan atorvastatine. Bovendien langere halfwaardetijd en minder drug interacties omdat het minder afhankelijk is van levermetabolisme (CYP2C9). 
    Cardiovasculaire preventie (ESC 2024)
    • Algemene adviezen in kader van cardiovasculair risicomanagement ESC 2023: 
     - Arteriële hypertensie: Richtwaarde systolische bloeddruk 120-129 mmHg.
     - Dyslipidemie: LDL-cholesterol < 55 mg/dl of <40mg/dl (bij 2 of meer CV events) en triglyceriden < 150 mg/dl. Target Apo B <65 mg/dL
     - Diabetes: HbA1c < 7% via levensstijlaanpassing en medicatie met bewezen cardiovasculair voordeel. 
    • Levensstijl: 
     - Lichaamsgewicht: BMI < 25 kg/m² via dieetmaatregelen, lichaamsbeweging en zo nodig advies diëtist.
    - Lichaamsbeweging: Aerobe beweging 150 minuten per week, in combinatie met krachttraining.
     - Gezond dieet rijk aan groenten, fruit, volwaardige granen, onverzadigde vetten en magere eiwitten. 
     - Beperken van verzadigde vetten en alcohol <100 gram per week. 
     - Nicotine: Voor rokers advies tot onmiddellijke en volledige rookstop.

    - Risicocalculatie kan het beste via SCORE2 in gezonde patiënten zonder diabetes. 
    - Bij laag risicopatiënten (Bij <50 jaar <2.5%, Bij 50-70 <5%) moet LDL-C target van <100mg/dl overwogen worden (IIa) 
    - Bij hoog risicopatiënten (Bij <50 jaar 2.5-7.5%, Bij 50-70 jaar 5-10%) <70 jaar moet LDL-C target van 70 mg/dL overwogen worden (IIa)
    - Bij zeer hoog risicopatiënten (Bij <50 jaar>7.5%, Bij 50-70 jaar >10%) moet LDL-C target van 55 mg/dL overwogen worden. (IIa)  

    Familiale hypercholesterolemie
    DLCN score = _▼
     Familiale voorbeschikking:
     1 - Eerste graads verwant met vroegtijdig ASCVD  (< 60 jaar vrouw, < 55 jaar man)
     1 - Eerste graads verwant met LDL-c > 95ste percentiel voor leeftijd en geslacht
     2 - Eerste graads verwant met peesxanthoma en/of arcus cornealis
     2 - Kinderen < 18 jaar met LDL-c > 95ste percentiel voor leeftijd en geslacht (> 135 mg/dL vrouwelijk, > 130mg/dL mannelijk)

     Persoonlijke voorgeschiedenis:
     1 - Premature CVA/TIA of PAD (< 60 jaar vrouw, < 55 jaar man)
     2 - Premature ASCVD (< 60 jaar vrouw, < 55 jaar man)
     4 - Arcus cornealis < 45 jaar
     6 - Peesxanthomen

     LDL-c niveau zonder therapie:
     1 - > 155 mg/dL
     3 - > 190 mg/dL
     5 - > 250 mg/dL
     8 - > 330 mg/dL

     Genetica
     8- DNA mutatie in LDLR, ApoB of PCSK9

    Definite FH >8
     Probable FH 6-8
     Possible FH 3-5
     Unlikely FH <3 

    Uw patiënt van [Leeftijd] bood zich aan op de multidisciplinaire lipiden raadpleging voor het bespreken van het resultaat van het genetisch onderzoek, uitgevoerd in kader van vermoeden van familiale hypercholesterolemie (FH).
     Bij patiente werd een heterozygote mutatie in het _▼gen vastgesteld, wat de klinische diagnose moleculair bevestigt.
     Patienten met een heterozygote FH (heFH) behoren door de langdurige blootstelling tot een hoog risico categorie voor de behandeling van het LDL cholesterol.
     Gezien onvoldoende controle van het LDL cholesterol, wordt ... aan de behandeling geassocieerd.
     Personen met HeFH hebben recht op een terugbetaling van lipidenverlagers statines en ezetimibe in Categorie A. Een aanvraag werd meegegeven.
     Controle lipiden parameters over 3 maanden.
    Bijkomende acties:
    Jaarlijkse opvolging door de behandelende cardioloog wordt aanbevolen met echocardiografie inclusief aorta en ischemische testing (cyclo-ergometrie of andere stresstest). Bij nog geen gekend coronarialijden CT coronairen.
     We adviseren ook screening van perifeer arterieel lijden door middel van duplex halsvaten en duplex van de onderste ledematen.


    *Screening naar subklinische atherosclerose tekens middels coronaire calciumscore, echocardio, ECG  en duplex halsvaten.

    Behandeldoel  voor personen met HeFH:
     In primair preventie en afwezigheid van overige risicofactoren: LDL cholesterol < 70 mg/dl EN minimale daling van het LDL cholesterol tov uitgangswaarden met minimaal 50 % (EAS/ESC guidelines 2021)
     In aanwezigheid van andere risicofactoren en/of cardiovasculaire antecedenten dient een LDL <55 mg/dl nagestreefd te worden.
    Behandeling wordt gestart vanaf 8-10 jarige leeftijd met laag tot intermediair statine (streefdoel LDL <135mg/dL), vanaf 18 jarige leeftijd titratie tot volwassen streefwaarden (LDL <70mg/dL).

    Bijkomende aandachtspunten:
     Bij vrouwen dienen statines gestopt te worden bij zwangerschapswens.   


    Familie
     Volgens de richtlijnen dienen alle eerste rangsverwanten van personen met een diagnose van he FH opgespoord te wordenin kader van cascadescreening.
     FH wordt op een autosomaal dominante wijze overgeërfd. Elk kind heeft dus 50 % kans op overerving van de pathogene mutatie.
    Hierbij zoeken we naar het fenotype van de aandoening, zijnde sterk verhoogde cholesterolwaarden voor de leeftijd en geslacht.
 
    De leeftijdsspecifieke BEL-MEDPED criteria voor de screening van eerste graads familieleden zijn de volgende:
    < 14 jaar - man 124 mg/dL - vrouw 135 mg/dL
    15-24 jaar - man 121 mg/dL - vrouw 133 mg/dL
    25-34 jaar - man 150 mg/dL - vrouw 143 mg/dL
    35-44 jaar - man 158 mg/dL - vrouw 148 mg/dL
    45-54 jaar - man 171 mg/dL - vrouw 161 mg/dL55-64 jaar - man 169 mg/dL - vrouw 173 mg/dL

    Zo een eerste graadsverwant een LDL-c hoger dan de vermelde cut-offs heeft, is aanvullend genetisch onderzoek ter bevestiging van het genotype noodzakelijk.
  
    Inclisiran is een short interfering RNA molecule dat de translatie van het RNA dat codeert voor PCSK9 verhindert. De aanmaak van PCSK9 wordt zo geblokkeerd waardoor de afbraak van LDL-R verhindert wordt. DIt zal zorgen voor een additionele 50% reductie van het LDL-c. Het eerste jaar moet het spuitje 3x geplaatst worden (bij opstart, na 3m en na 6m). Vanaf dan om de 6 maanden. Buiten lokale reacties thv de injectieplaats zijn er geen nevenwerkingen gekend. Na 48u is inclisiran niet meer detecteerbaar in het bloed (selectieve opname door de levercellen).
     De toediening moet gebeuren door een arts of verpleegkundige. 
    """,
                    ],
                },
                "Contrast allergie": {
                    "description": "Beleid bij vermoeden van contrastallergie",
                    "plan": [
                        """
    Contrast allergie
    Bij vermoeden contrast allergie. Meest gebruikte middelen zijn Iomeron (Iomeprol), Iodixanol (Visipaque) en Iohexol (Omnipaque).  
    Zo niet urgent eerst immunologisch uitwerken.
    Zo urgent (<24u) bespreken met immunoloog. 
    Zo urgent (onmiddellijk) gok Xenetix (= iobitridol) en premedicatie met Cetirizine 10mg en Solu-medrol 40mg IV. 
    Bij reactie: 
    - Adrenaline (1ml/ml) IM (intramusculair) 0.5mg (dosis 0.1 mg/kg) in de anterolaterale dij (m. vastus lateralis).
    - Bij hypotensie geef IV vocht: Bolus 500 ml plasmalyte.
    - Solu-Cortef (Hydrocortisone) IV 200mg 
    - Cetirizine 10 mg PO.
    - Bij bronchospasmen geef Duovent  (Ipratropium/Feneterol) aerosols. 
    - Bepaal tryptase 1 uur na ontstaan van klachten. (Bij voorkeur tussen 30 min - 120 min).
    - Bepaal tryptase > 24 na ontstaan van klachten. 
    - Significante zo piek tryptase > 1.2 keer baseline + 2 ng/ml. 
    - Het risico op bifasische reactie is klein, monitoring is te voorzien en alarmsymptomen zijn toe te lichten.
    """,
                    ],
                },
        }
