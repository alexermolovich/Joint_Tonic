# Reference solution

Subtract the supplied target noise from the prediction, square the residual, and apply the timestep mask across all D channels. Divide the total by the number of valid scalar targets, D times valid.sum(). Keep the calculation in tensors so gradients reach both floating inputs. The contract bounds keep this sum finite in float32. Time and temporary storage are O(BHD).

~~~python
import torch


def conditional_noise_loss(prediction, target_noise, valid):
    if any(not isinstance(x, torch.Tensor) for x in (prediction, target_noise, valid)):
        raise TypeError("all arguments must be tensors")
    if prediction.ndim != 3 or target_noise.shape != prediction.shape:
        raise ValueError("floating tensors must have identical (B,H,D) shape")
    b, h, d = prediction.shape
    if not (1 <= b <= 64 and 1 <= h <= 256 and 1 <= d <= 64) or prediction.numel() > 2_000_000:
        raise ValueError("dimensions outside bounds")
    for value in (prediction, target_noise):
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64):
            raise ValueError("expected CPU float32 or float64")
        if not torch.isfinite(value).all() or (value.abs() > 1e6).any():
            raise ValueError("invalid noise values")
    if prediction.dtype != target_noise.dtype:
        raise ValueError("floating dtypes must match")
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != (b, h) or not valid.any():
        raise ValueError("valid must be CPU bool (B,H) with a true entry")
    squared = (prediction - target_noise).square()
    return (squared * valid[:, :, None]).sum() / (valid.sum() * d)

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
