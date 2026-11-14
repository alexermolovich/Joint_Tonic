import torch


def build_vit_tokens(patches: torch.Tensor,projection: torch.Tensor,bias: torch.Tensor,
                     cls: torch.Tensor,positions: torch.Tensor) -> torch.Tensor:
    """Project patches, prepend a learned class token, and add positions."""
    pass
