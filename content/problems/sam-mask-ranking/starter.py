import numpy as np


def rank_masks(masks: np.ndarray,predicted_iou: np.ndarray,k: int) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    """Select candidate masks by descending raw quality and stable original index."""
    pass
