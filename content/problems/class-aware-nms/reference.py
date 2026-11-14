import numpy as np


def class_aware_nms(boxes, scores, class_ids, iou_threshold=0.5) -> list:
    if not np.isrealobj(boxes) or not np.isrealobj(scores) or not np.isrealobj(class_ids):
        raise ValueError("inputs must be real")
    boxes = np.asarray(boxes, dtype=np.float64)
    scores = np.asarray(scores, dtype=np.float64)
    raw_classes = np.asarray(class_ids)
    if boxes.ndim != 2 or boxes.shape[1] != 4 or scores.shape != (len(boxes),) or raw_classes.shape != (len(boxes),):
        raise ValueError("expected boxes (N,4), scores (N,), class_ids (N,)")
    if not np.isfinite(boxes).all() or np.any(np.abs(boxes) > 1e6) or np.any(boxes[:, 2:] < boxes[:, :2]):
        raise ValueError("boxes must be finite, bounded, and non-reversed")
    if not np.isfinite(scores).all() or np.any((scores < 0) | (scores > 1)):
        raise ValueError("scores must be finite in [0,1]")
    if raw_classes.dtype.kind not in "fiu" or any(isinstance(value, (bool, np.bool_)) for value in np.asarray(class_ids, dtype=object).flat) or not np.isfinite(raw_classes).all() or np.any(raw_classes < 0) or np.any(raw_classes > 2**31 - 1) or np.any(raw_classes != np.floor(raw_classes)):
        raise ValueError("class_ids must be nonnegative integer values")
    classes = raw_classes.astype(np.int64)
    threshold = np.asarray(iou_threshold)
    if threshold.ndim != 0 or threshold.dtype.kind not in "fiu" or not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("iou_threshold must be a finite scalar in [0,1]")
    areas = np.prod(boxes[:, 2:] - boxes[:, :2], axis=1)
    order = np.argsort(-scores, kind="stable")
    kept = []
    while order.size:
        chosen = int(order[0]); kept.append(chosen)
        rest = order[1:]
        lo = np.maximum(boxes[chosen, :2], boxes[rest, :2])
        hi = np.minimum(boxes[chosen, 2:], boxes[rest, 2:])
        intersection = np.prod(np.maximum(hi - lo, 0), axis=1)
        union = areas[chosen] + areas[rest] - intersection
        overlap = np.divide(intersection, union, out=np.zeros_like(intersection), where=union > 0)
        order = rest[(classes[rest] != classes[chosen]) | (overlap <= threshold)]
    return kept
