import torch


def normalize_clip_embeddings(image_features: torch.Tensor,
                              text_features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    """Normalize each feature row; preserve the gradient connection."""
    pass
