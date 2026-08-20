"""
NI Loop - Brain + World + Exploration

This is where it all comes together:
1. Brain receives sensations from world
2. Brain processes through mechanisms (spikes, oscillations, emotions)
3. Brain decides to act (exploration)
4. World responds
5. Brain observes consequence
6. Brain learns (Hebbian, emotional tagging, memory)
7. Brain sleeps and dreams

No LLM. No tokens. Just brain experiencing world.
"""

import time
import random
from typing import Optional

from .brain import NIBrain
from .world.grid_world import GridWorld
from .exploration.explorer import Explorer, ExplorationEvent


class NILoop:
    """
    The complete Natural Intelligence loop.

    Brain + World + Exploration = Learning
    """

    def __init__(self, name: str = "ni_loop"):
        self.name = name
        self.running = False

        # Core components
        self.brain = NIBrain(name=f"{name}_brain")
        self.world = GridWorld(width=15, height=15)
        self.explorer = Explorer()

        # State
        self.step_count = 0
        self.exploration_events: list[ExplorationEvent] = []

        # Tracking
        self.total_prediction_error = 0.0
        self.actions_taken = 0
        self.objects_discovered = set()

    def run(self, steps: int = 1000, report_interval: int = 100, sleep_interval: int = 200):
        """
        Run the NI loop.

        For each step:
        1. World generates sensations
        2. Brain receives sensations
        3. Brain processes (spikes, oscillations, emotions)
        4. Explorer chooses action
        5. World responds to action
        6. Brain observes consequence
        7. Brain learns
        8. Periodically: brain sleeps and dreams
        """
        self.running = True
        print(f"\n{'='*60}")
        print(f"NI LOOP STARTING: {self.name}")
        print(f"World: {self.world.width}x{self.world.height} grid")
        print(f"Objects: {len(self.world.objects)}")
        print(f"{'='*60}")

        for step in range(steps):
            if not self.running:
                break

            self.step_count = step + 1

            # 1. Brain receives sensations from world
            # Look around first
            look_result = self.world.step("look", {"range": 5})
            sensations = look_result.get("sensations", [])

            # 2. Brain processes each sensation
            for sensation in sensations:
                brain_input = {
                    "modality": sensation.get("modality", "unknown"),
                    "value": sensation.get("data", {}),
                    "source": "world",
                    "time": self.world.time,
                }
                result = self.brain.perceive(brain_input, "world")

                # Track prediction error
                if "prediction_error" in result:
                    self.total_prediction_error += result["prediction_error"]

            # 3. Explorer chooses action
            available_actions = list(self.world.actions.keys())
            action_type, parameters = self.explorer.choose_action(available_actions)

            if action_type:
                # 4. World responds to action
                world_result = self.world.step(action_type, parameters)
                self.actions_taken += 1

                # 5. Brain observes consequence
                emotional_weight = self._compute_emotional_weight(world_result)
                exploration_event = ExplorationEvent(
                    action_type=action_type,
                    parameters=parameters,
                    result=world_result,
                    timestamp=time.time(),
                    emotional_weight=emotional_weight,
                )
                self.explorer.observe_result(exploration_event)
                self.exploration_events.append(exploration_event)

                # 6. Brain learns from this
                brain_input = {
                    "action": action_type,
                    "success": world_result.get("result", {}).get("success", False),
                    "emotional_weight": emotional_weight,
                    "world_state": self.world.get_state(),
                }
                self.brain.perceive(brain_input, "exploration")

                # Track discovered objects
                if world_result.get("result", {}).get("success"):
                    for sensation in world_result.get("sensations", []):
                        if sensation.get("modality") == "visual":
                            obj_id = sensation.get("data", {}).get("object_id")
                            if obj_id:
                                self.objects_discovered.add(obj_id)

            # 7. Brain sleeps periodically
            if self.step_count % sleep_interval == 0:
                print(f"\n--- Step {self.step_count}: Brain sleeping and dreaming ---")
                sleep_result = self.brain.sleep(dream_duration=3)
                print(f"Dreams: {sleep_result['dreams']['patterns_found']} patterns found")
                print(f"Consolidated: {sleep_result['consolidation']['consolidated']} memories")

            # Report progress
            if self.step_count % report_interval == 0:
                self._report()

        print(f"\n{'='*60}")
        print(f"NI LOOP FINISHED: {self.step_count} steps")
        print(f"{'='*60}")
        self._final_report()

    def _compute_emotional_weight(self, world_result: dict) -> float:
        """How emotionally significant is this result?"""
        result = world_result.get("result", {})
        if result.get("success", False):
            return 0.6  # Success is positive
        else:
            reason = result.get("reason", "")
            if reason == "blocked":
                return 0.4  # Hitting wall is somewhat significant
            elif reason == "boundary":
                return 0.3  # Hitting boundary is mild
            return 0.2

    def _report(self):
        """Print progress report"""
        brain_state = self.brain.get_state()
        explorer_stats = self.explorer.get_stats()

        print(f"\n--- Step {self.step_count} ---")
        print(f"Brain: {brain_state['network']['neurons']} neurons, "
              f"{brain_state['network']['synapses']} synapses")
        print(f"Network activity: {brain_state['network']['activity']:.3f}")
        print(f"Emotional state: {brain_state['emotions'].get('dominant_emotion', 'none')}")
        print(f"Oscillations: {brain_state['oscillations'].get('dominant_wave', 'none')}")
        print(f"Exploration: {explorer_stats['total_events']} events, "
              f"curiosity={explorer_stats['curiosity']:.2f}")
        print(f"Objects discovered: {len(self.objects_discovered)}/{len(self.world.objects)}")
        print(f"Avg prediction error: {self.total_prediction_error / max(1, self.step_count):.3f}")
        print(f"World model: {brain_state['world_model_size']} entries")
        print(f"Dreams: {brain_state['dreams']['total_dreams']} total, "
              f"{brain_state['dreams']['patterns_discovered']} patterns")

    def _final_report(self):
        """Print final summary"""
        brain_state = self.brain.get_state()
        explorer_stats = self.explorer.get_stats()

        print(f"\n{'='*60}")
        print(f"FINAL REPORT")
        print(f"{'='*60}")
        print(f"Total steps: {self.step_count}")
        print(f"Total actions: {self.actions_taken}")
        print(f"Objects discovered: {len(self.objects_discovered)}/{len(self.world.objects)}")
        print(f"Brain neurons: {brain_state['network']['neurons']}")
        print(f"Brain synapses: {brain_state['network']['synapses']}")
        print(f"Total experiences: {brain_state['experience_count']}")
        print(f"Predictions learned: {brain_state['predictions_learned']}")
        print(f"World model entries: {brain_state['world_model_size']}")
        print(f"Total dreams: {brain_state['dreams']['total_dreams']}")
        print(f"Dream patterns: {brain_state['dreams']['patterns_discovered']}")
        print(f"Average prediction error: {self.total_prediction_error / max(1, self.step_count):.3f}")
        print(f"Curiosity level: {explorer_stats['curiosity']:.2f}")
        print(f"{'='*60}")

    def stop(self):
        """Stop the loop"""
        self.running = False
