"""
CrediLens — Evidence Cache
In-memory and hash-indexed cache to eliminate duplicate external network queries.
"""

import hashlib
import time
from typing import Dict, List, Optional
from backend.app.evidence.base import SearchHit

class EvidenceCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.ttl = ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _hash_query(self, query: str) -> str:
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def get(self, query: str) -> Optional[List[SearchHit]]:
        key = self._hash_query(query)
        entry = self._cache.get(key)
        if entry and (time.time() - entry['timestamp']) < self.ttl:
            return entry['hits']
        return None

    def set(self, query: str, hits: List[SearchHit]):
        key = self._hash_query(query)
        self._cache[key] = {
            'hits': hits,
            'timestamp': time.time()
        }

# Global cache instance
evidence_cache = EvidenceCache()
