"""
World Interface - What the agent experiences

The agent doesn't know what "internet" is.
It doesn't know what "files" are.
It doesn't know what "text" means.

It only knows: sensations come in, actions go out.
Everything else it LEARNS through exploration.
"""

import time
import random
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Sensation:
    """Raw sensory input - no interpretation"""
    modality: str          # "visual", "auditory", "textual", "temporal"
    raw_data: Any          # The actual data (unprocessed)
    timestamp: float
    source: str            # Where it came from
    metadata: dict = field(default_factory=dict)


@dataclass
class Action:
    """An action the agent can take"""
    action_type: str       # What kind of action
    parameters: dict       # Action parameters
    timestamp: float


class WorldInterface:
    """
    The boundary between agent and world.

    The agent doesn't know what this world IS.
    It only knows: sensations come in, actions go out.

    Over time, it learns:
    - What different sensations mean
    - What actions have what effects
    - What patterns exist
    - What "internet" is (eventually)
    """

    def __init__(self):
        self.sensation_history: list[Sensation] = []
        self.action_history: list[Action] = []

        # Available action channels (agent discovers these)
        self.available_channels: dict[str, callable] = {}

        # Sensory buffers (raw, unprocessed)
        self.sensory_buffer: list[Sensation] = []

    def register_channel(self, name: str, handler: callable):
        """Register an action channel (agent discovers these exist)"""
        self.available_channels[name] = handler

    def receive_sensation(self, sensation: Sensation):
        """Receive raw sensation from world"""
        self.sensory_buffer.append(sensation)
        self.sensation_history.append(sensation)

        # Keep history bounded
        if len(self.sensation_history) > 10000:
            self.sensation_history = self.sensation_history[-5000:]

    def perform_action(self, action: Action) -> Optional[Any]:
        """Perform action and return result"""
        self.action_history.append(action)

        # Execute if channel exists
        if action.action_type in self.available_channels:
            try:
                result = self.available_channels[action.action_type](action.parameters)
                return result
            except Exception as e:
                return {"error": str(e)}
        else:
            # Channel doesn't exist - agent learns this action does nothing
            return {"result": "no_effect", "channel": action.action_type}

    def get_recent_sensations(self, n: int = 10) -> list[Sensation]:
        """Get recent sensations"""
        return self.sensation_history[-n:]

    def get_available_actions(self) -> list[str]:
        """What actions are possible?"""
        return list(self.available_channels.keys())
