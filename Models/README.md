# PHC Triage Models - Evaluation Summary

## Overview

This repository contains three independently trained multi-output classification models for PHC triage support:

- **Adult model**
- **Child model**
- **Maternal / Pregnant model**

Each model predicts **two output variables** from structured clinical input features:

1. **`clinical_disposition`**
   - `Treat locally`
   - `Treat + monitor`
   - `Stabilize + refer`
   - `Emergency referral`

2. **`severity_score`**
   - `Low`
   - `Medium`
   - `High`

The models were trained and evaluated on **synthetic but clinically grounded datasets** built from rule-consistent triage logic. These metrics show how well the models learn the dataset patterns. They do **not** by themselves prove real-world clinical validity.

---

## Model Training Setup

For each patient type, three baseline models were trained and compared:

- **Logistic Regression**
- **Random Forest**
- **Extra Trees**

Model selection was based on a composite score:

**Composite score = 0.65 × Disposition Macro F1 + 0.35 × Severity Macro F1**

The best-performing model for all three patient types was **Random Forest (`rf`)**.

---

# 1. Adult Model Evaluation

## Best model
- **Selected model:** `Random Forest`

## Model comparison

| Model | Disposition Macro F1 | Severity Macro F1 | Composite Score |
|---|---:|---:|---:|
| Logistic Regression | 0.7596 | 0.8326 | 0.7851 |
| Random Forest | 0.9420 | 0.9344 | 0.9393 |
| Extra Trees | 0.8927 | 0.8909 | 0.8921 |

## Random Forest detailed performance

### `clinical_disposition`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Treat locally | 0.97 | 0.99 | 0.98 | 400 |
| Treat + monitor | 0.92 | 0.91 | 0.92 | 400 |
| Stabilize + refer | 0.89 | 0.91 | 0.90 | 400 |
| Emergency referral | 0.99 | 0.95 | 0.97 | 400 |

- **Accuracy:** 0.94
- **Macro Avg F1:** 0.94
- **Weighted Avg F1:** 0.94

### `severity_score`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Low | 0.96 | 0.98 | 0.97 | 451 |
| Medium | 0.90 | 0.88 | 0.89 | 485 |
| High | 0.94 | 0.94 | 0.94 | 664 |

- **Accuracy:** 0.93
- **Macro Avg F1:** 0.93
- **Weighted Avg F1:** 0.93

## Interpretation

The adult model shows strong separation between low-risk and high-risk cases. It performs especially well on the `Emergency referral` and `Treat locally` classes. Slightly lower performance on `Treat + monitor` and `Stabilize + refer` is expected because those classes are clinically closer and harder to separate cleanly.

---

# 2. Child Model Evaluation

## Best model
- **Selected model:** `Random Forest`

## Model comparison

| Model | Disposition Macro F1 | Severity Macro F1 | Composite Score |
|---|---:|---:|---:|
| Logistic Regression | 0.8346 | 0.8869 | 0.8529 |
| Random Forest | 0.9726 | 0.9674 | 0.9708 |
| Extra Trees | 0.9296 | 0.9317 | 0.9304 |

## Random Forest detailed performance

### `clinical_disposition`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Treat locally | 1.00 | 1.00 | 1.00 | 400 |
| Treat + monitor | 0.97 | 0.97 | 0.97 | 400 |
| Stabilize + refer | 0.94 | 0.95 | 0.95 | 400 |
| Emergency referral | 0.98 | 0.96 | 0.97 | 400 |

- **Accuracy:** 0.97
- **Macro Avg F1:** 0.97
- **Weighted Avg F1:** 0.97

### `severity_score`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Low | 1.00 | 0.99 | 0.99 | 683 |
| Medium | 0.93 | 0.97 | 0.95 | 450 |
| High | 0.97 | 0.94 | 0.96 | 467 |

- **Accuracy:** 0.97
- **Macro Avg F1:** 0.97
- **Weighted Avg F1:** 0.97

## Interpretation

The child model performs extremely well, likely because the synthetic dataset follows relatively crisp IMCI-inspired danger-sign logic. This makes emergency and stable cases easier to separate than in messy real-world pediatric data.

---

# 3. Maternal / Pregnant Model Evaluation

## Best model
- **Selected model:** `Random Forest`

## Model comparison

| Model | Disposition Macro F1 | Severity Macro F1 | Composite Score |
|---|---:|---:|---:|
| Logistic Regression | 0.8346 | 0.8869 | 0.8529 |
| Random Forest | 0.9726 | 0.9674 | 0.9708 |
| Extra Trees | 0.9296 | 0.9317 | 0.9304 |

## Random Forest detailed performance

### `clinical_disposition`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Treat locally | 1.00 | 1.00 | 1.00 | 400 |
| Treat + monitor | 0.97 | 0.97 | 0.97 | 400 |
| Stabilize + refer | 0.94 | 0.95 | 0.95 | 400 |
| Emergency referral | 0.98 | 0.96 | 0.97 | 400 |

- **Accuracy:** 0.97
- **Macro Avg F1:** 0.97
- **Weighted Avg F1:** 0.97

### `severity_score`

| Class | Precision | Recall | F1-score | Support |
|---|---:|---:|---:|---:|
| Low | 1.00 | 0.99 | 0.99 | 683 |
| Medium | 0.93 | 0.97 | 0.95 | 450 |
| High | 0.97 | 0.94 | 0.96 | 467 |

- **Accuracy:** 0.97
- **Macro Avg F1:** 0.97
- **Weighted Avg F1:** 0.97

## Interpretation

The maternal model strongly captures high-risk pregnancy patterns such as severe hypertension, bleeding, seizures, reduced fetal movement, anemia risk, and edema-linked danger conditions. As with the child model, the very high scores reflect synthetic rule-consistent data rather than noisy real-world variability.

---

## Final Model Selection Summary

| Patient Type | Best Model | Disposition Macro F1 | Severity Macro F1 | Composite Score |
|---|---|---:|---:|---:|
| Adult | Random Forest | 0.9420 | 0.9344 | 0.9393 |
| Child | Random Forest | 0.9726 | 0.9674 | 0.9708 |
| Maternal / Pregnant | Random Forest | 0.9726 | 0.9674 | 0.9708 |

---

## Important Note on Reliability

These results are **internally strong** and indicate that the models successfully learn the underlying patterns present in the datasets.

However:

- the datasets are **synthetic**
- the labels are **rule-grounded**
- the test set comes from the **same synthetic generation logic**

So these metrics should be interpreted as:

- **good evidence of pipeline correctness**
- **good evidence of learnable structure**
- **not sufficient evidence of real-world clinical validity**

For real deployment, the models would need:

- evaluation on external real-world patient data
- hospital capability features
- uncertainty handling
- clinician review and calibration
- robust input validation

---

## Conclusion

From an ML engineering perspective, the pipeline is working correctly:

- training and inference run successfully
- all three models produce clinically sensible outputs on representative samples
- Random Forest consistently outperforms Logistic Regression and Extra Trees
- the models are suitable for **hackathon / prototype / MVP** demonstration

They should not yet be described as clinically validated diagnostic systems, because medicine remains annoyingly strict about evidence.
