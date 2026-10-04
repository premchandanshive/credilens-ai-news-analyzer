"""
CrediLens — Credibility Scoring Engine Unit Tests
"""

import pytest
from backend.app.core.scoring import compute_credibility_score, get_credibility_band

def test_credibility_bands():
    assert get_credibility_band(95)[0] == "highly_reliable"
    assert get_credibility_band(72)[0] == "likely_reliable"
    assert get_credibility_band(50)[0] == "uncertain"
    assert get_credibility_band(30)[0] == "likely_misleading"
    assert get_credibility_band(10)[0] == "highly_unreliable"

def test_compute_credibility_score_reliable():
    claims = [
        {"id": "c1", "status": "SUPPORTED"},
        {"id": "c2", "status": "SUPPORTED"}
    ]
    res = compute_credibility_score(
        ai_score=85,
        evidence_score=90,
        source_score=80,
        sensationalism_score=10,
        claims=claims
    )
    assert res["credibilityScore"] >= 75
    assert res["credibilityBand"] in ("likely_reliable", "highly_reliable")
    assert "disclaimer" in res
    assert res["componentScores"]["aiClassification"] == 85
    assert res["componentScores"]["languageAnalysis"] == 90  # 100 - 10

def test_compute_credibility_score_unreliable():
    claims = [
        {"id": "c1", "status": "CONTRADICTED"},
        {"id": "c2", "status": "INSUFFICIENT_EVIDENCE"}
    ]
    res = compute_credibility_score(
        ai_score=20,
        evidence_score=15,
        source_score=25,
        sensationalism_score=80,
        claims=claims
    )
    assert res["credibilityScore"] <= 35
    assert res["credibilityBand"] in ("likely_misleading", "highly_unreliable")
