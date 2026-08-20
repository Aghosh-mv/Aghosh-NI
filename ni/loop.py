"""
NI Loop - Brain + World + Exploration

This is where it all comes together:
1. Brain receives sensations from world
2. Brain processes through mechanisms (spikes, oscillations, emotions)
3. Brain decides to act (exploration)
4. World responds
5. Brain observes consequence
6. Brain learns (Hebbian, emotional tagging, memory)

No LLM. No tokens. Just brain experiencing world.
"""

import time
import random
from typing import Optional

from .brain import NIBrain
from .world.world import World, Sensation
from .exploration.explorer import Explorer, ExplorationEvent
from .tools.internet import InternetTool, FileTool


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
        self.world = World()
        self.explorer = Explorer()

        # Tools (brain discovers these exist)
        self.internet = InternetTool()
        self.files = FileTool()

        # Register tools as world actions
        self.world.register_action("search_internet", self._action_search)
        self.world.register_action("read_file", self._action_read_file)
        self.world.register_action("write_file", self._action_write_file)
        self.world.register_action("list_files", self._action_list_files)

        # State
        self.step_count = 0
        self.exploration_events: list[ExplorationEvent] = []

    def _action_search(self, params: dict) -> dict:
        """Search the internet"""
        query = params.get("query", "")
        return self.internet.use(query)

    def _action_read_file(self, params: dict) -> dict:
        """Read a file"""
        filename = params.get("filename", "")
        return self.files.read(filename)

    def _action_write_file(self, params: dict) -> dict:
        """Write a file"""
        filename = params.get("filename", "")
        content = params.get("content", "")
        return self.files.write(filename, content)

    def _action_list_files(self, params: dict) -> dict:
        """List files"""
        return self.files.list_files()

    def run(self, steps: int = 1000, report_interval: int = 100):
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
        """
        self.running = True
        print(f"\n{'='*60}")
        print(f"NI LOOP STARTING: {self.name}")
        print(f"{'='*60}")

        for step in range(steps):
            if not self.running:
                break

            self.step_count = step + 1

            # 1. World generates sensations
            sensations = self.world.step(dt=0.1)

            # 2. Brain receives sensations
            for sensation in sensations:
                # Convert sensation to brain input
                brain_input = {
                    "modality": sensation.modality,
                    "value": sensation.raw_data,
                    "source": sensation.source,
                    "time": sensation.timestamp,
                }

                # 3. Brain processes
                result = self.brain.perceive(brain_input, sensation.source)

            # 4. Explorer chooses action
            available_actions = self.world.get_available_actions()
            action_type, parameters = self.explorer.choose_action(available_actions)

            if action_type:
                # 5. World responds to action
                result = self.world.receive_action(action_type, parameters)

                # 6. Brain observes consequence
                emotional_weight = self._compute_emotional_weight(result)
                exploration_event = ExplorationEvent(
                    action_type=action_type,
                    parameters=parameters,
                    result=result,
                    timestamp=time.time(),
                    emotional_weight=emotional_weight,
                )
                self.explorer.observe_result(exploration_event)
                self.exploration_events.append(exploration_event)

                # 7. Brain learns from this
                brain_input = {
                    "action": action_type,
                    "result": result,
                    "emotional_weight": emotional_weight,
                }
                self.brain.perceive(brain_input, "exploration")

            # Report progress
            if self.step_count % report_interval == 0:
                self._report()

        print(f"\n{'='*60}")
        print(f"NI LOOP FINISHED: {self.step_count} steps")
        print(f"{'='*60}")

    def _compute_emotional_weight(self, result: dict) -> float:
        """How emotionally significant is this result?"""
        if result.get("success", False):
            return 0.5  # Success is somewhat emotional
        else:
            return 0.3  # Failure is also informative

    def _report(self):
        """Print progress report"""
        brain_state = self.brain.get_state()
        explorer_stats = self.explorer.get_stats()

        print(f"\n--- Step {self.step_count} ---")
        print(f"Brain: {brain_state['network']['neurons']} neurons, "
              f"{brain_state['network']['synapses']} synapses")
        print(f"Network activity: {brain_state['network']['activity']:.3f}")
        print(f"Emotional state: {brain_state['emotions'].get('dominant_emotion', 'none')}")
        print(f"Exploration: {explorer_stats['total_events']} events, "
              f"curiosity={explorer_stats['curiosity']:.2f}")
        print(f"Tools discovered: internet={self.internet.discovered}, "
              f"files={self.files.discovered}")

    def stop(self):
        """Stop the loop"""
        self.running = False
