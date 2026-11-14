import torch


def compact_visual_tokens(
    features: torch.Tensor,
    logits: torch.Tensor,
    valid: torch.Tensor | None = None,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Return spatially weighted visual tokens and their attention weights."""
    # Validate inputs, normalize over locations, and aggregate feature vectors.
    pass
