import numpy as np


def interpolate_joint_state(times, q, queries, max_gap) -> tuple[np.ndarray, np.ndarray]:
    """Return float64 joint states (M,D) and bool validity (M,).

    Times are seconds on one clock; q is already-unwrapped radians.
    Exact samples remain valid. Do not extrapolate or cross excessive gaps.
    """
    # Validate inputs, locate exact samples/brackets, and interpolate valid rows.
    pass
