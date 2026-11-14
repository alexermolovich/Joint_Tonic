import numpy as np

def detector_frontier(accuracy: np.ndarray, latency_ms: np.ndarray, budget_ms: float) -> tuple[np.ndarray, int]:
    """Benchmark Detector Accuracy Against Edge Latency. See the problem contract for shapes and units."""
    raise NotImplementedError
