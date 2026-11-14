import numpy as np


def _real_array(value):
    try:
        array = np.asarray(value)
        if array.dtype.kind not in "iuf":
            raise ValueError("Expected real integer or floating data")
        return array.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc


def unproject_depth(depth, K):
    depth, K = map(_real_array, (depth, K))
    if depth.ndim != 2 or np.any(np.abs(depth[np.isfinite(depth)]) > 1e6):
        raise ValueError("Depth must be 2D, with finite magnitudes <=1e6")
    if K.shape != (3, 3) or not np.isfinite(K).all():
        raise ValueError("K must be finite (3,3)")
    fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]
    expected = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    if not (1e-6 <= fx <= 1e6 and 1e-6 <= fy <= 1e6 and abs(cx) <= 1e6 and abs(cy) <= 1e6):
        raise ValueError("Invalid focal length or principal point")
    if not np.allclose(K, expected, rtol=0, atol=1e-9):
        raise ValueError("K must use the zero-skew pinhole form")
    v, u = np.indices(depth.shape)
    z = depth.ravel()
    valid = np.isfinite(z) & (z > 0)
    points = np.full((z.size, 3), np.nan, dtype=np.float64)
    points[valid, 0] = (u.ravel()[valid] - cx) * z[valid] / fx
    points[valid, 1] = (v.ravel()[valid] - cy) * z[valid] / fy
    points[valid, 2] = z[valid]
    return points, valid
