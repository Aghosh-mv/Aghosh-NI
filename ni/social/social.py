"""
Social System - Multiple Brains

Intelligence isn't just individual. It's collective.
Multiple NI agents in the same world, interacting.

How they interact:
1. Observe each other's actions
2. Copy successful behaviors
3. Compete for resources
4. Form alliances
5. Develop communication signals
6. Create culture

This is how human intelligence evolved - socially.
"""

import time
import random
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class SocialSignal:
    """A signal between agents"""
    signal_id: str
    sender_id: str
    receiver_id: Optional[str]  # None = broadcast
    signal_type: str           # "warning", "food", "help", etc
    content: dict
    timestamp: float
    meaning: Optional[str] = None  # Learned meaning


@dataclass
class AgentObservation:
    """What one agent observed about another"""
    observer_id: str
    observed_id: str
    action: str
    result: dict
    timestamp: float
    learned: bool = False


class SocialSystem:
    """
    Social System.

    Multiple agents interacting in a shared world.
    They learn from each other, compete, cooperate.
    """

    def __init__(self):
        self.agents: dict[str, Any] = {}  # agent_id -> agent brain
        self.signals: list[SocialSignal] = []
        self.observations: list[AgentObservation] = []

        # Social dynamics
        self.signal_meanings: dict[str, dict] = {}  # signal_type -> learned meaning
        self.cultural_patterns: list[dict] = []  # Emergent social norms

        # Communication
        self.vocabulary: dict[str, str] = {}  # signal -> meaning
        self.next_signal_id = 0

    def register_agent(self, agent_id: str, brain):
        """Register an agent in the social system"""
        self.agents[agent_id] = brain

    def broadcast_signal(self, sender_id: str, signal_type: str, content: dict) -> SocialSignal:
        """Send a signal to all agents"""
        signal = SocialSignal(
            signal_id=f"sig_{self.next_signal_id}",
            sender_id=sender_id,
            receiver_id=None,
            signal_type=signal_type,
            content=content,
            timestamp=time.time(),
        )
        self.next_signal_id += 1
        self.signals.append(signal)
        return signal

    def send_signal(self, sender_id: str, receiver_id: str, signal_type: str, content: dict) -> SocialSignal:
        """Send a signal to a specific agent"""
        signal = SocialSignal(
            signal_id=f"sig_{self.next_signal_id}",
            sender_id=sender_id,
            receiver_id=receiver_id,
            signal_type=signal_type,
            content=content,
            timestamp=time.time(),
        )
        self.next_signal_id += 1
        self.signals.append(signal)
        return signal

    def observe_agent(self, observer_id: str, observed_id: str, action: str, result: dict):
        """Record an observation of another agent's behavior"""
        observation = AgentObservation(
            observer_id=observer_id,
            observed_id=observed_id,
            action=action,
            result=result,
            timestamp=time.time(),
        )
        self.observations.append(observation)

    def learn_from_observations(self, agent_id: str) -> list[dict]:
        """
        Agent learns from observing others.
        This is social learning - imitation.
        """
        learnings = []

        for obs in self.observations:
            if obs.observer_id == agent_id and not obs.learned:
                # Learn from this observation
                learning = {
                    "observed_agent": obs.observed_id,
                    "observed_action": obs.action,
                    "observed_result": obs.result,
                    "success": obs.result.get("success", False),
                }

                if learning["success"]:
                    # Successful action - worth imitating
                    learnings.append(learning)
                    obs.learned = True

        return learnings

    def detect_cultural_patterns(self) -> list[dict]:
        """
        Detect emergent cultural patterns.
        When multiple agents do the same thing, it becomes a norm.
        """
        patterns = []

        # Group observations by action
        action_counts: dict[str, int] = {}
        for obs in self.observations:
            action = obs.action
            action_counts[action] = action_counts.get(action, 0) + 1

        # Find common actions (cultural patterns)
        for action, count in action_counts.items():
            if count > 3:  # Threshold for "cultural"
                pattern = {
                    "action": action,
                    "frequency": count,
                    "agents_involved": len(set(
                        obs.observer_id for obs in self.observations if obs.action == action
                    )),
                }
                patterns.append(pattern)

        self.cultural_patterns = patterns
        return patterns

    def learn_signal_meaning(self, signal_type: str, context: dict, meaning: str):
        """Learn what a signal means based on context"""
        if signal_type not in self.signal_meanings:
            self.signal_meanings[signal_type] = {}

        self.signal_meanings[signal_type][meaning] = context

    def interpret_signal(self, signal: SocialSignal, context: dict) -> Optional[str]:
        """Interpret a signal based on learned meanings"""
        if signal.signal_type in self.signal_meanings:
            # Find best matching meaning
            for meaning, known_context in self.signal_meanings[signal.signal_type].items():
                # Simple matching
                if self._contexts_match(context, known_context):
                    return meaning

        return None

    def _contexts_match(self, ctx1: dict, ctx2: dict) -> bool:
        """Check if two contexts are similar"""
        # Simple matching
        common_keys = set(ctx1.keys()) & set(ctx2.keys())
        if not common_keys:
            return False

        matches = sum(1 for k in common_keys if ctx1[k] == ctx2[k])
        return matches / len(common_keys) > 0.5

    def get_state(self) -> dict:
        """Get social system state"""
        return {
            "agent_count": len(self.agents),
            "signal_count": len(self.signals),
            "observation_count": len(self.observations),
            "vocabulary_size": len(self.vocabulary),
            "cultural_patterns": len(self.cultural_patterns),
            "signal_meanings": len(self.signal_meanings),
        }
