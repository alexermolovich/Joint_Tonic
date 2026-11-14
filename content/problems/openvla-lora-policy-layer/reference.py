import math
import torch


def lora_policy_linear(x, base_weight, adapter_down, adapter_up, alpha):
    values = (x, base_weight, adapter_down, adapter_up)
    if any(not isinstance(v,torch.Tensor) for v in values):
        raise TypeError("tensor inputs required")
    if x.ndim != 3 or any(v.ndim != 2 for v in values[1:]):
        raise ValueError("invalid ranks")
    b,t,i = x.shape
    o,r = base_weight.shape[0],adapter_down.shape[0]
    if not (1<=b<=32 and 1<=t<=256 and 1<=i<=256 and 1<=o<=256 and 1<=r<=min(i,o,64)):
        raise ValueError("dimensions out of range")
    if base_weight.shape != (o,i) or adapter_down.shape != (r,i) or adapter_up.shape != (o,r) or b*t*o>1_000_000:
        raise ValueError("invalid shapes or output size")
    for v in values:
        if v.device.type!='cpu' or v.dtype not in (torch.float32,torch.float64) or v.dtype!=x.dtype:
            raise ValueError("common CPU floating dtype required")
        if v.numel()>1_000_000 or not torch.isfinite(v).all() or (v.abs()>10).any():
            raise ValueError("invalid values or size")
    if type(alpha) not in (int,float) or not 0<=alpha<=64 or not math.isfinite(alpha):
        raise ValueError("alpha must be a finite built-in number in [0,64]")
    return x @ base_weight.detach().T + (alpha/r)*((x @ adapter_down.T) @ adapter_up.T)
