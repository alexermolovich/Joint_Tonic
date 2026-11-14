import math
import numpy as np


def temporal_ensemble(predictions, start_ticks, valid, target_tick, decay):
    if any(not isinstance(x, np.ndarray) for x in (predictions, start_ticks, valid)):
        raise TypeError("prediction, ticks and mask must be arrays")
    if type(target_tick) is not int or type(decay) not in (int, float):
        raise TypeError("invalid scalar type")
    if not 0 <= target_tick <= 1_000_000 or not 0 <= decay <= 100 or not math.isfinite(decay):
        raise ValueError("scalar outside bounds")
    if predictions.ndim != 3 or predictions.dtype not in (np.dtype("float32"), np.dtype("float64")):
        raise ValueError("predictions must be float32/64 (C,H,D)")
    c, h, d = predictions.shape
    if not (0 <= c <= 256 and 1 <= h <= 256 and 1 <= d <= 64) or predictions.size > 2_000_000:
        raise ValueError("prediction dimensions outside bounds")
    if not np.isfinite(predictions).all() or (np.abs(predictions) > 1e6).any():
        raise ValueError("invalid predictions")
    if start_ticks.shape != (c,) or start_ticks.dtype != np.dtype("int64"):
        raise ValueError("ticks must be int64 (C,)")
    if ((start_ticks < 0) | (start_ticks > 1_000_000)).any() or (np.diff(start_ticks) <= 0).any():
        raise ValueError("ticks must increase strictly in range")
    if valid.shape != (c, h) or valid.dtype != np.bool_:
        raise ValueError("valid must be bool (C,H)")
    offsets = target_tick - start_ticks
    rows = np.flatnonzero((offsets >= 0) & (offsets < h))
    rows = rows[valid[rows, offsets[rows]]]
    if rows.size == 0:
        raise ValueError("no eligible predictions")
    normalized = np.exp(-decay * np.arange(rows.size, dtype=np.float64))
    normalized /= normalized.sum()
    action = normalized @ predictions[rows, offsets[rows]].astype(np.float64)
    weights = np.zeros(c, dtype=predictions.dtype)
    weights[rows] = normalized
    return action.astype(predictions.dtype), weights
