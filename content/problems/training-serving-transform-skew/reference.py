import math
import re
import numpy as np


def transform_skew(train: np.ndarray, serve: np.ndarray,
                   feature_names: list[str], atol: np.ndarray,
                   rtol: float = 0.0) -> list[tuple[int, str]]:
    if any(not isinstance(value, np.ndarray) or value.dtype != np.float64
           for value in (train, serve, atol)):
        raise ValueError("Expected float64 NumPy arrays")
    if train.ndim != 2 or serve.ndim != 2 or train.shape != serve.shape:
        raise ValueError("Expected aligned feature matrices")
    rows, columns = train.shape
    if rows > 10000 or columns > 128 or atol.shape != (columns,):
        raise ValueError("Invalid shape or size")
    if not isinstance(feature_names, list) or len(feature_names) != columns:
        raise ValueError("Expected one feature name per column")
    if any(not isinstance(name, str) or re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", name) is None
           for name in feature_names) or len(set(feature_names)) != columns:
        raise ValueError("Invalid or duplicate feature name")
    if type(rtol) not in (int, float) or not 0 <= rtol <= 1 or not math.isfinite(rtol):
        raise ValueError("Invalid relative tolerance")
    for values in (train, serve):
        if not np.isfinite(values).all() or np.any(np.abs(values) > 1e100):
            raise ValueError("Invalid feature values")
    if not np.isfinite(atol).all() or np.any(atol < 0) or np.any(atol > 1e100):
        raise ValueError("Invalid absolute tolerances")
    mismatches = np.abs(serve - train) > atol + rtol * np.abs(train)
    return [(int(row), feature_names[int(column)]) for row, column in np.argwhere(mismatches)]
