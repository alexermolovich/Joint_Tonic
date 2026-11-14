import torch


def feature_transform_penalty(transforms):
    if not isinstance(transforms,torch.Tensor):raise TypeError("Expected tensor")
    if transforms.device.type!="cpu" or transforms.dtype not in (torch.float32,torch.float64) or transforms.ndim!=3:
        raise ValueError("Invalid transforms")
    b,d,e=transforms.shape
    if not 1<=b<=256 or not 1<=d<=64 or e!=d or transforms.numel()>1_000_000 or not torch.isfinite(transforms).all() or torch.any(transforms.abs()>10):
        raise ValueError("Invalid transform values or shape")
    residual=transforms@transforms.transpose(-1,-2)-torch.eye(d,dtype=transforms.dtype)
    return residual.square().sum(dim=(-2,-1)).mean()
