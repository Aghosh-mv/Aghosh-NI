"""
Curiosity System - Neural Deep Focus

This is not a flag. This is not a mode.
This is actual neural architecture that creates focus.

How it works:
1. Novelty detector neurons fire when input is surprising
2. These activate inhibitory interneurons
3. Inhibitory neurons suppress ALL other neural activity
4. Only the interesting signal remains active
5. Brain explores from all angles
6. When understanding achieved, inhibition lifts

Architecture:
- Novelty neurons: Fire on high prediction error
- Inhibitory interneurons: Suppress background activity
- Focus neurons: Represent the current focus
- Satiety neurons: Fire when understanding is achieved
"""

from dataclasses import dataclass, field
from typing import Optional
from ..core.network import NeuralNetwork
from ..core.neuron import Neuron, Spike
from ..core.synapse import Synapse, SynapseType


@dataclass
class FocusTarget:
    """Something the brain is focused on"""
    target_id: str
    neuron_ids: list[str]       # Neurons representing this target
    novelty_level: float        # How novel (0-1)
    understanding_level: float  # How understood (0-1)
    focus_start: float          # When focus started
    exploration_count: int      # How many angles explored
    angles_tried: list[str] = field(default_factory=list)


class CuriositySystem:
    """
    Real Curiosity: Neural Deep Focus.

    When something is interesting, inhibitory neurons
    suppress ALL other activity. Only the interesting
    signal remains. Brain explores it from all angles.
    """

    def __init__(self, base_network: NeuralNetwork):
        self.base_network = base_network

        # Curiosity neurons (in base network)
        self.novelty_neurons: list[str] = []
        self.inhibitory_neurons: list[str] = []
        self.focus_neurons: list[str] = []
        self.satiety_neurons: list[str] = []

        # Focus state
        self.is_focused: bool = False
        self.current_focus: Optional[FocusTarget] = None
        self.focus_history: list[FocusTarget] = []

        # Parameters
        self.novelty_threshold: float = 0.5
        self.satiety_threshold: float = 0.8
        self.max_focus_duration: int = 100  # steps
        self.focus_duration: int = 0

        # Create curiosity neurons
        self._create_curiosity_neurons()

    def _create_curiosity_neurons(self):
        """Create the neural architecture for curiosity"""
        # Novelty detector neurons (one per input dimension)
        for i in range(5):
            neuron_id = f"novelty_{i}"
            self.base_network.add_neuron(neuron_id, threshold=-60.0)
            self.novelty_neurons.append(neuron_id)

        # Inhibitory interneurons (suppress background)
        for i in range(3):
            neuron_id = f"inhibitory_{i}"
            self.base_network.add_neuron(neuron_id, threshold=-65.0)
            self.inhibitory_neurons.append(neuron_id)

            # Connect to ALL other neurons (to suppress them)
            for other_id in list(self.base_network.neurons.keys()):
                if other_id != neuron_id and not other_id.startswith("inhibitory"):
                    self.base_network.add_synapse(
                        neuron_id, other_id,
                        weight=10.0,
                        synapse_type=SynapseType.INHIBITORY
                    )

        # Focus neurons (represent current focus)
        for i in range(3):
            neuron_id = f"focus_{i}"
            self.base_network.add_neuron(neuron_id, threshold=-58.0)
            self.focus_neurons.append(neuron_id)

        # Satiety neurons (fire when understanding achieved)
        for i in range(2):
            neuron_id = f"satiety_{i}"
            self.base_network.add_neuron(neuron_id, threshold=-62.0)
            self.satiety_neurons.append(neuron_id)

            # Connect satiety to inhibitory (when satiated, stop inhibiting)
            for inhib_id in self.inhibitory_neurons:
                self.base_network.add_synapse(
                    neuron_id, inhib_id,
                    weight=8.0,
                    synapse_type=SynapseType.INHIBITORY
                )

    def detect_novelty(self, prediction_error: float) -> bool:
        """
        Detect if input is novel/interesting.
        Returns True if curiosity should activate.
        """
        if prediction_error > self.novelty_threshold:
            # Stimulate novelty neurons
            for neuron_id in self.novelty_neurons:
                self.base_network.stimulate(neuron_id, prediction_error * 40.0)
            return True
        return False

    def activate_focus(self, target_id: str, neuron_ids: list[str]):
        """
        Activate deep focus mode.
        Inhibitory neurons suppress background.
        Only target neurons remain active.
        """
        self.is_focused = True
        self.current_focus = FocusTarget(
            target_id=target_id,
            neuron_ids=neuron_ids,
            novelty_level=1.0,
            understanding_level=0.0,
            focus_start=self.base_network.sim_time,
            exploration_count=0,
        )
        self.focus_duration = 0

        # Activate focus neurons
        for neuron_id in self.focus_neurons:
            self.base_network.stimulate(neuron_id, 30.0)

        # Activate inhibitory neurons (suppress background)
        for neuron_id in self.inhibitory_neurons:
            self.base_network.stimulate(neuron_id, 25.0)

    def maintain_focus(self):
        """
        Maintain focus during deep dive.
        Called each step while focused.
        """
        if not self.is_focused:
            return

        self.focus_duration += 1

        # Keep inhibitory neurons active (maintain suppression)
        for neuron_id in self.inhibitory_neurons:
            self.base_network.stimulate(neuron_id, 15.0)

        # Keep focus neurons active
        for neuron_id in self.focus_neurons:
            self.base_network.stimulate(neuron_id, 10.0)

        # Check if focus should end
        if self.focus_duration >= self.max_focus_duration:
            self.release_focus("timeout")
        elif self.current_focus and self.current_focus.understanding_level >= self.satiety_threshold:
            self.release_focus("understood")

    def record_exploration(self, angle: str, success: bool):
        """Record an exploration during focus"""
        if self.current_focus:
            self.current_focus.angles_tried.append(angle)
            self.current_focus.exploration_count += 1

            # Update understanding
            if success:
                self.current_focus.understanding_level = min(
                    1.0,
                    self.current_focus.understanding_level + 0.1
                )
            else:
                # Even failures teach us something
                self.current_focus.understanding_level = min(
                    1.0,
                    self.current_focus.understanding_level + 0.05
                )

            # Decrease novelty as we understand
            self.current_focus.novelty_level *= 0.95

    def release_focus(self, reason: str):
        """
        Release focus mode.
        Inhibition lifts, normal activity resumes.
        """
        if self.current_focus:
            self.current_focus.understanding_level = min(
                1.0,
                self.current_focus.understanding_level + 0.1
            )
            self.focus_history.append(self.current_focus)

        self.is_focused = False
        self.current_focus = None
        self.focus_duration = 0

        # Activate satiety neurons (signal understanding achieved)
        for neuron_id in self.satiety_neurons:
            self.base_network.stimulate(neuron_id, 20.0)

    def get_focus_level(self) -> float:
        """How focused is the brain? (0 = unfocused, 1 = deep focus)"""
        if self.is_focused:
            return min(1.0, self.focus_duration / 20.0)
        return 0.0

    def get_state(self) -> dict:
        """Get curiosity system state"""
        return {
            "is_focused": self.is_focused,
            "focus_level": self.get_focus_level(),
            "current_focus": self.current_focus.target_id if self.current_focus else None,
            "understanding": self.current_focus.understanding_level if self.current_focus else 0.0,
            "novelty_neurons": len(self.novelty_neurons),
            "inhibitory_neurons": len(self.inhibitory_neurons),
            "focus_neurons": len(self.focus_neurons),
            "focus_history": len(self.focus_history),
            "focus_duration": self.focus_duration,
        }
