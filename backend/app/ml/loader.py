"""
CrediLens — ML Model Loader & Registry
Loads trained model pipelines once during application startup.
"""

import os
import joblib
from typing import Optional, Any

class ModelManager:
    _instance: Optional['ModelManager'] = None
    
    def __init__(self):
        self.baseline_pipeline: Optional[Any] = None
        self.transformer_pipeline: Optional[Any] = None
        self.model_name: str = "TF-IDF + Logistic Regression"
        self._is_loaded: bool = False

    @classmethod
    def get_instance(cls) -> 'ModelManager':
        if cls._instance is None:
            cls._instance = ModelManager()
        return cls._instance

    def load_models(self, baseline_path: str = "ml/saved_models/tfidf_logreg_credilens.joblib") -> bool:
        """Load saved models into memory."""
        if os.path.exists(baseline_path):
            try:
                self.baseline_pipeline = joblib.load(baseline_path)
                self.model_name = "TF-IDF + Logistic Regression"
                self._is_loaded = True
                print(f"[ML Loader] Baseline model successfully loaded from {baseline_path}")
                return True
            except Exception as e:
                print(f"[ML Loader] Warning: Failed to load baseline model: {e}")
                self._is_loaded = False
                return False
        else:
            print(f"[ML Loader] Model artifact not found at {baseline_path}.")
            self._is_loaded = False
            return False

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

# Global singleton instance
model_manager = ModelManager.get_instance()
