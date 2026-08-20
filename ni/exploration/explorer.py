"""
Exploration - How the brain discovers things

The brain doesn't know what anything IS.
It discovers through:
1. Trying random actions
2. Observing what happens
3. Noticing patterns
4. Building models
5. Testing predictions

This is how a child learns:
- Touch fire → pain → "fire = danger"
- Press button → light → "button causes light"
- No one TELLS them. They DISCOVER.
"""

import time
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ExplorationEvent:
    """One exploration attempt"""
    action_type: str
    parameters: dict
    result: dict
    timestamp: float
    emotional_weight: float  # How surprising/noteworthy


class Explorer:
    """
    The exploration system.

    Drives the brain to:
    1. Try things it hasn't tried
    2. Repeat things that worked
    3. Avoid things that caused "pain"
    4. Explore unknown territories
    """

    def __init__(self):
        self.events: list[ExplorationEvent] = []
        self.tried_actions: dict[str, int] = {}  # action → times tried
        self.successful_actions: dict[str, int] = {}
        self.failed_actions: dict[str, int] = {}

        # Curiosity drive
        self.curiosity = 0.5  # 0 = no curiosity, 1 = maximum

        # Novelty seeking
        self.novelty_bonus = 0.3

    def choose_action(self, available_actions: list[str]) -> tuple[str, dict]:
        """
        Choose what to try next.
        Strategy: balance between:
        - Exploiting known good actions
        - Exploring unknown actions
        """
        if not available_actions:
            return None, {}

        # Score each action
        scores = []
        for action in available_actions:
            score = 0.0

            # Novelty score (never tried = high score)
            times_tried = self.tried_actions.get(action, 0)
            novelty = 1.0 / (1.0 + times_tried)
            score += novelty * self.novelty_bonus

            # Success rate (if tried before)
            successes = self.successful_actions.get(action, 0)
            if times_tried > 0:
                success_rate = successes / times_tried
                score += success_rate * 0.5

            # Curiosity bonus (random exploration)
            score += random.random() * self.curiosity * 0.2

            scores.append((score, action))

        # Choose action (weighted by score)
        scores.sort(reverse=True, key=lambda x: x[0])
        best_score, best_action = scores[0]

        # Sometimes explore randomly (exploration vs exploitation)
        if random.random() < self.curiosity * 0.3:
            best_action = random.choice(available_actions)

        # Generate random parameters for now
        # (Brain will learn what parameters work over time)
        parameters = self._generate_parameters(best_action)

        return best_action, parameters

    def observe_result(self, event: ExplorationEvent):
        """Observe what happened after an action"""
        self.events.append(event)

        # Update statistics
        action = event.action_type
        self.tried_actions[action] = self.tried_actions.get(action, 0) + 1

        if event.result.get("success", False):
            self.successful_actions[action] = self.successful_actions.get(action, 0) + 1
        else:
            self.failed_actions[action] = self.failed_actions.get(action, 0) + 1

        # Update curiosity based on novelty
        if event.emotional_weight > 0.5:
            # Surprising result → increase curiosity
            self.curiosity = min(1.0, self.curiosity + 0.05)
        elif event.emotional_weight < 0.1:
            # Boring result → decrease curiosity slightly
            self.curiosity = max(0.1, self.curiosity - 0.01)

    def _generate_parameters(self, action: str) -> dict:
        """Generate parameters for an action (brain learns what works)"""
        # Start with random parameters
        # Brain will learn which parameters produce good results
        return {
            "value": random.random(),
            "intensity": random.random(),
            "target": random.choice(["self", "environment", "unknown"]),
        }

    def get_curiosity_level(self) -> float:
        """How curious is the brain right now?"""
        return self.curiosity

    def get_stats(self) -> dict:
        """Exploration statistics"""
        return {
            "total_events": len(self.events),
            "unique_actions_tried": len(self.tried_actions),
            "curiosity": self.curiosity,
            "successful_actions": len(self.successful_actions),
            "failed_actions": len(self.failed_actions),
        }
