---
name: doctor-blood-tests
title: "Blood Test Results: Reference Ranges and Patterns"
description: "Explains blood test results (CBC, metabolic, lipid, thyroid): flags out-of-range values, shows patterns across markers, lists critical values."
license: Apache-2.0
compatibility: "Requires: the medical-reference tools or web search for current reference ranges. US units shown; conversions to SI included."
domains: doctor
rules:
  - match((?i)\b(blood (tests?|work|panel|results?|count)|lab (results?|reports?|values?|panel)|reference ranges?|out[- ]of[- ]range)\b)
  - match((?i)\b(cbc|complete blood count|hemoglobin|hgb|hematocrit|ferritin|tibc|transferrin|hba1c|a1c|ldl|hdl|triglycerides?|creatinine|egfr|tsh|free t[34]|platelets?|wbc|alt|alp|bilirubin|b12|folate|glucose|rdw|mcv)\b.{0,80}\b(high|low|normal|mean|means|range|result|results|elevated|measure\w*|markers?|flag\w*|interact\w*|disagree|calculated|reliable)\b)
  - match((?i)\b(high|low|elevated)\b.{0,30}\b(cholesterol|ldl|tsh|ferritin|hemoglobin|creatinine|platelets?|wbc)\b)
  - match((?i)\b(cholesterol|thyroid|lipid|metabolic|kidney|liver|iron|vitamin|electrolyte)\s+(panel|tests?|results?|function|markers?|studies|enzymes?)\b)
  - match((?i)\b(flag\w*|interpret\w*)\b.{0,40}\b(values?|markers?|results?|panel)\b)
  - semantic(explain my blood test results and which values are out of range)
  - semantic(what does a high white blood cell count mean on my lab report)
  - semantic(my thyroid and glucose numbers came back, are they normal)
---

## Overview

A person shares laboratory results or asks what a blood marker means. The outcome is an explanation of each marker with its range and caveats, the out-of-range values, the patterns across markers, and specific questions for the doctor. This is educational interpretation, not a clinical one: results need a clinician's correlation before any health decision.

## Mental model

Reference ranges describe populations, and an individual sits somewhere inside or outside them for reasons that are often not disease. A value is a clue: it points to several possibilities, and a pattern across markers narrows them. Context (age, sex, medications, conditions, how the sample was taken) changes what a number means.

## Rules

Interpretation principles:
- Reference ranges describe populations; individual variation is real, and "normal" isn't always "optimal."
- Trends over time beat a single value; direction of change matters more than one result.
- Context is everything: age, sex, medications, and conditions all shift results.
- Abnormal values don't always mean disease; tests have false positives and negatives.
- Pre-analytical factors (fasting, time of day, hydration) affect results; account for them.
- Phrase implications as "this might indicate...", never "you have...". Never decide what is "normal" for a specific person or recommend treatment.

Workflow:
1. Flag out-of-range values: identify the high and low results.
2. Check for patterns: related abnormalities across markers (for example MCV with MCHC points to the anemia type).
3. Explain each test: what it measures, why it was ordered, the typical range with caveats.
4. Describe implications: what high or low might indicate, as several possibilities, not a verdict.
5. Note context: the pre-analytical and physiological factors that affect the result.
6. Close with specific questions for the doctor and any follow-up tests worth discussing.

### Complete blood count (CBC)

| Component | What it measures | Typical range* | Clinical significance |
|-----------|-----------------|----------------|----------------------|
| WBC | White blood cells (immune) | 4,500-11,000/µL | Infection, inflammation, immune disorders |
| RBC | Red blood cells (oxygen) | 4.5-5.9 million/µL | Anemia, polycythemia |
| Hemoglobin | Oxygen-carrying protein | 13.5-17.5 g/dL (M), 12-15.5 g/dL (F) | Anemia screening |
| Hematocrit | % blood volume as RBCs | 38.8-50% (M), 34.9-44.5% (F) | Anemia, dehydration |
| MCV | Average RBC size | 80-100 fL | Anemia classification |
| MCHC | RBC hemoglobin concentration | 32-36 g/dL | Iron deficiency, thalassemia |
| Platelets | Clotting cells | 150,000-450,000/µL | Bleeding/clotting disorders |

*Ranges vary by lab: always check the report. US units shown; for SI reports: glucose mg/dL ÷ 18 = mmol/L, cholesterol ÷ 38.67, triglycerides ÷ 88.57, creatinine mg/dL × 88.4 = µmol/L.

### Metabolic panel (CMP/BMP)

| Test | What it measures | Typical range* | Clinical significance |
|------|------------------|----------------|----------------------|
| Glucose | Blood sugar | 70-99 mg/dL (fasting) | 100-125 prediabetes, ≥ 126 diabetes range (ADA Standards of Care 2026; diagnosis needs confirmation) |
| HbA1c | ~3-month average glucose | < 5.7% | 5.7-6.4% prediabetes, ≥ 6.5% diabetes range; anemia, hemoglobin variants, and recent transfusion distort it |
| BUN | Kidney function | 7-20 mg/dL | Kidney function, hydration |
| Creatinine | Kidney function | 0.7-1.3 mg/dL | Kidney function, muscle mass |
| eGFR | Filtration estimate (CKD-EPI 2021, race-free) | ≥ 60 mL/min/1.73m² | CKD = eGFR < 60 or urine albumin-creatinine ratio ≥ 30 mg/g for ≥ 3 months (KDIGO 2024); cystatin C refines it |
| Sodium | Electrolyte | 135-145 mEq/L | Hydration, adrenal function |
| Potassium | Electrolyte | 3.5-5.0 mEq/L | Cardiac, muscle function |
| Calcium | Bone/metabolic | 8.5-10.5 mg/dL | Parathyroid, bone, kidney |
| ALT | Liver enzyme | 7-56 U/L (many labs) | Liver damage; ACG 2017 puts healthy upper limits lower: 29-33 U/L men, 19-25 U/L women |
| AST | Liver enzyme | 10-40 U/L | Liver, heart, muscle damage |

### Lipid panel (2026 ACC/AHA dyslipidemia guideline)

| Test | What it measures | Goal / threshold | Clinical significance |
|------|------------------|------------------|----------------------|
| LDL-C | Main atherogenic cholesterol | Goal set by risk: < 100 (borderline/intermediate), < 70 (high, PREVENT 10-yr ≥ 10%), < 55 mg/dL (very-high-risk ASCVD) | Atherosclerosis risk; no single "normal" |
| Non-HDL-C | Total minus HDL | Co-target, ~30 mg/dL above the LDL goal | Captures triglyceride-rich particles |
| HDL | High-density lipoprotein | Risk marker only | Not a treatment target |
| Triglycerides | Fat in blood | < 150 fasting; nonfasting ≥ 175 is a risk enhancer | ≥ 500 raises pancreatitis risk |
| Lp(a) | Inherited atherogenic particle | Measure once in adulthood; ≥ 125 nmol/L (≥ 50 mg/dL) is elevated | Genetic, barely moved by lifestyle; nmol/L and mg/dL don't convert reliably |
| ApoB | Count of atherogenic particles | Selective: residual risk once LDL/non-HDL goals are met | Useful with diabetes, high TG, cardiometabolic disease |

Risk tier comes from the PREVENT calculator (ages 30-79), not the old Pooled Cohort Equations; the goal is the clinician's call, not the lab's flag.

### Thyroid panel

| Test | What it measures | Typical range* | Clinical significance |
|------|------------------|----------------|----------------------|
| TSH | Thyroid-stimulating hormone | 0.4-4.0 mIU/L | Thyroid regulation |
| Free T4 | Thyroxine | 0.8-1.8 ng/dL | Thyroid function |
| Free T3 | Triiodothyronine | 2.3-4.2 pg/mL | Thyroid function |

### Anemia classification (MCV-based)

| MCV | Type | Common causes |
|-----|------|---------------|
| Low (< 80 fL) | Microcytic | Iron deficiency, thalassemia, chronic disease |
| Normal (80-100 fL) | Normocytic | Acute blood loss, chronic disease, renal disease |
| High (> 100 fL) | Macrocytic | B12/folate deficiency, alcohol, hypothyroidism |

Iron deficiency: ferritin < 45 ng/mL in an anemic adult is the AGA 2020 cutoff; ferritin rises with inflammation, so a "normal" value can hide deficiency (transferrin saturation and CRP help).

### Kidney function patterns

| Pattern | BUN | Creatinine | Possible causes |
|---------|-----|------------|-----------------|
| Both elevated | High | High | Kidney dysfunction, dehydration |
| BUN high, Cr normal | High | Normal | GI bleeding, high protein, dehydration |
| BUN:Cr ratio > 20:1 | Very high | Elevated | Pre-renal causes (dehydration, heart failure) |

### Liver function patterns

| Pattern | ALT/AST | Bilirubin | Alk Phos | Possible causes |
|---------|---------|-----------|----------|-----------------|
| Hepatocellular | Very high | Mild elevation | Normal/mild | Hepatitis, drugs, alcohol |
| Cholestatic | Mild elevation | High | Very high | Bile duct obstruction |
| Mixed | Elevated | Elevated | Elevated | Multiple causes |

### Factors affecting results

| Factor | Effect |
|--------|--------|
| Fasting status | Glucose needs fasting; lipids usually don't (nonfasting is acceptable unless triglycerides ≥ 400 mg/dL) |
| Time of day | Cortisol, iron vary diurnally |
| Hydration | Affects kidney function, electrolytes |
| Exercise | Can elevate CK, liver enzymes temporarily |
| Medications | Many drugs affect lab values |
| Recent illness | Can temporarily affect many values |
| Pregnancy | Dramatically changes many values |
| Biotin (supplements) | Interferes with thyroid tests, cardiac markers |
| Hemolysis | Falsely raises potassium, LDH, AST |

### Critical values

Advise prompt medical consultation for:
- Very high glucose (> 300 mg/dL) or low (< 54 mg/dL, ADA level 2 hypoglycemia)
- Very high potassium (> 6.5 mEq/L): cardiac risk
- Very low sodium (< 120 mEq/L): neurological risk
- Very low platelets (< 50,000/µL): bleeding risk
- Very high WBC (> 30,000/µL): serious infection or leukemia
- Very low WBC (< 2,000/µL): infection risk
- Very high creatinine: acute kidney injury concern

A single alarming value gets context and the questions to ask, calmly; a critical-range value gets a prompt call to the doctor.

## Examples

Bad: "Your TSH is 6.1, so you have hypothyroidism."
Good: "A TSH of 6.1 mIU/L is above the typical 0.4-4.0 range at most labs. That might indicate an underactive thyroid, but recent illness, some medications and biotin supplements can also shift it. Ask your doctor whether to repeat it with free T4."

## Output format

One-line disclaimer, then per marker: what it measures, the range with caveats, what high or low might mean (several possibilities), how it relates to other values, and what can distort it. Close with specific questions for the doctor and follow-up tests worth discussing.

## Checklist

- [ ] Out-of-range and critical values flagged first.
- [ ] Range caveats and distorting factors stated.
- [ ] Implications phrased as possibilities, no diagnosis.
- [ ] Questions for the doctor included.
