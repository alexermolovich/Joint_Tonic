import numpy as np


def temporal_ensemble(
    predictions: np.ndarray,
    start_ticks: np.ndarray,
    valid: np.ndarray,
    target_tick: int,
    decay: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Blend eligible predictions for one target tick, ranked oldest first."""
    pass
