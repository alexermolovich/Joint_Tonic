# Reference solution

Multiply each sensor feature row by the supplied projection matrix, then add the bias and zero invalid rows. Masking after the bias prevents missing tokens from receiving a bias-only embedding or contributing to its gradient. The operation preserves token positions and changes only feature width. Time is O(BNCE), output storage O(BNE).

~~~python
import torch


def project_sensor_features(features, weight, bias, valid):
    if any(not isinstance(x, torch.Tensor) for x in (features, weight, bias, valid)):
        raise TypeError("all arguments must be tensors")
    if features.ndim != 3 or weight.ndim != 2 or bias.ndim != 1:
        raise ValueError("invalid tensor ranks")
    b, n, c = features.shape
    e = bias.shape[0]
    if not (1 <= b <= 32 and 0 <= n <= 1024 and 1 <= c <= 512 and 1 <= e <= 512):
        raise ValueError("dimensions outside bounds")
    if weight.shape != (c, e) or b * n * e > 2_000_000:
        raise ValueError("weight shape or output size invalid")
    for value in (features, weight, bias):
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64) or value.dtype != features.dtype:
            raise ValueError("matching CPU floating dtypes required")
        if value.numel() > 2_000_000 or not torch.isfinite(value).all() or (value.abs() > 1000).any():
            raise ValueError("floating values or size outside bounds")
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != (b, n):
        raise ValueError("valid must be CPU bool (B,N)")
    return (features @ weight + bias).masked_fill(~valid[:, :, None], 0)

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
