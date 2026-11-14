"""Original Joint Tonic teaching implementation."""
import math
import numbers
import torch
import torch.nn.functional as F


def clip_loss(image_features, text_features, temperature=0.07):
    if not isinstance(image_features, torch.Tensor) or not isinstance(text_features, torch.Tensor):
        raise TypeError("features must be tensors")
    if (image_features.ndim != 2 or image_features.shape != text_features.shape
            or min(image_features.shape, default=0) < 1):
        raise ValueError("features must have equal nonempty (B,D) shapes")
    if (not image_features.is_floating_point() or not text_features.is_floating_point()
            or image_features.dtype != text_features.dtype
            or image_features.device != text_features.device):
        raise ValueError("features must share floating dtype and device")
    if (isinstance(temperature, bool) or not isinstance(temperature, numbers.Real)
            or not math.isfinite(float(temperature)) or temperature <= 0):
        raise ValueError("temperature must be finite and positive")
    for x in (image_features, text_features):
        if not bool(torch.isfinite(x).all()) or bool((torch.linalg.vector_norm(x, dim=1) == 0).any()):
            raise ValueError("features must be finite and nonzero")
    images = F.normalize(image_features, dim=1)
    texts = F.normalize(text_features, dim=1)
    logits = images @ texts.T / temperature
    labels = torch.arange(logits.shape[0], device=logits.device)
    return (F.cross_entropy(logits, labels) + F.cross_entropy(logits.T, labels)) / 2
