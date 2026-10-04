"""
CrediLens — Report Generation Service
Prepares detailed structured academic reports for printable views and file downloads.
"""

from typing import Dict, Any
from backend.app.core.errors import NotFoundException
from backend.app.database.repositories import analysis_repo

class ReportService:
    async def generate_report_payload(self, analysis_id: str) -> Dict[str, Any]:
        analysis = await analysis_repo.get_by_id(analysis_id)
        if not analysis:
            raise NotFoundException(f"Analysis '{analysis_id}' not found.")

        return {
            "reportId": f"REP-{analysis['id'][-8:].upper()}",
            "generatedAt": analysis.get("createdAt"),
            "metadata": {
                "title": analysis.get("title"),
                "inputType": analysis.get("inputType"),
                "inputUrl": analysis.get("inputUrl"),
                "fileName": analysis.get("fileName"),
                "excerpt": analysis.get("articleExcerpt")
            },
            "assessment": {
                "credibilityScore": analysis.get("credibilityScore"),
                "credibilityBand": analysis.get("credibilityBand"),
                "disclaimer": analysis.get("disclaimer"),
                "componentScores": analysis.get("componentScores"),
                "weightsUsed": analysis.get("weightsUsed")
            },
            "mlModel": analysis.get("prediction"),
            "claimVerification": {
                "totalClaims": len(analysis.get("claims", [])),
                "claims": analysis.get("claims", [])
            },
            "sourceAnalysis": {
                "totalSources": len(analysis.get("sources", [])),
                "sources": analysis.get("sources", [])
            },
            "linguistics": analysis.get("languageAnalysis"),
            "explainability": analysis.get("explanation")
        }

report_service = ReportService()
