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
- PredictiveCoding: Error-driven learning
- DreamSystem: Active imagination

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
from .memory.dreams import DreamSystem
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
        self.dreams = DreamSystem()

        # Predictive coding system
        self.predictions: dict[str, float] = {}
        self.prediction_errors: list[float] = []

        # State
        self.awake = True
        self.consciousness_level = 0.5
        self.internal_state = "baseline"

        # Experience counter
        self.experience_count = 0
        self.learning_events = 0

        # Current beliefs about the world
        self.world_model: dict[str, Any] = {}

    def perceive(self, input_data: dict, source: str = "external") -> dict:
        """
        Perceive input from the world.

        Flow:
        1. Compute prediction based on model
        2. Compare with actual input
        3. Compute prediction error
        4. Only prediction error propagates (PREDICTIVE CODING)
        5. Update model based on error
        6. If attended → process further
        """
        # 1. Generate prediction (what do I EXPECT?)
        prediction = self._generate_prediction(input_data)

        # 2. Compute prediction error (what's DIFFERENT?)
        error = self._compute_prediction_error(input_data, prediction)

        # 3. Store prediction error
        self.prediction_errors.append(error)
        if len(self.prediction_errors) > 1000:
            self.prediction_errors = self.prediction_errors[-500:]

        # 4. Thalamus receives prediction error (not raw input!)
        salience = abs(error)  # More surprising = more salient
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
            return {"status": "inhibited", "reason": "low_priority"}

        # 5. Process prediction error through brain mechanisms
        result = self._process_error(input_data, prediction, error)

        # 6. Store in memory
        emotional_weight = self._compute_emotional_weight(input_data, error)
        self.memory.experience(input_data, emotional_weight)

        # 7. Buffer for dreams
        self.dreams.buffer_experience({
            "input": input_data,
            "prediction": prediction,
            "error": error,
            "source": source,
        })

        # 8. Update predictions (learn from error)
        self._update_predictions(input_data, error)

        # 9. Update world model
        self._update_world_model(input_data, error)

        self.experience_count += 1

        return result

    def _generate_prediction(self, input_data: dict) -> dict:
        """
        Generate prediction based on current model.
        This is what the brain EXPECTS to see.
        """
        prediction = {}
        for key, value in input_data.items():
            if key in self.predictions:
                prediction[key] = self.predictions[key]
            elif key in self.world_model:
                prediction[key] = self.world_model[key]
            else:
                prediction[key] = 0.0
        return prediction

    def _compute_prediction_error(self, actual: dict, predicted: dict) -> float:
        """
        Compute prediction error.
        This is the KEY insight of predictive coding:
        Only SURPRISE propagates through the brain.
        """
        total_error = 0.0
        count = 0

        for key in actual:
            if key in predicted:
                if isinstance(actual[key], (int, float)):
                    error = abs(actual[key] - predicted[key])
                    total_error += error
                    count += 1

        if count == 0:
            return 0.0

        return total_error / count

    def _process_error(self, input_data: dict, prediction: dict, error: float) -> dict:
        """
        Process prediction error through brain mechanisms.
        The error IS the signal that drives learning.
        """
        # Generate neural activity based on ERROR (not input!)
        # Create neurons for ALL input keys (not just numeric)
        for key, value in input_data.items():
            neuron_id = f"error_{key}"
            if neuron_id not in self.network.neurons:
                self.network.add_neuron(neuron_id)

            # All inputs cause neural activity (error drives everything)
            if isinstance(value, (int, float)):
                # Numeric values: error drives activity
                self.network.stimulate(neuron_id, error * 50.0)
            else:
                # Non-numeric values: still cause some activity
                self.network.stimulate(neuron_id, error * 20.0)

        # Run network dynamics
        spikes = []
        for _ in range(10):
            step_spikes = self.network.step()
            spikes.extend(step_spikes)

        # HEBBIAN LEARNING: Connect neurons that fire together
        self._hebbian_connect(spikes)

        # Update oscillations based on error magnitude
        self.oscillations.update(dt=0.01)
        if error > 0.5:
            self.oscillations.set_state("alert")
        elif error < 0.1:
            self.oscillations.set_state("relaxed")

        # Compute emotional response to error
        emotional_tags = self._compute_emotions(input_data, error)

        # Apply neuromodulation based on error
        self._update_neuromodulation(error)

        # Generate response
        response = {
            "status": "processed",
            "prediction_error": error,
            "network_activity": self.network.network_activity,
            "dominant_emotion": self.emotions.get_dominant_emotion().name,
            "oscillation_state": self.oscillations.dominant_wave.name,
            "spike_count": len(spikes),
        }

        return response

    def _hebbian_connect(self, spikes: list):
        """
        Connect neurons that fire together.
        "Neurons that fire together wire together."
        """
        # Get neurons that spiked in this step
        spiked_neurons = [s.neuron_id for s in spikes]

        # Connect pairs of neurons that fired together
        for i in range(len(spiked_neurons)):
            for j in range(i + 1, len(spiked_neurons)):
                pre_id = spiked_neurons[i]
                post_id = spiked_neurons[j]

                # Check if synapse already exists
                synapse_id = f"{pre_id}→{post_id}"
                if synapse_id not in self.network.synapses:
                    # Create new synapse (fire together = wire together)
                    self.network.add_synapse(pre_id, post_id, weight=0.3)
                    self.learning_events += 1

                # Also connect in reverse direction
                reverse_id = f"{post_id}→{pre_id}"
                if reverse_id not in self.network.synapses:
                    self.network.add_synapse(post_id, pre_id, weight=0.3)
                    self.learning_events += 1

    def _compute_emotions(self, input_data: dict, error: float) -> list:
        """Compute emotional tags based on prediction error"""
        tags = []

        if error > 0.5:
            tag = self.emotions.tag_experience(
                EmotionType.NOVELTY,
                intensity=min(1.0, error),
                valence=0.3,
            )
            tags.append(tag)

        if error > 0.8:
            tag = self.emotions.tag_experience(
                EmotionType.CURIOSITY,
                intensity=error,
                valence=0.5,
            )
            tags.append(tag)

        return tags

    def _update_neuromodulation(self, error: float):
        """Update neuromodulation based on prediction error"""
        self.neuromodulation.release(Modulator.NOREPINEPHRINE, error * 0.3)

        if error > 0.3:
            self.neuromodulation.release(Modulator.ACETYLCHOLINE, 0.3)

        plasticity_rate = self.neuromodulation.get_plasticity_rate()
        for synapse in self.network.synapses.values():
            synapse.plasticity_rate = plasticity_rate

    def _compute_emotional_weight(self, input_data: dict, error: float) -> float:
        """Compute emotional weight of an experience"""
        weight = 0.1
        if error > 0.5:
            weight = 0.8
        elif error > 0.3:
            weight = 0.5
        return weight

    def _update_predictions(self, input_data: dict, error: float):
        """
        Update predictions based on prediction error.
        This is HOW the brain learns.
        """
        learning_rate = self.neuromodulation.get_plasticity_rate() * 0.1

        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                current_pred = self.predictions.get(key, 0.0)
                self.predictions[key] = current_pred + learning_rate * (value - current_pred)

    def _update_world_model(self, input_data: dict, error: float):
        """Update internal model of the world"""
        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                current = self.world_model.get(key, 0.0)
                self.world_model[key] = current + 0.05 * (value - current)

    def think(self, duration_ms: float = 100.0) -> dict:
        """
        Think for a duration.
        Internal processing - no external input.
        Just the brain running its dynamics.
        """
        steps = int(duration_ms / 1.0)
        all_spikes = []

        for _ in range(steps):
            spikes = self.network.step()
            all_spikes.extend(spikes)
            self.oscillations.update(dt=0.001)
            self.neuromodulation.decay(dt=0.001)
            self.emotions.decay(dt=0.001)

        self.memory.consolidate()

        return {
            "spikes": len(all_spikes),
            "activity": self.network.network_activity,
            "oscillations": self.oscillations.dominant_wave.name,
            "emotional_state": self.emotions.get_dominant_emotion().name,
        }

    def sleep(self, dream_duration: int = 5) -> dict:
        """
        Sleep and dream.
        Brain consolidates memories and generates new scenarios.
        """
        self.awake = False

        # Dream
        dream_result = self.dreams.dream(dream_duration)

        # Consolidate memories
        consolidation = self.dreams.consolidate()

        # Consolidate brain memories
        self.memory.consolidate()

        self.awake = True

        return {
            "status": "woke_up",
            "dreams": dream_result,
            "consolidation": consolidation,
        }

    def get_state(self) -> dict:
        """Get complete brain state"""
        return {
            "name": self.name,
            "age": time.time() - self.born_at,
            "awake": self.awake,
            "consciousness_level": self.consciousness_level,
            "experience_count": self.experience_count,
            "learning_events": self.learning_events,
            "network": self.network.get_stats(),
            "memory": self.memory.get_stats(),
            "dreams": self.dreams.get_state(),
            "emotions": self.emotions.get_emotional_state(),
            "oscillations": self.oscillations.get_state(),
            "attention": self.thalamus.get_state(),
            "neuromodulation": self.neuromodulation.get_state(),
            "prediction_errors": len(self.prediction_errors),
            "predictions_learned": len(self.predictions),
            "world_model_size": len(self.world_model),
        }

    def __repr__(self):
        return (
            f"NIBrain({self.name}: "
            f"neurons={self.network.neuron_count}, "
            f"synapses={self.network.synapse_count}, "
            f"experiences={self.experience_count})"
        )
