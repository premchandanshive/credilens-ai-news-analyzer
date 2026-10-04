"""
CrediLens — Claim Stance & Verification Classifier
Categorizes claim relationship against retrieved evidence into SUPPORTED, CONTRADICTED, or INSUFFICIENT_EVIDENCE.
"""

from typing import List, Tuple
from backend.app.evidence.base import SearchHit, ClaimVerificationResult

CONTRADICTION_CUES = {
    "debunk", "debunked", "false", "hoax", "fake", "denied", "refuted",
    "untrue", "misleading", "unfounded", "no evidence", "fabricated",
    "fact check", "misinformation", "disproved", "incorrect", "myth"
}

SUPPORT_CUES = {
    "confirmed", "reported", "announced", "published", "discovered",
    "found", "identified", "showed", "concluded", "demonstrated", "passed"
}

def classify_claim_verification(
    claim_id: str,
    claim_text: str,
    ranked_hits: List[SearchHit]
) -> ClaimVerificationResult:
    """
    Classify whether a claim is SUPPORTED, CONTRADICTED, or has INSUFFICIENT_EVIDENCE.
    CRITICAL RULE: Missing evidence must NEVER be classified as CONTRADICTED.
    """
    if not ranked_hits:
        return ClaimVerificationResult(
            claim_id=claim_id,
            claim_text=claim_text,
            status="INSUFFICIENT_EVIDENCE",
            confidence=0.2,
            evidence_ids=[],
            top_hits=[]
        )

    # Filter to top relevant hits
    relevant_hits = [h for h in ranked_hits if h.relevance_score >= 20.0]
    
    if not relevant_hits:
        return ClaimVerificationResult(
            claim_id=claim_id,
            claim_text=claim_text,
            status="INSUFFICIENT_EVIDENCE",
            confidence=0.3,
            evidence_ids=[],
            top_hits=ranked_hits[:2]
        )

    top_hit = relevant_hits[0]
    snippet_lower = f"{top_hit.title} {top_hit.snippet}".lower()
    
    # Check for contradiction / fact-check debunking signals
    contradiction_found = any(cue in snippet_lower for cue in CONTRADICTION_CUES)
    
    if contradiction_found and top_hit.relevance_score >= 30.0:
        status = "CONTRADICTED"
        relationship = "contradicts"
        confidence = min(0.95, round(top_hit.relevance_score / 100.0 + 0.1, 2))
    elif top_hit.relevance_score >= 35.0:
        status = "SUPPORTED"
        relationship = "supports"
        confidence = min(0.95, round(top_hit.relevance_score / 100.0, 2))
    else:
        status = "INSUFFICIENT_EVIDENCE"
        relationship = "related"
        confidence = 0.45

    for h in relevant_hits:
        h.relationship = relationship

    return ClaimVerificationResult(
        claim_id=claim_id,
        claim_text=claim_text,
        status=status,
        confidence=confidence,
        evidence_ids=[h.url for h in relevant_hits if h.url],
        top_hits=relevant_hits[:3]
    )
