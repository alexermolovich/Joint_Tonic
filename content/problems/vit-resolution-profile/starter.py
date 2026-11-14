import numpy as np

def profile_vit(resolutions: np.ndarray, patch_size: int, heads: int, bytes_per_value: int, latency_ms: np.ndarray) -> dict:
    """Profile Token Count, Memory, and Latency by Resolution. See the problem contract for shapes and units."""
    raise NotImplementedError
