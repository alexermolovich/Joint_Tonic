import torch
import torch.nn.functional as F


def resize_positions(positions: torch.Tensor, old_grid: tuple[int,int], new_grid: tuple[int,int]) -> torch.Tensor:
    """Resize spatial position embeddings while preserving the class row."""
    # Implement the documented interpolation contract.
    pass

