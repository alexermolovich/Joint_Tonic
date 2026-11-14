# Reference solution

Validate every tensor before masking. Apply softmax along the spatial axis after replacing invalid logits with negative infinity, then multiply the attention weights by the feature matrix. Because no tensor is detached, gradients reach both the feature extractor and the attention-logit generator. Time is O(BKNC); auxiliary/output storage is O(BK(N+C)).

~~~python
import torch


def compact_visual_tokens(features, logits, valid=None):
    if not isinstance(features, torch.Tensor) or not isinstance(logits, torch.Tensor):
        raise TypeError("features and logits must be tensors")
    if valid is not None and not isinstance(valid, torch.Tensor):
        raise TypeError("valid must be a tensor or None")
    if features.ndim != 3 or logits.ndim != 3:
        raise ValueError("expected rank-three features and logits")
    b, n, c = features.shape
    if not (1 <= b <= 16 and 1 <= n <= 4096 and 1 <= c <= 256):
        raise ValueError("feature shape outside bounds")
    if logits.shape[0] != b or logits.shape[2] != n or not 1 <= logits.shape[1] <= min(n, 32):
        raise ValueError("logit shape mismatch")
    for value, limit in ((features, 1e6), (logits, 1e4)):
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64):
            raise ValueError("expected CPU float32 or float64")
        if value.numel() > 2_000_000 or not torch.isfinite(value).all() or (value.abs() > limit).any():
            raise ValueError("invalid tensor values or size")
    if logits.dtype != features.dtype:
        raise ValueError("floating dtypes must match")
    if valid is None:
        valid = torch.ones((b, n), dtype=torch.bool)
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != (b, n):
        raise ValueError("valid must be CPU bool (B,N)")
    if not valid.any(dim=1).all():
        raise ValueError("each image needs a valid location")
    weights = torch.softmax(logits.masked_fill(~valid[:, None, :], -torch.inf), dim=-1)
    return torch.bmm(weights, features), weights

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
