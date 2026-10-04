"""
CrediLens — LIME Explainer Integration
Provides local interpretable model-agnostic explanations when suitable.
"""

from typing import Dict, Any, List
from backend.app.explainability.feature_importance import get_feature_importance

def explain_prediction(text: str, top_k: int = 6) -> Dict[str, Any]:
    """
    Generate model explanation using instance feature importance or LIME.
    """
    # Feature importance provides exact linear instance attribution
    return get_feature_importance(text, top_k=top_k)
