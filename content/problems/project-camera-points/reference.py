import numpy as np


def project_points(points, K, image_size):
    if not np.isrealobj(points) or not np.isrealobj(K):
        raise ValueError("points and K must be real")
    points = np.asarray(points, dtype=np.float64)
    K = np.asarray(K, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3 or K.shape != (3, 3):
        raise ValueError("expected points (N,3) and K (3,3)")
    if not np.isfinite(points).all() or not np.isfinite(K).all():
        raise ValueError("points and K must be finite")
    canonical = np.array([[K[0, 0], 0, K[0, 2]], [0, K[1, 1], K[1, 2]], [0, 0, 1.]])
    if K[0, 0] <= 0 or K[1, 1] <= 0 or not np.allclose(K, canonical, rtol=0, atol=1e-9):
        raise ValueError("K must be positive-focal-length zero-skew pinhole intrinsics")
    size = np.asarray(image_size)
    if size.shape != (2,) or size.dtype.kind not in "iu" or np.any(size <= 0) or any(isinstance(value, (bool, np.bool_)) for value in np.asarray(image_size, dtype=object).flat):
        raise ValueError("image_size must contain positive integers")
    width, height = size
    depths = points[:, 2].copy()
    front = depths > 1e-8
    pixels = np.full((len(points), 2), np.nan, dtype=np.float64)
    pixels[front, 0] = K[0, 0] * points[front, 0] / depths[front] + K[0, 2]
    pixels[front, 1] = K[1, 1] * points[front, 1] / depths[front] + K[1, 2]
    valid = front & (pixels[:, 0] >= 0) & (pixels[:, 0] < width) & (pixels[:, 1] >= 0) & (pixels[:, 1] < height)
    return pixels, depths, valid
