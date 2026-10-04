"""
CrediLens — Evidence & Multi-Factor Reason Synthesizer
Generates transparent human-readable Key Findings explaining the credibility assessment.
"""

from typing import List, Dict, Any

def generate_key_findings(
    claims: List[Dict[str, Any]],
    sources: List[Dict[str, Any]],
    language_analysis: Dict[str, Any],
    prediction: Dict[str, Any],
    credibility_score: int
) -> List[Dict[str, Any]]:
    """
    Synthesize structured Key Findings corresponding directly to underlying pipeline components.
    Returns:
        [
            {"tone": "positive", "text": "...", "basis": "evidence"},
            {"tone": "warning", "text": "...", "basis": "language"},
            ...
        ]
    """
    findings: List[Dict[str, Any]] = []

    # 1. Evidence Verification Findings
    supported_count = sum(1 for c in claims if c.get("status") == "SUPPORTED")
    contradicted_count = sum(1 for c in claims if c.get("status") == "CONTRADICTED")
    insufficient_count = sum(1 for c in claims if c.get("status") == "INSUFFICIENT_EVIDENCE")
    total_claims = len(claims)

    if supported_count > 0:
        plural = "claim is" if supported_count == 1 else "claims are"
        findings.append({
            "tone": "positive",
            "text": f"{supported_count} of {total_claims} extracted {plural} supported by retrieved authoritative sources.",
            "basis": "evidence"
        })

    if contradicted_count > 0:
        plural = "claim is" if contradicted_count == 1 else "claims are"
        findings.append({
            "tone": "negative",
            "text": f"{contradicted_count} {plural} directly contradicted by external factual verification.",
            "basis": "evidence"
        })

    if insufficient_count > 0:
        plural = "claim needs" if insufficient_count == 1 else "claims need"
        findings.append({
            "tone": "warning",
            "text": f"{insufficient_count} {plural} further independent verification due to limited public reference data.",
            "basis": "evidence"
        })

    # 2. Source Analysis Findings
    reliable_sources = [s for s in sources if s.get("transparencyScore", 0) >= 70]
    if reliable_sources:
        source_names = [s.get("title", s.get("domain", "source")) for s in reliable_sources[:2]]
        findings.append({
            "tone": "positive",
            "text": f"High source transparency and contextual alignment from {', '.join(source_names)}.",
            "basis": "source"
        })
    elif sources and all(s.get("transparencyScore", 0) < 50 for s in sources):
        findings.append({
            "tone": "warning",
            "text": "Matched external sources display limited editorial transparency or lack author attribution.",
            "basis": "source"
        })

    # 3. Linguistic & Sensationalism Findings
    sensational_score = language_analysis.get("sensationalismScore", 0)
    emotional_level = language_analysis.get("emotionalLanguage", "low")
    clickbait_level = language_analysis.get("clickbaitIndicators", "low")
    absolute_count = language_analysis.get("absoluteClaimCount", 0)

    if sensational_score <= 20:
        findings.append({
            "tone": "positive",
            "text": "No sensational, inflammatory, or manipulative language patterns detected.",
            "basis": "language"
        })
    elif sensational_score >= 60 or clickbait_level == "high":
        findings.append({
            "tone": "negative",
            "text": f"Elevated sensationalism detected (score: {sensational_score}/100) with clickbait markers and emotional framing.",
            "basis": "language"
        })
    elif emotional_level == "moderate" or absolute_count > 0:
        findings.append({
            "tone": "warning",
            "text": f"Moderate emotional intensity and {absolute_count} unhedged absolute assertions identified.",
            "basis": "language"
        })

    # 4. Overall Holistic Assessment Summary
    if credibility_score >= 80:
        findings.append({
            "tone": "positive",
            "text": "Overall context, language, and corroborating citations indicate highly reliable reporting.",
            "basis": "model"
        })
    elif credibility_score >= 60:
        findings.append({
            "tone": "positive",
            "text": "Overall context suggests this reporting is mostly accurate, though additional primary source corroboration is advised.",
            "basis": "model"
        })
    elif credibility_score >= 40:
        findings.append({
            "tone": "warning",
            "text": "Mixed credibility signals detected. Independent fact-checking is recommended before relying on this information.",
            "basis": "model"
        })
    else:
        findings.append({
            "tone": "negative",
            "text": "Substantial misinformation markers, low source corroboration, or unverified claims detected.",
            "basis": "model"
        })

    return findings[:6]
