"""
Synapse - The Connection That Learns

Not a weight matrix. Not a linear layer.
A biological synapse that changes based on spike timing.

Implements STDP (Spike-Timing-Dependent Plasticity):
- Pre before post → STRENGTHEN (causality detected)
- Post before pre → WEAKEN (anti-causality)
- This is HOW the brain learns causation
"""

import time
import math
from dataclasses import dataclass
from enum import Enum, auto


class SynapseType(Enum):
    EXCITATORY = auto()  # Glutamate - makes target fire more
    INHIBITORY = auto()  # GABA - makes target fire less
    MODULATORY = auto()  # Dopamine/Serotonin - changes learning


@dataclass
class SynapticTrace:
    """History of spikes for STDP calculation."""
    pre_spikes: list[float] = None   # Timestamps of pre-synaptic spikes
    post_spikes: list[float] = None  # Timestamps of post-synaptic spikes

    def __post_init__(self):
        if self.pre_spikes is None:
            self.pre_spikes = []
        if self.post_spikes is None:
            self.post_spikes = []

    def prune(self, max_age_ms: float = 100.0):
        """Remove old spikes beyond STDP window."""
        now = time.time() * 1000
        self.pre_spikes = [t for t in self.pre_spikes if now - t < max_age_ms]
        self.post_spikes = [t for t in self.post_spikes if now - t < max_age_ms]


class Synapse:
    """
    A biological synapse with STDP learning.

    Properties:
    - Weight (connection strength)
    - Plasticity (how much it can change)
    - Type (excitatory/inhibitory/modulatory)
    - STDP parameters (learning rules)
    """

    def __init__(
        self,
        pre_id: str,
        post_id: str,
        weight: float = 0.5,
        synapse_type: SynapseType = SynapseType.EXCITATORY,
        # STDP parameters
        A_plus: float = 0.01,      # LTP amplitude
        A_minus: float = 0.012,    # LTD amplitude (slightly stronger)
        tau_plus: float = 20.0,    # LTP time constant (ms)
        tau_minus: float = 20.0,   # LTD time constant (ms)
        # Plasticity limits
        weight_min: float = 0.0,
        weight_max: float = 1.0,
        plasticity_rate: float = 1.0,
    ):
        self.pre_id = pre_id
        self.post_id = post_id
        self.type = synapse_type

        # Weight (connection strength)
        self.weight = weight
        self.weight_min = weight_min
        self.weight_max = weight_max

        # STDP parameters
        self.A_plus = A_plus
        self.A_minus = A_minus
        self.tau_plus = tau_plus
        self.tau_minus = tau_minus

        # Plasticity control
        self.plasticity_rate = plasticity_rate
        self.age = 0.0  # Synapses that are used more stay strong

        # Spike history for STDP
        self.trace = SynapticTrace()

        # Statistics
        self.strengthen_count = 0
        self.weaken_count = 0
        self.last_plasticity_time = 0.0

    def receive_pre_spike(self):
        """Called when pre-synaptic neuron fires."""
        now = time.time() * 1000
        self.trace.pre_spikes.append(now)

        # Check for post-synaptic spikes that happened AFTER this pre-spike
        # If post fires after pre → STRENGTHEN (causality)
        for post_time in self.trace.post_spikes:
            dt = now - post_time
            if 0 < dt < self.tau_plus * 5:
                # Post happened before pre - this is anti-causality
                # WEAKEN
                self._weaken(abs(dt))

    def receive_post_spike(self):
        """Called when post-synaptic neuron fires."""
        now = time.time() * 1000
        self.trace.post_spikes.append(now)

        # Check for pre-synaptic spikes that happened BEFORE this post-spike
        # If post fires after pre → STRENGTHEN (causality detected)
        for pre_time in self.trace.pre_spikes:
            dt = now - pre_time
            if 0 < dt < self.tau_plus * 5:
                # Post fired after pre - this is causality!
                # STRENGTHEN
                self._strengthen(abs(dt))

        # Prune old spikes
        self.trace.prune(max_age_ms=self.tau_plus * 5)

    def _strengthen(self, dt: float):
        """Strengthen synapse (LTP)."""
        # STDP rule: strength increases when pre fires before post
        dw = self.A_plus * math.exp(-dt / self.tau_plus)

        # Apply plasticity modulation
        dw *= self.plasticity_rate

        # Inhibitory synapses get weaker when strengthened (counterintuitive but correct)
        if self.type == SynapseType.INHIBITORY:
            dw = -dw

        self.weight = min(self.weight_max, self.weight + dw)
        self.strengthen_count += 1
        self.last_plasticity_time = time.time() * 1000

    def _weaken(self, dt: float):
        """Weaken synapse (LTD)."""
        # STDP rule: strength decreases when post fires before pre
        dw = self.A_minus * math.exp(-dt / self.tau_minus)

        # Apply plasticity modulation
        dw *= self.plasticity_rate

        # Inhibitory synapses get weaker when weakened (back to normal)
        if self.type == SynapseType.INHIBITORY:
            dw = -dw

        self.weight = max(self.weight_min, self.weight - dw)
        self.weaken_count += 1
        self.last_plasticity_time = time.time() * 1000

    def transmit(self, pre_spike_strength: float = 1.0) -> float:
        """
        Transmit signal across synapse.
        Returns current injected into post-synaptic neuron.
        """
        signal = pre_spike_strength * self.weight

        # Inhibitory synapses subtract current
        if self.type == SynapseType.INHIBITORY:
            signal = -signal

        return signal

    @property
    def plasticity_ratio(self) -> float:
        """How much has this synapse been modified?"""
        total = self.strengthen_count + self.weaken_count
        if total == 0:
            return 0.5  # Neutral
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
