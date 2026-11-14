import numpy as np


def transform_points(T, points) -> np.ndarray:
    if not np.isrealobj(T) or not np.isrealobj(points):
        raise ValueError("inputs must be real")
    T = np.asarray(T, dtype=np.float64)
    points = np.asarray(points, dtype=np.float64)
    if T.shape != (4, 4) or not (points.shape == (3,) or (points.ndim == 2 and points.shape[1] == 3)):
        raise ValueError("expected T (4,4) and points (3,) or (N,3)")
    if not np.isfinite(T).all() or not np.isfinite(points).all():
        raise ValueError("inputs must be finite")
    R, t = T[:3, :3], T[:3, 3]
    if not np.allclose(T[3], [0, 0, 0, 1], rtol=0, atol=1e-7):
        raise ValueError("invalid homogeneous bottom row")
    if not np.allclose(R.T @ R, np.eye(3), rtol=0, atol=1e-7) or not np.isclose(np.linalg.det(R), 1, rtol=0, atol=1e-7):
        raise ValueError("rotation must be proper and orthonormal")
    return points @ R.T + t
