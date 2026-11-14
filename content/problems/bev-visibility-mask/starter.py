import numpy as np

def bev_visibility(uv: np.ndarray, depth: np.ndarray, image_sizes: np.ndarray) -> np.ndarray:
    """Mask Out-of-View and Behind-Camera Samples. See the problem contract for shapes and units."""
    raise NotImplementedError
