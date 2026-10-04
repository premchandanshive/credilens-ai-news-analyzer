"""
CrediLens — Evidence Service Orchestrator
Coordinates external providers, ranking, verification, and source analysis.
"""

import asyncio
from typing import List, Dict, Any, Optional
from backend.app.evidence.base import SearchHit, ClaimVerificationResult, EvidenceProvider
from backend.app.evidence.wikipedia import WikipediaProvider
from backend.app.evidence.web_search import WebSearchProvider
from backend.app.evidence.ranker import rank_evidence
from backend.app.evidence.classify import classify_claim_verification
from backend.app.evidence.transparency import evaluate_source_transparency
from backend.app.evidence.cache import evidence_cache

class EvidenceService:
    def __init__(
        self,
        tavily_key: Optional[str] = None,
        serper_key: Optional[str] = None
    ):
        self.wiki_provider = WikipediaProvider()
        self.web_provider = WebSearchProvider(tavily_key=tavily_key, serper_key=serper_key)

    async def verify_claims(
        self,
        claims: List[Dict[str, Any]],
        article_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform evidence retrieval and verification for all extracted claims.
        Returns:
            {
                "verified_claims": list[dict],
                "matched_sources": list[dict],
                "evidence_verification_score": int (0-100),
                "source_transparency_score": int (0-100)
            }
        """
        if not claims:
            return {
                "verified_claims": [],
                "matched_sources": [],
                "evidence_verification_score": 50,
                "source_transparency_score": 50
            }

        verified_claims = []
        all_sources: Dict[str, Dict[str, Any]] = {}

        # Search for evidence for each claim asynchronously
        search_tasks = [self._search_for_claim(c, article_title) for c in claims]
        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        for claim_dict, result in zip(claims, results):
            if isinstance(result, Exception) or result is None:
                verified_claims.append({
                    "id": claim_dict.get("id", "c1"),
                    "text": claim_dict.get("text", ""),
                    "status": "INSUFFICIENT_EVIDENCE",
                    "confidence": 0.2,
                    "evidenceIds": []
                })
            else:
                ver_res: ClaimVerificationResult = result
                verified_claims.append({
                    "id": ver_res.claim_id,
                    "text": ver_res.claim_text,
                    "status": ver_res.status,
                    "confidence": ver_res.confidence,
                    "evidenceIds": ver_res.evidence_ids
                })

                # Aggregate sources
                for hit in ver_res.top_hits:
                    if hit.url and hit.url not in all_sources:
                        transparency = evaluate_source_transparency(
                            url=hit.url,
                            domain=hit.domain,
                            title=hit.title,
                            publisher=hit.publisher,
                            author=hit.author,
                            published_at=hit.published_at
                        )
                        hit.transparency_score = transparency
                        all_sources[hit.url] = {
                            "title": hit.title,
                            "url": hit.url,
                            "domain": hit.domain,
                            "publisher": hit.publisher,
                            "author": hit.author,
                            "publishedAt": hit.published_at,
                            "excerpt": hit.snippet[:240],
                            "relevanceScore": int(hit.relevance_score),
                            "transparencyScore": int(transparency),
                            "relationship": hit.relationship
                        }

        sources_list = list(all_sources.values())
        # Sort sources by relevance and transparency
        sources_list.sort(key=lambda s: (s["relevanceScore"] + s["transparencyScore"]), reverse=True)

        # Calculate component score: Evidence Verification Score (0-100)
        # Ratio of supported claims vs total
        supported = sum(1 for c in verified_claims if c["status"] == "SUPPORTED")
        contradicted = sum(1 for c in verified_claims if c["status"] == "CONTRADICTED")
        total = len(verified_claims)

        if total == 0:
            evidence_score = 50
        elif contradicted > 0:
            evidence_score = max(5, int(round((supported / total) * 60.0 - (contradicted * 25.0))))
        else:
            evidence_score = int(round(40.0 + (supported / total) * 55.0))

        evidence_score = max(0, min(100, evidence_score))

        # Calculate Source Transparency Score (0-100)
        if sources_list:
            avg_transparency = sum(s["transparencyScore"] for s in sources_list) / len(sources_list)
            source_score = int(round(avg_transparency))
        else:
            source_score = 50

        return {
            "verified_claims": verified_claims,
            "matched_sources": sources_list[:6],
            "evidence_verification_score": evidence_score,
            "source_transparency_score": source_score
        }

    async def _search_for_claim(self, claim: Dict[str, Any], article_title: Optional[str]) -> ClaimVerificationResult:
        claim_id = claim.get("id", "c1")
        claim_text = claim.get("text", "")
        
        # Check cache
        cached_hits = evidence_cache.get(claim_text)
        if cached_hits is None:
            # Query Wikipedia and Web Search concurrently
            wiki_task = self.wiki_provider.search(claim_text, limit=3)
            web_task = self.web_provider.search(claim_text, limit=3)
            
            wiki_hits, web_hits = await asyncio.gather(wiki_task, web_task, return_exceptions=True)
            
            combined_hits: List[SearchHit] = []
            if isinstance(wiki_hits, list):
                combined_hits.extend(wiki_hits)
            if isinstance(web_hits, list):
                combined_hits.extend(web_hits)
                
            # If nothing found with full claim, try title keywords
            if not combined_hits and article_title:
                title_hits = await self.wiki_provider.search(article_title, limit=2)
                if isinstance(title_hits, list):
                    combined_hits.extend(title_hits)

            ranked_hits = rank_evidence(claim_text, combined_hits)
            evidence_cache.set(claim_text, ranked_hits)
        else:
            ranked_hits = cached_hits

        return classify_claim_verification(claim_id, claim_text, ranked_hits)
