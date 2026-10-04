"""
CrediLens — Web Search Evidence Provider
Integrates Tavily, Serper, and DuckDuckGo search with robust multi-layer fallback.
"""

import httpx
from typing import List, Optional
from backend.app.evidence.base import SearchHit

class WebSearchProvider:
    name: str = "web_search"

    def __init__(
        self,
        tavily_key: Optional[str] = None,
        serper_key: Optional[str] = None,
        timeout: float = 8.0
    ):
        self.tavily_key = tavily_key
        self.serper_key = serper_key
        self.timeout = timeout

    async def search(self, query: str, limit: int = 4) -> List[SearchHit]:
        hits: List[SearchHit] = []
        if not query or not query.strip():
            return hits

        # 1. Try Tavily if configured
        if self.tavily_key:
            hits = await self._search_tavily(query, limit)
            if hits:
                return hits

        # 2. Try Serper if configured
        if self.serper_key:
            hits = await self._search_serper(query, limit)
            if hits:
                return hits

        # 3. Try DuckDuckGo
        hits = await self._search_ddg(query, limit)
        return hits

    async def _search_tavily(self, query: str, limit: int) -> List[SearchHit]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.tavily_key,
                        "query": query,
                        "search_depth": "basic",
                        "max_results": limit
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    hits = []
                    for r in results:
                        hits.append(SearchHit(
                            title=r.get("title", "Web Result"),
                            url=r.get("url", ""),
                            snippet=r.get("content", ""),
                            publisher=None,
                            author=None,
                            published_at=r.get("published_date")
                        ))
                    return hits
        except Exception as e:
            print(f"[WebSearch - Tavily] Error: {e}")
        return []

    async def _search_serper(self, query: str, limit: int) -> List[SearchHit]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    "https://google.serper.dev/search",
                    headers={"X-API-KEY": self.serper_key, "Content-Type": "application/json"},
                    json={"q": query, "num": limit}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    organic = data.get("organic", [])
                    hits = []
                    for item in organic:
                        hits.append(SearchHit(
                            title=item.get("title", "Web Result"),
                            url=item.get("link", ""),
                            snippet=item.get("snippet", ""),
                            published_at=item.get("date")
                        ))
                    return hits
        except Exception as e:
            print(f"[WebSearch - Serper] Error: {e}")
        return []

    async def _search_ddg(self, query: str, limit: int) -> List[SearchHit]:
        """DuckDuckGo instant search fallback."""
        hits = []
        try:
            from duckduckgo_search import DDGS
            with DDGS(timeout=5) as ddgs:
                results = list(ddgs.text(query, max_results=limit))
                for r in results:
                    hits.append(SearchHit(
                        title=r.get("title", "Web Result"),
                        url=r.get("href", ""),
                        snippet=r.get("body", "")
                    ))
        except Exception as e:
            # Fallback to direct duckduckgo instant answer API
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.get(
                        "https://api.duckduckgo.com/",
                        params={"q": query, "format": "json", "no_html": "1"}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        abstract = data.get("AbstractText")
                        url = data.get("AbstractURL")
                        title = data.get("Heading") or query
                        if abstract and url:
                            hits.append(SearchHit(title=title, url=url, snippet=abstract))
            except Exception as e2:
                print(f"[WebSearch - DDG Fallback] Error: {e2}")

        return hits
