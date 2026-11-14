import numpy as np


def build_query_targets(labels: np.ndarray,target_valid: np.ndarray,matches: np.ndarray,
                         num_classes: int,eos_weight: float) -> tuple[np.ndarray,np.ndarray]:
    """Return object/no-object targets and query weights from a valid supplied assignment."""
    pass
