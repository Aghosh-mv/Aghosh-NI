# Neural Mechanisms - How Neurons Actually Compute

## The Artificial vs Biological Gap

### What AI Calls a "Neuron"
```python
output = activation(sum(inputs * weights) + bias)
```
- Single computation
- Synchronous (all neurons update at once)
- Stateless (no memory of past)
- One type of signal (numbers)

### What a Real Neuron Does
```
Input dendrites → Soma (integration) → Axon hillock → Action potential
     ↑                                              ↓
     └──────── Synaptic plasticity ←── Synaptic terminals
```
- **Dendritic computation**: Each dendrite branch can compute independently
- **Temporal coding**: Timing of spikes matters, not just rate
- **Plasticity**: Connections change based on experience (Hebbian learning)
- **Multiple neurotransmitters**: Excitatory, inhibitory, modulatory
- **Glial cells**: Support, modulate, possibly compute

## Key Biological Mechanisms

### 1. Spike-Timing-Dependent Plasticity (STDP)
**What it is**: Connections strengthen when pre-synaptic neuron fires BEFORE post-synaptic, weaken when after.

**Why it matters**: This is HOW the brain learns causality. If A fires before B repeatedly, the connection A→B strengthens. The brain naturally learns "A causes B."

**Computational model**:
```python
def stdp(pre_spike_time, post_spike_time, weight):
    dt = post_spike_time - pre_spike_time
    if dt > 0:  # Pre before post
        weight += A_plus * exp(-dt / tau_plus)  # Strengthen
    else:       # Post before pre
        weight -= A_minus * exp(dt / tau_minus)  # Weaken
    return weight
```

### 2. Neural Oscillations (Brain Waves)
**What they are**: Groups of neurons firing in synchrony at specific frequencies.

| Frequency | Name | Function |
|-----------|------|----------|
| 0.5-4 Hz | Delta | Deep sleep, memory consolidation |
| 4-8 Hz | Theta | Memory encoding, navigation |
| 8-12 Hz | Alpha | Attention gating, inhibition |
| 12-30 Hz | Beta | Active thinking, motor control |
| 30-100 Hz | Gamma | Consciousness, binding, attention |

**Why it matters**: The brain uses oscillations to:
- **Bind** features together (red + round + moving = red ball)
- **Sequence** events (this happened before that)
- **Gate** information (alpha blocks irrelevant info)
- **Communicate** between regions (phase synchronization)

**LLMs have NOTHING like this.**

### 3. Dendritic Computation
**What it is**: Single dendrites can perform complex computations, not just sum inputs.

**Why it matters**: A single neuron with branching dendrites can implement:
- AND gates (both inputs needed)
- OR gates (either input works)
- XOR-like functions
- Temporal coincidence detection

**A single biological neuron ≈ a small neural network.**

### 4. Neuromodulation
**What it is**: Chemicals (dopamine, serotonin, norepinephrine) that change how entire brain regions function.

**Why it matters**:
- **Dopamine**: Reward prediction, motivation, learning rate
- **Serotonin**: Mood, patience, risk assessment
- **Norepinephrine**: Alertness, attention, arousal
- **Acetylcholine**: Learning, memory, attention

**These are NOT just "activation functions" - they're system-wide state changes.**

### 5. Glial Cells
**What they are**: Non-neural cells that outnumber neurons 10:1.

**What they might do**:
- Regulate synaptic transmission
- Modulate neural activity
- Possibly perform computation themselves
- Form their own networks

**AI ignores them entirely.**

## The Key Insight: The Brain is NOT a Neural Network

The brain is a:
- **Hybrid analog-digital system** (spikes are digital, dendritic computation is analog)
- **Chemically modulated** system (neurotransmitters change everything)
- **Plastic** system (rewires itself constantly)
- **Oscillatory** system (timing matters, not just rate)
- **Multi-cellular** system (neurons + glia)

## What This Means for NI

We can't just build "better neural networks." We need to:
1. Implement real plasticity (STDP, not backprop)
2. Use oscillations for binding and sequencing
3. Model dendritic computation
4. Include neuromodulation
5. Consider glial cell roles

## Next Steps
1. Find computational models for each mechanism
2. Implement them in code
3. Test against brain data
4. See what emerges
