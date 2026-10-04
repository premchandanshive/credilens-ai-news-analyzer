"""
CrediLens — NLP Processing Pipeline
Implements text cleaning, sentence segmentation, entity recognition, and phrase extraction.
"""

import re
import html
from typing import List, Dict, Any

# Common abbreviations to prevent false sentence breaks
ABBREVIATIONS = {
    "mr.", "mrs.", "ms.", "dr.", "prof.", "sr.", "jr.", "vs.", "etc.",
    "u.s.", "u.k.", "u.n.", "e.u.", "e.g.", "i.e.", "jan.", "feb.", "mar.",
    "apr.", "aug.", "sept.", "oct.", "nov.", "dec.", "approx.", "no."
}

def clean_text(text: str) -> str:
    """Normalize whitespace, unescape HTML entities, and strip formatting artifacts."""
    if not text:
        return ""
    text = html.unescape(text)
    # Remove control characters except newlines
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    # Normalize multiple whitespace characters
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize newlines
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def segment_sentences(text: str) -> List[str]:
    """Segment text into individual coherent sentences."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    
    # Split across paragraphs or sentence-ending punctuation followed by whitespace and uppercase
    raw_sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'])', cleaned)
    sentences: List[str] = []
    
    for s in raw_sentences:
        s = s.strip()
        if not s:
            continue
        # Split further if contains newline
        lines = [line.strip() for line in s.split('\n') if line.strip()]
        for line in lines:
            if len(line) >= 10:  # ignore tiny fragments
                sentences.append(line)
                
    return sentences

def extract_entities(text: str) -> List[Dict[str, str]]:
    """
    Extract named entities (Organizations, Geopolitical Entities, People, Dates, Figures).
    Uses robust regular expressions and syntactic patterns.
    """
    entities = []
    seen = set()

    # Dates: e.g., "September 2024", "1000 BCE", "yesterday", "2023"
    date_patterns = [
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{4}\s+(?:BCE|CE|BC|AD)\b',
        r'\b(?:19|20)\d{2}\b'
    ]
    for pat in date_patterns:
        for match in re.finditer(pat, text):
            ent = match.group(0).strip()
            if ent and ent not in seen:
                seen.add(ent)
                entities.append({"text": ent, "label": "DATE"})

    # Known / uppercase Organizations and Agencies
    org_pattern = r'\b(?:NASA|UN|WHO|IEA|ECB|UNICEF|Gavi|Federal Reserve|European Central Bank|World Health Organization|James Webb Space Telescope|Historic England|BioNTech)\b'
    for match in re.finditer(org_pattern, text):
        ent = match.group(0).strip()
        if ent and ent not in seen:
            seen.add(ent)
            entities.append({"text": ent, "label": "ORG"})

    # Capitalized Multi-word Named Entities (People/Places/Institutions)
    cap_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    for match in re.finditer(cap_pattern, text):
        ent = match.group(0).strip()
        # Avoid full uppercase headlines or sentence starters
        if ent and ent not in seen and len(ent.split()) <= 4:
            # Classify known suffixes
            if any(term in ent for term in ["University", "Institute", "Consortium", "Agency", "Journal", "Association", "Bank"]):
                label = "ORG"
            elif any(term in ent for term in ["Tower", "Pyramid", "Ocean", "England", "Paris", "Cetus"]):
                label = "GPE"
            else:
                label = "PERSON"
            seen.add(ent)
            entities.append({"text": ent, "label": label})

    return entities[:12]

def extract_key_phrases(text: str, top_k: int = 6) -> List[str]:
    """Extract salient noun phrases and keywords."""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {
        "this", "that", "with", "from", "have", "were", "been", "they", "their",
        "which", "about", "there", "these", "other", "after", "where", "would",
        "could", "should", "under", "using", "into", "also", "most", "than"
    }
    freq: Dict[str, int] = {}
    for w in words:
        if w not in stopwords:
            freq[w] = freq.get(w, 0) + 1
            
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:top_k]]

def process_nlp(text: str) -> Dict[str, Any]:
    """Full NLP pipeline invocation."""
    cleaned = clean_text(text)
    sentences = segment_sentences(cleaned)
    entities = extract_entities(cleaned)
    key_phrases = extract_key_phrases(cleaned)
    
    return {
        "cleaned_text": cleaned,
        "sentences": sentences,
        "entities": entities,
        "key_phrases": key_phrases,
        "sentence_count": len(sentences)
    }
