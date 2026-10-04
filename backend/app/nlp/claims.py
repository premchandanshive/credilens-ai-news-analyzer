"""
CrediLens — Factual Claim Extraction Engine
Extracts verifiable factual propositions and claims from input sentences.
"""

import re
from typing import List, Dict, Any

FACTUAL_VERBS = {
    "announce", "announced", "announces", "discover", "discovered", "discovers",
    "report", "reported", "reports", "confirm", "confirmed", "confirms",
    "publish", "published", "publishes", "prove", "proved", "proven", "proves",
    "show", "showed", "shows", "award", "awarded", "awards", "develop", "developed",
    "develops", "reveal", "revealed", "reveals", "find", "found", "finds",
    "test", "tested", "tests", "approve", "approved", "approves", "decrease",
    "decreased", "increase", "increased", "reach", "reached", "identify", "identified",
    "uncover", "uncovered", "conclude", "concluded", "demonstrate", "demonstrated"
}

NUMERIC_PATTERN = re.compile(r'\b\d+(?:[\.,]\d+)?\s*(?:%|percent|gigawatts|light-years|years|days|hours|dollars|nanometers|neurons)?\b', re.IGNORECASE)

def score_claim_sentence(sentence: str) -> float:
    """Score a candidate sentence on how factual and verifiable its assertion appears."""
    score = 0.0
    lower = sentence.lower()
    words = set(re.findall(r'\b[a-zA-Z]+\b', lower))
    
    # 1. Presence of factual reporting verbs
    matching_verbs = words.intersection(FACTUAL_VERBS)
    score += len(matching_verbs) * 1.5
    
    # 2. Presence of numeric and quantitative statements
    numeric_matches = NUMERIC_PATTERN.findall(sentence)
    score += len(numeric_matches) * 1.0
    
    # 3. Capitalized entity mentions
    capitalized_terms = re.findall(r'\b[A-Z][a-z]+\b', sentence)
    score += min(3, len(capitalized_terms)) * 0.5
    
    # 4. Length penalty for too short or excessively long run-on sentences
    word_count = len(sentence.split())
    if word_count < 6:
        score -= 2.0
    elif word_count > 45:
        score -= 1.0
    else:
        score += 1.0
        
    return score

def extract_claims(sentences: List[str], max_claims: int = 6) -> List[Dict[str, Any]]:
    """
    Extract the top factual verifiable claims from candidate sentences.
    Returns:
        [
            {
                "id": "c1",
                "text": "Astronomers identified water vapor signatures on exoplanet LHS 1140 b.",
                "status": "INSUFFICIENT_EVIDENCE",
                "confidence": 0.0,
                "evidenceIds": []
            }
        ]
    """
    if not sentences:
        return []

    scored_candidates = []
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) >= 15:
            score = score_claim_sentence(s_clean)
            scored_candidates.append((score, s_clean))

    # Sort descending by claim salience
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    
    selected_claims = []
    seen_texts = set()
    
    for idx, (_, text) in enumerate(scored_candidates[:max_claims], start=1):
        if text not in seen_texts:
            seen_texts.add(text)
            selected_claims.append({
                "id": f"c{idx}",
                "text": text,
                "status": "INSUFFICIENT_EVIDENCE",
                "confidence": 0.0,
                "evidenceIds": []
            })
            
    # Fallback if no specific high-scoring claim sentence found
    if not selected_claims and sentences:
        selected_claims.append({
            "id": "c1",
            "text": sentences[0].strip(),
            "status": "INSUFFICIENT_EVIDENCE",
            "confidence": 0.0,
            "evidenceIds": []
        })

    return selected_claims
