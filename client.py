"""
Information Entropy and Lexical Diversity Conversation Turn Pruner.
Zero external dependencies, standard library only.
"""

import math
import re
from typing import Dict, List, Any

LOW_INFORMATION_PHRASES = {
    "hello", "hi", "thanks", "thank you", "ok", "okay", "sure",
    "got it", "sounds good", "great", "cool", "yes", "no"
}

class TurnInformationEntropyPrunerClient:
    """
    Computes Shannon information entropy and lexical richness for each dialog turn:
    - Detects repetitive or vacuous conversational pleasantries
    - Prunes low-entropy turns from long context window before LLM submission
    - Preserves instruction density and operational parameters
    """

    def __init__(self, min_entropy_threshold: float = 2.0):
        self.min_entropy = min_entropy_threshold

    def calculate_shannon_entropy(self, text: str) -> float:
        """Calculates character-level Shannon entropy in bits."""
        if not text:
            return 0.0

        counts = {}
        for ch in text.lower():
            counts[ch] = counts.get(ch, 0) + 1

        total = len(text)
        entropy = 0.0
        for count in counts.values():
            p = count / total
            entropy -= p * math.log2(p)
        return round(entropy, 3)

    def prune_conversation(self, turns: List[Dict[str, str]]) -> Dict[str, Any]:
        """Filters conversational turns below information entropy threshold."""
        pruned_turns = []
        dropped_turns = []

        for turn in turns:
            role = turn.get("role", "user")
            content = turn.get("content", "").strip()

            clean_text = re.sub(r"[^a-zA-Z0-9\s]", "", content).lower().strip()
            entropy = self.calculate_shannon_entropy(content)

            is_noise = clean_text in LOW_INFORMATION_PHRASES or (entropy < self.min_entropy and len(content.split()) < 4)

            if is_noise:
                dropped_turns.append({"role": role, "content": content, "entropy": entropy})
            else:
                pruned_turns.append({"role": role, "content": content, "entropy": entropy})

        return {
            "initial_turn_count": len(turns),
            "retained_turn_count": len(pruned_turns),
            "dropped_turn_count": len(dropped_turns),
            "retained_turns": pruned_turns,
            "dropped_turns": dropped_turns
        }
