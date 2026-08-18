"""
Neuromodulation System - The Brain's Chemical Language

Not activation functions. Not layer norms.
Chemical signals that change how the ENTIRE system behaves.

Dopamine: "Was that better than expected?" (learning rate, motivation)
Serotonin: "Should I wait or act now?" (patience, threshold)
Norepinephrine: "ALERT! Something important!" (excitability, attention)
Acetylcholine: "LEARN THIS!" (plasticity gate)
GABA: "SHHHH." (global inhibition)
"""

import time
from dataclasses import dataclass
from enum import Enum, auto


class Modulator(Enum):
    DOPAMINE = "dopamine"              # Reward prediction error
    SEROTONIN = "serotonin"            # Patience, impulse control
    NOREPINEPHRINE = "norepinephrine"  # Alertness, arousal
    ACETYLCHOLINE = "acetylcholine"    # Learning gate
    GABA = "gaba"                      # Global inhibition
    GLUTAMATE = "glutamate"            # Global excitation


@dataclass
class ModulatorState:
    """Current state of a neuromodulator."""
    level: float = 0.0          # Current concentration (-1 to +1)
    baseline: float = 0.0       # Resting level
    decay_rate: float = 0.1     # How fast it returns to baseline
    last_release: float = 0.0   # Time of last release

    def release(self, amount: float):
        """Release modulator."""
        self.level = max(-1.0, min(1.0, self.level + amount))
        self.last_release = time.time()

    def decay(self, dt: float = 0.1):
        """Let modulator decay back to baseline."""
        diff = self.baseline - self.level
        self.level += diff * self.decay_rate * dt


class NeuromodulationSystem:
    """
    The brain's chemical communication system.

    Modulates:
    - Plasticity rate (how fast synapses change)
    - Excitability (how easily neurons fire)
    - Threshold (how much input needed to fire)
    - Learning rate (how much new info matters)
    """

    def __init__(self):
        self.modulators = {
            Modulator.DOPAMINE: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.05,
            ),
            Modulator.SEROTONIN: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.02,  # Slower decay (serotonin is slower)
            ),
            Modulator.NOREPINEPHRINE: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.1,  # Fast decay (quick alert, quick calm)
            ),
            Modulator.ACETYLCHOLINE: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.03,
            ),
            Modulator.GABA: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.08,
            ),
            Modulator.GLUTAMATE: ModulatorState(
                level=0.0,
                baseline=0.0,
                decay_rate=0.08,
            ),
        }

        # Prediction error tracking (for dopamine)
        self.expected_reward = 0.0
        self.reward_history = []

    def release(self, modulator: Modulator, amount: float):
        """Release a neuromodulator."""
        if modulator in self.modulators:
            self.modulators[modulator].release(amount)

    def compute_reward_prediction_error(self, actual_reward: float) -> float:
        """
        Compute dopamine signal based on reward prediction error.

        RPE = actual - expected
        Positive RPE → MORE dopamine (better than expected)
        Negative RPE → LESS dopamine (worse than expected)
        """
        rpe = actual_reward - self.expected_reward

        # Update expected reward (moving average)
        self.reward_history.append(actual_reward)
        if len(self.reward_history) > 100:
            self.reward_history.pop(0)
        self.expected_reward = sum(self.reward_history) / len(self.reward_history)

        # Release dopamine proportional to RPE
        self.release(Modulator.DOPAMINE, rpe * 0.5)

        return rpe

    def decay(self, dt: float = 0.1):
        """Let all modulators decay back to baseline."""
        for modulator in self.modulators.values():
            modulator.decay(dt)

    def get_plasticity_rate(self) -> float:
        """
        How fast should synapses change?
        - High acetylcholine → HIGH plasticity (LEARN THIS)
        - High dopamine → HIGH plasticity for rewarded patterns
        - High GABA → LOW plasticity (stable state)
        """
        ach = self.modulators[Modulator.ACETYLCHOLINE].level
        da = self.modulators[Modulator.DOPAMINE].level
        gaba = self.modulators[Modulator.GABA].level

        rate = 1.0
        rate += ach * 0.5      # Acetylcholine boosts learning
        rate += da * 0.3        # Dopamine boosts learning
        rate -= gaba * 0.5      # GABA suppresses learning

        return max(0.1, min(2.0, rate))

    def get_excitability(self) -> float:
        """
        How easily do neurons fire?
        - High norepinephrine → EASY to fire (alert)
        - High serotonin → HARD to fire (patient)
        - High GABA → HARD to fire (inhibited)
        """
        ne = self.modulators[Modulator.NOREPINEPHRINE].level
        ser = self.modulators[Modulator.SEROTONIN].level
        gaba = self.modulators[Modulator.GABA].level

        excitability = 1.0
        excitability += ne * 0.4     # Norepinephrine increases excitability
        excitability -= ser * 0.3    # Serotonin decreases excitability
        excitability -= gaba * 0.5   # GABA decreases excitability

        return max(0.2, min(2.0, excitability))

    def get_threshold_adjustment(self) -> float:
        """
        How much to adjust neuron firing thresholds.
        - High serotonin → RAISE threshold (harder to fire)
        - High norepinephrine → LOWER threshold (easier to fire)
        """
        ser = self.modulators[Modulator.SEROTONIN].level
        ne = self.modulators[Modulator.NOREPINEPHRINE].level

        # Positive = raise threshold (harder to fire)
        adjustment = ser * 3.0 - ne * 3.0

        return adjustment

    def get_state(self) -> dict:
        """Get current modulation state."""
        return {
            modulator.value: {
                'level': state.level,
                'baseline': state.baseline,
            }
            for modulator, state in self.modulators.items()
        }

    def __repr__(self):
        active = [
            f"{m.value}={s.level:.2f}"
            for m, s in self.modulators.items()
            if abs(s.level) > 0.1
        ]
        if active:
            return f"Neuromodulation({', '.join(active)})"
        return "Neuromodulation(baseline)"
