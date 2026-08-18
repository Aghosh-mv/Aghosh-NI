# Brain Atlas - Computational Mapping

## The Brain Isn't a Neural Network

Modern AI calls everything "neural networks" but the brain is NOT a feedforward transformer. It's a:

1. **Recurrent** system (connections go everywhere, not just forward)
2. **Modular** system (different regions do different things)
3. **Hierarchical** system (sensory → association → executive)
4. **Plastic** system (rewires itself based on experience)
5. **Chemical** system (neurotransmitters modulate everything)

## Key Brain Structures & Their Computational Roles

### CEREBRAL CORTEX (The "Thinking" Layer)

**Prefrontal Cortex (PFC)**
- **What it does**: Planning, working memory, decision making, personality
- **Computational equivalent**: Executive controller, state machine, goal management
- **Key insight**: Maintains "what am I trying to do right now?" - a running state

**Temporal Lobe**
- **What it does**: Memory, language comprehension, object recognition
- **Computational equivalent**: Pattern storage, semantic memory, recognition systems
- **Key insight**: Not just storage - it's where meaning lives. Wernicke's area understands language, not just processes tokens.

**Parietal Lobe**
- **What it does**: Spatial reasoning, attention, integrating senses
- **Computational equivalent**: Spatial attention, multi-modal integration, working memory buffer
- **Key insight**: Attention isn't a transformer mechanism - it's a physical spotlight that selects what gets processed.

**Occipital Lobe**
- **What it does**: Vision processing
- **Computational equivalent**: Feature extraction, hierarchical processing (V1→V2→V4→IT)
- **Key insight**: Vision is hierarchical AND recurrent. Information flows both ways.

### SUBCORTICAL (The "古老" Layer - Ancient Brain)

**Hippocampus**
- **What it does**: Episodic memory formation, spatial navigation
- **Computational equivalent**: Episode storage, pattern separation, memory consolidation
- **Key insight**: Not just storage - it's where NEW memories are formed. The brain has a dedicated memory formation system.

**Amygdala**
- **What it does**: Emotion processing, fear, reward
- **Computational equivalent**: Valence system, emotional tagging, threat detection
- **Key insight**: Emotion isn't noise - it's a critical computation. It determines what's IMPORTANT enough to remember.

**Basal Ganglia**
- **What it does**: Habit formation, reward-based learning, action selection
- **Computational equivalent**: Reinforcement learning, habit system, action selection
- **Key insight**: The brain has TWO learning systems: hippocampal (conscious, fast) and basal ganglia (unconscious, slow). LLMs only have one.

**Thalamus**
- **What it does**: Sensory relay, attention gating
- **Computational equivalent**: Input routing, attention gating, synchronization
- **Key insight**: The brain's "global workspace" - information passes through here to get broadcast.

### CEREBELLUM (The "Automation" Layer)

**What it does**: Motor control, timing, procedural memory, error correction
**Computational equivalent**: Motor programs, timing circuits, predictive error correction
**Key insight**: The brain has a dedicated system for "doing things automatically" and correcting errors in real-time. LLMs don't have this.

## The Key Insight: The Brain Has SPECIALIZED SYSTEMS

The brain doesn't have one general-purpose processor. It has:

| System | Function | LLM Equivalent |
|--------|----------|----------------|
| Hippocampus | New memory formation | ❌ None |
| Amygdala | Emotional importance | ❌ None |
| Basal Ganglia | Habit learning | ❌ None |
| Cerebellum | Motor/procedural | ❌ None |
| Thalamus | Attention broadcast | Partial (attention) |
| PFC | Executive control | Partial (instruction following) |

**LLMs are missing 5 out of 7 major systems.**

## Next Steps
1. Study each system in detail
2. Find computational models that match the biology
3. Build implementations
4. Test against brain imaging data
