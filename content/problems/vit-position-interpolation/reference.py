import torch
import torch.nn.functional as F


def resize_positions(positions, old_grid, new_grid):
    if not isinstance(positions, torch.Tensor):
        raise TypeError("positions must be a tensor")
    if positions.device.type != "cpu" or positions.dtype not in (torch.float32, torch.float64) or positions.ndim != 3:
        raise ValueError("CPU floating positional table required")
    for grid in (old_grid, new_grid):
        if not isinstance(grid, tuple) or len(grid) != 2 or any(type(d) is not int or not 1 <= d <= 128 for d in grid):
            raise ValueError("grid must be a bounded pair of built-in integers")
    height, width = old_grid
    batch, length, channels = positions.shape
    if batch != 1 or length != 1 + height * width or not 1 <= channels <= 256:
        raise ValueError("positional shape mismatch")
    if positions.numel() > 1000000 or (1 + new_grid[0] * new_grid[1]) * channels > 1000000:
        raise ValueError("positional table budget")
    if not torch.isfinite(positions).all() or (positions.abs() > 100).any():
        raise ValueError("finite bounded embeddings required")
    grid = positions[:,1:,:].reshape(1,height,width,channels).permute(0,3,1,2)
    resized = F.interpolate(grid,size=new_grid,mode="bicubic",align_corners=False,antialias=False)
    spatial = resized.permute(0,2,3,1).reshape(1,new_grid[0]*new_grid[1],channels)
    return torch.cat((positions[:,:1,:],spatial),dim=1)

