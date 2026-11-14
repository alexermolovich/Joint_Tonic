import torch


def cvae_loss(
    prediction: torch.Tensor, target: torch.Tensor, valid: torch.Tensor,
    mean: torch.Tensor, log_variance: torch.Tensor, beta: float,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return (total, masked L1 reconstruction, batch-mean Gaussian KL)."""
    pass
