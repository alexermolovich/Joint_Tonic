import numpy as np


def pairwise_iou(boxes_a, boxes_b) -> np.ndarray:
    """Return float64 IoU matrix (N,M) for continuous xyxy boxes.

    Reversed boxes are invalid; zero-area boxes have IoU zero.
    Use broadcasting across both sets without mutating inputs.
    """
    # TODO: validate boxes, broadcast intersections, and divide by unions.
    raise NotImplementedError("Implement pairwise_iou")
