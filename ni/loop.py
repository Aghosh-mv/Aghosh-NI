"""
NI Loop - Real Learning

Not just exploring. LEARNING.
Actions have consequences. Good actions get reinforced.
Bad actions get punished. The brain adapts.
"""

import time
import random
from typing import Optional

from .brain import NIBrain
from .world.grid_world import GridWorld
from .exploration.explorer import Explorer, ExplorationEvent


class NILoop:
    """
    The Natural Intelligence loop with REAL learning.

    Brain acts → World responds → Brain learns → Behavior changes
    """

    def __init__(self, name: str = "ni_loop"):
        self.name = name
        self.running = False

        # Core
        self.brain = NIBrain(name=f"{name}_brain")
        self.world = GridWorld(width=15, height=15)
        self.explorer = Explorer()

        # State
        self.step_count = 0
        self.total_reward = 0.0
        self.reward_history: list[float] = []

        # Tracking
        self.actions_taken = 0
        self.objects_discovered = set()
        self.behavior_changes: list[dict] = []

    def run(self, steps: int = 1000, report_interval: int = 100, sleep_interval: int = 200):
        """
        Run the NI loop with REAL learning.

        Key difference: Actions have REWARD consequences.
        """
        self.running = True
        print(f"\n{'='*60}")
        print(f"NI LOOP: {self.name}")
        print(f"World: {self.world.width}x{self.world.height}")
        print(f"Objects: {len(self.world.objects)}")
        print(f"{'='*60}")

        for step in range(steps):
            if not self.running:
                break

            self.step_count = step + 1

            # 1. Look around
            look_result = self.world.step("look", {"range": 5})
            sensations = look_result.get("sensations", [])

            # 2. Brain processes sensations
            for sensation in sensations:
                brain_input = {
                    "modality": sensation.get("modality", "unknown"),
                    "value": sensation.get("data", {}),
                    "source": "world",
                    "time": self.world.time,
                }
                result = self.brain.perceive(brain_input, "world")

            # 3. Choose action (with learning influence)
            action_type, parameters = self._choose_action()

            if action_type:
                # 4. Execute action
                world_result = self.world.step(action_type, parameters)
                self.actions_taken += 1

                # 5. Compute REWARD based on outcome
                reward = self._compute_action_reward(action_type, world_result)
                self.total_reward += reward
                self.reward_history.append(reward)

                # 6. Brain LEARNS from this action
                success = world_result.get("result", {}).get("success", False)
                action_record = self.brain.act(
                    action=action_type,
                    parameters=parameters,
                    world_feedback={"success": success, "reward": reward}
                )

                # 7. Track behavior changes
                self._track_behavior_change(action_type, reward)

                # 8. Discover objects
                if success:
                    for sensation in world_result.get("sensations", []):
                        if sensation.get("modality") == "visual":
                            obj_id = sensation.get("data", {}).get("object_id")
                            if obj_id:
                                self.objects_discovered.add(obj_id)

            # 9. Sleep periodically
            if self.step_count % sleep_interval == 0:
                print(f"\n--- Step {self.step_count}: Sleeping ---")
                self.brain.sleep(dream_duration=3)

            # 10. Report
            if self.step_count % report_interval == 0:
                self._report()

        print(f"\n{'='*60}")
        print(f"FINISHED: {self.step_count} steps")
        self._final_report()

    def _choose_action(self) -> tuple[str, dict]:
        """
        Choose action based on learned behavior.
        Brain prefers actions that worked before.
        """
        available_actions = list(self.world.actions.keys())

        # If brain has learned successful actions, prefer them
        if self.brain.successful_actions:
            # Get recent successful actions
            recent_successes = [a["action"] for a in self.brain.successful_actions[-20:]]

            # 70% chance to repeat successful action
            if random.random() < 0.7 and recent_successes:
                action = random.choice(recent_successes)
                return action, {}

        # Otherwise explore randomly
        action = random.choice(available_actions)
        return action, {}

    def _compute_action_reward(self, action: str, world_result: dict) -> float:
        """
        Compute reward for an action.
        This drives learning.
        """
        result = world_result.get("result", {})
        reward = 0.0

        if result.get("success", False):
            # Successful action = positive reward
            reward = 0.5

            # Extra reward for discovering new objects
            for sensation in world_result.get("sensations", []):
                if sensation.get("modality") == "visual":
                    obj_id = sensation.get("data", {}).get("object_id")
                    if obj_id and obj_id not in self.objects_discovered:
                        reward += 1.0  # Big reward for new discovery!

            # Extra reward for touching food
            if action == "touch":
                obj_type = result.get("type", "")
                if obj_type == "food":
                    reward += 0.3  # Food is good

        else:
            # Failed action = negative reward
            reason = result.get("reason", "")
            if reason == "blocked":
                reward = -0.2  # Hit a wall
            elif reason == "boundary":
                reward = -0.1  # Hit boundary
            else:
                reward = -0.1

        return reward

    def _track_behavior_change(self, action: str, reward: float):
        """Track if behavior is changing"""
        if len(self.reward_history) > 50:
            recent_avg = sum(self.reward_history[-50:]) / 50
            older_avg = sum(self.reward_history[-100:-50]) / 50 if len(self.reward_history) > 100 else recent_avg

            if abs(recent_avg - older_avg) > 0.1:
                self.behavior_changes.append({
                    "step": self.step_count,
                    "change": recent_avg - older_avg,
                    "direction": "improving" if recent_avg > older_avg else "declining",
                })

    def _report(self):
        """Print progress"""
        brain_state = self.brain.get_state()

        print(f"\n--- Step {self.step_count} ---")
        print(f"Brain: {brain_state['network']['neurons']} neurons, "
              f"{brain_state['network']['synapses']} synapses")
        print(f"Network activity: {brain_state['network']['activity']:.3f}")
        print(f"Total reward: {self.total_reward:.2f}")
        print(f"Avg reward (last 50): {brain_state['reward']['avg_reward']:.3f}")
        print(f"Success rate: {brain_state['actions']['success_rate']:.2%}")
        print(f"Objects discovered: {len(self.objects_discovered)}/{len(self.world.objects)}")
        print(f"Behavior changes: {len(self.behavior_changes)}")
        print(f"Curiosity: {brain_state['curiosity']['focus_level']:.2f}")
        print(f"Meta-cognition: confidence={brain_state['meta_cognition']['confidence_level']:.2f}, "
              f"confusion={brain_state['meta_cognition']['confusion_level']:.2f}")

    def _final_report(self):
        """Print final summary"""
        brain_state = self.brain.get_state()

        print(f"\n{'='*60}")
        print(f"FINAL REPORT")
        print(f"{'='*60}")
        print(f"Steps: {self.step_count}")
        print(f"Actions: {self.actions_taken}")
        print(f"Total reward: {self.total_reward:.2f}")
        print(f"Avg reward: {brain_state['reward']['avg_reward']:.3f}")
        print(f"Success rate: {brain_state['actions']['success_rate']:.2%}")
        print(f"Objects discovered: {len(self.objects_discovered)}/{len(self.world.objects)}")
        print(f"Neurons: {brain_state['network']['neurons']}")
        print(f"Synapses: {brain_state['network']['synapses']}")
        print(f"Total spikes: {brain_state['network']['total_spikes']}")
        print(f"Learning events: {brain_state['learning_events']}")
        print(f"Behavior changes: {len(self.behavior_changes)}")
        print(f"Curiosity: {brain_state['curiosity']['focus_level']:.2f}")
        print(f"Meta-cognition: {brain_state['meta_cognition']['confidence_level']:.2f}")
        print(f"{'='*60}")

    def stop(self):
        self.running = False
