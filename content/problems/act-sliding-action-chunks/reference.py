import numpy as np


def sliding_action_chunks(actions, start_indices, horizon):
    if not isinstance(actions, np.ndarray) or not isinstance(start_indices, np.ndarray):
        raise TypeError("actions and starts must be NumPy arrays")
    if type(horizon) is not int:
        raise TypeError("horizon must be a built-in non-bool int")
    if actions.ndim != 2 or actions.dtype not in (np.dtype("float32"), np.dtype("float64")):
        raise ValueError("actions must be float32/64 (T,D)")
    t, d = actions.shape
    if not (1 <= t <= 10000 and 1 <= d <= 64) or not np.isfinite(actions).all() or (np.abs(actions) > 1e6).any():
        raise ValueError("invalid action dimensions or values")
    if start_indices.ndim != 1 or start_indices.dtype != np.dtype("int64") or len(start_indices) > 4096:
        raise ValueError("starts must be int64 (S,)")
    if ((start_indices < 0) | (start_indices >= t)).any():
        raise ValueError("start outside this episode")
    if not 1 <= horizon <= 256 or start_indices.size * horizon * d > 2_000_000:
        raise ValueError("horizon or output size outside bounds")
    indices = start_indices[:, None] + np.arange(horizon)
    valid = indices < t
    chunks = actions[np.minimum(indices, t - 1)].copy()
    chunks[~valid] = 0
    return chunks, valid
