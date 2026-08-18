# Neurotransmitters - The Brain's Chemical Language

## The Big Picture

Your brain has **86 billion neurons**. They don't just send electrical signals - they communicate through **chemicals**. These chemicals determine:
- What you feel (emotions)
- What you remember (memory)
- What you want (motivation)
- How you learn (plasticity)
- Whether you're conscious (arousal)

## The Major Neurotransmitters

### DOPAMINE - The "Wanting" Chemical

**NOT the pleasure chemical. That's a myth.**

**What it actually does:**
- **Motivation**: Makes you SEEK things, not enjoy them
- **Prediction error**: Fires when reality is BETTER than expected
- **Learning signal**: Tells your brain "do that again"
- **Movement**: Controls motor initiation (Parkinson's = dopamine death)

**How it works:**
```
Event happens → Brain predicts outcome → Actual outcome differs
                                        ↓
                        Dopamine fires proportionally to DIFFERENCE
                                        ↓
                        If better than expected: MORE dopamine
                        If worse than expected: LESS dopamine
                        If as expected: NO dopamine (habituation)
```

**The terrible truth:**
- Cocaine/amphetamines HIJACK this system
- They flood dopamine regardless of actual reward
- Your brain learns "this is amazing" when it's not
- Then normal life feels gray by comparison

**Computational insight:**
Dopamine implements **temporal difference learning** - the same algorithm used in reinforcement learning. The brain discovered RL before computer scientists did.

**Key pathways:**
| Pathway | Function | When it breaks |
|---------|----------|----------------|
| Mesolimbic | Motivation, reward | Addiction, depression |
| Mesocortical | Decision making, attention | ADHD, schizophrenia |
| Nigrostriatal | Movement control | Parkinson's disease |
| Tuberoinfundibular | Hormone regulation | Hyperprolactinemia |

---

### SEROTONIN - The "Patience" Chemical

**What it actually does:**
- **Patience**: Helps you wait for delayed rewards
- **Mood regulation**: Not "happiness" but "emotional stability"
- **Impulse control**: Prevents you from doing stupid things
- **Sleep-wake cycle**: Precursor to melatonin
- **Pain modulation**: Changes how you perceive pain

**How it works:**
```
Serotonin levels high → Patient, stable, can delay gratification
Serotonin levels low → Impulsive, anxious, seeks immediate reward
```

**The gut connection:**
- **90% of serotonin is in your GUT**, not your brain
- Gut bacteria produce serotonin
- This is why gut health affects mood
- SSRIs (antidepressants) affect gut serotonin too

**Computational insight:**
Serotonin implements a **discount factor** in temporal discounting. High serotonin = you value future rewards more. Low serotonin = you only care about NOW.

---

### NOREPINEPHRINE (Noradrenaline) - The "Alertness" Chemical

**What it actually does:**
- **Alertness**: Wakes you up, keeps you focused
- **Fight-or-flight**: Released during stress
- **Attention**: Narrows focus to threat
- **Memory encoding**: Enhances memory of emotional events

**How it works:**
```
Threat detected → Locus coeruleus fires → Norepinephrine released
                                          ↓
                    Heart rate ↑, Pupils dilate, Muscles tense
                    Attention narrows to threat
                    Memory encoding enhanced
```

**The interesting bit:**
- Locus coeruleus has only ~50,000 neurons
- But it projects to virtually EVERY part of the brain
- It's a single "panic button" that changes the whole system

**Computational insight:**
Norepinephrine implements **urgency signals**. It's the brain's way of saying "stop what you're doing, THIS IS IMPORTANT."

---

### ACETYLCHOLINE - The "Learning" Chemical

**What it actually does:**
- **Learning**: Enables synaptic plasticity
- **Memory**: Helps form new memories
- **Attention**: Sustains focus on tasks
- **Muscle activation**: Triggers muscle contraction

**How it works:**
```
Acetylcholine released → Enables LTP (Long-Term Potentiation)
                        → Synapses become more plastic
                        → New connections form more easily
                        → Learning happens
```

**The interesting bit:**
- Alzheimer's disease DESTROYS acetylcholine neurons
- This is why memory is the first thing to go
- Cholinesterase inhibitors (drugs) slow this by preventing breakdown

**Computational insight:**
Acetylcholine implements a **learning rate** parameter. When it's high, the system learns fast. When it's low, the system is stable but can't adapt.

---

### GABA - The "Inhibitor" Chemical

**What it actually does:**
- **Inhibition**: Prevents neurons from firing
- **Calming**: Reduces anxiety
- **Filtering**: Blocks irrelevant information
- **Balance**: Keeps excitatory activity in check

**How it works:**
```
GABA binds to receptor → Chloride channels open
                       → Neuron becomes MORE negative
                       → Harder to fire
                       → Activity suppressed
```

**The interesting bit:**
- GABA is the brain's "off switch"
- Benzodiazepines (Valium, Xanax) enhance GABA
- Alcohol also enhances GABA (this is why you get clumsy and forget)
- Too little GABA = epilepsy, anxiety, insomnia

**Computational insight:**
GABA implements **inhibition** - the ability to suppress activity. Without it, you get runaway excitation (seizures). AI has nothing like this - no mechanism to actively suppress wrong answers.

---

### GLUTAMATE - The "Exciter" Chemical

**What it actually does:**
- **Excitation**: Makes neurons more likely to fire
- **Learning**: Essential for LTP (Long-Term Potentiation)
- **Memory**: Forms memory traces
- **Plasticity**: Enables brain rewiring

**How it works:**
```
Glutamate binds to AMPA/NMDA receptors → Ion channels open
                                        → Neuron becomes MORE positive
                                        → More likely to fire
                                        → Learning occurs
```

**The interesting bit:**
- Glutamate is the MOST common neurotransmitter
- It's involved in virtually ALL brain functions
- Too much = excitotoxicity (neurons die from overactivation)
- This is how strokes damage the brain - blood cut off, glutamate floods, neurons die

**Computational insight:**
Glutamate implements **excitation** - the ability to activate patterns. Combined with GABA, it creates the brain's excitation/inhibition balance.

---

### ENDORPHINS - The "Painkiller" Chemical

**What it actually does:**
- **Pain relief**: Blocks pain signals
- **Euphoria**: Creates feelings of wellbeing (runner's high)
- **Stress response**: Released during extreme stress
- **Social bonding**: Released during trust and connection

**How it works:**
```
Pain/Stress → Endorphins released → Bind to opioid receptors
                                   → Pain signals blocked
                                   → Euphoria produced
                                   → Stress reduced
```

**The interesting bit:**
- Endorphins are chemically similar to morphine
- Your brain has its own opiate system
- Placebo effect works partly through endorphins
- Social rejection activates the same pathways as physical pain

**Computational insight:**
Endorphins implement **pain suppression** and **reward**. They're the brain's way of saying "ignore the damage, keep going."

---

## The Key Insight: The Brain is a CHEMICAL Computer

It's not just electrical signals. It's a complex chemical soup where:
- **Multiple chemicals** interact simultaneously
- **Ratios matter** more than absolute levels
- **Timing matters** - same chemical, different effect based on when
- **Location matters** - same chemical, different effect based on where
- **Receptor density matters** - more receptors = more sensitive

## What This Means for NI

We can't just simulate neurons. We need to simulate:
1. Multiple chemical systems
2. Their interactions
3. How they modulate each other
4. How they affect learning and behavior
5. How they create emergent properties like "mood" and "motivation"

## Next Steps
1. Study each system in depth
2. Map interactions between chemicals
3. Find computational models
4. Implement in code
5. Test against brain data
