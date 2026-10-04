"""
CrediLens — Language & Sensationalism Analyzer
Analyzes linguistic cues including sensationalism, clickbait markers, emotional intensity, and absolute claims.
"""

import re
from typing import Dict, Any, List

CLICKBAIT_TERMS = {
    "shocking", "miracle", "doctors hate", "one weird trick", "exposed",
    "unmasked", "secret", "top secret", "banned", "censored", "wake up sheeple",
    "you won't believe", "mind blowing", "bombshell", "forbidden", "leaked proof",
    "free money", "instant million", "don't let them", "they don't want you to know"
}

EMOTIONAL_TERMS = {
    "panic", "terrified", "emergency", "urgent warning", "apocalyptic",
    "sinister", "evil", "terrifying", "horrific", "furious", "outrageous",
    "nightmare", "disaster", "catastrophe", "invasion", "insane", "corrupt"
}

ABSOLUTE_TERMS = {
    "always", "never", "completely", "100%", "guaranteed", "impossible",
    "entirely", "totally", "every type", "destroys all", "cures all",
    "undeniable proof", "definitive proof"
}

def analyze_language(text: str) -> Dict[str, Any]:
    """
    Compute linguistic metrics and sensationalism signals.
    Returns:
        {
            "sensationalismScore": int (0-100),
            "emotionalLanguage": "low" | "moderate" | "high",
            "clickbaitIndicators": "low" | "moderate" | "high",
            "absoluteClaimCount": int,
            "signals": list[str]
        }
    """
    if not text or not text.strip():
        return {
            "sensationalismScore": 0,
            "emotionalLanguage": "low",
            "clickbaitIndicators": "low",
            "absoluteClaimCount": 0,
            "signals": ["No text provided for linguistic analysis."]
        }

    cleaned = text.strip()
    words = re.findall(r'\b[a-zA-Z0-9%\']+\b', cleaned)
    total_words = max(1, len(words))
    lower_text = cleaned.lower()

    # 1. Capitalization ratio (excluding short text)
    letters = [c for c in cleaned if c.isalpha()]
    total_letters = max(1, len(letters))
    uppercase_letters = sum(1 for c in letters if c.isupper())
    caps_ratio = uppercase_letters / total_letters

    # 2. Punctuation intensity (! and ?)
    exclamation_count = cleaned.count('!')
    question_count = cleaned.count('?')
    excessive_punct_matches = len(re.findall(r'[!?]{2,}', cleaned))
    punct_density = (exclamation_count + question_count) / total_words

    # 3. Clickbait markers
    clickbait_matches = []
    for phrase in CLICKBAIT_TERMS:
        if phrase in lower_text:
            clickbait_matches.append(phrase)

    # 4. Emotional language matches
    emotional_matches = []
    for term in EMOTIONAL_TERMS:
        if term in lower_text:
            emotional_matches.append(term)

    # 5. Absolute claims count
    absolute_matches = []
    for term in ABSOLUTE_TERMS:
        if term in lower_text:
            absolute_matches.append(term)

    # Compute continuous sensationalism score (0 to 100)
    # Higher score = more sensationalized / manipulative language
    raw_score = 0.0
    
    # Caps penalty
    if caps_ratio > 0.35:
        raw_score += 30.0
    elif caps_ratio > 0.15:
        raw_score += 15.0

    # Punctuation penalty
    if excessive_punct_matches > 0 or punct_density > 0.05:
        raw_score += min(25.0, (excessive_punct_matches * 10.0) + (punct_density * 100.0))

    # Clickbait phrases
    raw_score += min(30.0, len(clickbait_matches) * 12.0)

    # Emotional vocabulary
    raw_score += min(20.0, len(emotional_matches) * 8.0)

    # Absolute claims
    raw_score += min(15.0, len(absolute_matches) * 5.0)

    sensationalism_score = int(min(100, max(0, round(raw_score))))

    # Categorical labels
    if len(emotional_matches) >= 3 or (len(emotional_matches) >= 1 and caps_ratio > 0.25):
        emotional_level = "high"
    elif len(emotional_matches) >= 1 or caps_ratio > 0.12:
        emotional_level = "moderate"
    else:
        emotional_level = "low"

    if len(clickbait_matches) >= 2 or excessive_punct_matches >= 2:
        clickbait_level = "high"
    elif len(clickbait_matches) >= 1 or excessive_punct_matches >= 1:
        clickbait_level = "moderate"
    else:
        clickbait_level = "low"

    # Human-readable signals
    signals: List[str] = []
    if sensationalism_score < 25:
        signals.append("Objective, measured tone without excessive emotional framing.")
    else:
        if caps_ratio > 0.20:
            signals.append(f"Elevated uppercase lettering ({int(caps_ratio*100)}% of characters).")
        if exclamation_count >= 2:
            signals.append(f"High exclamation punctuation frequency ({exclamation_count} exclamation marks).")
        if clickbait_matches:
            signals.append(f"Clickbait phrase triggers detected: {', '.join(clickbait_matches[:3])}.")
        if emotional_matches:
            signals.append(f"High-intensity emotive vocabulary: {', '.join(emotional_matches[:3])}.")
        if absolute_matches:
            signals.append(f"Absolute unhedged claims detected: {', '.join(absolute_matches[:3])}.")

    return {
        "sensationalismScore": sensationalism_score,
        "emotionalLanguage": emotional_level,
        "clickbaitIndicators": clickbait_level,
        "absoluteClaimCount": len(absolute_matches),
        "signals": signals
    }
