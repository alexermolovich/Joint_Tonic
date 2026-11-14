import torch


def conditional_noise_loss(
    prediction: torch.Tensor, target_noise: torch.Tensor, valid: torch.Tensor
) -> torch.Tensor:
    """Return one global mean squared error over valid action scalars."""
    pass
