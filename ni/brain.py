"""
NI Brain - The Complete Natural Intelligence System

NOT a chatbot. NOT an LLM wrapper.
A system made of brain mechanisms that LEARNS and THINKS through those mechanisms.

Components:
- NeuralNetwork: Spiking neurons + Hebbian synapses
- NeuromodulationSystem: Dopamine, serotonin, etc.
- OscillationSystem: Gamma/theta timing
- EmotionalSystem: Importance weighting
- MemorySystem: Hippocampus + Neocortex + Cerebellum
- Thalamus: Attention routing

Behavior EMERGES from mechanisms interacting.
No central controller. No token prediction.
"""

import time
from typing import Optional

from .core.network import NeuralNetwork
from .core.neuromodulation import NeuromodulationSystem, Modulator
from .oscillation.oscillator import OscillationSystem, WaveType
from .emotion.amygdala import EmotionalSystem, EmotionType
from .memory.system import MemorySystem
from .attention.thalamus import Thalamus


class NIBrain:
    """
    The Natural Intelligence Brain.

    This is not a language model. This is a brain.
    It thinks through mechanisms, not token prediction.
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

        # State
        self.awake = True
        self.consciousness_level = 0.5  # 0 = unconscious, 1 = fully conscious
        self.internal_state = "baseline"

        # Experience counter
        self.experience_count = 0
        self.learning_events = 0

    def perceive(self, input_data: dict, source: str = "external") -> dict:
        """
        Perceive input from the world.
        This is the START of processing - not the end.

        Flow:
        1. Signal enters thalamus
        2. Thalamus gates (filters)
        3. If attended → process
        4. If not → inhibit
        """
        # 1. Thalamus receives signal
        # Compute salience based on novelty and emotional content
        salience = self._compute_salience(input_data)
        relevance = self.thalamus.compute_relevance(
            type('Signal', (), {'content': input_data})()
        )

        attended = self.thalamus.receive_signal(
            source=source,
            content=input_data,
            salience=salience,
            relevance=relevance,
        )

        if not attended:
            # Signal was inhibited - didn't pass attention gate
            return {"status": "inhibited", "reason": "low_priority"}

        # 2. Process attended signal
        result = self._process(input_data)

        # 3. Store in memory
        emotional_weight = self._compute_emotional_weight(input_data)
        self.memory.experience(input_data, emotional_weight)

        self.experience_count += 1

        return result

    def _process(self, input_data: dict) -> dict:
        """
        Process attended input through brain mechanisms.
        No LLM. Just mechanisms.
        """
        # 1. Generate neural activity based on input
        # Map input features to neurons
        for key, value in input_data.items():
            neuron_id = f"input_{key}"
            if neuron_id not in self.network.neurons:
                self.network.add_neuron(neuron_id)

            # Stimulate corresponding neuron
            if isinstance(value, (int, float)):
                self.network.stimulate(neuron_id, float(value))
            elif isinstance(value, str):
                # Map string to numeric stimulation
                hash_val = hash(value) % 100 / 100.0
                self.network.stimulate(neuron_id, hash_val * 10.0)

        # 2. Run network dynamics
        spikes = []
        for _ in range(10):  # 10 time steps
            step_spikes = self.network.step()
            spikes.extend(step_spikes)

        # 3. Update oscillations based on activity
        self.oscillations.update(dt=0.01)

        # 4. Compute emotional response
        emotional_tags = self._compute_emotions(input_data)

        # 5. Apply neuromodulation based on state
        self._update_neuromodulation(input_data, spikes)

        # 6. Generate response based on network state
        response = self._generate_response(spikes, emotional_tags)

        return response

    def _compute_salience(self, data: dict) -> float:
        """
        How attention-grabbing is this input?
        Based on novelty and emotional content.
        """
        # Check if we've seen similar input before
        similar_count = 0
        for memory in self.memory.hippocampus.memories.values():
            similarity = self.memory.hippocampus._compute_similarity(
                memory.content, data
            )
            if similarity > 0.5:
                similar_count += 1

        # Novelty = inverse of familiarity
        novelty = 1.0 / (1.0 + similar_count * 0.3)

        # Check emotional content
        emotional = 0.0
        for key, value in data.items():
            if isinstance(value, (int, float)):
                emotional += abs(value) * 0.1

        return min(1.0, novelty * 0.6 + emotional * 0.4)

    def _compute_emotional_weight(self, data: dict) -> float:
        """
        How emotionally significant is this input?
        Determines memory encoding strength.
        """
        # Simple heuristic: unexpected values are emotional
        weight = 0.0
        for key, value in data.items():
            if isinstance(value, (int, float)):
                # Extreme values are more emotional
                weight += abs(value) / 100.0
            elif isinstance(value, str):
                # Unknown strings are novel (emotional)
                weight += 0.1

        return min(1.0, weight)

    def _compute_emotions(self, data: dict) -> list:
        """
        Compute emotional tags for input.
        """
        tags = []

        # Check for novelty
        novelty = self._compute_salience(data)
        if novelty > 0.5:
            tag = self.emotions.tag_experience(
                EmotionType.NOVELTY,
                intensity=novelty,
                valence=0.3,  # Novelty is slightly positive
            )
            tags.append(tag)

        # Check for potential reward/punishment
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if value > 50:
                    tag = self.emotions.tag_experience(
                        EmotionType.REWARD,
                        intensity=value / 100.0,
                        valence=0.8,
                    )
                    tags.append(tag)
                elif value < -50:
                    tag = self.emotions.tag_experience(
                        EmotionType.PAIN,
                        intensity=abs(value) / 100.0,
                        valence=-0.8,
                    )
                    tags.append(tag)

        return tags

    def _update_neuromodulation(self, data: dict, spikes: list):
        """
        Update neuromodulation based on experience.
        """
        # Norepinephrine: increase with salience
        salience = self._compute_salience(data)
        self.neuromodulation.release(Modulator.NOREPINEPHRINE, salience * 0.3)

        # Dopamine: based on reward prediction error
        reward = sum(
            v for v in data.values()
            if isinstance(v, (int, float)) and v > 0
        )
        if reward > 0:
            self.neuromodulation.compute_reward_prediction_error(reward)

        # Acetylcholine: increase with novelty (LEARN THIS)
        novelty = self._compute_salience(data)
        if novelty > 0.5:
            self.neuromodulation.release(Modulator.ACETYLCHOLINE, 0.3)

        # Apply modulation to network
        plasticity_rate = self.neuromodulation.get_plasticity_rate()
        for synapse in self.network.synapses.values():
            synapse.plasticity_rate = plasticity_rate

    def _generate_response(self, spikes: list, emotional_tags: list) -> dict:
        """
        Generate response based on current brain state.
        Not token prediction - state-based response.
        """
        # Compute response based on:
        # 1. Network activity pattern
        # 2. Emotional state
        # 3. Oscillation state
        # 4. Attention focus

        response = {
            "status": "processed",
            "network_activity": self.network.network_activity,
            "dominant_emotion": self.emotions.get_dominant_emotion().name,
            "oscillation_state": self.oscillations.dominant_wave.name,
            "attention_focus": self.thalamus.current_focus,
            "spike_count": len(spikes),
            "neuromodulation": self.neuromodulation.get_state(),
        }

        return response

    def think(self, duration_ms: float = 100.0) -> dict:
        """
        Think for a duration.
        This is internal processing - no external input.
        Just the brain running its dynamics.
        """
        steps = int(duration_ms / 1.0)  # 1ms per step
        all_spikes = []

        for _ in range(steps):
            # Run network dynamics
            spikes = self.network.step()
            all_spikes.extend(spikes)

            # Update oscillations
            self.oscillations.update(dt=0.001)

            # Decay neuromodulation
            self.neuromodulation.decay(dt=0.001)

            # Decay emotions
            self.emotions.decay(dt=0.001)

        # Consolidate memories periodically
        self.memory.consolidate()

        return {
            "spikes": len(all_spikes),
            "activity": self.network.network_activity,
            "oscillations": self.oscillations.dominant_wave.name,
            "emotional_state": self.emotions.get_dominant_emotion().name,
        }

    def get_state(self) -> dict:
        """Get complete brain state."""
        return {
            "name": self.name,
            "age": time.time() - self.born_at,
            "awake": self.awake,
            "consciousness_level": self.consciousness_level,
            "internal_state": self.internal_state,
            "experience_count": self.experience_count,
            "learning_events": self.learning_events,
            "network": self.network.get_stats(),
            "memory": self.memory.get_stats(),
            "emotions": self.emotions.get_emotional_state(),
            "oscillations": self.oscillations.get_state(),
            "attention": self.thalamus.get_state(),
            "neuromodulation": self.neuromodulation.get_state(),
        }

    def __repr__(self):
        return (
            f"NIBrain({self.name}: "
            f"neurons={self.network.neuron_count}, "
            f"synapses={self.network.synapse_count}, "
            f"experiences={self.experience_count})"
        )
