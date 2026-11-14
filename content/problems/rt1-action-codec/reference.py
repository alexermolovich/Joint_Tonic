"""Uniform, bin-center action codec; not an RT-1 model."""
import numbers
import numpy as np


def action_codec(actions, lower, upper, bins=256, token_offset=0):
    for name, value in (("bins", bins), ("token_offset", token_offset)):
        if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Integral):
            raise TypeError(f"{name} must be an integer")
    if bins < 2 or token_offset < 0 or token_offset + bins - 1 > np.iinfo(np.int64).max:
        raise ValueError("invalid token range")
    try:
        a = np.asarray(actions, dtype=np.float64)
        lo = np.asarray(lower, dtype=np.float64)
        hi = np.asarray(upper, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ValueError("actions and bounds must be numeric") from exc
    if a.ndim < 1 or a.shape[-1] < 1 or lo.shape != (a.shape[-1],) or hi.shape != lo.shape:
        raise ValueError("bounds must match the final action dimension")
    if not all(np.isfinite(x).all() for x in (a, lo, hi)) or np.any(hi <= lo):
        raise ValueError("finite actions and strictly ordered bounds required")
    width = hi - lo
    if not np.isfinite(width).all():
        raise ValueError("bound width must be finite")
    scaled = (np.clip(a, lo, hi) - lo) / width
    indices = np.minimum(np.floor(scaled * bins), bins - 1).astype(np.int64)
    tokens = indices + np.int64(token_offset)
    decoded = lo + (indices.astype(np.float64) + 0.5) * (width / bins)
    return tokens, decoded
