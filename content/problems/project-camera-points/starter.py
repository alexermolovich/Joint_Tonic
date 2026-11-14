import numpy as np


def project_points(points, K, image_size):
    """Return pixels (N,2), copied depths (N,), and bool valid mask.

    Camera axes: x-right, y-down, z-forward. image_size=(width,height).
    z<=1e-8 yields NaN pixels; image bounds are half-open.
    """
    # TODO: validate inputs, mask depth, project, and test image bounds.
    raise NotImplementedError("Implement project_points")
