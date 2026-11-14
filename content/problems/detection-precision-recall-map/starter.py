import numpy as np

def detection_map(pred_boxes: np.ndarray, scores: np.ndarray, pred_labels: np.ndarray, pred_images: np.ndarray, target_boxes: np.ndarray, target_labels: np.ndarray, target_images: np.ndarray, num_classes: int, iou_threshold: float) -> dict:
    """Evaluate Detection with IoU, Precision-Recall, and mAP. See the problem contract for shapes and units."""
    raise NotImplementedError
