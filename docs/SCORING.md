# Credibility scoring methodology

These weights are an **initial engineering framework** for a student project. They are **not** scientifically validated as an optimal or peer-reviewed model of “truth.”

The product must label the output **Credibility Assessment**.

## Formula

```
score = 100 * (
  w_ai * s_ai +
  w_ev * s_ev +
  w_src * s_src +
  w_lang * s_lang +
  w_claim * s_claim
)
```

All component scores `s_*` are in `[0, 1]` then displayed as 0–100.

Default weights (sum = 1.0):

| Key | Weight | Meaning |
|-----|--------|---------|
| `aiClassification` | 0.30 | Supervised model P(reliable-class) mapped to 0–1 |
| `evidenceVerification` | 0.30 | Fraction of claims SUPPORTED minus penalty for CONTRADICTED; INSUFFICIENT does not count as false |
| `sourceAnalysis` | 0.20 | Mean transparency × relevance of top sources |
| `languageAnalysis` | 0.10 | Inverse sensationalism (high sensationalism lowers this component only) |
| `claimConsistency` | 0.10 | Internal consistency / contradiction among extracted claims |

Weights live in backend config (`SCORING_WEIGHTS` JSON or settings) so they can change without rewriting the UI.

## Bands

| Inclusive range | Band |
|-----------------|------|
| 0–20 | Highly Unreliable |
| 21–40 | Likely Misleading |
| 41–60 | Uncertain |
| 61–80 | Likely Reliable |
| 81–100 | Highly Reliable |

## Evidence component (critical)

- `SUPPORTED` raises `s_ev`.
- `CONTRADICTED` lowers `s_ev`.
- `INSUFFICIENT_EVIDENCE` is **neutral** (does not treat the claim as false).

## Language component

Sensational language is a **signal**, not proof of misinformation. Extreme language can appear in true breaking news.

## Disclaimer (API + UI)

Stored on every analysis:

> This assessment estimates credibility using AI classification, evidence retrieval, source analysis, and linguistic signals. It is not a determination of absolute truth.
