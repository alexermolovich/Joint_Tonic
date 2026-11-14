import numpy as np


def detr_matching_cost(class_probs: np.ndarray, pred_boxes: np.ndarray,
                       target_labels: np.ndarray, target_boxes: np.ndarray,
                       weights: tuple[float,float,float]=(1.0,5.0,2.0)) -> np.ndarray:
    """Return query-by-target costs using negative probability, L1, and negative GIoU."""
    pass
