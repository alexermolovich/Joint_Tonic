import torch


def build_vit_tokens(patches,projection,bias,cls,positions):
    values=(patches,projection,bias,cls,positions)
    for v in values:
        if not isinstance(v,torch.Tensor):raise TypeError("Expected tensors")
        if v.device.type!="cpu" or v.dtype not in (torch.float32,torch.float64) or v.numel()>1_000_000 or not torch.isfinite(v).all() or torch.any(v.abs()>100):
            raise ValueError("Invalid tensor")
    if any(v.dtype!=patches.dtype for v in values) or patches.ndim!=3 or projection.ndim!=2:
        raise ValueError("Invalid dtype or rank")
    b,n,f=patches.shape
    if not 0<=b<=1024 or not 1<=n<=1024 or not 1<=f<=1024:
        raise ValueError("Invalid patch dimensions")
    d=projection.shape[1]
    if not 1<=d<=1024 or projection.shape[0]!=f or bias.shape!=(d,) or cls.shape!=(d,) or positions.shape!=(n+1,d) or b*(n+1)*d>1_000_000:
        raise ValueError("Incompatible token shapes")
    projected=patches@projection+bias
    sequence=torch.cat((cls.view(1,1,d).expand(b,1,d),projected),dim=1)
    return sequence+positions
