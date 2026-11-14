import numpy as np

def pose_diagnostics(pixel_residuals: np.ndarray, color_residuals: np.ndarray, valid: np.ndarray, pixel_limit: float, color_limit: float) -> dict:
    """Detect Bad Poses with Reprojection and Render Residuals. See the problem contract for shapes and units."""
    raise NotImplementedError
