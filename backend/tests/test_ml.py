"""
CrediLens — Machine Learning & Inference Unit Tests
"""

import pytest
from backend.app.ml.loader import model_manager
from backend.app.ml.inference import predict_credibility
from backend.app.explainability.feature_importance import get_feature_importance

def test_model_loading_and_inference():
    model_manager.load_models()
    assert model_manager.is_loaded is True

    # Test reliable text
    reliable_text = "Astronomers using the James Webb Space Telescope identified water vapor on exoplanet LHS 1140 b. The research was published in Astrophysical Journal Letters."
    pred_rel = predict_credibility(reliable_text)
    assert pred_rel["label"] in ("likely_reliable", "uncertain")
    assert "reliable" in pred_rel["probabilities"]
    assert 0 <= pred_rel["aiClassificationScore"] <= 100

    # Test sensational text
    unreliable_text = "SHOCKING TRUTH! Secret microchips found in all tap water to control human brainwaves! Share immediately before internet gets shut down!"
    pred_unrel = predict_credibility(unreliable_text)
    assert pred_unrel["label"] in ("likely_unreliable", "uncertain")
    assert pred_unrel["probabilities"]["unreliable"] >= 0.40

def test_feature_importance():
    model_manager.load_models()
    text = "Astronomers using telescope discovered new planet with water signatures."
    feat = get_feature_importance(text)
    assert "method" in feat
    assert "topFeatures" in feat
