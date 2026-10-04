"""
CrediLens — Wikipedia Evidence Provider
Retrieves encyclopedic summary evidence via the public MediaWiki API without requiring API keys.
"""

import httpx
from typing import List
from backend.app.evidence.base import SearchHit

class WikipediaProvider:
    name: str = "wikipedia"

    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.headers = {
            "User-Agent": "CrediLensAI/1.0 (academic misinformation analysis project; contact@credilens.local)"
        }

    async def search(self, query: str, limit: int = 4) -> List[SearchHit]:
        hits: List[SearchHit] = []
        if not query or not query.strip():
            return hits

        # Clean query terms
        clean_query = query.strip()[:100]

        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                # 1. OpenSearch to find relevant Wikipedia articles
                params = {
                    "action": "opensearch",
                    "search": clean_query,
                    "limit": limit,
                    "namespace": 0,
                    "format": "json"
                }
                resp = await client.get(self.api_url, params=params)
                if resp.status_code != 200:
                    return hits

                data = resp.json()
                if len(data) >= 4:
                    titles = data[1]
                    snippets = data[2]
                    urls = data[3]

                    for title, snippet, url in zip(titles, snippets, urls):
                        if url:
                            hits.append(SearchHit(
                                title=title,
                                url=url,
                                snippet=snippet or f"Wikipedia article regarding {title}.",
                                domain="en.wikipedia.org",
                                publisher="Wikipedia, The Free Encyclopedia",
                                author="Wikipedia Contributors",
                                transparency_score=85.0
                            ))
        except Exception as e:
            print(f"[Wikipedia Provider] Search error: {e}")

        return hits
