import torch


def normalize_clip_embeddings(image_features, text_features):
    for value in (image_features, text_features):
        if not isinstance(value, torch.Tensor):
            raise TypeError("Expected tensors")
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64):
            raise ValueError("Expected CPU floating-point tensors")
        if value.ndim != 2 or not 1 <= value.shape[0] <= 1024 or not 1 <= value.shape[1] <= 4096 or value.numel() > 1_000_000:
            raise ValueError("Invalid embedding shape")
        if not torch.isfinite(value).all():
            raise ValueError("Features must be finite")
        norm = torch.linalg.vector_norm(value.to(torch.float64), dim=1)
        if torch.any(norm < 1e-6) or torch.any(norm > 1e6):
            raise ValueError("Row norm outside supported range")
    if image_features.shape != text_features.shape or image_features.dtype != text_features.dtype:
        raise ValueError("Embeddings must share shape and dtype")
    return tuple(x / torch.linalg.vector_norm(x, dim=1, keepdim=True) for x in (image_features, text_features))
