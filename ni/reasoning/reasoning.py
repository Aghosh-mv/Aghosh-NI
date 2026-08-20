"""
Reasoning System - Emotional + Logical

Humans don't use pure logic OR pure emotion.
They use BOTH. Sometimes emotion leads, sometimes logic leads.

Example:
- Touching fire: EMOTION says "danger!" (fast, automatic)
- Solving math: LOGIC says "calculate" (slow, deliberate)
- Choosing food: BOTH (emotional preference + nutritional logic)

The brain switches between modes based on:
- Urgency (emotions for fast decisions)
- Complexity (logic for hard problems)
- Stakes (emotions for survival, logic for planning)
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum, auto


class ReasoningMode(Enum):
    EMOTIONAL = auto()      # Fast, intuitive, survival
    LOGICAL = auto()        # Slow, deliberate, planning
    HYBRID = auto()         # Both working together
    INTUITIVE = auto()      # Pattern matching (learned heuristics)


@dataclass
class ReasoningEpisode:
    """One reasoning episode"""
    episode_id: str
    mode: ReasoningMode
    input_data: dict
    emotional_input: dict
    logical_input: dict
    decision: Any
    confidence: float
    timestamp: float
    outcome: Optional[dict] = None


class ReasoningSystem:
    """
    Reasoning System.

    Combines emotional and logical processing.
    Like humans: sometimes feel first, sometimes think first.
    """

    def __init__(self):
        self.mode = ReasoningMode.HYBRID
        self.episodes: list[ReasoningEpisode] = []

        # Reasoning weights
        self.emotional_weight = 0.5
        self.logical_weight = 0.5

        # Learning
        self.mode_switches: dict[str, int] = {
            "emotional": 0,
            "logical": 0,
            "hybrid": 0,
            "intuitive": 0,
        }

        # Performance tracking
        self.emotional_accuracy = 0.5
        self.logical_accuracy = 0.5

    def reason(self, input_data: dict, emotional_state: dict, world_model: dict) -> dict:
        """
        Reason about a situation.
        Uses both emotional and logical inputs.
        """
        # Determine which mode to use
        mode = self._select_mode(input_data, emotional_state)

        # Get emotional reasoning
        emotional_result = self._emotional_reasoning(input_data, emotional_state)

        # Get logical reasoning
        logical_result = self._logical_reasoning(input_data, world_model)

        # Combine based on mode
        if mode == ReasoningMode.EMOTIONAL:
            decision = emotional_result
            confidence = emotional_result.get("confidence", 0.5)
        elif mode == ReasoningMode.LOGICAL:
            decision = logical_result
            confidence = logical_result.get("confidence", 0.5)
        elif mode == ReasoningMode.HYBRID:
            decision = self._combine_reasoning(emotional_result, logical_result)
            confidence = (emotional_result.get("confidence", 0.5) + logical_result.get("confidence", 0.5)) / 2
        else:  # INTUITIVE
            decision = self._intuitive_reasoning(input_data, emotional_state)
            confidence = 0.6

        # Record episode
        episode = ReasoningEpisode(
            episode_id=f"reason_{len(self.episodes)}",
            mode=mode,
            input_data=input_data,
            emotional_input=emotional_state,
            logical_input=world_model,
            decision=decision,
            confidence=confidence,
            timestamp=time.time(),
        )
        self.episodes.append(episode)

        # Update mode statistics
        self.mode_switches[mode.name.lower()] += 1

        return {
            "mode": mode.name,
            "decision": decision,
            "confidence": confidence,
            "emotional_contribution": emotional_result,
            "logical_contribution": logical_result,
        }

    def _select_mode(self, input_data: dict, emotional_state: dict) -> ReasoningMode:
        """Select which reasoning mode to use"""
        # High emotion = emotional mode
        total_emotion = sum(abs(v) for v in emotional_state.values() if isinstance(v, (int, float)))
        if total_emotion > 2.0:
            return ReasoningMode.EMOTIONAL

        # Complex input = logical mode
        complexity = len(input_data)
        if complexity > 5:
            return ReasoningMode.LOGICAL

        # Default: hybrid
        return ReasoningMode.HYBRID

    def _emotional_reasoning(self, input_data: dict, emotional_state: dict) -> dict:
        """Fast, intuitive reasoning based on emotions"""
        # Simple emotional logic
        if emotional_state.get("FEAR", 0) > 0.5:
            return {"action": "avoid", "confidence": 0.8, "reason": "fear"}
        elif emotional_state.get("REWARD", 0) > 0.5:
            return {"action": "approach", "confidence": 0.7, "reason": "reward"}
        elif emotional_state.get("CURIOSITY", 0) > 0.5:
            return {"action": "explore", "confidence": 0.6, "reason": "curiosity"}
        else:
            return {"action": "observe", "confidence": 0.5, "reason": "neutral"}

    def _logical_reasoning(self, input_data: dict, world_model: dict) -> dict:
        """Slow, deliberate reasoning based on logic"""
        # Simple logical reasoning
        # Check if we've seen this before
        input_str = str(sorted(input_data.items()))
        if input_str in world_model:
            past_result = world_model[input_str]
            return {"action": "repeat", "confidence": 0.7, "reason": "known_pattern"}
        else:
            return {"action": "explore", "confidence": 0.5, "reason": "unknown"}

    def _combine_reasoning(self, emotional: dict, logical: dict) -> dict:
        """Combine emotional and logical reasoning"""
        # If both agree, high confidence
        if emotional.get("action") == logical.get("action"):
            return {
                "action": emotional["action"],
                "confidence": (emotional["confidence"] + logical["confidence"]) / 2,
                "reason": "both_agree",
            }
        else:
            # Disagreement - use emotional for survival, logical for planning
            if emotional.get("reason") in ["fear", "danger"]:
                return emotional  # Emotion wins for survival
            else:
                return logical  # Logic wins for planning

    def _intuitive_reasoning(self, input_data: dict, emotional_state: dict) -> dict:
        """Pattern matching (learned heuristics)"""
        # Simple intuition based on past patterns
        return {"action": "intuitive", "confidence": 0.6, "reason": "pattern_match"}

    def update_performance(self, episode_id: str, outcome: dict):
        """Update performance based on outcome"""
        for episode in self.episodes:
            if episode.episode_id == episode_id:
                episode.outcome = outcome

                # Update accuracy based on outcome
                if outcome.get("success", False):
                    if episode.mode in [ReasoningMode.EMOTIONAL, ReasoningMode.HYBRID]:
                        self.emotional_accuracy = min(1.0, self.emotional_accuracy + 0.02)
                    if episode.mode in [ReasoningMode.LOGICAL, ReasoningMode.HYBRID]:
                        self.logical_accuracy = min(1.0, self.logical_accuracy + 0.02)
                else:
                    if episode.mode in [ReasoningMode.EMOTIONAL, ReasoningMode.HYBRID]:
                        self.emotional_accuracy = max(0.0, self.emotional_accuracy - 0.01)
                    if episode.mode in [ReasoningMode.LOGICAL, ReasoningMode.HYBRID]:
                        self.logical_accuracy = max(0.0, self.logical_accuracy - 0.01)
                break

    def get_state(self) -> dict:
        """Get reasoning system state"""
        return {
            "mode": self.mode.name,
            "episodes": len(self.episodes),
            "mode_switches": self.mode_switches,
            "emotional_accuracy": self.emotional_accuracy,
            "logical_accuracy": self.logical_accuracy,
            "emotional_weight": self.emotional_weight,
            "logical_weight": self.logical_weight,
        }
