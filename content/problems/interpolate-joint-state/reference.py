import numpy as np


def _array(value):
    try:
        raw = np.asarray(value)
        if raw.dtype.kind not in "iuf":
            raise ValueError("Expected real numeric data")
        result = raw.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(result).all() or np.any(np.abs(result) > 1e6):
        raise ValueError("Values must be finite and bounded by 1e6")
    return result


def interpolate_joint_state(times, q, queries, max_gap):
    times, q, queries, gap = map(_array, (times, q, queries, max_gap))
    if times.ndim != 1 or len(times) < 2 or np.any(np.diff(times) <= 0):
        raise ValueError("Need at least two strictly increasing times")
    if q.ndim != 2 or q.shape[0] != len(times) or q.shape[1] < 1:
        raise ValueError("q must have shape (T,D), D>=1")
    if queries.ndim != 1 or gap.ndim != 0 or gap <= 0:
        raise ValueError("Queries must be 1D and max_gap a positive scalar")
    aligned = np.full((len(queries), q.shape[1]), np.nan, dtype=np.float64)
    valid = np.zeros(len(queries), dtype=bool)
    right = np.searchsorted(times, queries)
    safe = np.minimum(right, len(times) - 1)
    exact = (right < len(times)) & (times[safe] == queries)
    aligned[exact] = q[safe[exact]]
    valid[exact] = True
    rows = np.flatnonzero(~exact & (right > 0) & (right < len(times)))
    hi = right[rows]
    allowed = (times[hi] - times[hi - 1]) <= gap
    rows, hi = rows[allowed], hi[allowed]
    weight = ((queries[rows] - times[hi - 1]) / (times[hi] - times[hi - 1]))[:, None]
    aligned[rows] = (1 - weight) * q[hi - 1] + weight * q[hi]
    valid[rows] = True
    return aligned, valid
