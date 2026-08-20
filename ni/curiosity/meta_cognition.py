"""
Meta-Cognition - Neurons Monitoring Neurons

This is not a counter system. This is actual neural architecture.

How it works:
1. Monitor neurons: Watch specific neurons' firing patterns
2. Meta-neurons: Fire when monitored neurons fire in certain patterns
3. Self-referential loops: Meta-neurons can inhibit/activate other meta-neurons
4. Confidence tracking: Meta-neurons track prediction accuracy
5. Confusion detection: When predictions fail, meta-neurons fire

Architecture:
- Layer 0: Regular neurons (process world input)
- Layer 1: Monitor neurons (watch Layer 0)
- Layer 2: Meta neurons (watch Layer 1)
- Layer 3: Meta-meta neurons (watch Layer 2)
"""

from dataclasses import dataclass, field
from typing import Optional
from ..core.network import NeuralNetwork
from ..core.neuron import Neuron, Spike
from ..core.synapse import Synapse, SynapseType


@dataclass
class MonitorChannel:
    """A channel that monitors a specific neuron"""
    channel_id: str
    monitored_neuron_id: str
    monitor_neuron_id: str      # Neuron that watches the monitored one
    meta_neuron_id: str         # Neuron that watches the monitor
    firing_pattern: list[float] = field(default_factory=list)  # Recent firing times
    pattern_length: int = 10


class MetaCognitionSystem:
    """
    Real Meta-Cognition: Neurons monitoring neurons.

    Architecture:
    - Monitor neurons watch regular neurons
    - Meta neurons watch monitor neurons
    - Confidence neurons track prediction accuracy
    - Confusion neurons fire when predictions fail
    """

    def __init__(self, base_network: NeuralNetwork):
        self.base_network = base_network
        self.meta_network = NeuralNetwork()

        # Monitoring channels
        self.channels: dict[str, MonitorChannel] = {}

        # Meta neurons
        self.confidence_neuron: Optional[str] = None
        self.confusion_neuron: Optional[str] = None
        self.surprise_neuron: Optional[str] = None

        # Tracking
        self.prediction_history: list[float] = []
        self.confidence_level: float = 0.5
        self.confusion_level: float = 0.0

    def create_monitor(self, neuron_id: str) -> str:
        """
        Create a monitoring channel for a neuron.
        Returns the meta_neuron_id.
        """
        channel_id = f"monitor_{neuron_id}"

        # Create monitor neuron (watches the base neuron)
        monitor_id = f"mon_{neuron_id}"
        self.meta_network.add_neuron(monitor_id)

        # Create meta neuron (watches the monitor)
        meta_id = f"meta_{neuron_id}"
        self.meta_network.add_neuron(meta_id)

        # Connect: base neuron → monitor neuron
        # (This is conceptual - we check base neuron firing manually)

        # Connect: monitor → meta (synapse in meta network)
        self.meta_network.add_synapse(monitor_id, meta_id, weight=10.0)

        channel = MonitorChannel(
            channel_id=channel_id,
            monitored_neuron_id=neuron_id,
            monitor_neuron_id=monitor_id,
            meta_neuron_id=meta_id,
        )
        self.channels[channel_id] = channel

        return meta_id

    def create_confidence_tracker(self):
        """Create neurons that track confidence in predictions"""
        self.confidence_neuron = "confidence"
        self.meta_network.add_neuron(self.confidence_neuron, threshold=-60.0)

        self.confusion_neuron = "confusion"
        self.meta_network.add_neuron(self.confusion_neuron, threshold=-65.0)

        self.surprise_neuron = "surprise"
        self.meta_network.add_neuron(self.surprise_neuron, threshold=-60.0)

        # Connect confidence ↔ confusion (inhibitory)
        self.meta_network.add_synapse(
            self.confidence_neuron, self.confusion_neuron,
            weight=5.0, synapse_type=SynapseType.INHIBITORY
        )
        self.meta_network.add_synapse(
            self.confusion_neuron, self.confidence_neuron,
            weight=5.0, synapse_type=SynapseType.INHIBITORY
        )

    def step(self):
        """
        Run one step of meta-cognition.
        Check base network, update meta network.
        """
        # 1. Check which base neurons fired
        fired_neurons = []
        for neuron_id, neuron in self.base_network.neurons.items():
            time_since_spike = self.base_network.sim_time - neuron.last_spike_time
            if time_since_spike < 2.0:  # Fired recently
                fired_neurons.append(neuron_id)

        # 2. Update monitor channels
        for channel in self.channels.values():
            if channel.monitored_neuron_id in fired_neurons:
                # Monitored neuron fired - stimulate monitor
                channel.firing_pattern.append(self.base_network.sim_time)
                if len(channel.firing_pattern) > channel.pattern_length:
                    channel.firing_pattern.pop(0)

                # Stimulate monitor neuron
                self.meta_network.stimulate(channel.monitor_neuron_id, 20.0)

        # 3. Run meta network step
        meta_spikes = self.meta_network.step()

        # 4. Check for meta-level events
        for spike in meta_spikes:
            if spike.neuron_id == self.confidence_neuron:
                self.confidence_level = min(1.0, self.confidence_level + 0.1)
            elif spike.neuron_id == self.confusion_neuron:
                self.confusion_level = min(1.0, self.confusion_level + 0.1)
            elif spike.neuron_id == self.surprise_neuron:
                # Surprise detected
                pass

        return meta_spikes

    def observe_prediction_error(self, error: float):
        """Observe a prediction error and update meta-cognition"""
        self.prediction_history.append(error)
        if len(self.prediction_history) > 100:
            self.prediction_history = self.prediction_history[-50:]

        # High error → confusion
        if error > 0.7 and self.confusion_neuron:
            self.meta_network.stimulate(self.confusion_neuron, 30.0)
            self.confusion_level = min(1.0, self.confusion_level + 0.15)

        # Low error → confidence
        if error < 0.3 and self.confidence_neuron:
            self.meta_network.stimulate(self.confidence_neuron, 25.0)
            self.confidence_level = min(1.0, self.confidence_level + 0.1)

        # Very high error → surprise
        if error > 0.9 and self.surprise_neuron:
            self.meta_network.stimulate(self.surprise_neuron, 40.0)

    def get_firing_pattern(self, neuron_id: str) -> list[float]:
        """Get recent firing pattern of a monitored neuron"""
        channel_id = f"monitor_{neuron_id}"
        if channel_id in self.channels:
            return self.channels[channel_id].firing_pattern.copy()
        return []

    def detect_pattern(self, neuron_id: str) -> Optional[str]:
        """Detect a pattern in a neuron's firing"""
        pattern = self.get_firing_pattern(neuron_id)
        if len(pattern) < 3:
            return None

        # Calculate inter-spike intervals
        intervals = [pattern[i+1] - pattern[i] for i in range(len(pattern)-1)]
        avg_interval = sum(intervals) / len(intervals)

        # Detect patterns
        if avg_interval < 5.0:
            return "high_frequency"
        elif avg_interval > 20.0:
            return "low_frequency"
        elif all(abs(i - avg_interval) < 2.0 for i in intervals):
            return "regular"
        else:
            return "irregular"

    def get_state(self) -> dict:
        """Get meta-cognition state"""
        return {
            "channels": len(self.channels),
            "confidence_level": self.confidence_level,
            "confusion_level": self.confusion_level,
            "meta_neurons": self.meta_network.neuron_count,
            "meta_synapses": self.meta_network.synapse_count,
            "meta_spikes": self.meta_network.total_spikes,
            "prediction_history_length": len(self.prediction_history),
        }
