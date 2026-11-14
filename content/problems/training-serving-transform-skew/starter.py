"""Detect Training-Serving Transform Skew."""
import numpy as np


def transform_skew(train: np.ndarray, serve: np.ndarray,
                   feature_names: list[str], atol: np.ndarray,
                   rtol: float = 0.0) -> list[tuple[int, str]]:
    """Return strict-tolerance failures in row-major order."""
    raise NotImplementedError("Implement transform_skew")
