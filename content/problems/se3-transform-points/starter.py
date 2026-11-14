import numpy as np


def transform_points(T, points) -> np.ndarray:
    """Map camera-frame points (3,) or (N,3) into world coordinates.

    Validate a finite proper rigid transform and preserve input storage.
    Return float64 coordinates with the original point shape.
    """
    # TODO: validate T and points, then rotate and translate all rows.
    raise NotImplementedError("Implement transform_points")
