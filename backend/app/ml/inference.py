"""
CrediLens — ML Inference Engine
Performs calibrated prediction on input text using the loaded model artifact.
"""

from typing import Dict, Any, Optional
from backend.app.ml.loader import model_manager

def predict_credibility(text: str, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Predict credibility probabilities and score for an article or claim.
    Returns:
        {
            "label": "likely_reliable" | "likely_unreliable" | "uncertain",
            "modelName": str,
            "probabilities": {"reliable": float, "unreliable": float},
            "aiClassificationScore": int (0-100)
        }
    """
    full_text = f"{title or ''} {text}".strip()
    
    if not full_text:
        return {
            "label": "uncertain",
            "modelName": "Heuristic Default",
            "probabilities": {"reliable": 0.5, "unreliable": 0.5},
            "aiClassificationScore": 50
        }

    # If model is loaded, use calibrated pipeline prediction
    if model_manager.is_loaded and model_manager.baseline_pipeline is not None:
        try:
            pipeline = model_manager.baseline_pipeline
            # Probabilities: [P(unreliable=0), P(reliable=1)]
            probs = pipeline.predict_proba([full_text])[0]
            p_unreliable = float(probs[0])
            p_reliable = float(probs[1])
            
            # Map probability to continuous 0-100 score
            score = int(round(p_reliable * 100))
            score = max(0, min(100, score))
            
            if p_reliable >= 0.60:
                label = "likely_reliable"
            elif p_reliable <= 0.40:
                label = "likely_unreliable"
            else:
                label = "uncertain"
                
            return {
                "label": label,
                "modelName": model_manager.model_name,
                "probabilities": {
                    "reliable": round(p_reliable, 4),
                    "unreliable": round(p_unreliable, 4)
                },
                "aiClassificationScore": score
            }
        except Exception as e:
            print(f"[ML Inference] Error during model prediction: {e}")

    # Fallback heuristic prediction if model not loaded
    lower = full_text.lower()
    sensational_cues = ["shocking", "miracle", "secret", "exposed", "banned", "100%", "cure", "hoax", "conspiracy", "sheeple"]
    hits = sum(1 for c in sensational_cues if c in lower)
    
    if hits >= 2:
        p_rel = max(0.1, 0.5 - (hits * 0.15))
    else:
        p_rel = min(0.85, 0.55 + (0.05 if len(full_text) > 100 else 0.0))
        
    p_unrel = 1.0 - p_rel
    score = int(round(p_rel * 100))
    label = "likely_reliable" if score >= 60 else ("likely_unreliable" if score <= 40 else "uncertain")
    
    return {
        "label": label,
        "modelName": "Rule-Based Heuristic Fallback",
        "probabilities": {
            "reliable": round(p_rel, 4),
            "unreliable": round(p_unrel, 4)
        },
        "aiClassificationScore": score
    }
