"""
Memory System - Hippocampus + Neocortex + Consolidation

Not a vector database. Not embeddings.
Multiple memory systems that work like the brain:

1. Episodic Memory (Hippocampus)
   - What happened and when
   - Sparse, pattern-separated
   - Quick learning of individual events

2. Semantic Memory (Neocortex)
   - What I know about the world
   - Dense, overlapping representations
   - Gradual learning from many experiences

3. Procedural Memory (Cerebellum/Basal Ganglia)
   - How to do things
   - Implicit, automatic
   - Learned through repetition

4. Working Memory (Prefrontal Cortex)
   - What I'm thinking about RIGHT NOW
   - Limited capacity
   - Temporary storage
"""

import time
import math
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import random


class MemoryType(Enum):
    EPISODIC = auto()    # What happened (hippocampus)
    SEMANTIC = auto()    # What I know (neocortex)
    PROCEDURAL = auto()  # How to do (cerebellum)
    EMOTIONAL = auto()   # What matters (amygdala)


@dataclass
class Memory:
    """A single memory trace."""
    id: str
    memory_type: MemoryType
    content: dict          # What is remembered
    emotional_weight: float  # How important (from amygdala)
    timestamp: float       # When it was formed
    strength: float = 1.0  # Current memory strength
    access_count: int = 0  # How many times recalled
    last_accessed: float = 0.0

    # Associations (connections to other memories)
    associations: dict[str, float] = field(default_factory=dict)

    @property
    def age(self) -> float:
        """Age in seconds."""
        return time.time() - self.timestamp

    @property
    def is_recent(self) -> bool:
        """Was this formed in the last hour?"""
        return self.age < 3600

    @property
    def is_consolidated(self) -> bool:
        """Has this been transferred to long-term storage?"""
        return self.age > 3600 and self.strength > 0.3

    def access(self):
        """Access this memory (increases strength temporarily)."""
        self.access_count += 1
        self.last_accessed = time.time()
        # Access strengthens memory
        self.strength = min(1.0, self.strength + 0.05)

    def decay(self, dt: float = 0.1):
        """Memory strength decays over time (Ebbinghaus forgetting curve)."""
        # Power law forgetting (slow initial decay, then faster)
        if self.age > 0:
            decay_factor = 1.0 / (1.0 + math.log1p(self.age / 3600))
            self.strength *= decay_factor

        # Emotional memories decay slower
        if self.emotional_weight > 0.5:
            self.strength *= 1.1  # Emotional memories are preserved better


class Hippocampus:
    """
    Episodic Memory System.

    Stores what happened and when.
    - Sparse coding (each memory is unique)
    - Pattern separation (similar events → different memories)
    - Quick encoding (one-shot learning)
    """

    def __init__(self, capacity: int = 10000):
        self.memories: dict[str, Memory] = {}
        self.capacity = capacity
        self.encoding_threshold = 0.3  # Minimum emotional weight to encode

    def encode(
        self,
        content: dict,
        emotional_weight: float = 0.5,
        associations: dict[str, float] = None,
    ) -> Optional[Memory]:
        """
        Encode a new episodic memory.
        Only encodes if emotional weight exceeds threshold.
        """
        if emotional_weight < self.encoding_threshold:
            return None  # Not important enough to remember

        memory_id = f"ep_{int(time.time() * 1000)}_{random.randint(0, 9999)}"

        memory = Memory(
            id=memory_id,
            memory_type=MemoryType.EPISODIC,
            content=content,
            emotional_weight=emotional_weight,
            timestamp=time.time(),
            strength=emotional_weight,  # Initial strength based on emotion
            associations=associations or {},
        )

        # Enforce capacity (forget weakest memories)
        if len(self.memories) >= self.capacity:
            self._forget_weakest()

        self.memories[memory_id] = memory
        return memory

    def recall(
        self,
        query: dict,
        context: dict = None,
        max_results: int = 5,
    ) -> list[Memory]:
        """
        Recall episodic memories based on content similarity.
        Uses pattern matching, not vector similarity.
        """
        scored_memories = []

        for memory in self.memories.values():
            # Compute similarity (simple key overlap)
            score = self._compute_similarity(memory.content, query)

            # Context boost (if context provided)
            if context:
                context_score = self._compute_similarity(memory.content, context)
                score += context_score * 0.3

            # Recency boost (recent memories are easier to recall)
            recency = 1.0 / (1.0 + math.log1p(memory.age / 3600))
            score += recency * 0.2

            # Emotional boost
            score += memory.emotional_weight * 0.3

            # Access frequency boost
            score += min(0.2, memory.access_count * 0.01)

            if score > 0.1:
                scored_memories.append((score, memory))

        # Sort by score, return top results
        scored_memories.sort(key=lambda x: x[0], reverse=True)

        recalled = []
        for score, memory in scored_memories[:max_results]:
            memory.access()
            recalled.append(memory)

        return recalled

    def _compute_similarity(self, a: dict, b: dict) -> float:
        """Simple dictionary similarity (key overlap + value match)."""
        if not a or not b:
            return 0.0

        common_keys = set(a.keys()) & set(b.keys())
        if not common_keys:
            return 0.0

        matches = sum(1 for k in common_keys if a[k] == b[k])
        return matches / max(len(a), len(b))

    def _forget_weakest(self):
        """Remove the weakest memories to make room."""
        if not self.memories:
            return

        # Find memory with lowest strength
        weakest_id = min(
            self.memories.keys(),
            key=lambda k: self.memories[k].strength
        )

        # Only forget if it's not recent
        if not self.memories[weakest_id].is_recent:
            del self.memories[weakest_id]

    def consolidate(self) -> list[Memory]:
        """
        Consolidate recent memories into long-term storage.
        This is the 'sleep' process - replay and strengthen.
        """
        consolidated = []

        for memory in self.memories.values():
            if memory.is_recent and memory.strength > 0.5:
                # Strengthen through consolidation
                memory.strength = min(1.0, memory.strength + 0.2)
                consolidated.append(memory)

        return consolidated


class Neocortex:
    """
    Semantic Memory System.

    Stores what I know about the world.
    - Dense coding (overlapping representations)
    - Gradual learning (many experiences → one concept)
    - Generalization (extract patterns from episodes)
    """

    def __init__(self):
        self.concepts: dict[str, dict] = {}  # concept_id → properties
        self.relationships: dict[str, list[str]] = {}  # concept → related concepts
        self.experience_count: dict[str, int] = {}  # How many times seen

    def learn_from_episode(self, episode: Memory):
        """
        Learn semantic knowledge from episodic memory.
        This is how facts emerge from experiences.
        """
        content = episode.content

        # Extract concepts from episode
        for key, value in content.items():
            if isinstance(value, str):
                concept = value.lower()
            else:
                concept = str(value).lower()

            # Update concept experience count
            self.experience_count[concept] = self.experience_count.get(concept, 0) + 1

            # If seen enough times, create/update concept
            if self.experience_count[concept] >= 3:
                if concept not in self.concepts:
                    self.concepts[concept] = {
                        'first_seen': episode.timestamp,
                        'properties': {},
                        'associations': [],
                    }

                # Update properties
                self.concepts[concept]['properties'][key] = value
                self.concepts[concept]['last_seen'] = time.time()

        # Create relationships between concepts in same episode
        concepts = [
            str(v).lower() for v in content.values()
            if isinstance(v, (str, int, float))
        ]
        for i, c1 in enumerate(concepts):
            for c2 in concepts[i+1:]:
                if c1 != c2:
                    if c1 not in self.relationships:
                        self.relationships[c1] = []
                    if c2 not in self.relationships[c1]:
                        self.relationships[c1].append(c2)

    def query(self, concept: str) -> Optional[dict]:
        """Query semantic memory about a concept."""
        concept = concept.lower()
        if concept in self.concepts:
            return self.concepts[concept]
        return None

    def get_related(self, concept: str) -> list[str]:
        """Get concepts related to a given concept."""
        concept = concept.lower()
        return self.relationships.get(concept, [])


class Cerebellum:
    """
    Procedural Memory System.

    Stores how to do things.
    - Implicit (not conscious)
    - Automatic (once learned, runs without thinking)
    - Learned through repetition
    """

    def __init__(self):
        self.procedures: dict[str, dict] = {}  # procedure → steps/timing
        self.proficiency: dict[str, float] = {}  # procedure → skill level
        self.practice_count: dict[str, int] = {}  # procedure → times practiced

    def learn_procedure(self, name: str, steps: list[dict]):
        """Learn a new procedure."""
        if name not in self.procedures:
            self.procedures[name] = {
                'steps': steps,
                'learned_at': time.time(),
            }
            self.proficiency[name] = 0.1  # Start low
            self.practice_count[name] = 0

    def practice(self, name: str, success: bool = True):
        """Practice a procedure (improves proficiency)."""
        if name in self.procedures:
            self.practice_count[name] += 1

            if success:
                # Success → improve
                self.proficiency[name] = min(
                    1.0,
                    self.proficiency[name] + 0.1 * (1.0 - self.proficiency[name])
                )
            else:
                # Failure → slight improvement (learning from mistakes)
                self.proficiency[name] = min(
                    1.0,
                    self.proficiency[name] + 0.02
                )

    def is_automatic(self, name: str) -> bool:
        """Is this procedure automatic (high proficiency)?"""
        return self.proficiency.get(name, 0) > 0.8


class WorkingMemory:
    """
    Working Memory System.

    What I'm thinking about RIGHT NOW.
    - Limited capacity (7±2 items)
    - Temporary storage
    - Active manipulation
    """

    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: list[dict] = []
        self.attention_focus: Optional[str] = None

    def add(self, item: dict) -> bool:
        """Add item to working memory. Returns False if full."""
        if len(self.items) >= self.capacity:
            # Remove oldest item
            self.items.pop(0)

        self.items.append(item)
        return True

    def remove(self, item: dict):
        """Remove item from working memory."""
        if item in self.items:
            self.items.remove(item)

    def clear(self):
        """Clear working memory."""
        self.items.clear()
        self.attention_focus = None

    def focus(self, item: dict):
        """Focus attention on a specific item."""
        if item in self.items:
            self.attention_focus = str(item)

    @property
    def utilization(self) -> float:
        """How full is working memory?"""
        return len(self.items) / self.capacity

    @property
    def is_overloaded(self) -> bool:
        """Is working memory at capacity?"""
        return len(self.items) >= self.capacity


class MemorySystem:
    """
    Complete Memory System.

    Integrates:
    - Hippocampus (episodic)
    - Neocortex (semantic)
    - Cerebellum (procedural)
    - Working memory (temporary)
    """

    def __init__(self):
        self.hippocampus = Hippocampus()
        self.neocortex = Neocortex()
        self.cerebellum = Cerebellum()
        self.working_memory = WorkingMemory()

        # Consolidation timer
        self.last_consolidation = time.time()
        self.consolidation_interval = 3600  # 1 hour

    def experience(self, content: dict, emotional_weight: float = 0.5):
        """
        Have an experience. This is how memory formation works:
        1. Amygdala tags it with emotional weight
        2. Hippocampus encodes if weight > threshold
        3. Over time, neocortex learns patterns
        """
        # 1. Encode in hippocampus
        memory = self.hippocampus.encode(
            content=content,
            emotional_weight=emotional_weight,
        )

        if memory:
            # 2. Add to working memory (if not overloaded)
            self.working_memory.add(content)

            # 3. Learn semantic knowledge
            self.neocortex.learn_from_episode(memory)

        return memory

    def recall(self, query: dict, context: dict = None) -> list[Memory]:
        """Recall memories based on query."""
        return self.hippocampus.recall(query, context)

    def learn_procedure(self, name: str, steps: list[dict]):
        """Learn a new procedure."""
        self.cerebellum.learn_procedure(name, steps)

    def practice(self, name: str, success: bool = True):
        """Practice a procedure."""
        self.cerebellum.practice(name, success)

    def consolidate(self):
        """
        Consolidate memories (like sleep).
        Transfers recent memories to long-term storage.
        """
        now = time.time()
        if now - self.last_consolidation < self.consolidation_interval:
            return

        # Consolidate hippocampal memories
        consolidated = self.hippocampus.consolidate()

        # Transfer to neocortex
        for memory in consolidated:
            self.neocortex.learn_from_episode(memory)

        self.last_consolidation = now

    def get_stats(self) -> dict:
        """Get memory system statistics."""
        return {
            'episodic_memories': len(self.hippocampus.memories),
            'semantic_concepts': len(self.neocortex.concepts),
            'procedures': len(self.cerebellum.procedures),
            'working_memory_items': len(self.working_memory.items),
            'working_memory_utilization': self.working_memory.utilization,
        }
