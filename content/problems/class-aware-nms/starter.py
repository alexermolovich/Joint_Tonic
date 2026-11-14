import numpy as np


def class_aware_nms(boxes, scores, class_ids, iou_threshold=0.5) -> list:
    """Return kept original indices in score-descending, stable greedy order.

    Suppress matching classes only when IoU is strictly above threshold.
    Continuous xyxy geometry; zero-area IoU is zero; preserve inputs.
    """
    # TODO: validate, order candidates, and apply greedy class-aware filtering.
    raise NotImplementedError("Implement class_aware_nms")
