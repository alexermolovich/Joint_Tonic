import math
from numbers import Real
import numpy as np


def planar_ik(L1, L2, target):
    for length in (L1, L2):
        if not isinstance(length, Real) or isinstance(length, bool) or not 1e-3 <= length <= 1e3:
            raise ValueError("Link lengths must be real scalars in [1e-3,1e3]")
    L1, L2 = float(L1), float(L2)
    if max(L1,L2)/min(L1,L2)>1e3:
        raise ValueError("Link-length ratio must not exceed 1000")
    try:
        raw = np.asarray(target)
        if raw.dtype.kind not in "iuf":
            raise ValueError("Target must be real numeric data")
        point = raw.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Invalid target") from exc
    if point.shape != (2,) or not np.isfinite(point).all() or np.any(np.abs(point) > 1e6):
        raise ValueError("Target must have shape (2,) with finite bounded coordinates")
    x, y = map(float, point)
    r = math.hypot(x, y)
    if r < abs(L1 - L2) - 1e-9 or r > L1 + L2 + 1e-9:
        return dict(reachable=False, angles=None, singular=False)
    if L1 == L2 and r == 0:
        return dict(reachable=True, angles=np.array([0., math.pi]), singular=True)
    cosine = (r*r - L1*L1 - L2*L2) / (2*L1*L2)
    q2 = math.acos(min(1., max(-1., cosine)))
    q1 = math.atan2(y, x) - math.atan2(L2*math.sin(q2), L1+L2*math.cos(q2))
    q1 = (q1+math.pi) % (2*math.pi) - math.pi
    return dict(reachable=True, angles=np.array([q1, q2], dtype=np.float64), singular=bool(abs(math.sin(q2)) <= 1e-9))
