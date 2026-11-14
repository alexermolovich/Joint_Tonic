import numpy as np


def compose_quaternions(q_after,q_before) -> np.ndarray:
    """Normalize and compose scalar-first Hamilton quaternions (w,x,y,z).

    Apply q_before first, then q_after. Preserve the product sign.
    Return a new float64 unit quaternion of shape (4,).
    """
    # Normalize safely, take the Hamilton product, and renormalize.
    pass
