import numpy as np


def _array(value):
    if not isinstance(value, np.ndarray):
        raise TypeError("Expected a NumPy array")
    if value.dtype not in (np.float32, np.float64) or value.size > 1_000_000 or not np.isfinite(value).all():
        raise ValueError("Expected finite bounded floating-point data")


def _shape(shape, patch_size):
    if not isinstance(shape, tuple) or len(shape) != 4 or any(type(v) is not int for v in shape):
        raise ValueError("Expected a four-integer image shape")
    b, c, h, w = shape
    if not 0 <= b <= 1024 or any(not 1 <= v <= 4096 for v in (c, h, w)):
        raise ValueError("Invalid image dimensions")
    if type(patch_size) is not int or not 1 <= patch_size <= 4096 or h % patch_size or w % patch_size:
        raise ValueError("Patch size must divide both image axes")
    if b * c * h * w > 1_000_000:
        raise ValueError("Too many elements")
    return b, c, h, w, patch_size


def patchify(images, patch_size):
    _array(images)
    b, c, h, w, p = _shape(images.shape, patch_size)
    return images.reshape(b, c, h//p, p, w//p, p).transpose(0, 2, 4, 1, 3, 5).reshape(b, (h//p)*(w//p), c*p*p).copy()


def unpatchify(patches, image_shape, patch_size):
    _array(patches)
    b, c, h, w, p = _shape(image_shape, patch_size)
    if patches.shape != (b, (h//p)*(w//p), c*p*p):
        raise ValueError("Patch shape does not match image shape")
    return patches.reshape(b, h//p, w//p, c, p, p).transpose(0, 3, 1, 4, 2, 5).reshape(b, c, h, w).copy()
