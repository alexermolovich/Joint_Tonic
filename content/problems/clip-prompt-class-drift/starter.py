import numpy as np

def prompt_class_drift(old_prototypes: np.ndarray, new_prototypes: np.ndarray, old_counts: np.ndarray, new_counts: np.ndarray) -> tuple[np.ndarray, float]:
    """Detect Prompt and Class Distribution Drift. See the problem contract for shapes and units."""
    raise NotImplementedError
