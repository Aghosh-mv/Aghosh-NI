"""
Spiking Neuron - The Fundamental Unit

Not an artificial neuron. Not a perceptron.
A spiking neuron that fires action potentials.

Biologically inspired:
- Membrane potential dynamics
- Refractory period
- Spike-timing-dependent plasticity
- Chemical modulation
"""

import time
import math
from dataclasses import dataclass, field
from typing import Optional
import random


@dataclass
class Spike:
    """A single action potential."""
    neuron_id: str
    timestamp: float
    strength: float = 1.0


class Neuron:
    """
    A spiking neuron.

    Dynamics:
    - Membrane potential accumulates input
    - When threshold is reached, FIRES (spike)
    - After firing, enters refractory period
    - Potential decays over time (leaky)
    """

    def __init__(
        self,
        neuron_id: str,
        threshold: float = -55.0,      # mV, spike threshold
        resting: float = -70.0,         # mV, resting potential
        reset: float = -75.0,           # mV, post-spike reset
        tau_membrane: float = 20.0,     # ms, membrane time constant
        refractory_time: float = 2.0,   # ms, absolute refractory period
    ):
        self.id = neuron_id
        self.threshold = threshold
        self.resting = resting
        self.reset = reset
        self.tau_membrane = tau_membrane
        self.refractory_time = refractory_time

        # State
        self.potential = resting
        self.last_spike_time = -1000.0  # Time of last spike
        self.is_refractory = False

        # Connections
        self.incoming: list[tuple[str, float]] = []  # (source_id, weight)
        self.outgoing: list[tuple[str, float]] = []   # (target_id, weight)

        # Chemical modulation (neuromodulators affect this neuron)
        self.modulation = {
            'dopamine': 0.0,      # -1 to +1, affects plasticity
            'serotonin': 0.0,     # -1 to +1, affects patience/threshold
            'norepinephrine': 0.0,# -1 to +1, affects excitability
            'acetylcholine': 0.0, # -1 to +1, affects learning rate
        }

        # Statistics
        self.spike_count = 0
        self.total_input = 0.0

    @property
    def time_since_spike(self) -> float:
        return time.time() * 1000 - self.last_spike_time  # Convert to ms

    @property
    def in_refractory(self) -> bool:
        return self.time_since_spike < self.refractory_time

    @property
    def firing_rate(self) -> float:
        """Estimated firing rate in Hz."""
        if self.spike_count < 2:
            return 0.0
        # Simple estimate based on recent activity
        return min(200.0, self.spike_count / max(0.001, self.time_since_spike / 1000))

    def receive_input(self, input_current: float, dt: float = 1.0):
        """
        Receive input current and update membrane potential.

        Uses leaky integrate-and-fire dynamics:
        dV/dt = -(V - V_rest) / tau + I / C
        """
        if self.in_refractory:
            return False  # Don't process during refractory

        # Apply neuromodulation to input
        modulated_input = input_current * (1.0 + self.modulation['norepinephrine'] * 0.5)

        # Leaky integrate-and-fire
        self.potential += (
            -(self.potential - self.resting) / self.tau_membrane
            + modulated_input
        ) * dt

        self.total_input += abs(input_current)

        # Check for spike
        if self.potential >= self.threshold:
            return self._fire()
        return False

    def _fire(self) -> bool:
        """Fire an action potential."""
        self.potential = self.reset
        self.last_spike_time = time.time() * 1000
        self.is_refractory = True
        self.spike_count += 1

        # Release refractory after delay
        # (In real implementation, this would be async)
        return True

    def get_spike(self) -> Optional[Spike]:
        """Get spike if neuron just fired."""
        if self.time_since_spike < 1.0:  # Fired in last 1ms
            return Spike(
                neuron_id=self.id,
                timestamp=self.last_spike_time,
                strength=1.0
            )
        return None

    def apply_modulation(self, modulator: str, level: float):
        """Apply neuromodulator effect."""
        if modulator in self.modulation:
            # Clamp to [-1, 1]
            self.modulation[modulator] = max(-1.0, min(1.0, level))

            # Modulators affect threshold
            if modulator == 'serotonin':
                # Serotonin raises threshold (harder to fire = more patient)
                self.threshold = -55.0 + self.modulation['serotonin'] * 5.0
            elif modulator == 'norepinephrine':
                # Norepinephrine lowers threshold (easier to fire = more alert)
                self.threshold = -55.0 - self.modulation['norepinephrine'] * 5.0

    def __repr__(self):
        state = "FIRING" if self.in_refractory else f"V={self.potential:.1f}mV"
        return f"Neuron({self.id}: {state}, spikes={self.spike_count})"
