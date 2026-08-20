"""
J-Lens - Brain Observatory

A monitoring system that lets you SEE what the brain is doing.
Not a safety system. A DIAGNOSTIC system.

Shows:
- Which neurons are firing
- Which synapses are strengthening/weakening
- What prediction errors are occurring
- What emotions are active
- What oscillations are happening
- What the brain is "thinking" about

Like an fMRI for artificial brains.
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class NeuronSnapshot:
    """State of a neuron at a point in time"""
    neuron_id: str
    potential: float
    threshold: float
    spike_count: int
    is_refractory: bool
    time_since_spike: float
    input_received: float
    modulation: dict


@dataclass
class SynapseSnapshot:
    """State of a synapse at a point in time"""
    synapse_id: str
    pre_id: str
    post_id: str
    weight: float
    strengthen_count: int
    weaken_count: int
    plasticity_ratio: float
    last_plasticity_time: float


@dataclass
class BrainSnapshot:
    """Complete brain state at a point in time"""
    timestamp: float
    step: int
    neurons: list[NeuronSnapshot]
    synapses: list[SynapseSnapshot]
    prediction_error: float
    emotions: dict
    oscillations: dict
    neuromodulation: dict
    network_activity: float
    total_spikes: int
    learning_events: int


class JLens:
    """
    J-Lens: Brain Observatory

    Watches the brain and records everything.
    Use to understand what the brain is doing and why.
    """

    def __init__(self):
        self.snapshots: list[BrainSnapshot] = []
        self.step_count = 0
        self.recording = True

        # Event log
        self.events: list[dict] = []

        # Alerts
        self.alerts: list[dict] = []

    def record(self, brain) -> BrainSnapshot:
        """Record current brain state"""
        if not self.recording:
            return None

        self.step_count += 1

        # Capture neuron states
        neurons = []
        for neuron_id, neuron in brain.network.neurons.items():
            snapshot = NeuronSnapshot(
                neuron_id=neuron_id,
                potential=neuron.potential,
                threshold=neuron.threshold,
                spike_count=neuron.spike_count,
                is_refractory=neuron.refractory_counter > 0,
                time_since_spike=brain.network.sim_time - neuron.last_spike_time,
                input_received=neuron.total_input,
                modulation=neuron.modulation.copy(),
            )
            neurons.append(snapshot)

        # Capture synapse states
        synapses = []
        for synapse_id, synapse in brain.network.synapses.items():
            snapshot = SynapseSnapshot(
                synapse_id=synapse_id,
                pre_id=synapse.pre_id,
                post_id=synapse.post_id,
                weight=synapse.weight,
                strengthen_count=synapse.strengthen_count,
                weaken_count=synapse.weaken_count,
                plasticity_ratio=synapse.plasticity_ratio,
                last_plasticity_time=0.0,
            )
            synapses.append(snapshot)

        # Get emotional state
        emotional_state = brain.emotions.get_emotional_state()

        # Get oscillation state
        oscillation_state = {
            brain.oscillations.dominant_wave.name: {
                "frequency": brain.oscillations.oscillations[brain.oscillations.dominant_wave].frequency,
                "amplitude": brain.oscillations.oscillations[brain.oscillations.dominant_wave].amplitude,
            }
        }

        # Get neuromodulation state
        neuro_state = brain.neuromodulation.get_state()

        # Create snapshot
        snapshot = BrainSnapshot(
            timestamp=time.time(),
            step=self.step_count,
            neurons=neurons,
            synapses=synapses,
            prediction_error=brain.prediction_errors[-1] if brain.prediction_errors else 0.0,
            emotions=emotional_state,
            oscillations=oscillation_state,
            neuromodulation=neuro_state,
            network_activity=brain.network.network_activity,
            total_spikes=brain.network.total_spikes,
            learning_events=brain.learning_events,
        )

        self.snapshots.append(snapshot)

        # Check for alerts
        self._check_alerts(snapshot)

        return snapshot

    def log_event(self, event_type: str, data: dict):
        """Log a significant event"""
        self.events.append({
            "step": self.step_count,
            "timestamp": time.time(),
            "type": event_type,
            "data": data,
        })

    def _check_alerts(self, snapshot: BrainSnapshot):
        """Check for notable conditions"""
        # No neurons firing
        if snapshot.total_spikes == 0 and self.step_count > 10:
            self.alerts.append({
                "step": self.step_count,
                "type": "no_spikes",
                "message": "No neurons have fired yet",
            })

        # No synapses formed
        if len(snapshot.synapses) == 0 and self.step_count > 20:
            self.alerts.append({
                "step": self.step_count,
                "type": "no_synapses",
                "message": "No synapses have formed yet",
            })

        # High prediction error
        if snapshot.prediction_error > 0.8:
            self.alerts.append({
                "step": self.step_count,
                "type": "high_prediction_error",
                "message": f"Prediction error is high: {snapshot.prediction_error:.3f}",
            })

    def get_neuron_report(self, snapshot: BrainSnapshot = None) -> str:
        """Get detailed neuron report"""
        if snapshot is None:
            snapshot = self.snapshots[-1] if self.snapshots else None
        if snapshot is None:
            return "No snapshots recorded"

        lines = []
        lines.append(f"=== NEURON REPORT (Step {snapshot.step}) ===")
        lines.append(f"Total neurons: {len(snapshot.neurons)}")
        lines.append(f"Network activity: {snapshot.network_activity:.3f}")
        lines.append(f"Total spikes: {snapshot.total_spikes}")
        lines.append("")

        for neuron in snapshot.neurons:
            state = "FIRING" if neuron.is_refractory else "RESTING"
            lines.append(f"  {neuron.neuron_id}:")
            lines.append(f"    Potential: {neuron.potential:.2f}mV (threshold: {neuron.threshold}mV)")
            lines.append(f"    State: {state}")
            lines.append(f"    Spikes: {neuron.spike_count}")
            lines.append(f"    Time since spike: {neuron.time_since_spike:.2f}ms")
            lines.append(f"    Total input: {neuron.input_received:.2f}")

        return "\n".join(lines)

    def get_synapse_report(self, snapshot: BrainSnapshot = None) -> str:
        """Get detailed synapse report"""
        if snapshot is None:
            snapshot = self.snapshots[-1] if self.snapshots else None
        if snapshot is None:
            return "No snapshots recorded"

        lines = []
        lines.append(f"=== SYNAPSE REPORT (Step {snapshot.step}) ===")
        lines.append(f"Total synapses: {len(snapshot.synapses)}")
        lines.append("")

        if not snapshot.synapses:
            lines.append("  NO SYNAPSES EXIST")
            lines.append("  This means neurons are not connecting!")
        else:
            for synapse in snapshot.synapses:
                lines.append(f"  {synapse.synapse_id}:")
                lines.append(f"    Weight: {synapse.weight:.4f}")
                lines.append(f"    Strengthened: {synapse.strengthen_count} times")
                lines.append(f"    Weakened: {synapse.weaken_count} times")
                lines.append(f"    Plasticity ratio: {synapse.plasticity_ratio:.3f}")

        return "\n".join(lines)

    def get_full_report(self, snapshot: BrainSnapshot = None) -> str:
        """Get complete brain report"""
        if snapshot is None:
            snapshot = self.snapshots[-1] if self.snapshots else None
        if snapshot is None:
            return "No snapshots recorded"

        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"J-LENS FULL REPORT - Step {snapshot.step}")
        lines.append(f"{'='*60}")
        lines.append("")

        # Network status
        lines.append(f"NETWORK:")
        lines.append(f"  Neurons: {len(snapshot.neurons)}")
        lines.append(f"  Synapses: {len(snapshot.synapses)}")
        lines.append(f"  Activity: {snapshot.network_activity:.3f}")
        lines.append(f"  Total spikes: {snapshot.total_spikes}")
        lines.append(f"  Learning events: {snapshot.learning_events}")
        lines.append("")

        # Prediction error
        lines.append(f"PREDICTIVE CODING:")
        lines.append(f"  Current prediction error: {snapshot.prediction_error:.4f}")
        lines.append("")

        # Emotions
        lines.append(f"EMOTIONS:")
        for emotion, level in snapshot.emotions.items():
            if level > 0.01:
                lines.append(f"  {emotion}: {level:.3f}")
        lines.append("")

        # Oscillations
        lines.append(f"OSCILLATIONS:")
        for wave, data in snapshot.oscillations.items():
            lines.append(f"  {wave}: freq={data['frequency']:.1f}Hz, amp={data['amplitude']:.3f}")
        lines.append("")

        # Neuromodulation
        lines.append(f"NEUROMODULATION:")
        neuro = snapshot.neuromodulation
        for mod in ['dopamine', 'serotonin', 'norepinephrine', 'acetylcholine']:
            if mod in neuro:
                level = neuro[mod].get('level', 0)
                if level > 0.01:
                    lines.append(f"  {mod}: {level:.3f}")
        lines.append("")

        # Alerts
        if self.alerts:
            lines.append(f"ALERTS:")
            for alert in self.alerts[-5:]:  # Last 5 alerts
                lines.append(f"  Step {alert['step']}: {alert['message']}")
        lines.append("")

        # Neuron details
        lines.append(self.get_neuron_report(snapshot))
        lines.append("")

        # Synapse details
        lines.append(self.get_synapse_report(snapshot))

        return "\n".join(lines)

    def get_timeline(self, metric: str, last_n: int = 50) -> list[float]:
        """Get timeline of a metric"""
        if metric == "prediction_error":
            return [s.prediction_error for s in self.snapshots[-last_n:]]
        elif metric == "network_activity":
            return [s.network_activity for s in self.snapshots[-last_n:]]
        elif metric == "total_spikes":
            return [s.total_spikes for s in self.snapshots[-last_n:]]
        elif metric == "neuron_count":
            return [len(s.neurons) for s in self.snapshots[-last_n:]]
        elif metric == "synapse_count":
            return [len(s.synapses) for s in self.snapshots[-last_n:]]
        return []

    def print_ascii_graph(self, data: list[float], width: int = 60, height: int = 20):
        """Print ASCII graph of data"""
        if not data:
            print("No data")
            return

        min_val = min(data)
        max_val = max(data)
        range_val = max_val - min_val if max_val > min_val else 1.0

        # Sample data to fit width
        step = max(1, len(data) // width)
        sampled = data[::step][:width]

        # Normalize to height
        normalized = [(v - min_val) / range_val * height for v in sampled]

        # Print graph (bottom to top)
        for row in range(height, -1, -1):
            line = ""
            for col in range(len(normalized)):
                if normalized[col] >= row:
                    line += "#"
                else:
                    line += " "
            print(f"{row:3d} |{line}|")

        print(f"    +{'-'*len(normalized)}+")
        print(f"     Min: {min_val:.3f}, Max: {max_val:.3f}")

    def save_log(self, filename: str = "jlens_log.txt"):
        """Save complete log to file"""
        with open(filename, 'w') as f:
            f.write(f"J-LENS LOG\n")
            f.write(f"{'='*60}\n\n")

            for snapshot in self.snapshots:
                f.write(f"STEP {snapshot.step}\n")
                f.write(f"  Neurons: {len(snapshot.neurons)}\n")
                f.write(f"  Synapses: {len(snapshot.synapses)}\n")
                f.write(f"  Spikes: {snapshot.total_spikes}\n")
                f.write(f"  Prediction error: {snapshot.prediction_error:.4f}\n")
                f.write(f"  Activity: {snapshot.network_activity:.3f}\n")
                f.write("\n")

            f.write(f"\nEVENTS ({len(self.events)} total)\n")
            for event in self.events:
                f.write(f"  Step {event['step']}: {event['type']} - {event['data']}\n")

            f.write(f"\nALERTS ({len(self.alerts)} total)\n")
            for alert in self.alerts:
                f.write(f"  Step {alert['step']}: {alert['message']}\n")

        print(f"Log saved to {filename}")
