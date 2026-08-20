"""
NI Brain - Real Learning Through Reward

NOT just prediction errors. Real REWARD that drives behavior.

The brain needs:
1. Actions that have consequences (good/bad)
2. Reward signal (dopamine) that fires on success
3. Punishment signal that fires on failure
4. Learning that strengthens successful pathways
5. Memory that recalls what worked

Without reward, there's no learning. Just noise.
"""

import time
from typing import Optional

from .core.network import NeuralNetwork
from .core.neuromodulation import NeuromodulationSystem, Modulator
from .oscillation.oscillator import OscillationSystem
from .emotion.amygdala import EmotionalSystem, EmotionType
from .memory.system import MemorySystem
from .memory.dreams import DreamSystem
from .attention.thalamus import Thalamus
from .curiosity.meta_cognition import MetaCognitionSystem
from .curiosity.curiosity import CuriositySystem


class NIBrain:
    """
    The Natural Intelligence Brain.

    Learns through REWARD, not just prediction errors.
    Actions have consequences. Good actions get reinforced.
    """

    def __init__(self, name: str = "ni_brain"):
        self.name = name
        self.born_at = time.time()

        # Core systems
        self.network = NeuralNetwork()
        self.neuromodulation = NeuromodulationSystem()
        self.oscillations = OscillationSystem()
        self.emotions = EmotionalSystem()
        self.memory = MemorySystem()
        self.thalamus = Thalamus()
        self.dreams = DreamSystem()
        self.meta_cognition = MetaCognitionSystem(self.network)
        self.curiosity = CuriositySystem(self.network)

        # Create confidence/confusion trackers
        self.meta_cognition.create_confidence_tracker()

        # Predictive coding
        self.predictions: dict[str, float] = {}
        self.prediction_errors: list[float] = []

        # REWARD SYSTEM - This is what drives learning
        self.reward_history: list[float] = []
        self.total_reward: float = 0.0
        self.last_action_reward: float = 0.0

        # Action history (what worked, what didn't)
        self.successful_actions: list[dict] = []
        self.failed_actions: list[dict] = []

        # State
        self.awake = True
        self.experience_count = 0
        self.learning_events = 0

        # World model
        self.world_model: dict[str, Any] = {}

        # Active goals
        self.goals: list[str] = ["discover_objects", "survive", "learn"]

    def perceive(self, input_data: dict, source: str = "external") -> dict:
        """
        Perceive input from the world.
        Now with REWARD integration.
        """
        # 1. Generate prediction
        prediction = self._generate_prediction(input_data)

        # 2. Compute prediction error
        error = self._compute_prediction_error(input_data, prediction)

        # 3. Store prediction error
        self.prediction_errors.append(error)
        if len(self.prediction_errors) > 1000:
            self.prediction_errors = self.prediction_errors[-500:]

        # 4. Check if this was a rewarding/punishing experience
        reward = self._compute_reward(input_data, error)
        self.total_reward += reward
        self.last_action_reward = reward
        self.reward_history.append(reward)

        # 5. DOPAMINE: Fire on reward, strengthen pathways
        if reward > 0:
            self._fire_reward(reward)
        elif reward < 0:
            self._fire_punishment(abs(reward))

        # 6. Curiosity: detect novelty
        is_novel = self.curiosity.detect_novelty(error)
        if is_novel and not self.curiosity.is_focused:
            target_id = f"focus_{self.experience_count}"
            self.curiosity.activate_focus(target_id, list(self.network.neurons.keys()))
        elif self.curiosity.is_focused:
            self.curiosity.maintain_focus()

        # 7. Process through brain
        result = self._process_error(input_data, prediction, error)

        # 8. Store in memory with emotional weight
        emotional_weight = abs(reward) + error * 0.5
        self.memory.experience({
            "input": input_data,
            "prediction": prediction,
            "error": error,
            "reward": reward,
            "source": source,
        }, emotional_weight)

        # 9. Update predictions
        self._update_predictions(input_data, error)

        # 10. Update world model
        self._update_world_model(input_data, reward)

        self.experience_count += 1

        return {
            **result,
            "reward": reward,
            "total_reward": self.total_reward,
        }

    def act(self, action: str, parameters: dict, world_feedback: dict) -> dict:
        """
        Take an action and learn from the consequence.
        This is the main learning loop.
        """
        # Execute action
        success = world_feedback.get("success", False)
        reward = world_feedback.get("reward", 0.0)

        # Record action
        action_record = {
            "action": action,
            "parameters": parameters,
            "success": success,
            "reward": reward,
            "time": self.network.sim_time,
        }

        if success:
            self.successful_actions.append(action_record)
            # REINFORCE: strengthen this action pathway
            self._reinforce_action(action, reward)
        else:
            self.failed_actions.append(action_record)
            # PUNISH: weaken this action pathway
            self._punish_action(action, abs(reward))

        # Dopamine signal
        if reward > 0:
            self.neuromodulation.release(Modulator.DOPAMINE, reward * 0.5)

        return action_record

    def _compute_reward(self, input_data: dict, prediction_error: float) -> float:
        """
        Compute reward from experience.
        High prediction error + success = positive reward
        High prediction error + failure = negative reward
        """
        reward = 0.0

        # Reward for successful discovery
        if input_data.get("success", False):
            reward += 0.3

        # Reward for learning (reducing prediction error)
        if prediction_error < 0.3:
            reward += 0.2  # Good prediction = reward

        # Punishment for high prediction error
        if prediction_error > 0.7:
            reward -= 0.2  # Bad prediction = punishment

        return reward

    def _fire_reward(self, reward: float):
        """Fire dopamine on reward - strengthen everything active"""
        # Release dopamine
        self.neuromodulation.release(Modulator.DOPAMINE, reward * 0.5)

        # Increase plasticity
        for synapse in self.network.synapses.values():
            synapse.plasticity_rate = 2.0  # High plasticity on reward

        # Release acetylcholine (learning signal)
        self.neuromodulation.release(Modulator.ACETYLCHOLINE, 0.5)

    def _fire_punishment(self, punishment: float):
        """Fire punishment signal - weaken pathways"""
        # Norepinephrine (stress response)
        self.neuromodulation.release(Modulator.NOREPINEPHRINE, punishment * 0.3)

        # Reduce plasticity (stop learning temporarily)
        for synapse in self.network.synapses.values():
            synapse.plasticity_rate = 0.3  # Low plasticity on punishment

    def _reinforce_action(self, action: str, reward: float):
        """Strengthen neural pathways for successful actions"""
        # Find neurons related to this action
        action_neurons = [n for n in self.network.neurons if action in n]

        # Stimulate them with reward
        for neuron_id in action_neurons:
            self.network.stimulate(neuron_id, reward * 30.0)

        # Increase plasticity for reward-related synapses
        for synapse in self.network.synapses.values():
            if synapse.pre_id in action_neurons or synapse.post_id in action_neurons:
                synapse.plasticity_rate = 3.0  # Very high plasticity

    def _punish_action(self, action: str, punishment: float):
        """Weaken neural pathways for failed actions"""
        action_neurons = [n for n in self.network.neurons if action in n]

        for neuron_id in action_neurons:
            self.network.stimulate(neuron_id, -punishment * 20.0)

    def _process_error(self, input_data: dict, prediction: dict, error: float) -> dict:
        """Process prediction error through brain mechanisms"""
        # Create neurons for all input keys
        for key, value in input_data.items():
            neuron_id = f"error_{key}"
            if neuron_id not in self.network.neurons:
                self.network.add_neuron(neuron_id)

            # Error drives activity
            if isinstance(value, (int, float)):
                self.network.stimulate(neuron_id, error * 50.0)
            else:
                self.network.stimulate(neuron_id, error * 20.0)

        # Run network
        spikes = []
        for _ in range(10):
            step_spikes = self.network.step()
            spikes.extend(step_spikes)

        # Hebbian learning
        self._hebbian_connect(spikes)

        # Meta-cognition
        self.meta_cognition.step()
        self.meta_cognition.observe_prediction_error(error)

        # Oscillations
        self.oscillations.update(dt=0.01)
        if error > 0.5:
            self.oscillations.set_state("alert")
        elif error < 0.1:
            self.oscillations.set_state("relaxed")

        return {
            "status": "processed",
            "prediction_error": error,
            "network_activity": self.network.network_activity,
            "spike_count": len(spikes),
        }

    def _hebbian_connect(self, spikes: list):
        """Connect neurons that fire together"""
        spiked = [s.neuron_id for s in spikes]
        for i in range(len(spiked)):
            for j in range(i + 1, len(spiked)):
                pre_id = spiked[i]
                post_id = spiked[j]

                synapse_id = f"{pre_id}→{post_id}"
                if synapse_id not in self.network.synapses:
                    self.network.add_synapse(pre_id, post_id, weight=15.0)
                    self.learning_events += 1

                reverse_id = f"{post_id}→{pre_id}"
                if reverse_id not in self.network.synapses:
                    self.network.add_synapse(post_id, pre_id, weight=15.0)
                    self.learning_events += 1

    def _generate_prediction(self, input_data: dict) -> dict:
        """Generate prediction based on world model"""
        prediction = {}
        for key in input_data:
            if key in self.predictions:
                prediction[key] = self.predictions[key]
            elif key in self.world_model:
                prediction[key] = self.world_model[key]
            else:
                prediction[key] = 0.0
        return prediction

    def _compute_prediction_error(self, actual: dict, predicted: dict) -> float:
        """Compute prediction error"""
        total_error = 0.0
        count = 0
        for key in actual:
            if key in predicted and isinstance(actual[key], (int, float)):
                total_error += abs(actual[key] - predicted[key])
                count += 1
        return total_error / max(1, count)

    def _update_predictions(self, input_data: dict, error: float):
        """Update predictions based on error"""
        lr = self.neuromodulation.get_plasticity_rate() * 0.1
        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                current = self.predictions.get(key, 0.0)
                self.predictions[key] = current + lr * (value - current)

    def _update_world_model(self, input_data: dict, reward: float):
        """Update world model based on experience"""
        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                current = self.world_model.get(key, 0.0)
                self.world_model[key] = current + 0.05 * (value - current)

    def think(self, duration_ms: float = 100.0) -> dict:
        """Think internally"""
        steps = int(duration_ms / 1.0)
        all_spikes = []
        for _ in range(steps):
            spikes = self.network.step()
            all_spikes.extend(spikes)
            self.oscillations.update(dt=0.001)
            self.neuromodulation.decay(dt=0.001)
            self.emotions.decay(dt=0.001)
        self.memory.consolidate()
        return {"spikes": len(all_spikes), "activity": self.network.network_activity}

    def sleep(self, dream_duration: int = 5) -> dict:
        """Sleep and dream"""
        self.awake = False
        dream_result = self.dreams.dream(dream_duration)
        consolidation = self.dreams.consolidate()
        self.memory.consolidate()
        self.awake = True
        return {"status": "woke_up", "dreams": dream_result, "consolidation": consolidation}

    def get_state(self) -> dict:
        """Get complete brain state"""
        return {
            "name": self.name,
            "age": time.time() - self.born_at,
            "awake": self.awake,
            "experience_count": self.experience_count,
            "learning_events": self.learning_events,
            "network": self.network.get_stats(),
            "memory": self.memory.get_stats(),
            "dreams": self.dreams.get_state(),
            "emotions": self.emotions.get_emotional_state(),
            "oscillations": self.oscillations.get_state(),
            "attention": self.thalamus.get_state(),
            "neuromodulation": self.neuromodulation.get_state(),
            "meta_cognition": self.meta_cognition.get_state(),
            "curiosity": self.curiosity.get_state(),
            "reward": {
                "total": self.total_reward,
                "history_length": len(self.reward_history),
                "avg_reward": sum(self.reward_history[-100:]) / max(1, len(self.reward_history[-100:])),
            },
            "actions": {
                "successful": len(self.successful_actions),
                "failed": len(self.failed_actions),
                "success_rate": len(self.successful_actions) / max(1, len(self.successful_actions) + len(self.failed_actions)),
            },
        }

    def __repr__(self):
        return (
            f"NIBrain({self.name}: "
            f"neurons={self.network.neuron_count}, "
            f"synapses={self.network.synapse_count}, "
            f"reward={self.total_reward:.2f})"
        )
