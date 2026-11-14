import numpy as np


def pairwise_iou(boxes_a, boxes_b) -> np.ndarray:
    arrays = []
    for boxes in (boxes_a, boxes_b):
        if not np.isrealobj(boxes):
            raise ValueError("boxes must be real")
        boxes = np.asarray(boxes, dtype=np.float64)
        if boxes.ndim != 2 or boxes.shape[1] != 4:
            raise ValueError("boxes must have shape (N,4)")
        if not np.isfinite(boxes).all() or np.any(np.abs(boxes) > 1e6):
            raise ValueError("coordinates must be finite and within [-1e6,1e6]")
        if np.any(boxes[:, 2:] < boxes[:, :2]):
            raise ValueError("box corners must not be reversed")
        arrays.append(boxes)
    a, b = arrays
    lo = np.maximum(a[:, None, :2], b[None, :, :2])
    hi = np.minimum(a[:, None, 2:], b[None, :, 2:])
    intersection = np.prod(np.maximum(hi - lo, 0), axis=-1)
    area_a = np.prod(a[:, 2:] - a[:, :2], axis=1)
    area_b = np.prod(b[:, 2:] - b[:, :2], axis=1)
    union = area_a[:, None] + area_b[None, :] - intersection
    return np.divide(intersection, union, out=np.zeros_like(intersection), where=union > 0)
