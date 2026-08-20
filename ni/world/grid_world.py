"""
Grid World - An environment for the brain to explore

Not a game. Not a simulation.
A WORLD with objects, relationships, and consequences.

The brain doesn't know:
- What a "grid" is
- What "objects" are
- What "movement" means

It discovers ALL of this through experience.
"""

import random
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class WorldObject:
    """Something that exists in the world"""
    id: str
    obj_type: str       # "food", "wall", "agent", "tool", "unknown"
    x: int
    y: int
    properties: dict = field(default_factory=dict)
    alive: bool = True


class GridWorld:
    """
    A world the brain can experience.

    Simple grid. Objects exist. Brain moves around.
    Brain learns what things are through interaction.
    """

    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.time = 0
        self.step_count = 0

        # The brain's position (it doesn't know this yet)
        self.brain_x = width // 2
        self.brain_y = height // 2

        # Objects in the world
        self.objects: dict[str, WorldObject] = {}
        self.next_object_id = 0

        # History of sensations
        self.sensation_history: list[dict] = []

        # Actions available
        self.actions = {
            "move_up": self._move_up,
            "move_down": self._move_down,
            "move_left": self._move_left,
            "move_right": self._move_right,
            "look": self._look,
            "touch": self._touch,
            "take": self._take,
            "use": self._use,
        }

        # Initialize world with objects
        self._populate_world()

    def _populate_world(self):
        """Put things in the world (brain discovers them)"""
        # Food objects
        for _ in range(5):
            self._add_object("food", properties={
                "nutrition": random.uniform(0.3, 1.0),
                "taste": random.choice(["sweet", "sour", "bitter"]),
            })

        # Walls (obstacles)
        for _ in range(10):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not (x == self.brain_x and y == self.brain_y):
                self._add_object("wall", x=x, y=y, properties={
                    "material": random.choice(["stone", "wood", "metal"]),
                    "hardness": random.uniform(0.5, 1.0),
                })

        # Tools (things that can be used)
        for _ in range(3):
            self._add_object("tool", properties={
                "function": random.choice(["magnify", "amplify", "store", "transmit"]),
                "power": random.uniform(0.1, 1.0),
            })

        # Unknown objects (brain must figure out what these are)
        for _ in range(4):
            self._add_object("unknown", properties={
                "mystery": random.uniform(0.0, 1.0),
                "reacts_to_touch": random.choice([True, False]),
            })

    def _add_object(self, obj_type: str, x: int = None, y: int = None, properties: dict = None):
        """Add an object to the world"""
        if x is None:
            x = random.randint(0, self.width - 1)
        if y is None:
            y = random.randint(0, self.height - 1)
        if properties is None:
            properties = {}

        obj_id = f"obj_{self.next_object_id}"
        self.next_object_id += 1

        self.objects[obj_id] = WorldObject(
            id=obj_id,
            obj_type=obj_type,
            x=x,
            y=y,
            properties=properties,
        )

    def step(self, action: str, parameters: dict = None) -> dict:
        """
        Brain takes an action. World responds.
        Returns sensations the brain receives.
        """
        if parameters is None:
            parameters = {}

        self.step_count += 1
        self.time += 0.1

        # Execute action
        if action in self.actions:
            result = self.actions[action](parameters)
        else:
            result = {"success": False, "reason": "unknown_action"}

        # Generate sensations from result
        sensations = self._generate_sensations(action, result)

        # Natural world changes (things move, decay, etc)
        self._world_update()

        return {
            "action": action,
            "result": result,
            "sensations": sensations,
            "time": self.time,
            "step": self.step_count,
        }

    def _move_up(self, params: dict) -> dict:
        return self._move(0, -1)

    def _move_down(self, params: dict) -> dict:
        return self._move(0, 1)

    def _move_left(self, params: dict) -> dict:
        return self._move(-1, 0)

    def _move_right(self, params: dict) -> dict:
        return self._move(1, 0)

    def _move(self, dx: int, dy: int) -> dict:
        """Move brain in direction"""
        new_x = self.brain_x + dx
        new_y = self.brain_y + dy

        # Check bounds
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            return {"success": False, "reason": "boundary"}

        # Check for walls
        for obj in self.objects.values():
            if obj.obj_type == "wall" and obj.x == new_x and obj.y == new_y:
                return {"success": False, "reason": "blocked", "by": obj.id}

        # Move
        self.brain_x = new_x
        self.brain_y = new_y

        return {"success": True, "new_position": (new_x, new_y)}

    def _look(self, params: dict) -> dict:
        """Look around. What's nearby?"""
        visible = []
        look_range = params.get("range", 3)

        for obj in self.objects.values():
            if not obj.alive:
                continue
            dist = abs(obj.x - self.brain_x) + abs(obj.y - self.brain_y)
            if dist <= look_range:
                visible.append({
                    "id": obj.id,
                    "type": obj.obj_type,
                    "distance": dist,
                    "direction": self._get_direction(obj.x, obj.y),
                    "properties": obj.properties,
                })

        return {"success": True, "visible": visible, "position": (self.brain_x, self.brain_y)}

    def _touch(self, params: dict) -> dict:
        """Touch something nearby"""
        target_id = params.get("target")

        if not target_id:
            # Touch whatever is at current position
            for obj in self.objects.values():
                if obj.x == self.brain_x and obj.y == self.brain_y:
                    target_id = obj.id
                    break

        if target_id and target_id in self.objects:
            obj = self.objects[target_id]
            return {
                "success": True,
                "object": obj.id,
                "type": obj.obj_type,
                "properties": obj.properties,
                "reaction": f"Object {obj.id} reacts to touch",
            }

        return {"success": False, "reason": "nothing_to_touch"}

    def _take(self, params: dict) -> dict:
        """Take an object"""
        target_id = params.get("target")

        for obj in self.objects.values():
            if obj.x == self.brain_x and obj.y == self.brain_y:
                if obj.obj_type != "wall":
                    return {
                        "success": True,
                        "taken": obj.id,
                        "type": obj.obj_type,
                        "properties": obj.properties,
                    }

        return {"success": False, "reason": "nothing_to_take"}

    def _use(self, params: dict) -> dict:
        """Use something"""
        target_id = params.get("target")
        if target_id and target_id in self.objects:
            obj = self.objects[target_id]
            return {
                "success": True,
                "used": obj.id,
                "function": obj.properties.get("function", "unknown"),
                "effect": f"Used {obj.id}",
            }
        return {"success": False, "reason": "cant_use"}

    def _get_direction(self, obj_x: int, obj_y: int) -> str:
        """Get direction from brain to object"""
        dx = obj_x - self.brain_x
        dy = obj_y - self.brain_y
        if abs(dx) > abs(dy):
            return "east" if dx > 0 else "west"
        else:
            return "south" if dy > 0 else "north"

    def _generate_sensations(self, action: str, result: dict) -> list[dict]:
        """Generate raw sensations from action result"""
        sensations = []

        # Proprioception - where am I?
        sensations.append({
            "modality": "proprioception",
            "data": {"x": self.brain_x, "y": self.brain_y},
        })

        # Visual - what do I see?
        if result.get("success") and "visible" in result:
            for obj in result["visible"]:
                sensations.append({
                    "modality": "visual",
                    "data": {
                        "object_id": obj["id"],
                        "object_type": obj["type"],
                        "distance": obj["distance"],
                        "direction": obj["direction"],
                    },
                })

        # Tactile - what did I touch?
        if action == "touch" and result.get("success"):
            sensations.append({
                "modality": "tactile",
                "data": {
                    "object": result.get("object"),
                    "type": result.get("type"),
                    "properties": result.get("properties"),
                },
            })

        # Result feedback
        sensations.append({
            "modality": "feedback",
            "data": {"action": action, "success": result.get("success", False)},
        })

        return sensations

    def _world_update(self):
        """World changes over time"""
        # Objects might move slightly
        for obj in self.objects.values():
            if obj.obj_type == "food":
                # Food doesn't move
                pass
            elif obj.obj_type == "unknown":
                # Unknown objects might shift
                if random.random() < 0.01:
                    obj.x += random.choice([-1, 0, 1])
                    obj.y += random.choice([-1, 0, 1])
                    obj.x = max(0, min(self.width - 1, obj.x))
                    obj.y = max(0, min(self.height - 1, obj.y))

    def get_state(self) -> dict:
        """Current world state"""
        return {
            "time": self.time,
            "step": self.step_count,
            "brain_position": (self.brain_x, self.brain_y),
            "object_count": len([o for o in self.objects.values() if o.alive]),
            "available_actions": list(self.actions.keys()),
        }
