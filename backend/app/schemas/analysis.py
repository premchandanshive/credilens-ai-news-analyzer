"""
CrediLens — Analysis Request & Response Schemas
Directly aligns with frontend/src/types/analysis.js and ARCHITECTURE.md specifications.
"""

from typing import List, Dict, Optional, Literal, Any
from pydantic import BaseModel, Field

class AnalyzeTextRequest(BaseModel):
    text: str = Field(min_length=10, max_length=100000)
    title: Optional[str] = None

class AnalyzeUrlRequest(BaseModel):
    url: str = Field(min_length=8, max_length=2048)

class ClaimSchema(BaseModel):
    id: str
    text: str
    status: Literal["SUPPORTED", "CONTRADICTED", "INSUFFICIENT_EVIDENCE"]
    confidence: float = 0.0
    evidenceIds: List[str] = Field(default_factory=list)

class SourceSchema(BaseModel):
    id: Optional[str] = None
    title: str
    url: str
    domain: str
    publisher: Optional[str] = None
    author: Optional[str] = None
    publishedAt: Optional[str] = None
    excerpt: str
    relevanceScore: int
    transparencyScore: int
    relationship: Literal["supports", "contradicts", "related", "insufficient"] = "related"

class FindingSchema(BaseModel):
    tone: Literal["positive", "warning", "negative", "info"]
    text: str
    basis: Literal["evidence", "language", "model", "source"]

class ModelExplanationFeature(BaseModel):
    feature: str
    weight: float

class ModelExplanationSchema(BaseModel):
    method: str = "feature_importance"
    topFeatures: List[ModelExplanationFeature] = Field(default_factory=list)

class ExplanationSchema(BaseModel):
    findings: List[FindingSchema] = Field(default_factory=list)
    modelExplanation: ModelExplanationSchema = Field(default_factory=ModelExplanationSchema)

class LanguageAnalysisSchema(BaseModel):
    sensationalismScore: int
    emotionalLanguage: str
    clickbaitIndicators: str
    absoluteClaimCount: int
    signals: List[str] = Field(default_factory=list)

class ComponentScoresSchema(BaseModel):
    aiClassification: int
    evidenceVerification: int
    sourceAnalysis: int
    languageAnalysis: int
    claimConsistency: int

class PredictionSchema(BaseModel):
    label: Literal["likely_reliable", "likely_unreliable", "uncertain"]
    modelName: str
    probabilities: Dict[str, float]
    aiClassificationScore: int

class EntitySchema(BaseModel):
    text: str
    label: str

class NlpDataSchema(BaseModel):
    entities: List[EntitySchema] = Field(default_factory=list)
    claimCount: int = 0

class AnalysisResponse(BaseModel):
    id: str
    userId: Optional[str] = None
    inputType: Literal["text", "url", "file"]
    inputText: Optional[str] = None
    inputUrl: Optional[str] = None
    fileName: Optional[str] = None
    title: str
    articleExcerpt: str = ""
    prediction: PredictionSchema
    credibilityScore: int
    credibilityBand: str
    disclaimer: str
    componentScores: ComponentScoresSchema
    weightsUsed: Optional[Dict[str, float]] = None
    claims: List[ClaimSchema] = Field(default_factory=list)
    sources: List[SourceSchema] = Field(default_factory=list)
    languageAnalysis: LanguageAnalysisSchema
    explanation: ExplanationSchema
    nlp: Optional[NlpDataSchema] = None
    status: Literal["completed", "failed", "partial"] = "completed"
    error: Optional[Dict[str, str]] = None
    createdAt: str

class HistoryListResponse(BaseModel):
    items: List[AnalysisResponse]
    total: int
    page: int
    limit: int

class SystemStatusResponse(BaseModel):
    api: bool = True
    database: bool = True
    models: bool = True
    nlp: bool = True
    evidence: bool = True
    searchKeyConfigured: bool = False
