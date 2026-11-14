# Reference solution

Reshape the per-example flow times to (B,1,1), interpolate linearly between supplied noise and normalized actions, and compute the constant path derivative actions minus noise. Apply the timestep mask to both outputs. Tensor operations preserve gradients through actions, noise and flow time; no random draw or diffusion schedule belongs here. Time and output memory are O(BHD).

~~~python
import torch


def flow_action_interpolants(actions, noise, tau, valid):
    if any(not isinstance(x, torch.Tensor) for x in (actions, noise, tau, valid)):
        raise TypeError("all arguments must be tensors")
    if actions.ndim != 3 or noise.shape != actions.shape:
        raise ValueError("actions and noise must have identical (B,H,D) shape")
    b, h, d = actions.shape
    if not (1 <= b <= 64 and 1 <= h <= 256 and 1 <= d <= 64) or actions.numel() > 2_000_000:
        raise ValueError("dimensions outside bounds")
    for value in (actions, noise, tau):
        if value.device.type != "cpu" or value.dtype not in (torch.float32, torch.float64) or value.dtype != actions.dtype:
            raise ValueError("floating inputs must share a CPU float32/64 dtype")
        if not torch.isfinite(value).all():
            raise ValueError("floating inputs must be finite")
    if (actions.abs() > 1e6).any() or (noise.abs() > 1e6).any():
        raise ValueError("action and noise magnitude outside bounds")
    if tau.shape != (b,) or ((tau < 0) | (tau > 1)).any():
        raise ValueError("tau must be (B,) in [0,1]")
    if valid.device.type != "cpu" or valid.dtype != torch.bool or valid.shape != (b, h):
        raise ValueError("valid must be CPU bool (B,H)")
    time = tau[:, None, None]
    interpolant = (1 - time) * noise + time * actions
    velocity = actions - noise
    return interpolant.masked_fill(~valid[:, :, None], 0), velocity.masked_fill(~valid[:, :, None], 0)

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
