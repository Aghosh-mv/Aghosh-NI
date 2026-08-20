"""
World - What the brain experiences

The brain doesn't know what "world" means.
It only knows: sensations come in, actions go out.

This module provides:
1. A world with things to discover
2. Sensations that flow into the brain
3. Actions that the brain can take
4. Consequences that feed back

The brain LEARNS what this all is through experience.
"""

import time
import random
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Sensation:
    """Raw sensory input - no interpretation"""
    modality: str          # "visual", "textual", "temporal", etc
    raw_data: Any          # Unprocessed data
    timestamp: float
    source: str


class World:
    """
    A world the brain can experience.

    The brain doesn't know:
    - What this world is
    - What "internet" means
    - What "files" are
    - What "text" means

    It discovers ALL of this through:
    1. Receiving sensations
    2. Taking actions
    3. Observing consequences
    4. Building models of what works
    """

    def __init__(self):
        self.time = 0.0
        self.sensations: list[Sensation] = []
        self.available_actions: dict[str, callable] = {}

        # Things in the world (brain discovers these exist)
        self.objects: dict[str, dict] = {}
        self.relationships: list[tuple[str, str, str]] = []

    def get_available_actions(self) -> list[str]:
        """Get list of available actions"""
        return list(self.available_actions.keys())

    def register_action(self, name: str, handler: callable):
        """Register an action the brain can try"""
        self.available_actions[name] = handler

    def step(self, dt: float = 0.1) -> list[Sensation]:
        """
        Advance the world. Returns new sensations.
        The brain receives these and must figure out what they mean.
        """
        self.time += dt
        new_sensations = []

        # Generate sensations from world state
        # (Brain doesn't know what these mean - it learns)
        for obj_id, obj_data in self.objects.items():
            # Object properties create sensations
            for prop, value in obj_data.get('properties', {}).items():
                sensation = Sensation(
                    modality=prop,
                    raw_data=value,
                    timestamp=self.time,
                    source=obj_id,
                )
                new_sensations.append(sensation)

        self.sensations.extend(new_sensations)
        return new_sensations

    def receive_action(self, action_type: str, parameters: dict) -> Optional[dict]:
        """
        Brain performs an action. World responds.
        Brain observes the consequence and learns.
        """
        if action_type in self.available_actions:
            try:
                result = self.available_actions[action_type](parameters)
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            # Action doesn't exist yet - brain learns this
            return {"success": False, "error": "unknown_action"}

    def add_object(self, obj_id: str, properties: dict):
        """Add something to the world"""
        self.objects[obj_id] = {"properties": properties}

    def get_state(self) -> dict:
        """Current world state (brain receives this as sensations)"""
        return {
            "time": self.time,
            "objects": len(self.objects),
            "available_actions": list(self.available_actions.keys()),
        }
