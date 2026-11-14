import numpy as np


def sliding_action_chunks(
    actions: np.ndarray, start_indices: np.ndarray, horizon: int
) -> tuple[np.ndarray, np.ndarray]:
    """Extract fixed-length action targets with zero padding and True=valid."""
    pass
