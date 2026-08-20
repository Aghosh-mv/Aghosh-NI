"""
Meta-Cognition - Thinking About Thinking

The brain doesn't just predict the world.
It predicts ITS OWN predictions.

"I think I'll predict X"
"I predict that my prediction will be wrong"
"I notice I'm confused about Y"

This is self-awareness. Not magic. Just another layer of prediction.
"""

import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetaPrediction:
    """A prediction about the brain's own predictions"""
    meta_id: str
    what: str                    # What the brain is predicting about itself
    prediction: str              # The meta-prediction
    confidence: float            # How confident (0-1)
    actual_outcome: Optional[str] = None  # What actually happened
    error: Optional[float] = None         # Meta-prediction error
    timestamp: float = 0.0


class MetaCognition:
    """
    Meta-Cognition System.

    The brain observes its own processes:
    1. Predicts what it will predict
    2. Notices when it's confused
    3. Tracks its own confidence
    4. Detects when it's wrong about itself
    5. Adjusts its self-model

    This is the beginning of self-awareness.
    """

    def __init__(self):
        self.meta_predictions: list[MetaPrediction] = []

        # Self-model
        self.self_model = {
            "prediction_accuracy": 0.5,     # How accurate are my predictions?
            "confusion_level": 0.0,         # How confused am I?
            "confidence_level": 0.5,        # How confident am I?
            "learning_rate": 0.1,           # How fast am I learning?
            "attention_span": 0.5,          # How long can I focus?
            "emotional_stability": 0.5,     # How stable are my emotions?
        }

        # History of self-observations
        self.self_observations: list[dict] = []

        # Meta-learning
        self.meta_learning_rate = 0.05

    def predict_own_prediction(self, context: dict) -> MetaPrediction:
        """
        Predict what the brain will predict about the world.
        This is thinking about thinking.
        """
        meta = MetaPrediction(
            meta_id=f"meta_{len(self.meta_predictions)}",
            what="my_own_prediction",
            prediction=self._generate_self_prediction(context),
            confidence=self.self_model["confidence_level"],
            timestamp=time.time(),
        )

        self.meta_predictions.append(meta)
        return meta

    def observe_own_performance(self, prediction_error: float, context: dict):
        """
        Observe how well the brain is performing.
        Update self-model based on performance.
        """
        # Update prediction accuracy
        accuracy = 1.0 - min(1.0, prediction_error)
        self.self_model["prediction_accuracy"] = (
            self.self_model["prediction_accuracy"] * 0.9 +
            accuracy * 0.1
        )

        # Update confusion level
        if prediction_error > 0.7:
            self.self_model["confusion_level"] = min(
                1.0,
                self.self_model["confusion_level"] + 0.1
            )
        else:
            self.self_model["confusion_level"] *= 0.9

        # Update confidence based on accuracy
        if accuracy > 0.7:
            self.self_model["confidence_level"] = min(
                1.0,
                self.self_model["confidence_level"] + 0.05
            )
        else:
            self.self_model["confidence_level"] *= 0.95

        # Record observation
        self.self_observations.append({
            "timestamp": time.time(),
            "prediction_error": prediction_error,
            "accuracy": accuracy,
            "confusion": self.self_model["confusion_level"],
            "confidence": self.self_model["confidence_level"],
            "context": str(context)[:100],
        })

        # Keep history bounded
        if len(self.self_observations) > 1000:
            self.self_observations = self.self_observations[-500:]

    def detect_confusion(self) -> float:
        """
        Detect if the brain is confused.
        Returns confusion level (0 = clear, 1 = very confused).
        """
        return self.self_model["confusion_level"]

    def detect_surprise_in_self(self, meta_prediction_error: float) -> dict:
        """
        Detect when the brain is surprised by its own behavior.
        This is the beginning of self-awareness.
        """
        surprise = {
            "magnitude": meta_prediction_error,
            "type": "self_surprise",
            "timestamp": time.time(),
        }

        if meta_prediction_error > 0.5:
            # I didn't expect to predict that!
            surprise["interpretation"] = "unexpected_self"
            self.self_model["confusion_level"] = min(
                1.0,
                self.self_model["confusion_level"] + 0.2
            )

        return surprise

    def _generate_self_prediction(self, context: dict) -> str:
        """Generate a prediction about the brain's own behavior"""
        # Simple self-prediction based on current state
        if self.self_model["confusion_level"] > 0.5:
            return "I will be confused"
        elif self.self_model["confidence_level"] > 0.7:
            return "I will be confident"
        elif self.self_model["prediction_accuracy"] < 0.3:
            return "I will make errors"
        else:
            return "I will perform normally"

    def get_self_model(self) -> dict:
        """Get the brain's model of itself"""
        return self.self_model.copy()

    def get_state(self) -> dict:
        """Get meta-cognition state"""
        return {
            "meta_predictions": len(self.meta_predictions),
            "self_observations": len(self.self_observations),
            "self_model": self.self_model,
            "confusion_level": self.self_model["confusion_level"],
            "confidence_level": self.self_model["confidence_level"],
        }
