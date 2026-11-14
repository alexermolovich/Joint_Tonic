import torch


def flow_action_interpolants(
    actions: torch.Tensor, noise: torch.Tensor, tau: torch.Tensor, valid: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Build a linear noise-to-action interpolant and its constant velocity target."""
    pass
