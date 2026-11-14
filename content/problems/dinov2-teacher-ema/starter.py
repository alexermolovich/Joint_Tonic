import torch


def update_teacher_ema(teacher: dict[str,torch.Tensor],student: dict[str,torch.Tensor],
                       momentum: float) -> dict[str,torch.Tensor]:
    """Return a detached EMA snapshot, pairing parameters by name."""
    pass
