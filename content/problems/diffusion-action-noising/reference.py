"""Deterministic forward diffusion with supplied noise."""
import torch


def diffuse_actions(actions, alpha_bar, timesteps, noise, mask=None):
    tensors = (actions, alpha_bar, timesteps, noise)
    if not all(isinstance(x, torch.Tensor) for x in tensors):
        raise TypeError("actions, alpha_bar, timesteps, noise must be tensors")
    if actions.ndim != 3 or min(actions.shape) < 1 or noise.shape != actions.shape:
        raise ValueError("actions and noise need the same positive (B,H,D) shape")
    if not actions.is_floating_point():
        raise ValueError("actions must be floating point")
    if any(x.dtype != actions.dtype or x.device != actions.device for x in (alpha_bar, noise)):
        raise ValueError("schedule and noise must share action dtype/device")
    if not all(bool(torch.isfinite(x).all()) for x in (actions, alpha_bar, noise)):
        raise ValueError("floating inputs must be finite")
    if (alpha_bar.ndim != 1 or alpha_bar.numel() < 1
            or bool(((alpha_bar < 0) | (alpha_bar > 1)).any())
            or bool((alpha_bar[1:] > alpha_bar[:-1]).any())):
        raise ValueError("alpha_bar must be a nonincreasing schedule in [0,1]")
    if (timesteps.dtype != torch.int64 or timesteps.device != actions.device
            or timesteps.shape != (actions.shape[0],)
            or bool(((timesteps < 0) | (timesteps >= alpha_bar.numel())).any())):
        raise ValueError("timesteps must be valid int64 indices, one per batch")
    if mask is not None and (not isinstance(mask, torch.Tensor)
            or mask.dtype != torch.bool or mask.device != actions.device
            or mask.shape != actions.shape[:2]):
        raise ValueError("mask must be bool (B,H) on the action device")
    coefficient = alpha_bar[timesteps].reshape(-1, 1, 1)
    noised = coefficient.sqrt() * actions + (1 - coefficient).sqrt() * noise
    target = noise.clone()
    if mask is not None:
        noised = torch.where(mask.unsqueeze(-1), noised, torch.zeros_like(noised))
        target = torch.where(mask.unsqueeze(-1), target, torch.zeros_like(target))
    return noised, target
