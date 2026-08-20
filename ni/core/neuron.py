"""
Spiking Neuron - The Fundamental Unit

Not an artificial neuron. Not a perceptron.
A spiking neuron that fires action potentials.

Uses SIMULATION TIME, not real time.
This is critical - the brain runs in its own time.
"""

import math
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Spike:
    """A single action potential."""
    neuron_id: str
    timestamp: float
    strength: float = 1.0


class Neuron:
    """
    A spiking neuron with leaky integrate-and-fire dynamics.

    Uses simulation time (not real time).
    This allows the brain to run at any speed.
    """

    def __init__(
        self,
        neuron_id: str,
        threshold: float = -55.0,
        resting: float = -70.0,
        reset: float = -75.0,
        tau_membrane: float = 20.0,
        refractory_steps: int = 3,
    ):
        self.id = neuron_id
        self.threshold = threshold
        self.resting = resting
        self.reset = reset
        self.tau_membrane = tau_membrane
        self.refractory_steps = refractory_steps

        # State (all in simulation time)
        self.potential = resting
        self.last_spike_time = -1000.0  # Simulation time of last spike
        self.refractory_counter = 0     # Steps remaining in refractory

        # Connections
        self.incoming: list[tuple[str, float]] = []
        self.outgoing: list[tuple[str, float]] = []

        # Neuromodulation
        self.modulation = {
            'dopamine': 0.0,
            'serotonin': 0.0,
            'norepinephrine': 0.0,
            'acetylcholine': 0.0,
        }

        # Statistics
        self.spike_count = 0
        self.total_input = 0.0

    def step(self, dt: float = 1.0, sim_time: float = 0.0) -> bool:
        """
        Advance neuron by one time step.
        Returns True if neuron spiked.
        """
        # Handle refractory period
        if self.refractory_counter > 0:
            self.refractory_counter -= 1
            return False

        # Apply neuromodulation to threshold
        effective_threshold = self.threshold
        if self.modulation['norepinephrine'] > 0:
            effective_threshold -= self.modulation['norepinephrine'] * 5.0
        if self.modulation['serotonin'] > 0:
            effective_threshold += self.modulation['serotonin'] * 5.0

        # Check for spike
        if self.potential >= effective_threshold:
            return self._fire(sim_time)

        return False

    def receive_input(self, input_current: float, dt: float = 1.0):
        """Receive input current and update membrane potential."""
        if self.refractory_counter > 0:
            return

        # Apply neuromodulation to input
        modulated_input = input_current * (1.0 + self.modulation['norepinephrine'] * 0.5)

        # Leaky integrate-and-fire
        self.potential += (
            -(self.potential - self.resting) / self.tau_membrane
            + modulated_input
        ) * dt

        self.total_input += abs(input_current)

    def _fire(self, sim_time: float) -> bool:
        """Fire an action potential."""
        self.potential = self.reset
        self.last_spike_time = sim_time
        self.refractory_counter = self.refractory_steps
        self.spike_count += 1
        return True

    def get_spike(self, sim_time: float) -> Optional[Spike]:
        """Get spike if neuron just fired (within last 1ms of sim time)."""
        if sim_time - self.last_spike_time < 1.0:
            return Spike(
                neuron_id=self.id,
                timestamp=self.last_spike_time,
                strength=1.0,
            )
        return None

    def apply_modulation(self, modulator: str, level: float):
        """Apply neuromodulator effect."""
        if modulator in self.modulation:
            self.modulation[modulator] = max(-1.0, min(1.0, level))

    def __repr__(self):
        state = "REFRACTORY" if self.refractory_counter > 0 else f"V={self.potential:.1f}mV"
        return f"Neuron({self.id}: {state}, spikes={self.spike_count})"
