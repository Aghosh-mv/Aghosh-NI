"""
Dream Consolidation - Active Dreaming

Not replay. Not memory storage.
ACTIVE DREAMING - the brain generates new scenarios,
tests predictions, expands knowledge beyond experience.

During sleep:
1. Replay recent experiences
2. Extract patterns
3. DREAM new scenarios
4. Test predictions in dreams
5. Consolidate what worked
6. Wake up with expanded knowledge

This is how the brain creates imagination.
"""

import random
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Dream:
    """A single dream episode"""
    id: str
    scenario: dict           # What happened in the dream
    predictions: list[dict]  # What the brain predicted
    outcomes: list[dict]     # What actually "happened"
    errors: list[float]      # Prediction errors
    consolidated: bool       # Has this been consolidated?
    emotional_weight: float  # How important was this dream
    timestamp: float


class DreamSystem:
    """
    The Dream Consolidation System.

    This is NOT memory replay.
    This is ACTIVE IMAGINATION.

    The brain:
    1. Takes recent experiences
    2. Mutates them
    3. Creates new scenarios
    4. Runs predictions in the dream
    5. Observes outcomes
    6. Updates its model

    Dreams are SIMULATIONS that test the brain's model of reality.
    """

    def __init__(self):
        self.dreams: list[Dream] = []
        self.dream_count = 0

        # Experience buffer (recent experiences to dream about)
        self.experience_buffer: list[dict] = []
        self.buffer_max = 100

        # Dream parameters
        self.mutation_rate = 0.3      # How much to mutate experiences
        self.dream_intensity = 0.5    # How vivid dreams are
        self.consolidation_threshold = 0.3  # Min error to consolidate

        # Patterns extracted from dreams
        self.discovered_patterns: list[dict] = []

        # Dream history
        self.dream_history: list[dict] = []

    def buffer_experience(self, experience: dict):
        """Add experience to dream buffer"""
        self.experience_buffer.append(experience)
        if len(self.experience_buffer) > self.buffer_max:
            self.experience_buffer.pop(0)

    def dream(self, duration: int = 10) -> dict:
        """
        Have a dream session.

        duration: number of dream episodes to generate
        """
        self.dream_count += 1
        dream_session = {
            "id": f"dream_{self.dream_count}",
            "episodes": [],
            "patterns_found": 0,
            "total_error": 0,
        }

        for _ in range(duration):
            episode = self._dream_episode()
            dream_session["episodes"].append(episode)
            dream_session["total_error"] += sum(episode["errors"])

            # Extract patterns from low-error dreams
            if episode["avg_error"] < self.consolidation_threshold:
                pattern = self._extract_pattern(episode)
                if pattern:
                    self.discovered_patterns.append(pattern)
                    dream_session["patterns_found"] += 1

        self.dream_history.append(dream_session)
        return dream_session

    def _dream_episode(self) -> dict:
        """Generate one dream episode"""
        # 1. Select experience to mutate
        if self.experience_buffer:
            base_experience = random.choice(self.experience_buffer)
        else:
            # No experiences yet - dream about nothing
            base_experience = {"type": "void", "data": {}}

        # 2. Mutate the experience
        mutated = self._mutate_experience(base_experience)

        # 3. Generate predictions about what will happen
        predictions = self._generate_predictions(mutated)

        # 4. Simulate the dream scenario
        outcomes = self._simulate_scenario(mutated)

        # 5. Compute prediction errors
        errors = []
        for pred, outcome in zip(predictions, outcomes):
            error = self._compute_error(pred, outcome)
            errors.append(error)

        avg_error = sum(errors) / len(errors) if errors else 0.0

        # 6. Create dream
        dream = Dream(
            id=f"dream_{self.dream_count}_{len(self.dream_history)}",
            scenario=mutated,
            predictions=predictions,
            outcomes=outcomes,
            errors=errors,
            consolidated=False,
            emotional_weight=1.0 - avg_error,  # Good predictions = positive emotion
            timestamp=time.time(),
        )
        self.dreams.append(dream)

        return {
            "scenario_type": mutated.get("type", "unknown"),
            "predictions": len(predictions),
            "errors": errors,
            "avg_error": avg_error,
            "consolidated": avg_error < self.consolidation_threshold,
        }

    def _mutate_experience(self, experience: dict) -> dict:
        """Mutate an experience to create a dream scenario"""
        mutated = experience.copy()
        mutated_data = mutated.get("data", {}).copy()

        # Apply mutations
        for key in mutated_data:
            if isinstance(mutated_data[key], (int, float)):
                # Numerical values: add noise
                noise = random.gauss(0, self.mutation_rate)
                mutated_data[key] += noise
            elif isinstance(mutated_data[key], str):
                # Strings: sometimes change
                if random.random() < self.mutation_rate:
                    mutated_data[key] = f"dream_{mutated_data[key]}"

        # Sometimes add new elements
        if random.random() < self.mutation_rate:
            mutated_data["dream_element"] = random.choice([
                "flying", "falling", "speed", "discovery",
                "danger", "safety", "mystery", "clarity",
            ])

        mutated["data"] = mutated_data
        mutated["type"] = f"dream_{mutated.get('type', 'unknown')}"

        return mutated

    def _generate_predictions(self, scenario: dict) -> list[dict]:
        """Generate predictions about what will happen in dream"""
        predictions = []

        # Based on scenario type, predict outcomes
        scenario_type = scenario.get("type", "unknown")

        if "food" in scenario_type:
            predictions.append({
                "what": "taste",
                "prediction": random.choice(["sweet", "sour", "bitter"]),
                "confidence": 0.5,
            })
        elif "tool" in scenario_type:
            predictions.append({
                "what": "function",
                "prediction": scenario.get("data", {}).get("function", "unknown"),
                "confidence": 0.6,
            })
        else:
            predictions.append({
                "what": "outcome",
                "prediction": "unknown",
                "confidence": 0.3,
            })

        return predictions

    def _simulate_scenario(self, scenario: dict) -> list[dict]:
        """Simulate what happens in the dream scenario"""
        outcomes = []

        # Dream physics are loose - anything can happen
        for _ in range(random.randint(1, 3)):
            outcome = {
                "what": random.choice(["success", "failure", "surprise", "nothing"]),
                "intensity": random.random(),
                "duration": random.uniform(0.1, 1.0),
            }
            outcomes.append(outcome)

        return outcomes

    def _compute_error(self, prediction: dict, outcome: dict) -> float:
        """Compute prediction error in dream"""
        # Simple error metric
        pred_value = prediction.get("prediction", "")
        outcome_value = outcome.get("what", "")

        if pred_value == outcome_value:
            return 0.0  # Perfect prediction
        elif pred_value in str(outcome_value) or outcome_value in str(pred_value):
            return 0.3  # Partial match
        else:
            return 1.0  # Complete miss

    def _extract_pattern(self, episode: dict) -> Optional[dict]:
        """Extract a pattern from a successful dream"""
        if episode["avg_error"] > self.consolidation_threshold:
            return None

        # Pattern = what worked
        pattern = {
            "scenario_type": episode.get("scenario_type", "unknown"),
            "prediction_strategy": "default",
            "success_rate": 1.0 - episode["avg_error"],
            "discovered_at": time.time(),
        }

        return pattern

    def consolidate(self) -> dict:
        """
        Consolidate dreams into lasting knowledge.
        This is what happens during deep sleep.
        """
        consolidated = []
        forgotten = []

        for dream in self.dreams:
            if not dream.consolidated:
                # Dreams with low error get consolidated (strengthened)
                if dream.emotional_weight > 0.5:
                    dream.consolidated = True
                    consolidated.append(dream.id)
                else:
                    forgotten.append(dream.id)

        return {
            "consolidated": len(consolidated),
            "forgotten": len(forgotten),
            "total_dreams": len(self.dreams),
            "patterns_discovered": len(self.discovered_patterns),
        }

    def get_state(self) -> dict:
        """Get dream system state"""
        return {
            "dream_count": self.dream_count,
            "total_dreams": len(self.dreams),
            "buffer_size": len(self.experience_buffer),
            "patterns_discovered": len(self.discovered_patterns),
            "dream_intensity": self.dream_intensity,
        }
