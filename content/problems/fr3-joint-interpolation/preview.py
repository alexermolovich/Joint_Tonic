"""Public demonstration only; executed inside the isolated learner worker."""
import numpy as np


def build_preview(solution):
    start = [0, 0, 0, -1.57079, 0, 1.57079, -0.7853]
    goal = [0.4, -0.3, 0.2, -1.8, 0.1, 1.9, -0.4]
    result = solution.interpolate_fr3_joints(start, goal, 41)
    if not isinstance(result, np.ndarray) or result.shape != (41, 7) or result.dtype != np.float64:
        raise ValueError("The public preview must return a float64 array with shape (41, 7)")
    lower = np.array([-2.9007, -1.8361, -2.9007, -3.0770, -2.8763, 0.4398, -3.0508])
    upper = np.array([2.9007, 1.8361, 2.9007, -0.1169, 2.8763, 4.6216, 3.0508])
    if not np.isfinite(result).all() or np.any(result < lower) or np.any(result > upper):
        raise ValueError("The public preview contains non-finite or out-of-limit joint values")
    return {"kind": "fr3-joint-trajectory-v1", "q": result.tolist()}
