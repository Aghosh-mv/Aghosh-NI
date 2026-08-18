"""
Attention System - The Thalamus Equivalent

Not transformer attention. Not softmax over tokens.
A competitive routing system where information competes for access.

The thalamus is the brain's relay station:
- Sensory input comes in
- Only SOME gets through to cortex
- The rest is gated (inhibited)
- Competition determines what gets processed

Types of attention:
- Bottom-up: Salience-driven (something grabs your attention)
- Top-down: Goal-directed (you choose what to pay attention to)
- Competitive: Limited capacity (can only attend to a few things)
"""

import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class AttentionType(Enum):
    BOTTOM_UP = auto()    # Salience-driven (something grabs attention)
    TOP_DOWN = auto()     # Goal-directed (you choose what to attend)
    SUSTAINED = auto()    # Maintained focus on one thing
    DIVIDED = auto()      # Split attention across multiple things


@dataclass
class AttentionSignal:
    """A signal competing for attention."""
    source: str           # Where it came from
    content: dict         # What it contains
    salience: float       # How attention-grabbing (0-1)
    relevance: float      # How relevant to current goals (0-1)
    timestamp: float
    attention_type: AttentionType = AttentionType.BOTTOM_UP

    @property
    def priority(self) -> float:
        """Combined priority score."""
        if self.attention_type == AttentionType.BOTTOM_UP:
            return self.salience * 0.7 + self.relevance * 0.3
        else:  # TOP_DOWN
            return self.salience * 0.3 + self.relevance * 0.7


class AttentionGating:
    """
    The gating mechanism that filters information.

    Only information that passes the gate gets processed.
    This is the thalamus's filtering function.
    """

    def __init__(self, capacity: int = 4):
        self.capacity = capacity  # How many things can be attended at once
        self.gate_threshold = 0.3  # Minimum priority to pass
        self.attended: list[AttentionSignal] = []
        self.inhibited: list[AttentionSignal] = []

    def evaluate(self, signal: AttentionSignal) -> bool:
        """
        Should this signal pass the attention gate?
        Based on priority and current load.
        """
        # Check if gate is full
        if len(self.attended) >= self.capacity:
            # Can only attend if priority is very high
            if signal.priority < 0.7:
                self.inhibited.append(signal)
                return False

        # Check priority threshold
        if signal.priority < self.gate_threshold:
            self.inhibited.append(signal)
            return False

        # Pass the gate
        self.attended.append(signal)
        return True

    def release(self, signal: AttentionSignal):
        """Release attention from a signal."""
        if signal in self.attended:
            self.attended.remove(signal)

    def clear(self):
        """Clear all attended signals."""
        self.attended.clear()
        self.inhibited.clear()

    @property
    def utilization(self) -> float:
        """How full is the attention gate?"""
        return len(self.attended) / self.capacity


class Thalamus:
    """
    The Thalamus - Attention Routing Center.

    Responsibilities:
    1. Receive all incoming signals
    2. Route based on attention type
    3. Gate (filter) based on priority
    4. Send attended signals to cortex
    5. Suppress unattended signals
    """

    def __init__(self):
        self.gating = AttentionGating(capacity=4)

        # Current attention state
        self.current_focus: Optional[str] = None
        self.attention_type: AttentionType = AttentionType.BOTTOM_UP

        # Goal tracking (for top-down attention)
        self.active_goals: list[dict] = []

        # Signal history
        self.signal_history: list[AttentionSignal] = []
        self.max_history = 100

    def receive_signal(
        self,
        source: str,
        content: dict,
        salience: float = 0.5,
        relevance: float = 0.5,
        attention_type: AttentionType = AttentionType.BOTTOM_UP,
    ) -> bool:
        """
        Receive an attention signal.
        Returns True if signal passes the gate (is attended).
        """
        signal = AttentionSignal(
            source=source,
            content=content,
            salience=salience,
            relevance=relevance,
            timestamp=time.time(),
            attention_type=attention_type,
        )

        # Store in history
        self.signal_history.append(signal)
        if len(self.signal_history) > self.max_history:
            self.signal_history.pop(0)

        # Evaluate through gate
        passed = self.gating.evaluate(signal)

        if passed:
            # Update focus
            if self.gating.attended:
                highest_priority = max(self.gating.attended, key=lambda s: s.priority)
                self.current_focus = highest_priority.source

        return passed

    def set_goal(self, goal: dict):
        """
        Set a goal for top-down attention.
        Future signals relevant to this goal get priority boost.
        """
        self.active_goals.append(goal)
        self.attention_type = AttentionType.TOP_DOWN

    def clear_goals(self):
        """Clear all goals."""
        self.active_goals.clear()
        self.attention_type = AttentionType.BOTTOM_UP

    def compute_relevance(self, signal: AttentionSignal) -> float:
        """
        How relevant is this signal to current goals?
        Used for top-down attention.
        """
        if not self.active_goals:
            return 0.5  # No goals = neutral relevance

        # Simple relevance: check if signal content overlaps with goals
        relevance = 0.0
        for goal in self.active_goals:
            # Check key overlap
            goal_keys = set(goal.keys())
            signal_keys = set(signal.content.keys())
            overlap = len(goal_keys & signal_keys)
            if overlap > 0:
                relevance += 0.3

        return min(1.0, relevance)

    def release_attention(self):
        """Release all current attention."""
        self.gating.clear()
        self.current_focus = None

    def get_state(self) -> dict:
        """Get current attention state."""
        return {
            'current_focus': self.current_focus,
            'attention_type': self.attention_type.name,
            'attended_count': len(self.gating.attended),
            'inhibited_count': len(self.gating.inhibited),
            'utilization': self.gating.utilization,
            'active_goals': len(self.active_goals),
        }
