"""
Synapse - The Connection That Learns

Uses SIMULATION TIME for STDP.
Pre before post → STRENGTHEN
Post before pre → WEAKEN
"""

import math
from dataclasses import dataclass, field
from enum import Enum, auto


class SynapseType(Enum):
    EXCITATORY = auto()
    INHIBITORY = auto()
    MODULATORY = auto()


class Synapse:
    """
    A biological synapse with STDP learning.
    Uses simulation time for all timing.
    """

    def __init__(
        self,
        pre_id: str,
        post_id: str,
        weight: float = 0.5,
        synapse_type: SynapseType = SynapseType.EXCITATORY,
        A_plus: float = 0.01,
        A_minus: float = 0.012,
        tau_plus: float = 20.0,
        tau_minus: float = 20.0,
        weight_min: float = 0.0,
        weight_max: float = 1.0,
        plasticity_rate: float = 1.0,
    ):
        self.pre_id = pre_id
        self.post_id = post_id
        self.type = synapse_type

        self.weight = weight
        self.weight_min = weight_min
        self.weight_max = weight_max

        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus

        self.plasticity_rate = plasticity_rate

        # Spike history for STDP (simulation times)
        self.pre_spike_times: list[float] = []
        self.post_spike_times: list[float] = []

        # Statistics
        self.strengthen_count = 0
        self.weaken_count = 0

    def receive_pre_spike(self, sim_time: float):
        """Called when pre-synaptic neuron fires."""
        self.pre_spike_times.append(sim_time)

        # Check: did post fire BEFORE this pre? (anti-causality → weaken)
        for post_time in self.post_spike_times:
            dt = sim_time - post_time
            if 0 < dt < self.tau_minus * 3:
                self._weaken(dt)

        # Prune old spikes
        self.pre_spike_times = [t for t in self.pre_spike_times if sim_time - t < self.tau_plus * 3]

    def receive_post_spike(self, sim_time: float):
        """Called when post-synaptic neuron fires."""
        self.post_spike_times.append(sim_time)

        # Check: did pre fire BEFORE this post? (causality → strengthen)
        for pre_time in self.pre_spike_times:
            dt = sim_time - pre_time
            if 0 < dt < self.tau_plus * 3:
                self._strengthen(dt)

        # Prune old spikes
        self.post_spike_times = [t for t in self.post_spike_times if sim_time - t < self.tau_minus * 3]

    def update_stdp(self, sim_time: float):
        """Update STDP (called each step)."""
        # Prune old spike times
        max_age = max(self.tau_plus, self.tau_minus) * 3
        self.pre_spike_times = [t for t in self.pre_spike_times if sim_time - t < max_age]
        self.post_spike_times = [t for t in self.post_spike_times if sim_time - t < max_age]

    def _strengthen(self, dt: float):
        """Strengthen synapse (LTP)."""
        dw = self.A_plus * math.exp(-dt / self.tau_plus)
        dw *= self.plasticity_rate

        if self.type == SynapseType.INHIBITORY:
            dw = -dw

        self.weight = min(self.weight_max, self.weight + dw)
        self.strengthen_count += 1

    def _weaken(self, dt: float):
        """Weaken synapse (LTD)."""
        dw = self.A_minus * math.exp(-dt / self.tau_minus)
        dw *= self.plasticity_rate

        if self.type == SynapseType.INHIBITORY:
            dw = -dw

        self.weight = max(self.weight_min, self.weight - dw)
        self.weaken_count += 1

    def transmit(self, pre_spike_strength: float = 1.0) -> float:
        """Transmit signal across synapse."""
        signal = pre_spike_strength * self.weight
        if self.type == SynapseType.INHIBITORY:
            signal = -signal
        return signal

    @property
    def plasticity_ratio(self) -> float:
        total = self.strengthen_count + self.weaken_count
        if total == 0:
            return 0.5
        return self.strengthen_count / total

    @property
    def is_strong(self) -> bool:
        return self.weight > 0.7

    @property
    def is_weak(self) -> bool:
        return self.weight < 0.3

    def __repr__(self):
        type_char = "+" if self.type == SynapseType.EXCITATORY else "-"
        return f"Syn({self.pre_id}→{self.post_id}: w={self.weight:.3f} {type_char})"
