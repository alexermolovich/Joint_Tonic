import numpy as np


def constrained_action_step(logits: np.ndarray, vocabulary: np.ndarray,
                            positions: np.ndarray, channels: int) -> tuple[np.ndarray, np.ndarray]:
    """Return allowed greedy token IDs (B,) and masked probabilities (B,V)."""
    # Implement one grammar-constrained decoder step.
    pass
