"""
Emotional Tagging System - The Amygdala Equivalent

Not sentiment analysis. Not emotion detection.
A system that determines WHAT IS IMPORTANT enough to remember.

The amygdala tags experiences with emotional weight:
- High emotional weight → STRONG memory formation
- Low emotional weight → weak/no memory formation
- This is why you remember your first kiss but not Tuesday lunch

Types of emotional tags:
- Fear/Pain: "Avoid this"
- Reward/Pleasure: "Seek more of this"
- Novelty: "Pay attention, this is new"
- Social: "This involves others"
"""

import time
from dataclasses import dataclass
from enum import Enum, auto


class EmotionType(Enum):
    FEAR = auto()           # Threat detection
    REWARD = auto()         # Positive outcome
    NOVELTY = auto()        # Something new/unexpected
    PAIN = auto()           # Negative experience
    SOCIAL = auto()         # Involves others
    SATIETY = auto()        # Enough of this
    CURIOSITY = auto()      # Want to know more


@dataclass
class EmotionalTag:
    """A tag attached to an experience or memory."""
    emotion_type: EmotionType
    intensity: float       # 0.0 to 1.0
    valence: float         # -1.0 (negative) to +1.0 (positive)
    timestamp: float
    decay_rate: float = 0.01  # How fast this emotion fades

    @property
    def arousal(self) -> float:
        """How activated is this emotion?"""
        return self.intensity * abs(self.valence)

    @property
    def is_approach(self) -> bool:
        """Is this something to approach?"""
        return self.valence > 0

    @property
    def is_avoid(self) -> bool:
        """Is this something to avoid?"""
        return self.valence < 0

    def decay(self, dt: float = 0.1):
        """Let emotion fade over time."""
        self.intensity *= (1.0 - self.decay_rate * dt)


class EmotionalSystem:
    """
    The brain's importance weighting system.

    Determines what's worth remembering based on emotional significance.
    High emotional weight = strong memory formation.
    """

    def __init__(self):
        # Current emotional state
        self.current_emotions: dict[EmotionType, float] = {
            et: 0.0 for et in EmotionType
        }

        # Emotional history (for learning patterns)
        self.emotional_history: list[EmotionalTag] = []

        # Emotional thresholds
        self.thresholds = {
            EmotionType.FEAR: 0.3,
            EmotionType.REWARD: 0.4,
            EmotionType.NOVELTY: 0.5,
            EmotionType.PAIN: 0.3,
            EmotionType.SOCIAL: 0.3,
            EmotionType.SATIETY: 0.6,
            EmotionType.CURIOSITY: 0.4,
        }

        # Emotional inertia (how quickly emotions change)
        self.inertia = 0.8  # 0 = instant change, 1 = never changes

    def tag_experience(
        self,
        emotion_type: EmotionType,
        intensity: float,
        valence: float,
    ) -> EmotionalTag:
        """
        Tag an experience with emotional weight.
        Returns the tag that should be attached to the memory.
        """
        tag = EmotionalTag(
            emotion_type=emotion_type,
            intensity=min(1.0, max(0.0, intensity)),
            valence=min(1.0, max(-1.0, valence)),
            timestamp=time.time(),
        )

        # Update current emotional state (with inertia)
        target_level = intensity * (1.0 if valence > 0 else -1.0)
        current = self.current_emotions[emotion_type]
        self.current_emotions[emotion_type] = (
            current * self.inertia + target_level * (1.0 - self.inertia)
        )

        # Store in history
        self.emotional_history.append(tag)
        if len(self.emotional_history) > 1000:
            self.emotional_history.pop(0)

        return tag

    def compute_memory_weight(self, tags: list[EmotionalTag]) -> float:
        """
        Compute how strongly a memory should be encoded.
        High emotional weight = STRONG memory formation.

        This is the amygdala's contribution to memory:
        Emotional events are remembered better.
        """
        if not tags:
            return 0.1  # Baseline (non-emotional events are weakly remembered)

        # Sum emotional intensities
        total_arousal = sum(tag.arousal for tag in tags)

        # Average valence (mixed emotions reduce encoding)
        avg_valence = sum(tag.valence for tag in tags) / len(tags)
        valence_factor = 1.0 - abs(avg_valence) * 0.3  # Mixed emotions slightly reduce encoding

        # Novelty bonus (new things are remembered better)
        novelty_tags = [t for t in tags if t.emotion_type == EmotionType.NOVELTY]
        novelty_bonus = sum(t.intensity for t in novelty_tags) * 0.5

        # Compute final weight
        weight = (total_arousal * 0.6 + novelty_bonus) * valence_factor

        return max(0.05, min(1.0, weight))

    def should_form_memory(self, tags: list[EmotionalTag]) -> bool:
        """
        Should this experience be encoded into long-term memory?
        Based on emotional significance.
        """
        weight = self.compute_memory_weight(tags)
        return weight > 0.3  # Threshold for memory formation

    def get_dominant_emotion(self) -> EmotionType:
        """What's the strongest current emotion?"""
        if not self.current_emotions:
            return EmotionType.NEUTRAL

        # Find emotion with highest absolute value
        dominant = max(
            self.current_emotions.items(),
            key=lambda x: abs(x[1])
        )
        return dominant[0]

    def get_emotional_state(self) -> dict:
        """Get current emotional state as a vector."""
        return {
            emotion.name: level
            for emotion, level in self.current_emotions.items()
        }

    def decay(self, dt: float = 0.1):
        """Let all emotions fade over time."""
        for emotion in self.current_emotions:
            self.current_emotions[emotion] *= (1.0 - 0.05 * dt)

        # Decay old tags
        for tag in self.emotional_history:
            tag.decay(dt)

    def __repr__(self):
        active = [
            f"{et.name}={level:.2f}"
            for et, level in self.current_emotions.items()
            if abs(level) > 0.1
        ]
        if active:
            return f"EmotionalSystem({', '.join(active)})"
        return "EmotionalSystem(baseline)"
