import numpy as np

def camera_health(received: np.ndarray, residuals: np.ndarray, valid: np.ndarray, max_dropout: float, max_rmse: float) -> dict:
    """Diagnose Camera Dropout and Calibration Drift in BEV. See the problem contract for shapes and units."""
    raise NotImplementedError
