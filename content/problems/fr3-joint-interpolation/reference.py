import numpy as np

LOWER = np.array([-2.9007, -1.8361, -2.9007, -3.0770, -2.8763, 0.4398, -3.0508])
UPPER = np.array([2.9007, 1.8361, 2.9007, -0.1169, 2.8763, 4.6216, 3.0508])


def interpolate_fr3_joints(q_start, q_goal, num_steps):
    if isinstance(num_steps, (bool, np.bool_)) or not isinstance(num_steps, (int, np.integer)) or not 2 <= num_steps <= 101:
        raise ValueError("num_steps must be an integer from 2 through 101")
    endpoints = []
    for value in (q_start, q_goal):
        try:
            q = np.asarray(value)
            if q.shape != (7,) or q.dtype.kind not in "iuf":
                raise ValueError("Joint inputs must be real vectors of shape (7,)")
            q = q.astype(np.float64)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("Invalid joint vector") from exc
        if not np.isfinite(q).all() or np.any(q < LOWER) or np.any(q > UPPER):
            raise ValueError("Joint positions must be finite and inside the FR3 model limits")
        endpoints.append(q)
    alpha = np.linspace(0.0, 1.0, int(num_steps), dtype=np.float64)[:, None]
    return (1.0 - alpha) * endpoints[0] + alpha * endpoints[1]
