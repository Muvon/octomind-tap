---
name: data-predictive-modeling
title: "Predictive Modeling: Validation & Model Cards"
description: "Build and validate an offline forecasting or classification model with leakage checks, baselines, calibration, a report and a model card."
license: Apache-2.0
compatibility: "Needs Python; scikit-learn, pandas and similar packages via uv when missing. Models are built offline and never deployed."
capabilities: image-view
rules:
  - match((?i)\b(predictive|churn|forecasting|forecast|demand|risk[\s-]score|propensity|classification|regression|machine[\s-]learning|ml)\s+model\b)
  - match((?i)\b(build|train|fit|create|develop)\s+(an?\s+|the\s+|my\s+)?(\w+\s+){0,3}(model|classifier|predictor)\s+(to\s+|that\s+|for\s+)?(predict|forecast|classify|score|rank)\w*)
  - match((?i)\b(predict|forecast)\s+(next\s+)?(\w+\s+){0,3}(churn|demand|sales|revenue|conversion|default|risk|quarter|month|week)\b)
  - match((?i)\b(data\s+leakage|auc|roc|cross[\s-]validation|backtest(ing)?|model\s+card|calibrat(e|ion)|overfit\w*)\b)
  - semantic(train and validate a model to predict an outcome from this dataset, 0.72)
  - semantic(forecast next quarter's demand from our past sales, 0.72)
  - semantic(check my model for data leakage and compare against a baseline, 0.72)
  - semantic(write a model card and report for the classifier I trained, 0.72)
  - semantic(build a churn prediction model and validate it offline, 0.72)
---

## Overview

Use this skill to build a predictive or forecasting model offline from a dataset the user supplies, validate it so the numbers can be trusted, and report what it can and cannot do. The deliverable is a validated model artifact plus a report and a model card, not a leaderboard score. A model that looks good because of leakage is worse than no model.

## Mental model

A claim goes no further than the held-out evidence. Say "the validation shows", never "the model will". Lead with the verdict: does the model beat the baseline, by how much, and with what uncertainty. Define a metric the first time you use it.

## Rules

### Method

Work in the project directory with Python and the shell. Use `uv run --with scikit-learn --with pandas` when a package is missing. Fix random seeds and save the environment's package versions with the artifact.

1. Frame: write down the target (one row = one what), the prediction time (what is known at that moment), the horizon, and the decision the prediction feeds. If the decision is unclear, the metric cannot be chosen; ask.
2. Split before looking: hold out the test set first and touch it once, at the end. Use a random split for independent rows. For time-dependent data split by time (train on the past, test on the future). For repeated entities (customers, devices) split by entity with grouped folds so one entity never sits on both sides.
3. Leakage checks before fitting: no feature built from data after the prediction time; no target-derived column (a "cancel_date" when predicting churn); scaling, imputation, encoding and selection fitted inside each training fold only (use a pipeline); no duplicates across the split. After fitting: a single feature with near-perfect importance, or an AUC above 0.95 on a hard problem, is a leak until proven otherwise (a practitioner heuristic, not a published threshold).
4. Baseline first: a trivial model (majority class, base rate, mean, or seasonal naive for time series) and a simple one (regularized logistic or linear regression). Keep a complex model only if it beats the simple one by more than the fold-to-fold spread.
5. Model and tune: gradient-boosted trees for tabular data once the baseline is set. Tune with cross-validation on the training set only, with a small search budget stated in the report.
6. Calibrate: for a classifier whose probabilities are used (ranking by risk is not enough), check a reliability curve and the Brier score on held-out data. Calibrate with sigmoid scaling, or isotonic regression only with roughly 1000 or more calibration samples. Calibration data is disjoint from training data.
7. Test once: score the untouched test set, report the metric with a bootstrap confidence interval, and compare it to the baseline on the same rows. Slice results by key segments; a good average can hide a failing segment.
8. Package: save the model, the code that reproduces it, and `model-card-[name].md`. Write the report with the `analytical-report` skill when a formatted report is asked for.

Models covered: scikit-learn, XGBoost, LightGBM, statsmodels and Prophet-style models.

### Situation rules

| Situation | Rule |
|---|---|
| Imbalanced classes (positive rate under about 10%, a practitioner heuristic) | Report precision-recall AUC (average precision) and the positive rate next to it; ROC AUC looks high when negatives dominate. Accuracy alone is not reported. |
| Threshold-based action | Pick the threshold from the cost of a false positive versus a false negative, or a capacity limit (top N contacted), on validation data, and report precision and recall at that threshold. |
| Regression | Report MAE and RMSE next to a naive baseline. Use a percentage error only when the target is never near zero. |
| Forecasting | Backtest with rolling-origin (expanding window) folds. Compare with the seasonal naive baseline using MASE (Hyndman and Koehler, 2006), where below 1 beats the naive forecast. Report error by horizon. With scikit-learn `TimeSeriesSplit`, set `gap` to the forecast horizon so near-term rows do not leak across the split. |
| Small data (a few hundred rows) | Repeated cross-validation, simple models, wide uncertainty stated. Say plainly when the data cannot support a model. |
| Distribution shift | Compare feature distributions train versus test. Large drift means the test score will not carry forward. State it. |
| Feature importance | Use permutation importance on held-out data. Importance is association, never cause. |

The model card (Mitchell et al., 2019) has: intended use and out-of-scope uses, data (source, period, size, target definition), split method, metrics with intervals and baseline, segment results, calibration, known failure modes, and the date and package versions.

### Common requests

| Request | Response |
|---|---|
| "Build me a churn, demand or risk model" | Ask for the target definition, the prediction time and the decision (one question if only one is missing), then proceed. |
| "Why is my AUC 0.99?" | Treat as a leak: run the leakage checks and name the feature. |
| "Forecast next quarter" | Time-based backtest against seasonal naive first; give the interval, not a single line. |
| "Deploy it" or "put it in production" | Decline: this work builds and validates offline. Hand over the artifact, the card and the preprocessing code for the team that deploys. |

In an autonomous, non-interactive brief, don't ask. State the target, split and metric you assume, proceed, and list the assumptions at the top of the report.

### Guards

- Don't deploy, schedule or serve a model, and don't write to production systems or databases.
- Don't touch the test set before the final scoring, and don't tune on it.
- Don't report a score without the baseline it beats and an uncertainty interval.
- Don't claim more than the held-out evidence shows: no "will reduce churn by X", no causal reading of feature importance.
- Don't use a random split on time-dependent or grouped data.
- Stop and say so when the data cannot support a useful model.
- Predictions about people (credit, hiring, health) need a qualified human review and a fairness check across groups before any use. Say so in the model card.

### Scope limits

Deploying or serving a model, scheduled retraining, feature stores and production pipelines, exploratory and causal analysis, fine-tuning neural networks or language models at scale, and decisions with legal or medical consequences are not covered.

## Output format

Deliver in the working directory:

- `model/` with the saved model and a reproducible script or notebook
- `report-[name].md`: verdict first, then target and split, leakage checks run and results, baseline versus model table, calibration, backtest or cross-validation results, segments, limits
- `model-card-[name].md`

Every number in the report comes from a command you ran; show the command's output when asked.

## Checklist

- [ ] Target, prediction time, horizon and decision are written down.
- [ ] The split matches the data (random, time, or grouped) and the test set was touched once.
- [ ] Leakage checks ran before and after fitting.
- [ ] A baseline and a simple model were scored on the same rows.
- [ ] Metrics carry a confidence interval, and segments were sliced.
- [ ] Probabilities in use were calibrated on disjoint data.
- [ ] The model card and the report are saved next to the model.

## Composition / References

- `data-analysis-statistics` covers exploratory and causal questions.
- `analytical-report` covers formatted reports.
- Mitchell et al., 2019, "Model Cards for Model Reporting".
- Hyndman and Koehler, 2006, "Another look at measures of forecast accuracy".
