"""
Oscillation System - The Brain's Timing Mechanism

Not attention heads. Not positional encoding.
Rhythmic patterns that coordinate WHEN neurons fire.

Gamma (30-100 Hz): Consciousness, binding, attention
Theta (4-8 Hz): Memory encoding, navigation
Alpha (8-12 Hz): Attention gating, inhibition
Beta (12-30 Hz): Active thinking, motor control
Delta (0.5-4 Hz): Deep sleep, consolidation

Cross-frequency coupling: Slow waves modulate fast waves.
This is how the brain codes hierarchies of time.
"""

import math
import time
from dataclasses import dataclass
from enum import Enum, auto


class WaveType(Enum):
    DELTA = auto()    # 0.5-4 Hz
    THETA = auto()    # 4-8 Hz
    ALPHA = auto()    # 8-12 Hz
    BETA = auto()     # 12-30 Hz
    GAMMA = auto()    # 30-100 Hz


@dataclass
class Oscillation:
    """A single oscillation with frequency, phase, and amplitude."""
    wave_type: WaveType
    frequency: float    # Hz
    phase: float = 0.0  # Current phase (0-2π)
    amplitude: float = 1.0
    active: bool = True

    def update(self, dt: float = 0.001):
        """Advance phase by dt seconds."""
        if self.active:
            self.phase += 2 * math.pi * self.frequency * dt
            self.phase %= 2 * math.pi  # Keep in [0, 2π)

    @property
    def value(self) -> float:
        """Current value of oscillation (sinusoidal)."""
        return self.amplitude * math.sin(self.phase)

    @property
    def in_peak(self) -> bool:
        """Is this oscillation at its peak? (Phase near π/2)"""
        return 0.3 < self.phase % (2 * math.pi) < 1.0  # Around π/2

    @property
    def in_trough(self) -> bool:
        """Is this oscillation at its trough? (Phase near 3π/2)"""
        return 3.5 < self.phase % (2 * math.pi) < 4.2  # Around 3π/2


class OscillationSystem:
    """
    The brain's timing coordination system.

    Manages multiple oscillations and their interactions:
    - Cross-frequency coupling (theta modulates gamma)
    - Phase synchrony (neurons fire at same phase)
    - Frequency transitions (state changes)
    """

    def __init__(self):
        # Initialize with default frequencies
        self.oscillations = {
            WaveType.DELTA: Oscillation(WaveType.DELTA, frequency=2.0),
            WaveType.THETA: Oscillation(WaveType.THETA, frequency=6.0),
            WaveType.ALPHA: Oscillation(WaveType.ALPHA, frequency=10.0),
            WaveType.BETA: Oscillation(WaveType.BETA, frequency=20.0),
            WaveType.GAMMA: Oscillation(WaveType.GAMMA, frequency=40.0),
        }

        # Cross-frequency coupling matrix
        # Key: which wave modulates which
        self.coupling = {
            (WaveType.THETA, WaveType.GAMMA): 0.3,   # Theta modulates gamma
            (WaveType.DELTA, WaveType.THETA): 0.2,    # Delta modulates theta
            (WaveType.ALPHA, WaveType.BETA): 0.1,     # Alpha weakly modulates beta
        }

        # State tracking
        self.last_update = time.time()
        self.dominant_wave = WaveType.ALPHA
        self.coherence = 0.0  # How synchronized are the waves

    def update(self, dt: float = 0.001):
        """Advance all oscillations by dt seconds."""
        # Update each oscillation
        for osc in self.oscillations.values():
            osc.update(dt)

        # Apply cross-frequency coupling
        for (modulator_type, target_type), strength in self.coupling.items():
            modulator = self.oscillations[modulator_type]
            target = self.oscillations[target_type]

            if modulator.active and target.active:
                # Modulator's amplitude affects target's amplitude
                modulation = modulator.value * strength
                target.amplitude = max(0.1, min(2.0, 1.0 + modulation))

        # Find dominant wave
        max_amplitude = 0
        for wave_type, osc in self.oscillations.items():
            if osc.amplitude > max_amplitude:
                max_amplitude = osc.amplitude
                self.dominant_wave = wave_type

        # Calculate coherence (phase synchrony between waves)
        phases = [osc.phase for osc in self.oscillations.values() if osc.active]
        if len(phases) > 1:
            # Circular variance (0 = random, 1 = perfectly synchronized)
            mean_cos = sum(math.cos(p) for p in phases) / len(phases)
            mean_sin = sum(math.sin(p) for p in phases) / len(phases)
            self.coherence = math.sqrt(mean_cos**2 + mean_sin**2)

    def is_gamma_peak(self) -> bool:
        """Is gamma at its peak? (Conscious processing moment)"""
        return self.oscillations[WaveType.GAMMA].in_peak

    def is_theta_peak(self) -> bool:
        """Is theta at its peak? (Memory encoding moment)"""
        return self.oscillations[WaveType.THETA].in_peak

    def get_gamma_theta_ratio(self) -> float:
        """
        Gamma/theta ratio.
        High ratio = active processing
        Low ratio = resting/encoding
        """
        gamma = self.oscillations[WaveType.GAMMA].amplitude
        theta = self.oscillations[WaveType.THETA].amplitude
        return gamma / max(0.01, theta)

    def set_state(self, state: str):
        """
        Set oscillatory state based on brain state.
        """
        if state == "alert":
            self.oscillations[WaveType.GAMMA].amplitude = 1.5
            self.oscillations[WaveType.BETA].amplitude = 1.2
            self.oscillations[WaveType.ALPHA].amplitude = 0.5
            self.oscillations[WaveType.THETA].amplitude = 0.8

        elif state == "relaxed":
            self.oscillations[WaveType.GAMMA].amplitude = 0.5
            self.oscillations[WaveType.BETA].amplitude = 0.6
            self.oscillations[WaveType.ALPHA].amplitude = 1.5
            self.oscillations[WaveType.THETA].amplitude = 0.7

        elif state == "focused":
            self.oscillations[WaveType.GAMMA].amplitude = 1.2
            self.oscillations[WaveType.BETA].amplitude = 1.0
            self.oscillations[WaveType.ALPHA].amplitude = 0.3
            self.oscillations[WaveType.THETA].amplitude = 0.8

        elif state == "memory_encoding":
            self.oscillations[WaveType.THETA].amplitude = 1.5
            self.oscillations[WaveType.GAMMA].amplitude = 1.0
            self.oscillations[WaveType.ALPHA].amplitude = 0.4

        elif state == "rest":
            self.oscillations[WaveType.GAMMA].amplitude = 0.3
            self.oscillations[WaveType.BETA].amplitude = 0.4
            self.oscillations[WaveType.ALPHA].amplitude = 1.0
            self.oscillations[WaveType.THETA].amplitude = 0.5
            self.oscillations[WaveType.DELTA].amplitude = 0.6

    def get_state(self) -> dict:
        """Get current oscillation state."""
        return {
            wave_type.name: {
                'frequency': osc.frequency,
                'amplitude': osc.amplitude,
                'phase': osc.phase,
                'active': osc.active,
            }
            for wave_type, osc in self.oscillations.items()
        }

    def __repr__(self):
        active = [f"{wt.name}={osc.amplitude:.2f}" for wt, osc in self.oscillations.items()]
        return f"Oscillations({', '.join(active)}, coherence={self.coherence:.2f})"
