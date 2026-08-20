"""
Curiosity System - Deep Dive

When the brain finds something interesting, it focuses EXCLUSIVELY.
Not multitasking. Not scattered attention. DEEP FOCUS.

Like a child who finds a bug and watches it for an hour.
Or a scientist obsessed with one problem.

The brain:
1. Detects something novel/interesting
2. Enters "deep dive" mode
3. Ignores everything else
4. Explores the interesting thing from all angles
5. Extracts maximum understanding
6. Returns to normal when satisfied
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Any
from enum import Enum, auto


class CuriosityState(Enum):
    IDLE = auto()           # Normal exploration
    DETECTED = auto()       # Something interesting found
    FOCUSING = auto()       # Locking onto target
    DEEP_DIVE = auto()      # Full immersion
    SATIATED = auto()       # Understanding achieved
    EXTRACTING = auto()     # Pulling out knowledge


@dataclass
class CuriosityTarget:
    """Something the brain is curious about"""
    target_id: str
    description: str
    novelty_score: float        # How new is this?
    complexity_score: float     # How complex?
    relevance_score: float      # How relevant to current goals?
    exploration_count: int      # How many times explored
    understanding_level: float  # How well is it understood (0-1)
    first_encounter: float      # When first seen
    last_exploration: float     # When last explored
    angles_tried: list[str] = field(default_factory=list)  # What approaches tried


class CuriositySystem:
    """
    Curiosity-Driven Deep Dive System.

    When something is interesting, the brain LOCKS ON.
    Everything else is ignored until understanding is achieved.
    """

    def __init__(self):
        self.state = CuriosityState.IDLE
        self.current_target: Optional[CuriosityTarget] = None
        self.targets: dict[str, CuriosityTarget] = {}

        # Curiosity parameters
        self.novelty_threshold = 0.3     # Minimum novelty to trigger curiosity
        self.complexity_bonus = 0.2      # Extra score for complex things
        self.relevance_weight = 0.3      # How much relevance matters
        self.satiety_threshold = 0.8     # Understanding level to stop
        self.max_focus_duration = 100    # Max steps in deep dive

        # Statistics
        self.deep_dive_count = 0
        self.total_focus_time = 0
        self.knowledge_gained = 0

        # Focus history
        self.focus_history: list[dict] = []

    def detect_novelty(self, input_data: dict, prediction_error: float) -> Optional[str]:
        """
        Detect if something novel/interesting is present.
        Returns target_id if something curious is found.
        """
        # High prediction error = novelty
        if prediction_error < self.novelty_threshold:
            return None

        # Create target ID from input
        target_id = self._create_target_id(input_data)

        # Check if already tracking this
        if target_id in self.targets:
            target = self.targets[target_id]
            # Update novelty based on prediction error
            target.novelty_score = max(target.novelty_score, prediction_error)
            target.last_exploration = time.time()
            return target_id

        # Create new target
        target = CuriosityTarget(
            target_id=target_id,
            description=str(input_data)[:100],
            novelty_score=prediction_error,
            complexity_score=self._estimate_complexity(input_data),
            relevance_score=self._estimate_relevance(input_data),
            exploration_count=0,
            understanding_level=0.0,
            first_encounter=time.time(),
            last_exploration=time.time(),
        )

        self.targets[target_id] = target
        return target_id

    def should_deep_dive(self, target_id: str) -> bool:
        """Should we enter deep dive mode for this target?"""
        if target_id not in self.targets:
            return False

        target = self.targets[target_id]

        # Already deeply diving?
        if self.state == CuriosityState.DEEP_DIVE:
            return True

        # Check if worth diving into
        curiosity_score = (
            target.novelty_score * 0.4 +
            target.complexity_score * 0.3 +
            target.relevance_score * self.relevance_weight
        )

        # Not understood yet?
        if target.understanding_level < self.satiety_threshold:
            return curiosity_score > 0.5

        return False

    def enter_deep_dive(self, target_id: str):
        """Enter deep dive mode"""
        if target_id not in self.targets:
            return

        self.current_target = self.targets[target_id]
        self.state = CuriosityState.DEEP_DIVE
        self.deep_dive_count += 1

        self.focus_history.append({
            "target": target_id,
            "start_time": time.time(),
            "novelty": self.current_target.novelty_score,
        })

    def explore_during_dive(self, action: str, result: dict) -> dict:
        """
        During deep dive, explore the target from new angles.
        Returns insights gained.
        """
        if self.state != CuriosityState.DEEP_DIVE or not self.current_target:
            return {"insight": "not_in_deep_dive"}

        # Record this exploration angle
        angle = f"{action}_{len(self.current_target.angles_tried)}"
        self.current_target.angles_tried.append(angle)
        self.current_target.exploration_count += 1

        # Compute understanding gain
        understanding_gain = self._compute_understanding_gain(result)
        self.current_target.understanding_level = min(
            1.0,
            self.current_target.understanding_level + understanding_gain
        )

        # Update novelty (decreases as we understand)
        self.current_target.novelty_score *= 0.95

        # Check if satiated
        if self.current_target.understanding_level >= self.satiety_threshold:
            self.exit_deep_dive("understood")
            return {"insight": "target_understood", "level": self.current_target.understanding_level}

        self.total_focus_time += 1

        return {
            "insight": "exploring",
            "angle": angle,
            "understanding": self.current_target.understanding_level,
            "angles_tried": len(self.current_target.angles_tried),
        }

    def exit_deep_dive(self, reason: str):
        """Exit deep dive mode"""
        if self.current_target:
            self.focus_history[-1]["end_time"] = time.time()
            self.focus_history[-1]["reason"] = reason
            self.focus_history[-1]["understanding"] = self.current_target.understanding_level

        self.state = CuriosityState.IDLE
        self.current_target = None

    def _create_target_id(self, input_data: dict) -> str:
        """Create a unique ID for a curiosity target"""
        # Simple ID based on input keys
        keys = sorted(input_data.keys())
        return f"curious_{'_'.join(keys)}"

    def _estimate_complexity(self, input_data: dict) -> float:
        """Estimate how complex something is"""
        # More keys = more complex
        complexity = len(input_data) * 0.1
        # Nested structures = more complex
        for value in input_data.values():
            if isinstance(value, dict):
                complexity += 0.2
            elif isinstance(value, list):
                complexity += 0.15
        return min(1.0, complexity)

    def _estimate_relevance(self, input_data: dict) -> float:
        """Estimate how relevant something is"""
        # Default: everything is somewhat relevant
        return 0.5

    def _compute_understanding_gain(self, result: dict) -> float:
        """How much understanding did we gain from this exploration?"""
        # More successful actions = more understanding
        if result.get("success", False):
            return 0.1
        else:
            # Even failures teach us something
            return 0.05

    def get_focus_level(self) -> float:
        """How focused is the brain right now?"""
        if self.state == CuriosityState.DEEP_DIVE:
            return 1.0
        elif self.state == CuriosityState.DETECTED:
            return 0.5
        else:
            return 0.0

    def get_state(self) -> dict:
        """Get curiosity system state"""
        return {
            "state": self.state.name,
            "current_target": self.current_target.target_id if self.current_target else None,
            "target_count": len(self.targets),
            "deep_dive_count": self.deep_dive_count,
            "total_focus_time": self.total_focus_time,
            "focus_level": self.get_focus_level(),
        }
