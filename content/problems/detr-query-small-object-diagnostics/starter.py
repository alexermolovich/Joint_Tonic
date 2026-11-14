import numpy as np

def diagnose_queries(features: np.ndarray, predicted_boxes: np.ndarray, target_boxes: np.ndarray, cosine_limit: float, iou_limit: float, small_area: float) -> dict:
    """Diagnose Query Collapse and Missed Small Objects. See the problem contract for shapes and units."""
    raise NotImplementedError
