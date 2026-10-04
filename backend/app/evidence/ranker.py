"""
CrediLens — Semantic Relevance Ranker
Computes semantic similarity between claims and retrieved evidence snippets.
"""

from typing import List
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.evidence.base import SearchHit

def rank_evidence(claim_text: str, hits: List[SearchHit]) -> List[SearchHit]:
    """
    Compute semantic relevance score between the claim and each search hit.
    Updates hit.relevance_score and returns hits sorted descending by relevance.
    """
    if not claim_text or not hits:
        return hits

    corpus = [claim_text] + [f"{h.title} {h.snippet}" for h in hits]
    
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Cosine similarity of each hit (indices 1..) against claim (index 0)
        claim_vec = tfidf_matrix[0:1]
        hit_vecs = tfidf_matrix[1:]
        
        sims = cosine_similarity(claim_vec, hit_vecs)[0]
        
        for idx, hit in enumerate(hits):
            score = float(sims[idx]) if idx < len(sims) else 0.0
            # Normalize to 0-100 scale
            hit.relevance_score = round(max(0.0, min(100.0, score * 100.0)), 2)
            
        # Sort descending
        hits.sort(key=lambda h: h.relevance_score, reverse=True)
    except Exception as e:
        print(f"[Evidence Ranker] Error ranking hits: {e}")
        for h in hits:
            h.relevance_score = 50.0

    return hits
