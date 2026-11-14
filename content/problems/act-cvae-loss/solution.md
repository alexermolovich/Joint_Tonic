# Reference solution

Reduce the masked absolute action residual over valid scalar targets. Independently sum diagonal-Gaussian KL terms over latent dimensions and average over all batch items. Combine the two scalars with beta, preserving gradients through actions, targets and posterior parameters. The two terms have deliberately different denominators. Time and temporary storage are O(BHD+BZ).

~~~python
import math
import torch


def cvae_loss(prediction, target, valid, mean, log_variance, beta):
    if any(not isinstance(x, torch.Tensor) for x in (prediction, target, valid, mean, log_variance)):
        raise TypeError("tensor arguments must be tensors")
    if type(beta) not in (int, float):
        raise TypeError("beta must be a built-in real number")
    if not 0 <= beta <= 100 or not math.isfinite(beta):
        raise ValueError("beta outside bounds")
    if prediction.ndim != 3 or target.shape != prediction.shape:
        raise ValueError("actions must have identical (B,H,D) shape")
    b, h, d = prediction.shape
    if not (1 <= b <= 64 and 1 <= h <= 256 and 1 <= d <= 64):
        raise ValueError("action dimensions outside bounds")
    if mean.ndim != 2 or log_variance.shape != mean.shape or mean.shape[0] != b or not 1 <= mean.shape[1] <= 256:
        raise ValueError("latent tensors must have identical (B,Z) shape")
    for value, lower, upper in ((prediction, -1e6, 1e6), (target, -1e6, 1e6), (mean, -1000, 1000), (log_variance, -20, 20)):
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64) or value.dtype != prediction.dtype:
            raise ValueError("matching CPU floating dtypes required")
        if value.numel() > 2_000_000 or not torch.isfinite(value).all() or ((value < lower) | (value > upper)).any():
            raise ValueError("floating values or size outside bounds")
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != (b, h) or not valid.any():
        raise ValueError("valid must be CPU bool (B,H) with a true entry")
    reconstruction = ((prediction - target).abs() * valid[:, :, None]).sum() / (d * valid.sum())
    kl = 0.5 * (mean.square() + log_variance.exp() - 1 - log_variance).sum(dim=1).mean()
    return reconstruction + beta * kl, reconstruction, kl

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
