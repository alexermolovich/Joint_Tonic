# Solution approach

Validate shapes, floating values, dtype/device agreement, the schedule bounds/order, index dtype/range and mask shape. Gather one alpha value per batch item and reshape to (B,1,1).

Calculate sqrt(alpha)*actions + sqrt(1-alpha)*noise. Clone noise for the target so callers do not accidentally share the original tensor through a direct reference. If a mask exists, use torch.where(mask[...,None], value, zeros_like(value)) for both outputs.

The operation uses O(BHD) time and memory and preserves autograd. The reference rejects nonfinite inputs before masking so corrupted data is visible rather than silently hidden.
