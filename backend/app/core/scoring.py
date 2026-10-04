"""
CrediLens — Credibility Score Engine
Transparent, weighted multi-factor credibility assessment algorithm.
"""

from typing import Dict, Any, Tuple

DEFAULT_WEIGHTS = {
    "aiClassification": 0.30,
    "evidenceVerification": 0.30,
    "sourceAnalysis": 0.20,
    "languageAnalysis": 0.10,
    "claimConsistency": 0.10
}

CREDIBILITY_DISCLAIMER = (
    "This assessment estimates credibility using AI classification, evidence retrieval, "
    "source analysis, and linguistic signals. It is not a determination of absolute truth."
)

def get_credibility_band(score: int) -> Tuple[str, str]:
    """
    Map numerical score (0-100) to standard credibility band and human-readable label.
    """
    if score >= 81:
        return "highly_reliable", "Highly Reliable"
    elif score >= 61:
        return "likely_reliable", "Likely Reliable"
    elif score >= 41:
        return "uncertain", "Uncertain"
    elif score >= 21:
        return "likely_misleading", "Likely Misleading"
    else:
        return "highly_unreliable", "Highly Unreliable"

def compute_credibility_score(
    ai_score: int,
    evidence_score: int,
    source_score: int,
    sensationalism_score: int,
    claims: list,
    weights: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Compute holistic credibility assessment and subcomponent scores.
    """
    w = weights or DEFAULT_WEIGHTS

    # Invert sensationalism (0 sensationalism = 100 language credibility score)
    language_score = max(0, min(100, 100 - sensationalism_score))

    # Calculate claim consistency score
    if claims:
        supported = sum(1 for c in claims if c.get("status") == "SUPPORTED")
        contradicted = sum(1 for c in claims if c.get("status") == "CONTRADICTED")
        total = len(claims)
        if total > 0:
            if contradicted > 0:
                claim_score = max(5, int(round((supported / total) * 60 - (contradicted * 25))))
            else:
                claim_score = int(round(40 + (supported / total) * 55))
        else:
            claim_score = 50
    else:
        claim_score = 50
    claim_score = max(0, min(100, claim_score))

    # Weighted sum
    total_score = (
        ai_score * w.get("aiClassification", 0.30) +
        evidence_score * w.get("evidenceVerification", 0.30) +
        source_score * w.get("sourceAnalysis", 0.20) +
        language_score * w.get("languageAnalysis", 0.10) +
        claim_score * w.get("claimConsistency", 0.10)
    )

    final_score = int(round(max(0.0, min(100.0, total_score))))
    band_key, band_label = get_credibility_band(final_score)

    return {
        "credibilityScore": final_score,
        "credibilityBand": band_key,
        "credibilityBandLabel": band_label,
        "disclaimer": CREDIBILITY_DISCLAIMER,
        "componentScores": {
            "aiClassification": ai_score,
            "evidenceVerification": evidence_score,
            "sourceAnalysis": source_score,
            "languageAnalysis": language_score,
            "claimConsistency": claim_score
        },
        "weightsUsed": w
    }
