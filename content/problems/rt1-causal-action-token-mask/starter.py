import numpy as np


def rt1_attention_mask(steps: int, visual_tokens: int, action_tokens: int) -> np.ndarray:
    """Return a bool query-by-key allowed-attention matrix."""
    # Keep causal pairs except those whose query and key are both action slots.
    pass
