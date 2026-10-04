"""
CrediLens — Evidence Provider Protocol & Data Models
"""

from typing import Protocol, List, Optional, runtime_checkable
from dataclasses import dataclass, field
from urllib.parse import urlparse

@dataclass
class SearchHit:
    title: str
    url: str
    snippet: str
    domain: str = ""
    publisher: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[str] = None
    relevance_score: float = 0.0
    transparency_score: float = 50.0
    relationship: str = "related"  # supports | contradicts | related | insufficient

    def __post_init__(self):
        if not self.domain and self.url:
            try:
                parsed = urlparse(self.url)
                self.domain = parsed.netloc.replace("www.", "")
            except Exception:
                self.domain = "unknown"

@dataclass
class ClaimVerificationResult:
    claim_id: str
    claim_text: str
    status: str  # SUPPORTED | CONTRADICTED | INSUFFICIENT_EVIDENCE
    confidence: float
    evidence_ids: List[str] = field(default_factory=list)
    top_hits: List[SearchHit] = field(default_factory=list)

@runtime_checkable
class EvidenceProvider(Protocol):
    name: str

    async def search(self, query: str, limit: int = 4) -> List[SearchHit]:
        """Search external sources for evidence relating to query."""
        ...
