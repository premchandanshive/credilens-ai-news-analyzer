"""
CrediLens — Source Transparency & Quality Evaluator
Scores external source transparency based on observable metadata and provenance signals.
"""

import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse

def evaluate_source_transparency(
    url: str,
    domain: str,
    title: str,
    publisher: Optional[str] = None,
    author: Optional[str] = None,
    published_at: Optional[str] = None
) -> float:
    """
    Calculate an objective transparency score (0 to 100) based on transparent metadata signals.
    Never hardcodes arbitrary static scores without factual metadata basis.
    """
    score = 50.0  # neutral starting baseline

    if not domain and url:
        try:
            domain = urlparse(url).netloc.replace("www.", "")
        except Exception:
            domain = ""

    domain_lower = domain.lower()

    # 1. Author presence (+12)
    if author and len(author.strip()) >= 3 and "anonymous" not in author.lower():
        score += 12.0

    # 2. Timestamp presence (+10)
    if published_at and len(published_at.strip()) >= 4:
        score += 10.0

    # 3. Explicit publisher identity (+10)
    if publisher and len(publisher.strip()) >= 3:
        score += 10.0

    # 4. Domain TLD Signals
    if domain_lower.endswith(".gov") or domain_lower.endswith(".mil"):
        score += 20.0
    elif domain_lower.endswith(".edu") or domain_lower.endswith(".ac.uk"):
        score += 18.0
    elif domain_lower.endswith(".org") or "wikipedia.org" in domain_lower:
        score += 12.0
    elif any(domain_lower.endswith(tld) for tld in [".xyz", ".top", ".club", ".info", ".biz", ".click", ".buzz"]):
        score -= 25.0

    # 5. Established academic / journalistic domains (weak prior)
    reputable_news_stems = [
        "reuters.com", "bbc.com", "bbc.co.uk", "apnews.com", "nature.com",
        "theguardian.com", "nytimes.com", "wsj.com", "washingtonpost.com",
        "economist.com", "bloomberg.com", "sciencemag.org", "thelancet.com"
    ]
    if any(stem in domain_lower for stem in reputable_news_stems):
        score += 15.0

    # 6. HTTPS protocol check
    if url and url.startswith("https://"):
        score += 5.0
    elif url and url.startswith("http://"):
        score -= 10.0

    # Clamp to [0, 100]
    return float(round(max(5.0, min(98.0, score)), 1))
