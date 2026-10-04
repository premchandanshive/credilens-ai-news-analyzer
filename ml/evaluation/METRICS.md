# CrediLens ML Model Evaluation Metrics

This document details the cross-validated performance of baseline text classification models for credibility prediction.

## Model Comparison (5-Fold Stratified Cross-Validation)

| Model | Accuracy | Precision (Reliable) | Recall (Reliable) | F1-Score |
|---|---|---|---|---|
| **TF-IDF + Logistic Regression** | 0.6333 | 0.5926 | 1.0000 | 0.7442 |
| **TF-IDF + Linear SVM** | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| **TF-IDF + Multinomial Naive Bayes** | 0.8333 | 0.7619 | 1.0000 | 0.8649 |

## Confusion Matrices

### TF-IDF + Logistic Regression

```
                Predicted Unreliable  Predicted Reliable
Actual Unreliable      3                     11
Actual Reliable        0                     16
```

### TF-IDF + Linear SVM

```
                Predicted Unreliable  Predicted Reliable
Actual Unreliable      14                    0
Actual Reliable        0                     16
```

### TF-IDF + Multinomial Naive Bayes

```
                Predicted Unreliable  Predicted Reliable
Actual Unreliable      9                     5
Actual Reliable        0                     16
```

## Feature Importance (Top Positive and Negative N-grams)

### Indicative of Reliable Reporting (+ Coefficients)

- **`for`**: +0.2012
- **`test`**: +0.1644
- **`percent`**: +0.1590
- **`published`**: +0.1542
- **`published in`**: +0.1372
- **`climate`**: +0.1169
- **`using`**: +0.1139
- **`50`**: +0.1126
- **`in the`**: +0.1109
- **`consortium`**: +0.1032

### Indicative of Misleading / Sensational Reporting (- Coefficients)

- **`secret`**: -0.2348
- **`this`**: -0.2103
- **`is`**: -0.1697
- **`all`**: -0.1663
- **`are`**: -0.1539
- **`now`**: -0.1156
- **`leaked`**: -0.1150
- **`activated`**: -0.1101
- **`control`**: -0.1066
- **`government`**: -0.1049

---
*Generated during Model 3 training pipeline.*
