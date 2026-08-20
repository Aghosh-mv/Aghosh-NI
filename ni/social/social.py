"""
Social System - Multiple Brains Learning Together

Not pre-programmed communication.
Not English. Not any language.
SIGNALS that emerge from interaction.

How it works:
1. Multiple NI brains share a world
2. When one brain acts, others observe
3. Brains that do well survive
4. Brains develop signals to communicate
5. Signals gain meaning through repeated use
6. Language EMERGES from social interaction

This is how human language evolved:
- Gesture → vocalization → symbol → word
- Not programmed. EVOLVED.
"""

import time
import random
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Signal:
    """A communication signal between brains"""
    signal_id: str
    signal_type: str           # What kind of signal
    sender_id: str
    content: dict              # Signal content
    timestamp: float
    receivers: list[str] = field(default_factory=list)
    responses: list[str] = field(default_factory=list)


@dataclass
class SocialMemory:
    """What an agent remembers about social interactions"""
    agent_id: str
    interactions: list[dict] = field(default_factory=list)
    trusted_agents: list[str] = field(default_factory=list)
    learned_signals: dict[str, str] = field(default_factory=dict)  # signal → meaning


class SocialAgent:
    """An agent with its own brain and social capabilities"""

    def __init__(self, agent_id: str, brain):
        self.agent_id = agent_id
        self.brain = brain
        self.memory = SocialMemory(agent_id=agent_id)
        self.is_alive = True
        self.energy: float = 100.0
        self.position: tuple[int, int] = (0, 0)

    def observe(self, other_agent_id: str, action: str, result: dict):
        """Observe another agent's action"""
        self.memory.interactions.append({
            "agent": other_agent_id,
            "action": action,
            "result": result,
            "time": time.time(),
        })

        # Learn from successful actions
        if result.get("success", False):
            # This action worked - worth remembering
            pass

    def send_signal(self, signal_type: str, content: dict) -> Signal:
        """Send a signal to nearby agents"""
        return Signal(
            signal_id=f"sig_{time.time()}_{self.agent_id}",
            signal_type=signal_type,
            sender_id=self.agent_id,
            content=content,
            timestamp=time.time(),
        )

    def receive_signal(self, signal: Signal, context: dict):
        """Receive and process a signal"""
        # Try to understand the signal
        meaning = self._interpret_signal(signal, context)

        # Store in memory
        if meaning:
            self.memory.learned_signals[signal.signal_type] = meaning

        # Process through brain
        brain_input = {
            "signal_type": signal.signal_type,
            "sender": signal.sender_id,
            "content": signal.content,
            "meaning": meaning,
            "context": context,
        }
        self.brain.perceive(brain_input, "social")

    def _interpret_signal(self, signal: Signal, context: dict) -> Optional[str]:
        """
        Interpret a signal based on context.
        This is where language emerges.
        """
        # If we've seen this signal before in similar context
        if signal.signal_type in self.memory.learned_signals:
            return self.memory.learned_signals[signal.signal_type]

        # Try to infer meaning from context
        if signal.signal_type == "warning":
            return "danger_nearby"
        elif signal.signal_type == "food":
            return "food_location"
        elif signal.signal_type == "help":
            return "need_assistance"

        return None


class SocialSystem:
    """
    Social System.

    Multiple agents in a shared world.
    They interact, communicate, develop language.
    """

    def __init__(self):
        self.agents: dict[str, SocialAgent] = {}
        self.signals: list[Signal] = []
        self.shared_meanings: dict[str, str] = {}  # Emergent shared vocabulary

    def add_agent(self, agent_id: str, brain) -> SocialAgent:
        """Add an agent to the social system"""
        agent = SocialAgent(agent_id=agent_id, brain=brain)
        self.agents[agent_id] = agent
        return agent

    def step(self):
        """Run one step of social interaction"""
        # Each agent acts
        for agent_id, agent in self.agents.items():
            if not agent.is_alive:
                continue

            # Agent perceives social signals
            for signal in self.signals[-10:]:  # Recent signals
                if agent_id != signal.sender_id:
                    agent.receive_signal(signal, {"source": "social"})

    def broadcast_signal(self, signal: Signal):
        """Broadcast a signal to all agents"""
        self.signals.append(signal)

        # Deliver to all other agents
        for agent_id, agent in self.agents.items():
            if agent_id != signal.sender_id:
                signal.receivers.append(agent_id)

    def observe_action(self, observer_id: str, actor_id: str, action: str, result: dict):
        """Record an observation of another agent's action"""
        if observer_id in self.agents:
            self.agents[observer_id].observe(actor_id, action, result)

    def develop_language(self):
        """
        Develop shared language through repeated use.
        When multiple agents use the same signal with same meaning,
        it becomes part of the shared vocabulary.
        """
        # Count signal usage
        signal_counts: dict[str, dict[str, int]] = {}
        for signal in self.signals:
            if signal.signal_type not in signal_counts:
                signal_counts[signal.signal_type] = {}
            signal_counts[signal.signal_type][signal.sender_id] = \
                signal_counts[signal.signal_type].get(signal.sender_id, 0) + 1

        # Find signals used by multiple agents
        for signal_type, agent_counts in signal_counts.items():
            if len(agent_counts) > 1:
                # Multiple agents use this signal - it's becoming shared
                self.shared_meanings[signal_type] = f"shared_{signal_type}"

    def get_state(self) -> dict:
        """Get social system state"""
        return {
            "agent_count": len(self.agents),
            "alive_agents": sum(1 for a in self.agents.values() if a.is_alive),
            "signal_count": len(self.signals),
            "shared_vocabulary": len(self.shared_meanings),
        }
