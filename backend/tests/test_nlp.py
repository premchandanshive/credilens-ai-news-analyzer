"""
CrediLens — NLP & Linguistic Analysis Unit Tests
"""

import pytest
from backend.app.nlp.pipeline import clean_text, segment_sentences, extract_entities, process_nlp
from backend.app.nlp.claims import extract_claims, score_claim_sentence
from backend.app.nlp.language import analyze_language

def test_clean_text():
    dirty = "  Breaking   News! &amp; Special Report  \n\n\n  Details here. "
    cleaned = clean_text(dirty)
    assert "&" in cleaned
    assert "Breaking News! & Special Report" in cleaned

def test_segment_sentences():
    text = "Scientists announced a new drug. The drug completely cures cancer. The government approved it."
    sentences = segment_sentences(text)
    assert len(sentences) == 3
    assert "Scientists announced a new drug." in sentences

def test_extract_entities():
    text = "NASA and World Health Organization announced the joint report in Paris on September 2024."
    entities = extract_entities(text)
    labels = [e["label"] for e in entities]
    assert "ORG" in labels or "DATE" in labels or "GPE" in labels

def test_extract_claims():
    sentences = [
        "Scientists discovered atmospheric water vapor on exoplanet LHS 1140 b.",
        "Hello world.",
        "The economy grew by 4.2 percent in 2023 according to official statistics."
    ]
    claims = extract_claims(sentences, max_claims=5)
    assert len(claims) >= 2
    assert any(c["id"] == "c1" for c in claims)
    assert all(c["status"] == "INSUFFICIENT_EVIDENCE" for c in claims)

def test_analyze_language_objective():
    text = "According to the annual report, renewable energy installations increased by 15 percent over the previous calendar year."
    res = analyze_language(text)
    assert res["sensationalismScore"] <= 25
    assert res["emotionalLanguage"] == "low"
    assert res["clickbaitIndicators"] == "low"

def test_analyze_language_sensational():
    text = "SHOCKING DISCOVERY! This miracle cure 100% ELIMINATES all cancer in 24 hours! Big Pharma is terrified! Share immediately before this gets banned forever!!!"
    res = analyze_language(text)
    assert res["sensationalismScore"] >= 60
    assert res["emotionalLanguage"] in ("moderate", "high")
    assert res["clickbaitIndicators"] in ("moderate", "high")
    assert res["absoluteClaimCount"] >= 1
