import torch


def fuse_visual_features(first, second, projection, bias, first_valid, second_valid):
    values = (first, second, projection, bias, first_valid, second_valid)
    if any(not isinstance(v, torch.Tensor) for v in values):
        raise TypeError("all inputs must be tensors")
    if first.ndim != 3 or second.ndim != 3 or projection.ndim != 2 or bias.ndim != 1:
        raise ValueError("invalid ranks")
    b, n, c1 = first.shape
    c2, e = second.shape[-1], bias.shape[0]
    if not (1 <= b <= 32 and 1 <= n <= 512 and 1 <= c1 <= 256 and 1 <= c2 <= 256 and 1 <= e <= 512):
        raise ValueError("invalid dimensions")
    if second.shape[:2] != (b,n) or projection.shape != (c1+c2,e) or b*n*e > 1_000_000:
        raise ValueError("unaligned shape or excessive output")
    for v in values[:4]:
        if v.device.type != 'cpu' or v.dtype not in (torch.float32,torch.float64) or v.dtype != first.dtype:
            raise ValueError("common CPU floating dtype required")
        if v.numel() > 1_000_000 or not torch.isfinite(v).all() or (v.abs()>100).any():
            raise ValueError("invalid values or size")
    for mask in values[4:]:
        if mask.device.type != 'cpu' or mask.dtype != torch.bool or mask.shape != (b,n):
            raise ValueError("invalid mask")
    valid = first_valid & second_valid
    fused = (torch.cat((first,second),dim=-1) @ projection + bias).masked_fill(~valid[...,None],0)
    return fused, valid
