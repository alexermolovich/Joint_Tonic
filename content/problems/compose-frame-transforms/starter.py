import numpy as np


def compose_transforms(first: dict, second: dict) -> tuple[np.ndarray, np.ndarray]:
    """Return (a-from-c, c-from-a), each a new float64 (4,4) array.

    Records contain matrix, target, source, stamp (seconds), and unit="m".
    Use a-from-b notation and homogeneous column vectors.
    """
    # Validate frame/time/unit compatibility and rigid matrices, then compose.
    pass
