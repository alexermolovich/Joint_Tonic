import numpy as np


def decode_yolo(predictions, image_size, score_threshold=0.25) -> list:
    if not np.isrealobj(predictions):
        raise ValueError("predictions must be real")
    predictions = np.asarray(predictions, dtype=np.float64)
    if predictions.ndim != 4 or any(n < 1 for n in predictions.shape[:3]) or predictions.shape[3] < 6:
        raise ValueError("expected (Sy,Sx,B,5+C) with positive sizes and C>=1")
    if not np.isfinite(predictions).all() or np.any((predictions < 0) | (predictions > 1)):
        raise ValueError("prediction values must be finite in [0,1]")
    size = np.asarray(image_size)
    if size.shape != (2,) or size.dtype.kind not in "iu" or np.any(size <= 0) or any(isinstance(value, (bool, np.bool_)) for value in np.asarray(image_size, dtype=object).flat):
        raise ValueError("image_size must contain positive integers")
    threshold = np.asarray(score_threshold)
    if threshold.ndim != 0 or threshold.dtype.kind not in "fiu" or not np.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("score_threshold must be a finite scalar in [0,1]")
    width, height = map(int, size)
    sy, sx, boxes, _ = predictions.shape
    results = []
    for row in range(sy):
        for col in range(sx):
            for box_index in range(boxes):
                p = predictions[row, col, box_index]
                cx, cy = (col + p[0]) * width / sx, (row + p[1]) * height / sy
                w, h = p[2] * width, p[3] * height
                box = [float(np.clip(cx - w / 2, 0, width)), float(np.clip(cy - h / 2, 0, height)), float(np.clip(cx + w / 2, 0, width)), float(np.clip(cy + h / 2, 0, height))]
                if box[2] <= box[0] or box[3] <= box[1]:
                    continue
                for class_id, class_probability in enumerate(p[5:]):
                    score = float(p[4] * class_probability)
                    if score >= threshold:
                        results.append({"box": box.copy(), "class_id": int(class_id), "score": score})
    return sorted(results, key=lambda record: -record["score"])
