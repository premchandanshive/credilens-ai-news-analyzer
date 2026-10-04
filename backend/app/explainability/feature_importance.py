"""
CrediLens — Model Feature Importance Explainer
Computes active n-gram contributions for the specific text instance based on model weights.
"""

from typing import List, Dict, Any
from backend.app.ml.loader import model_manager

def get_feature_importance(text: str, top_k: int = 6) -> Dict[str, Any]:
    """
    Extract the top n-grams from the article and their directional weights.
    Returns:
        {
            "method": "feature_importance",
            "topFeatures": [{"feature": "scientists", "weight": 0.42}, ...]
        }
    """
    if not text or not model_manager.is_loaded or model_manager.baseline_pipeline is None:
        return {
            "method": "unavailable",
            "topFeatures": []
        }

    try:
        pipeline = model_manager.baseline_pipeline
        tfidf = pipeline.named_steps.get('tfidf')
        clf = pipeline.named_steps.get('clf')

        if tfidf is None or clf is None or not hasattr(clf, 'coef_'):
            return {"method": "unavailable", "topFeatures": []}

        feature_names = tfidf.get_feature_names_out()
        coefs = clf.coef_[0]
        
        # Transform the single document
        tfidf_vec = tfidf.transform([text]).tocsr()
        indices = tfidf_vec.indices
        data = tfidf_vec.data

        if len(indices) == 0:
            return {"method": "feature_importance", "topFeatures": []}

        contributions = []
        for idx, val in zip(indices, data):
            feature = feature_names[idx]
            weight = float(coefs[idx] * val)
            contributions.append({
                "feature": feature,
                "weight": round(weight, 4)
            })

        # Sort by absolute impact
        contributions.sort(key=lambda x: abs(x["weight"]), reverse=True)
        return {
            "method": "feature_importance",
            "topFeatures": contributions[:top_k]
        }
    except Exception as e:
        print(f"[Feature Importance] Error computing weights: {e}")
        return {"method": "unavailable", "topFeatures": []}
