"""
Neural Network - NOT an Artificial Neural Network

A network of spiking neurons connected by plastic synapses.
No layers. No forward pass. Just neurons firing and learning.

Uses SIMULATION TIME for all operations.
This is critical for proper STDP and network dynamics.
"""

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
        self.sim_time: float = 0.0
        self.dt: float = 1.0  # Time step in ms

        # Global state
        self.total_spikes = 0
        self.network_activity = 0.0

        # Pending inputs (from stimulate calls)
        self.pending_inputs: dict[str, float] = {}

    def add_neuron(self, neuron_id: str, **kwargs) -> Neuron:
        """Add a neuron to the network."""
        neuron = Neuron(neuron_id=neuron_id, **kwargs)
        self.neurons[neuron_id] = neuron
        return neuron

    def add_synapse(
        self,
        pre_id: str,
        post_id: str,
        weight: float = 15.0,
        synapse_type: SynapseType = SynapseType.EXCITATORY,
    ) -> Synapse:
        """Connect two neurons."""
        if pre_id not in self.neurons:
            raise ValueError(f"Pre-synaptic neuron {pre_id} not found")
        if post_id not in self.neurons:
            raise ValueError(f"Post-synaptic neuron {post_id} not found")

        synapse_id = f"{pre_id}→{post_id}"

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

    def stimulate(self, neuron_id: str, current: float):
        """Inject current into a neuron (processed in next step)."""
        if neuron_id in self.neurons:
            self.pending_inputs[neuron_id] = self.pending_inputs.get(neuron_id, 0) + current

    def step(self) -> list[Spike]:
        """
        Advance network by one time step (in simulation time).
        Returns list of spikes that occurred.
        """
        self.sim_time += self.dt
        all_spikes = []

        # 1. Apply pending inputs
        for neuron_id, current in self.pending_inputs.items():
            if neuron_id in self.neurons:
                self.neurons[neuron_id].receive_input(current, self.dt)
        self.pending_inputs = {}

        # 2. Each neuron updates based on inputs from synapses
        for neuron in self.neurons.values():
            total_input = 0.0

            # Sum inputs from all incoming synapses
            for pre_id, _ in neuron.incoming:
                synapse_id = f"{pre_id}→{neuron.id}"
                if synapse_id in self.synapses:
                    syn = self.synapses[synapse_id]
                    pre_neuron = self.neurons[pre_id]

                    # Check if pre-synaptic neuron spiked recently
                    time_since_pre_spike = self.sim_time - pre_neuron.last_spike_time
                    if time_since_pre_spike < 3.0:  # Within 3ms window
                        total_input += syn.transmit()

            # Apply input to neuron
            neuron.receive_input(total_input, self.dt)

        # 3. Check for spikes
        for neuron in self.neurons.values():
            if neuron.step(self.dt, self.sim_time):
                spike = neuron.get_spike(self.sim_time)
                if spike:
                    all_spikes.append(spike)
                    self.total_spikes += 1

                    # Notify post-synaptic synapses (for STDP)
                    for post_id, _ in neuron.outgoing:
                        synapse_id = f"{neuron.id}→{post_id}"
                        if synapse_id in self.synapses:
                            self.synapses[synapse_id].receive_pre_spike(self.sim_time)

                    # Notify pre-synaptic synapses (for STDP)
                    for pre_id, _ in neuron.incoming:
                        synapse_id = f"{pre_id}→{neuron.id}"
                        if synapse_id in self.synapses:
                            self.synapses[synapse_id].receive_post_spike(self.sim_time)

        # 4. Update synapse STDP
        for syn in self.synapses.values():
            syn.update_stdp(self.sim_time)

        # 5. Update network statistics
        active_neurons = sum(
            1 for n in self.neurons.values()
            if self.sim_time - n.last_spike_time < 10.0
        )
        self.network_activity = active_neurons / max(1, len(self.neurons))

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
            'sim_time': self.sim_time,
        }

    def __repr__(self):
        return (
            f"NeuralNetwork("
            f"neurons={self.neuron_count}, "
            f"synapses={self.synapse_count}, "
            f"activity={self.network_activity:.3f}, "
            f"sim_time={self.sim_time:.1f})"
        )
