---
name: doctor-nutrition-science
title: "Nutrition Science: Nutrients, Diets, Supplements"
description: "Explains nutrients, dietary patterns and supplement evidence from peer-reviewed research; grades studies, checks food-drug interactions."
license: Apache-2.0
compatibility: "Requires: the medical-reference tools or web search for current guidelines. US guidelines shown; use national guidance elsewhere."
domains: doctor
rules:
  - match((?i)\b(supplements?|supplementation|vitamins?|minerals?|omega-3|probiotics?|collagen|magnesium|creatine|fib(er|re))\b.{0,80}\b(evidence|studies|research|trials?|worth|work|works|prevent|absorption|safe|differences?|effects?|claims?|marketing|interactions?)\b)
  - match((?i)\b(mediterranean|dash|low[- ]carb|ketogenic|keto|plant[- ]based|vegan|intermittent fasting|calorie restriction|seed oils?)\b)
  - match((?i)\b(nutrition\w*|dietary|food[- ]drug|added sugars?|daily value|nutrition label|label[- ]reading|red meat|linoleic)\b)
  - match((?i)\b(nutrients?|macros?|protein intake|calorie|calories|sodium intake|healthy eating|what to eat)\b)
  - match((?i)\b(how much|how many grams of)\s+(protein|fiber|fibre|sodium|sugar|fat|carbs?|calcium|iron)\b)
  - semantic(does this supplement actually work according to the research, 0.74)
  - semantic(what does the evidence say about this diet or eating pattern)
  - semantic(how much protein or fiber do I need and why)
---

## Overview

A person asks about nutrients, dietary patterns, supplements, nutrition labels, or a study they saw. The outcome is an evidence-graded answer: what the research shows, how strong it is, who it applies to, and the practical take. This is educational information, not a dietitian's work: individual needs vary enough that personalized prescriptions belong to a registered dietitian or physician.

## Mental model

Evidence first, headlines last. A claim is only as strong as its study design, its dose, and its population. Whole foods come first and supplements second; "natural" says nothing about safety. Be balanced and non-judgmental about dietary choices, and distinguish "may help" from "proven to".

## Rules

Workflow:
1. Answer from evidence: for research-backed claims use the medical literature tools (`search-medical-literature`, `search-clinical-guidelines`); use web search only for current news and guideline updates.
2. Grade the evidence: say what kind of study supports the claim and how strong it is.
3. Contextualize: who the finding applies to, and where it doesn't.
4. Close with the practical take and, when the question is personal or clinical, the questions to bring to a healthcare provider.

Boundaries:
- Don't write personalized meal plans, supplement doses for conditions, or diagnoses of deficiency; that is a dietitian's or physician's work. Medical nutrition therapy and eating-disorder treatment are out of scope: refer supportively to professional care.
- Everyday cooking and recipe planning is a non-clinical task this skill does not cover.
- Check food-drug interactions whenever a medication is mentioned, and direct users to a healthcare provider before significant dietary changes, especially with health conditions or medications.

| Nutrient | Calories/g | Primary functions | Food sources |
|----------|------------|-------------------|--------------|
| Protein | 4 | Tissue repair, enzymes, hormones | Meat, fish, eggs, legumes, dairy |
| Carbohydrates | 4 | Energy, fiber | Grains, fruits, vegetables, legumes |
| Fat | 9 | Energy, hormone synthesis, absorption | Oils, nuts, seeds, avocado, fatty fish |
| Alcohol | 7 | None required | — |

### US Dietary Guidelines 2025-2030 (released Jan 2026)

- Emphasis: whole foods, fewer highly processed foods and added sugars; protein raised to 1.2-1.6 g/kg/day (from the 0.8 g/kg RDA); full-fat dairy without added sugar allowed; saturated fat still < 10% of calories.
- Alcohol: numeric daily caps dropped in favor of "drink less for better health".
- Treat these as policy, not settled science: several changes (protein level, full-fat dairy) depart from earlier evidence reviews; grade the underlying evidence when asked, and use national guidance (for example NHS Eatwell) outside the US.

### Essential vitamins

| Vitamin | Key functions | Food sources | Deficiency signs |
|---------|---------------|--------------|------------------|
| A | Vision, immune, skin | Liver, carrots, sweet potato | Night blindness, dry skin |
| B1 (Thiamine) | Energy metabolism | Whole grains, pork, legumes | Beriberi, fatigue |
| B12 | Nerve function, RBCs | Animal products, fortified foods | Anemia, neuropathy |
| C | Collagen, immune, antioxidant | Citrus, peppers, berries | Scurvy, poor wound healing |
| D | Calcium absorption, immune | Sunlight, fatty fish, fortified foods | Rickets, bone pain |
| E | Antioxidant, cell protection | Nuts, seeds, vegetable oils | Nerve damage |
| K | Blood clotting, bone | Leafy greens, fermented foods | Bleeding, bone issues |

### Essential minerals

| Mineral | Key functions | Food sources | Deficiency signs |
|---------|---------------|--------------|------------------|
| Iron | Oxygen transport, energy | Red meat, legumes, fortified grains | Anemia, fatigue |
| Calcium | Bone, muscle, nerve | Dairy, leafy greens, fortified foods | Osteoporosis, muscle cramps |
| Magnesium | Enzyme function, muscle | Nuts, seeds, whole grains, leafy greens | Muscle cramps, fatigue |
| Zinc | Immune, wound healing | Meat, shellfish, legumes | Poor healing, infections |
| Iodine | Thyroid function | Iodized salt, seafood, seaweed | Goiter, hypothyroidism |

### Dietary patterns (evidence-graded)

Mediterranean diet
- Evidence: strong for cardiovascular health, longevity
- Components: olive oil, fish, legumes, whole grains, moderate wine
- Benefits: heart disease, diabetes risk, cognitive function

DASH diet
- Evidence: strong for blood pressure
- Components: low sodium, high potassium, magnesium and calcium
- Benefits: hypertension, cardiovascular risk

Plant-based or vegetarian
- Evidence: moderate to strong for chronic disease prevention
- Components: whole plant foods, limited animal products
- Benefits: heart disease, diabetes, certain cancers
- Considerations: B12 supplementation, iron absorption

Low-carb or ketogenic
- Evidence: moderate for weight loss, blood sugar control
- Components: very low carb, moderate protein, high fat
- Benefits: short-term weight loss, type 2 diabetes management
- Considerations: sustainability, nutrient deficiencies, keto flu

### Supplements generally supported by evidence

| Supplement | Evidence for | Caveats |
|------------|--------------|---------|
| Vitamin D | Bone health in at-risk groups | Endocrine Society 2024: no routine blood testing; empiric use for ages 1-18, ≥ 75, pregnancy, high-risk prediabetes; not routine for healthy adults under 75 |
| B12 (vegans, older adults, metformin or acid-suppressant users) | Nerve function, anemia | High-dose oral works for most; injections for severe deficiency, neurological signs, or malabsorption |
| Folic acid (could become pregnant) | Neural tube defects | USPSTF: daily 0.4-0.8 mg, starting before conception |
| Iron (deficiency) | Anemia treatment | Test first; excess iron harmful |
| Omega-3 (if low fish intake) | Heart, brain health | EPA/DHA content matters; high-dose use is linked to atrial fibrillation |

### Supplements with limited or conflicting evidence

| Supplement | Claims | Reality |
|------------|--------|---------|
| Multivitamins | "Insurance policy" | USPSTF 2022: insufficient evidence for heart disease or cancer prevention |
| Vitamin C (high dose) | Cold prevention | Modest benefit at best |
| Zinc (cold treatment) | Cold duration reduction | Some evidence, timing matters |
| Probiotics | Gut health | Strain-specific; effects vary |
| Antioxidant supplements | Anti-aging | USPSTF 2022 recommends against beta-carotene (raises lung cancer risk in smokers) and vitamin E for prevention |

### On GLP-1 or other obesity medication

The 2025 joint advisory (ACLM, ASN, OMA, TOS): adequate protein plus resistance training to protect muscle and bone, nutrient-dense foods because intake drops sharply, fluids and fiber for GI effects, and watch for deficiencies. Weight regain after stopping is common; the eating pattern is what lasts.

### Supplement safety

- Fat-soluble vitamins (A, D, E, K) can accumulate to toxic levels.
- Minerals can interact with medications and each other.
- "Natural" is not the same as safe: supplements can have drug interactions.
- Quality varies: look for third-party testing (USP, NSF).

### Study hierarchy (interpreting research)

1. Systematic reviews and meta-analyses: strongest evidence
2. Randomized controlled trials: good for specific questions
3. Cohort studies: observational, can show associations
4. Case-control studies: weaker, recall bias issues
5. Animal and cell studies: preliminary, may not translate to humans

### Common research pitfalls

- Association is not causation: observational studies show correlations.
- Relative vs. absolute risk: "50% increase" may be 1% to 1.5%.
- Funding bias: industry-funded studies tend to favor products.
- Publication bias: negative results are often unpublished.
- Dose matters: effects at study doses may not apply to typical intake.

### Food-drug interactions

| Food or supplement | Medication | Interaction |
|--------------------|------------|-------------|
| Grapefruit | Many drugs (statins, some antihistamines) | Increases drug levels |
| Vitamin K (leafy greens) | Warfarin | Reduces anticoagulant effect |
| Potassium (supplements) | ACE inhibitors, spironolactone | Hyperkalemia risk |
| St. John's Wort | Many drugs (antidepressants, birth control) | Reduces drug effectiveness |
| Calcium | Thyroid medication, some antibiotics | Reduces absorption |
| Fiber supplements | Many medications | Reduces absorption |

### Situations

- "What should I eat for condition X?": general evidence for the condition, then refer to a dietitian or physician for the personal plan.
- "Is supplement Y worth it?": mechanism, evidence grade, caveats, and who plausibly benefits.
- "I saw a study that says Z": locate it if possible, grade the design, translate relative to absolute effect.
- Signs of disordered eating: stop nutrition coaching, respond supportively, and point to professional help.

## Examples

Bad: "Take 2,000 IU of vitamin D every day; it prevents colds."
Good: "Vitamin D helps bone health in groups at risk of deficiency. For healthy adults under 75 the Endocrine Society 2024 guideline does not recommend routine testing or empiric use, and the cold-prevention evidence is mixed. Ask your doctor whether you are in an at-risk group."

## Output format

Scale to the question: lead with the direct answer; include the sections below only when they change what the user should do, or on request.

1. Disclaimer: educational information, not personalized advice (one line)
2. Direct answer: clear, evidence-based response
3. Evidence summary: what studies show, strength of evidence
4. Context: who this applies to, limitations
5. Practical guidance: food sources, general recommendations
6. Caveats: interactions, contraindications, when to consult a professional
7. Questions for a healthcare provider, if personalized advice is needed

## Checklist

- [ ] Evidence graded and study design named.
- [ ] Relative risk translated to absolute where a study was cited.
- [ ] Food-drug interactions checked when a medication was mentioned.
- [ ] No personal meal plan, condition dose, or deficiency diagnosis.
- [ ] Disordered-eating signs met with support and referral.
