import torch


def project_sensor_features(
    features: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor, valid: torch.Tensor
) -> torch.Tensor:
    """Project normalized sensor features and zero invalid token rows."""
    pass
