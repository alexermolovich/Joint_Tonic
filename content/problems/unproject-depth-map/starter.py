import numpy as np


def unproject_depth(depth, K) -> tuple[np.ndarray, np.ndarray]:
    """Return float64 points (H*W,3) and bool valid (H*W,).

    Depth is camera z in meters. Pixel centers are integer columns/rows.
    Preserve row-major pixel order; missing depths produce three NaNs.
    """
    # Validate calibration, create pixel grids, and unproject valid depths.
    pass
