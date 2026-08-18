"""
Neural Network - NOT an Artificial Neural Network

A network of spiking neurons connected by plastic synapses.
No layers. No forward pass. Just neurons firing and learning.

Properties:
- Recurrent connections (can loop)
- No designated input/output layers
- Learning happens continuously
- Behavior emerges from dynamics
"""

import time
import random
from typing import Optional
from .neuron import Neuron, Spike
from .synapse import Synapse, SynapseType


class NeuralNetwork:
    """
    A spiking neural network.

    Not a feedforward network. Not a transformer.
    A recurrent, plastic, spiking network.
    """

    def __init__(self):
        self.neurons: dict[str, Neuron] = {}
        self.synapses: dict[str, Synapse] = {}
        self.time = 0.0
        self.dt = 1.0  # Time step in ms

        # Global state
        self.total_spikes = 0
        self.average_firing_rate = 0.0
        self.network_activity = 0.0

    def add_neuron(self, neuron_id: str, **kwargs) -> Neuron:
        """Add a neuron to the network."""
        neuron = Neuron(neuron_id=neuron_id, **kwargs)
        self.neurons[neuron_id] = neuron
        return neuron

    def add_synapse(
        self,
        pre_id: str,
        post_id: str,
        weight: float = 0.5,
        synapse_type: SynapseType = SynapseType.EXCITATORY,
    ) -> Synapse:
        """Connect two neurons."""
        if pre_id not in self.neurons:
            raise ValueError(f"Pre-synaptic neuron {pre_id} not found")
        if post_id not in self.neurons:
            raise ValueError(f"Post-synaptic neuron {post_id} not found")

        synapse_id = f"{pre_id}→{post_id}"

        # Check if connection already exists
        if synapse_id in self.synapses:
            return self.synapses[synapse_id]

        synapse = Synapse(
            pre_id=pre_id,
            post_id=post_id,
            weight=weight,
            synapse_type=synapse_type,
        )

        self.synapses[synapse_id] = synapse
        self.neurons[pre_id].outgoing.append((post_id, weight))
        self.neurons[post_id].incoming.append((pre_id, weight))

        return synapse

    def connect_mutual(
        self,
        id_a: str,
        id_b: str,
        weight: float = 0.5,
        synapse_type: SynapseType = SynapseType.EXCITATORY,
    ):
        """Create bidirectional connection."""
        self.add_synapse(id_a, id_b, weight, synapse_type)
        self.add_synapse(id_b, id_a, weight, synapse_type)

    def stimulate(self, neuron_id: str, current: float):
        """Inject current into a neuron."""
        if neuron_id in self.neurons:
            self.neurons[neuron_id].receive_input(current, self.dt)

    def step(self) -> list[Spike]:
        """
        Advance network by one time step.
        Returns list of spikes that occurred.
        """
        self.time += self.dt
        all_spikes = []

        # 1. Each neuron updates based on inputs
        for neuron in self.neurons.values():
            # Calculate total input from incoming synapses
            total_input = 0.0
            for pre_id, _ in neuron.incoming:
                # Find synapse
                synapse_id = f"{pre_id}→{neuron.id}"
                if synapse_id in self.synapses:
                    syn = self.synapses[synapse_id]
                    # If pre-synaptic neuron spiked recently, transmit
                    pre_neuron = self.neurons[pre_id]
                    if pre_neuron.time_since_spike < 2.0:  # Spiked in last 2ms
                        total_input += syn.transmit()

            # Update membrane potential
            spiked = neuron.receive_input(total_input, self.dt)

            if spiked:
                spike = neuron.get_spike()
                if spike:
                    all_spikes.append(spike)
                    self.total_spikes += 1

                    # Notify post-synaptic synapses
                    for post_id, _ in neuron.outgoing:
                        synapse_id = f"{neuron.id}→{post_id}"
                        if synapse_id in self.synapses:
                            self.synapses[synapse_id].receive_pre_spike()

        # 2. Update synapse statistics (STDP already happened in receive_*)
        # Prune old spike traces
        for syn in self.synapses.values():
            syn.trace.prune(max_age_ms=100.0)

        # 3. Update network statistics
        active_neurons = sum(1 for n in self.neurons.values() if n.time_since_spike < 10.0)
        self.network_activity = active_neurons / max(1, len(self.neurons))
        self.average_firing_rate = self.total_spikes / max(1, self.time)

        return all_spikes

    def get_neuron(self, neuron_id: str) -> Optional[Neuron]:
        return self.neurons.get(neuron_id)

    def get_synapse(self, pre_id: str, post_id: str) -> Optional[Synapse]:
        return self.synapses.get(f"{pre_id}→{post_id}")

    @property
    def neuron_count(self) -> int:
        return len(self.neurons)

    @property
    def synapse_count(self) -> int:
        return len(self.synapses)

    @property
    def average_weight(self) -> float:
        if not self.synapses:
            return 0.0
        return sum(s.weight for s in self.synapses.values()) / len(self.synapses)

    def apply_modulation(self, modulator: str, level: float):
        """Apply neuromodulator to all neurons."""
        for neuron in self.neurons.values():
            neuron.apply_modulation(modulator, level)

    def get_stats(self) -> dict:
        """Get network statistics."""
        weights = [s.weight for s in self.synapses.values()]
        strong = sum(1 for s in self.synapses.values() if s.is_strong)
        weak = sum(1 for s in self.synapses.values() if s.is_weak)

        return {
            'neurons': self.neuron_count,
            'synapses': self.synapse_count,
            'activity': self.network_activity,
            'avg_weight': self.average_weight,
            'total_spikes': self.total_spikes,
            'strong_synapses': strong,
            'weak_synapses': weak,
            'time': self.time,
        }

    def __repr__(self):
        return (
            f"NeuralNetwork("
            f"neurons={self.neuron_count}, "
            f"synapses={self.synapse_count}, "
            f"activity={self.network_activity:.3f})"
        )
