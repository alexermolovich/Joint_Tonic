import numpy as np


def decode_yolo(predictions, image_size, score_threshold=0.25) -> list:
    """Decode (Sy,Sx,B,5+C): tx,ty,w,h,objectness,class values.

    Sizes are direct image fractions. Emit each class score >= cutoff,
    clip boxes, skip zero area, and retain traversal order for score ties.
    """
    # TODO: validate, decode, filter class records, and sort stably.
    raise NotImplementedError("Implement decode_yolo")
