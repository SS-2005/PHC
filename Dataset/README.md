# Guideline-grounded synthetic triage datasets

This package contains three **synthetic, class-balanced datasets** for prototyping triage/disposition models:

- `adult.csv`
- `child.csv`
- `maternal.csv`

Each dataset has **8,000 rows** with **2,000 rows per clinical disposition class**:

- Treat locally
- Treat + monitor
- Stabilize + refer
- Emergency referral

Each row is **synthetic**. It is **not real patient data** and must **not** be treated as a clinically validated production dataset.  
It is designed for:

- hackathon / prototype model development
- feature engineering
- baseline classification experiments
- UI / workflow testing
- explainable ML demos

It is **not suitable for clinical deployment** without real-world validation, bias testing, calibration studies, clinician review, and governance.

## Grounding approach

The feature set and label logic were grounded in publicly available clinical and dataset references:

### Adult grounding
- NEWS2-style adult deterioration variables and thresholds: respiration rate, oxygen saturation, systolic BP, pulse, consciousness, temperature
- Open critical care datasets showing these variables are routinely captured:
  - MIMIC-III / MIMIC-IV
- The adult label logic is therefore **deterioration-oriented**, not diagnosis-oriented.

### Child grounding
- WHO IMCI / IMNCI danger-sign logic:
  - unable to drink / breastfeed
  - vomiting everything
  - convulsions
  - lethargic or unconscious
  - chest indrawing
  - age-specific fast breathing thresholds
  - dehydration signs
  - oxygen saturation if available
- Open pediatric critical-care dataset:
  - PIC (Paediatric Intensive Care database)

### Maternal / pregnant grounding
- WHO pregnancy danger signs and rapid-assessment principles:
  - vaginal bleeding
  - convulsions
  - severe abdominal pain
  - dangerous fever
  - hypertension / pre-eclampsia signals
  - reduced fetal movement
  - anaemia and edema as risk context

## Important assumption used in labels

Because the requested feature set does **not** include a hospital-capability column, the output labels were generated under a **baseline primary-care / PHC-like capability assumption**:

The local facility is assumed to have:
- basic vitals assessment
- oral medicines
- ORS
- IV fluids
- oxygen and first-line stabilization
- basic antibiotics / antipyretics
- referral transport or referral pathway

The local facility is assumed **not** to have:
- ICU-level monitoring
- blood products
- advanced imaging
- specialist surgery
- full obstetric emergency theatre capability

So the labels mean:

- **Treat locally**: safe to manage at baseline primary-care level
- **Treat + monitor**: likely manageable locally but requires observation / reassessment
- **Stabilize + refer**: needs first-line stabilization locally, then referral
- **Emergency referral**: urgent transfer after immediate life-saving steps

## Output columns

### `clinical_disposition`
Target class for the 4-class model.

Values:
- `Treat locally`
- `Treat + monitor`
- `Stabilize + refer`
- `Emergency referral`

### `severity_score`
Auxiliary label.

Values:
- `Low`
- `Medium`
- `High`

This is **not** the same as the disposition class.
Example:
- a maternal case with mild hypertension can be `Treat + monitor` and `Medium`
- a child with severe dehydration may be `Stabilize + refer` and `High`

## Sanity-check modelability

A quick baseline random-forest sanity check on an 80/20 split showed that the synthetic signal is learnable:

| Dataset | Baseline accuracy | Baseline macro F1 |
|---|---:|---:|
| Adult | 0.940 | 0.940 |
| Child | 0.986 | 0.986 |
| Maternal | 0.968 | 0.968 |

These numbers only show that the synthetic label rules are internally learnable. They are **not clinical performance claims**.

---

# 1) ADULT DATASET

File: `adult.csv`  
Rows: 8000  
Disposition balance: {'Treat + monitor': 2000, 'Treat locally': 2000, 'Stabilize + refer': 2000, 'Emergency referral': 2000}  
Severity balance: {'High': 3319, 'Medium': 2423, 'Low': 2258}

## Adult column dictionary

| Column | Type | Allowed / observed range | What low values suggest | What high values suggest | Notes |
|---|---|---|---|---|---|
| `age_years` | integer | 18 to 95 | younger adult risk context | older age adds vulnerability / comorbidity burden | 18+ only |
| `sex` | categorical | Male / Female | not severity itself | not severity itself | included for heterogeneity |
| `heart_rate_bpm` | numeric | 47.7 to 185.0 | bradycardia / possible shock if very low | tachycardia, fever, sepsis, pain, shock compensation | adult deterioration feature |
| `respiratory_rate_bpm` | numeric | 10.0 to 44.0 | depressed respiration if very low | respiratory distress / metabolic compensation if high | NEWS2-style feature |
| `systolic_bp_mmHg` | numeric | 60.0 to 245.0 | shock / hypoperfusion if low | hypertensive emergency context if very high | systolic only by design |
| `spo2_percent` | numeric | 72.0 to 100.0 | hypoxaemia / respiratory compromise | normal oxygenation | severe cases cluster at low SpO₂ |
| `temperature_c` | numeric | 34.2 to 41.2 | hypothermia if very low | fever / systemic infection if high | |
| `level_of_consciousness` | categorical | Alert / Voice / Pain / Unresponsive | altered consciousness if below Alert | severe neurologic or shock concern | AVPU-style simplification |
| `chief_complaint_category` | categorical | Respiratory, Fever/Infection, Chest pain, Abdominal pain, Gastrointestinal, Trauma, Neurologic, Urinary, Hypertensive symptoms, General weakness | lower-risk complaint categories are not automatically safe | high-risk complaints are escalated when vitals are abnormal | complaint is not the target label |
| `duration_days` | integer | 0 to 14 | very short can reflect acute onset | longer duration may indicate unresolved illness / deterioration risk in some complaints | |
| `comorbidity_count` | integer | 0 to 6 | fewer chronic illnesses | more background risk / frailty | count only, not disease names |
| `pain_distress_score_0_10` | integer | 0 to 10 | mild discomfort | severe pain / distress, especially important in chest pain, abdominal pain, trauma | subjective severity proxy |
| `clinical_disposition` | categorical | 4 classes | lower acuity | higher acuity / referral need | target label |
| `severity_score` | categorical | Low / Medium / High | lower physiologic instability | higher instability / danger signs | auxiliary label |

## Adult label logic summary

Adult labels were generated from a **NEWS2-like vital-sign logic** plus complaint-risk adjustment.

Main adult escalation patterns:
- low SpO₂
- low systolic BP
- very high or very low respiratory rate
- altered consciousness
- chest pain / neurologic complaints with unstable vitals
- respiratory complaints with hypoxia
- hypertensive-symptom cases with markedly elevated BP

---

# 2) CHILD DATASET

File: `child.csv`  
Rows: 8000  
Disposition balance: {'Treat + monitor': 2000, 'Treat locally': 2000, 'Stabilize + refer': 2000, 'Emergency referral': 2000}  
Severity balance: {'Low': 3150, 'High': 2935, 'Medium': 1915}

## Child column dictionary

| Column | Type | Allowed / observed range | What low values suggest | What high values suggest | Notes |
|---|---|---|---|---|---|
| `age_months` | integer | 2 to 59 | very young infants have higher vulnerability | older under-5 child | dataset limited to 2–59 months |
| `weight_kg` | numeric | 3.0 to 21.8 | underweight / malnutrition risk when low for age | older / larger child | correlated with age and malnutrition |
| `fever_present` | categorical | Yes / No | no fever syndrome | infection / inflammation context | |
| `fever_duration_days` | integer | 0 to 11 | acute or no fever | persistent fever raises risk | used with fever flag |
| `respiratory_rate_bpm` | numeric | 21.3 to 85.0 | normal or low respiratory effort | fast breathing / respiratory distress | interpreted age-specifically |
| `chest_indrawing` | categorical | Yes / No | absent severe chest sign | present severe respiratory sign | major escalation feature |
| `ability_to_drink_feed` | categorical | Normal / Reduced / Unable | normal intake | inability to drink is a WHO danger sign | key pediatric danger sign |
| `vomiting_everything` | categorical | Yes / No | absent danger sign | present danger sign | WHO IMCI signal |
| `convulsions` | categorical | Yes / No | absent danger sign | present emergency danger sign | WHO IMCI signal |
| `lethargic_or_unconscious` | categorical | Yes / No | child alert | severe neurologic / systemic illness | WHO IMCI signal |
| `diarrhea_duration_days` | integer | 0 to 16 | no / short diarrheal illness | dehydration / persistent diarrhea risk | |
| `dehydration_signs` | categorical | None / Some / Severe | no visible dehydration | severe dehydration and urgent fluid needs | IMCI-style compression of dehydration findings |
| `spo2_percent` | numeric | 74.0 to 100.0 | hypoxaemia when low | normal oxygenation | if available in real deployment |
| `malnutrition_indicator` | categorical | None / Moderate / Severe | no nutrition red flag | severe acute malnutrition risk context | simplified nutrition risk label |
| `clinical_disposition` | categorical | 4 classes | lower acuity | higher acuity / referral need | target label |
| `severity_score` | categorical | Low / Medium / High | lower danger-sign burden | higher danger-sign burden | auxiliary label |

## Child label logic summary

Child labels were generated from **WHO IMCI-style danger signs and referral logic**.

Main child escalation patterns:
- unable to drink / feed
- vomiting everything
- convulsions
- lethargy / unconsciousness
- chest indrawing
- age-specific fast breathing
- severe dehydration
- severe malnutrition
- low oxygen saturation

Age-specific fast-breathing logic used in the synthetic rules:
- 2 months up to 12 months: fast breathing at **50 breaths/min or more**
- 12 months up to 5 years: fast breathing at **40 breaths/min or more**

---

# 3) MATERNAL / PREGNANT DATASET

File: `maternal.csv`  
Rows: 8000  
Disposition balance: {'Treat + monitor': 2000, 'Treat locally': 2000, 'Stabilize + refer': 2000, 'Emergency referral': 2000}  
Severity balance: {'Low': 3412, 'High': 2336, 'Medium': 2252}

## Maternal column dictionary

| Column | Type | Allowed / observed range | What low values suggest | What high values suggest | Notes |
|---|---|---|---|---|---|
| `age_years` | integer | 15 to 45 | younger pregnant patient | older maternal age risk context | |
| `gestational_age_weeks` | integer | 4 to 41 | early pregnancy | later gestation, fetal movement more relevant | 4–41 weeks in this synthetic set |
| `systolic_bp_mmHg` | numeric | 60.0 to 234.5 | hypotension / bleeding / shock if low | hypertensive disorder / severe pre-eclampsia concern if high | systolic used for model simplicity |
| `heart_rate_bpm` | numeric | 58.0 to 175.0 | relative bradycardia if unusually low | tachycardia from pain, fever, bleeding, shock | |
| `vaginal_bleeding` | categorical | Yes / No | absent major obstetric bleed signal | present danger sign requiring escalation | major referral feature |
| `severe_headache_or_vision_issues` | categorical | Yes / No | absent pre-eclampsia symptom | possible hypertensive disorder / severe pre-eclampsia symptom | more important after 20 weeks |
| `abdominal_pain_severity_0_10` | integer | 0 to 10 | mild discomfort | severe pain, possible obstetric emergency when high | |
| `fetal_movement` | categorical | Normal / Reduced | normal fetal activity | reduced movement is concerning, especially later pregnancy | simplified to 2 values |
| `fever_present` | categorical | Yes / No | no infectious signal | infection / sepsis context | |
| `seizures` | categorical | Yes / No | absent eclampsia-like emergency sign | emergency danger sign | |
| `previous_complications` | categorical | Yes / No | lower background risk | prior obstetric risk history | context feature |
| `hemoglobin_g_dL` | numeric | 4.5 to 14.6 | severe anaemia when very low | better oxygen-carrying reserve | |
| `edema` | categorical | None / Mild / Generalized | none | generalized swelling raises pre-eclampsia concern | supportive, not stand-alone |
| `duration_days` | integer | 0 to 9 | acute onset | persistent symptom burden | |
| `clinical_disposition` | categorical | 4 classes | lower acuity | higher acuity / referral need | target label |
| `severity_score` | categorical | Low / Medium / High | lower maternal danger-sign burden | higher danger-sign burden | auxiliary label |

## Maternal label logic summary

Maternal labels were generated from **WHO pregnancy danger-sign concepts** and a simplified pre-eclampsia / hemorrhage risk logic.

Main maternal escalation patterns:
- vaginal bleeding
- seizures
- severe abdominal pain
- dangerous fever with tachycardia
- reduced fetal movement in later pregnancy
- systolic hypertension, especially severe elevation
- headache / visual symptoms with elevated BP
- low hemoglobin suggesting severe anaemia

Rule-of-thumb BP anchors used in the synthetic logic:
- systolic BP **>= 140 mmHg** contributes to monitoring / referral concern
- systolic BP **>= 160 mmHg** strongly escalates referral need
- very high BP combined with headache / visual symptoms can become emergency referral

---

# Suggested modeling workflow

## A. Target to predict first
Use `clinical_disposition` as the **main target label**.

That is the most useful operational target because it answers:
- can this patient be managed locally?
- do they need monitoring?
- do they need stabilization then referral?
- do they need urgent referral?

## B. Secondary target
Use `severity_score` as:
- an auxiliary target
- a calibration / consistency target
- a multi-task learning option if you want to experiment

## C. Recommended model baseline
For a strong first baseline:
- one-hot encode categorical columns
- use CatBoost / LightGBM / XGBoost if available
- or a tuned RandomForest / HistGradientBoosting baseline
- evaluate with:
  - macro F1
  - per-class recall
  - confusion matrix
  - calibration plots
  - subgroup checks

## D. Important caveat
Because these datasets are synthetic:
- very high validation scores are possible
- that does **not** mean the model is clinically valid
- real-world generalization will depend on real data collection and clinician-reviewed labels

---

# Raw source URLs used for grounding

Adult / datasets / triage:
- https://physionet.org/content/mimiciii/1.4/
- https://physionet.org/content/mimiciv/
- https://www.rcp.ac.uk/resources/national-early-warning-score-news-2/
- https://www.rcp.ac.uk/media/alxev00t/news2-chart-1_the-news-scoring-system_0_0.pdf

Child / datasets / triage:
- https://physionet.org/content/picdb/1.1.0/
- https://cdn.who.int/media/docs/default-source/mca-documents/child/imci-integrated-management-of-childhood-illness/imci-in-service-training/imci-chart-booklet.pdf?sfvrsn=f63af425_1

Maternal / triage:
- https://www.who.int/news-room/fact-sheets/detail/pre-eclampsia
- https://www.afro.who.int/sites/default/files/2017-06/mps%20pcpnc.pdf
- https://platform.who.int/docs/default-source/mca-documents/policy-documents/guideline/TTO-CC-31-04-GUIDELINE-2018-eng-MOH-Hypertension-in-Pregnancy-Clinical-Guideline-2018.pdf

Primary-care capability context:
- https://aam.mohfw.gov.in/home/aboutus
- https://www.who.int/india/health-topics/primary-health-care
- https://nhsrcindia.org/practice-areas/cpc-phc/comprehensive-primary-health-care

---

# Final warning

These files are **good prototype datasets**, not a substitute for:
- real case records
- clinician adjudication
- hospital-capability data
- site-specific calibration
- fairness / safety review
- prospective validation
