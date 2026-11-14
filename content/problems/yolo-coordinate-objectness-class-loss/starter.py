import numpy as np

def yolo_loss(predicted_boxes: np.ndarray, confidence: np.ndarray, class_probabilities: np.ndarray, target_boxes: np.ndarray, target_labels: np.ndarray, responsible: np.ndarray, target_iou: np.ndarray) -> dict:
    """Compute YOLO Coordinate, Objectness, and Class Losses. See the problem contract for shapes and units."""
    raise NotImplementedError
