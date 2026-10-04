"""
CrediLens — Analysis Orchestrator Service
Coordinates end-to-end processing pipeline, database persistence, and SSE progress broadcasting.
"""

import uuid
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from backend.app.nlp.pipeline import process_nlp
from backend.app.nlp.claims import extract_claims
from backend.app.nlp.language import analyze_language
from backend.app.ml.inference import predict_credibility
from backend.app.evidence.service import EvidenceService
from backend.app.core.scoring import compute_credibility_score
from backend.app.explainability.evidence_reasons import generate_key_findings
from backend.app.explainability.feature_importance import get_feature_importance
from backend.app.database.repositories import analysis_repo
from backend.app.core.config import settings

# In-memory SSE event queue registry for active analyses
_progress_queues: Dict[str, asyncio.Queue] = {}

class AnalysisOrchestrator:
    def __init__(self):
        self.evidence_service = EvidenceService(
            tavily_key=settings.TAVILY_API_KEY,
            serper_key=settings.SERPER_API_KEY
        )

    async def _emit_progress(self, analysis_id: str, stage: str, label: str, done: bool = False):
        queue = _progress_queues.get(analysis_id)
        if queue:
            try:
                await queue.put({"stage": stage, "label": label, "done": done})
            except Exception:
                pass

    async def event_generator(self, analysis_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """SSE event stream generator for client progress subscriptions."""
        queue = asyncio.Queue()
        _progress_queues[analysis_id] = queue
        try:
            while True:
                # Wait for next progress event with timeout
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=45.0)
                    yield event
                    if event.get("stage") in ("completed", "failed"):
                        break
                except asyncio.TimeoutError:
                    break
        finally:
            _progress_queues.pop(analysis_id, None)

    async def run_analysis(
        self,
        input_type: str,
        text: str,
        title: Optional[str] = None,
        input_url: Optional[str] = None,
        file_name: Optional[str] = None,
        user_id: Optional[str] = None,
        max_claims: int = 6
    ) -> Dict[str, Any]:
        analysis_id = f"ana_{uuid.uuid4().hex[:16]}"
        
        try:
            # 1. Stage: Extracting Article
            await self._emit_progress(analysis_id, "extracting_article", "Extracting article content...", done=True)
            article_text = text.strip()
            article_title = (title or (article_text.split('\n')[0][:100] if article_text else "Untitled Article")).strip()
            article_excerpt = article_text[:280] + ("..." if len(article_text) > 280 else "")

            # 2. Stage: Analyzing Text (NLP)
            await self._emit_progress(analysis_id, "analyzing_text", "Performing NLP and entity recognition...", done=False)
            nlp_result = process_nlp(article_text)
            sentences = nlp_result["sentences"]
            entities = nlp_result["entities"]
            await self._emit_progress(analysis_id, "analyzing_text", "Text analyzed.", done=True)

            # 3. Stage: Extracting Claims
            await self._emit_progress(analysis_id, "extracting_claims", "Extracting factual claims...", done=False)
            claims = extract_claims(sentences, max_claims=max_claims)
            await self._emit_progress(analysis_id, "extracting_claims", f"Extracted {len(claims)} verifiable claims.", done=True)

            # 4. Stage: AI / ML Classification
            pred_result = predict_credibility(article_text, title=article_title)
            ai_score = pred_result["aiClassificationScore"]

            # 5. Stage: Searching Evidence
            await self._emit_progress(analysis_id, "searching_evidence", "Searching external evidence and databases...", done=False)
            evidence_result = await self.evidence_service.verify_claims(claims, article_title=article_title)
            verified_claims = evidence_result["verified_claims"]
            matched_sources = evidence_result["matched_sources"]
            evidence_score = evidence_result["evidence_verification_score"]
            source_score = evidence_result["source_transparency_score"]
            await self._emit_progress(analysis_id, "searching_evidence", "Evidence retrieved.", done=True)

            # 6. Stage: Evaluating Sources
            await self._emit_progress(analysis_id, "evaluating_sources", "Evaluating source transparency and citations...", done=True)

            # 7. Stage: Linguistic & Sensationalism Analysis
            language_analysis = analyze_language(article_text)
            sensationalism_score = language_analysis["sensationalismScore"]

            # 8. Stage: Calculating Credibility Score
            await self._emit_progress(analysis_id, "calculating_credibility", "Calculating credibility assessment...", done=False)
            score_data = compute_credibility_score(
                ai_score=ai_score,
                evidence_score=evidence_score,
                source_score=source_score,
                sensationalism_score=sensationalism_score,
                claims=verified_claims
            )
            await self._emit_progress(analysis_id, "calculating_credibility", "Credibility score calculated.", done=True)

            # 9. Stage: Generating Explanation
            await self._emit_progress(analysis_id, "generating_explanation", "Synthesizing explainability findings...", done=False)
            findings = generate_key_findings(
                claims=verified_claims,
                sources=matched_sources,
                language_analysis=language_analysis,
                prediction=pred_result,
                credibility_score=score_data["credibilityScore"]
            )
            model_explanation = get_feature_importance(article_text)
            await self._emit_progress(analysis_id, "generating_explanation", "Explanation ready.", done=True)

            # Assemble complete Analysis Document
            analysis_doc = {
                "id": analysis_id,
                "userId": user_id,
                "inputType": input_type,
                "inputText": article_text if input_type == "text" else None,
                "inputUrl": input_url,
                "fileName": file_name,
                "title": article_title,
                "articleExcerpt": article_excerpt,
                "prediction": pred_result,
                "credibilityScore": score_data["credibilityScore"],
                "credibilityBand": score_data["credibilityBand"],
                "disclaimer": score_data["disclaimer"],
                "componentScores": score_data["componentScores"],
                "weightsUsed": score_data["weightsUsed"],
                "claims": verified_claims,
                "sources": matched_sources,
                "languageAnalysis": language_analysis,
                "explanation": {
                    "findings": findings,
                    "modelExplanation": model_explanation
                },
                "nlp": {
                    "entities": entities,
                    "claimCount": len(verified_claims)
                },
                "status": "completed",
                "error": None
            }

            # Persist to database
            saved_doc = await analysis_repo.create(analysis_doc)
            
            # Emit completed event
            await self._emit_progress(analysis_id, "completed", "Analysis complete.", done=True)
            return saved_doc

        except Exception as e:
            print(f"[Orchestrator] Error during analysis: {e}")
            await self._emit_progress(analysis_id, "failed", f"Analysis failed: {str(e)}", done=True)
            raise e

orchestrator = AnalysisOrchestrator()
