import numpy as np

def project_bev(points: np.ndarray, ego_to_camera: np.ndarray, intrinsics: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Project BEV Reference Points into Calibrated Cameras. See the problem contract for shapes and units."""
    raise NotImplementedError
