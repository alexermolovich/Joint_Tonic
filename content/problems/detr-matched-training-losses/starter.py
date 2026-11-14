import numpy as np

def detr_losses(logits: np.ndarray, predicted_boxes: np.ndarray, target_labels: np.ndarray, target_boxes: np.ndarray, assignment: np.ndarray, eos_weight: float) -> dict:
    """Compute DETR Classification, L1, and GIoU Losses. See the problem contract for shapes and units."""
    raise NotImplementedError
